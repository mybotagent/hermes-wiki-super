#!/usr/bin/env python3
"""
Incremental Wiki -> Neo4j Indexer

Only re-indexes repos whose git HEAD changed since last run.
State stored in .metagraph/.index_state.json

Usage:
  source ~/.venv-neo4j/bin/activate
  python3 index_incremental.py              # incremental (default)
  python3 index_incremental.py --force      # full reindex
  python3 index_incremental.py --status     # show state only
  python3 index_incremental.py --dry-run    # show what would change
"""
import json, os, sys, subprocess, time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discover import discover_repos

STATE_FILE = Path(__file__).parent / ".index_state.json"
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
WIKI_SUPER = Path(os.path.expanduser("~/hermes-wiki-super"))
INDEXER = Path(__file__).parent / "indexer.py"

def get_git_head(path):
    """Return (HEAD_sha, HEAD_time) or (None, None)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(path), capture_output=True, text=True, timeout=15
        )
        sha = result.stdout.strip() if result.returncode == 0 else None

        result2 = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "HEAD"],
            cwd=str(path), capture_output=True, text=True, timeout=15
        )
        ts = result2.stdout.strip() if result2.returncode == 0 else None
        return sha, ts
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None, None

def git_cmd(path, args, timeout=30):
    """Run a git command in `path`. Returns (returncode, stdout) or (None, '')."""
    try:
        r = subprocess.run(
            ["git"] + args,
            cwd=str(path), capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, r.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return None, ""


def fetch_and_sync(path, apply=True):
    """
    Fetch origin and fast-forward the repo to its upstream branch if it is behind.

    Rationale (2026-11-17): index_incremental.py only compared the local HEAD SHA,
    so a submodule that lagged behind origin/main was reported as "unchanged" and
    silently skipped. This step removes that false negative.

    Returns (status, detail) where status is one of:
      up-to-date | fast-forwarded | behind | detached | no-upstream | error
    """
    rc, _ = git_cmd(path, ["rev-parse", "--is-inside-work-tree"], timeout=15)
    if rc != 0:
        return "error", "not a git repo"

    # Determine upstream: prefer the branch origin/HEAD points to.
    rc, out = git_cmd(path, ["symbolic-ref", "--quiet", "--short", "HEAD"], timeout=15)
    branch = out if rc == 0 else ""
    rc, out = git_cmd(path, ["rev-parse", "--abbrev-ref", "HEAD"], timeout=15)
    if rc != 0 or out.startswith("HEAD"):
        branch = ""

    if not branch:
        # Detached HEAD (e.g. submodules checked out by a recorded SHA):
        # try origin/HEAD as the canonical branch.
        rc, out = git_cmd(path, ["symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"], timeout=15)
        branch = out if rc == 0 else ""
        if branch.startswith("origin/"):
            branch = branch[len("origin/"):]
        if not branch:
            rc, out = git_cmd(path, ["remote", "show", "origin"], timeout=30)
            for line in out.splitlines():
                if line.strip().startswith("HEAD branch:"):
                    branch = line.split(":", 1)[1].strip()
                    break
        if not branch:
            return "detached", "detached HEAD and no origin/HEAD"

    git_cmd(path, ["fetch", "origin", "--quiet"], timeout=60)

    rc, out = git_cmd(path, ["rev-list", "--count", f"HEAD..origin/{branch}"], timeout=15)
    if rc != 0:
        return "no-upstream", f"cannot compare with origin/{branch}"
    behind = int(out or 0)
    if behind == 0:
        return "up-to-date", branch

    if not apply:
        return "behind", f"{behind} commit(s) behind origin/{branch}"

    rc, out = git_cmd(path, ["merge", "--ff-only", f"origin/{branch}"], timeout=60)
    if rc != 0:
        return "behind", f"{behind} behind origin/{branch}, ff-only merge failed"
    return "fast-forwarded", f"{behind} commit(s) -> origin/{branch}"


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Incremental Neo4j indexer")
    parser.add_argument("--force", action="store_true", help="Full reindex all repos")
    parser.add_argument("--status", action="store_true", help="Show current state")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--no-fetch", action="store_true",
                        help="Skip origin fetch / fast-forward sync of submodules")
    args = parser.parse_args()

    state = load_state()
    timestamp = int(time.time())

    if args.status:
        print("=== Index State ===")
        if not state:
            print("  No previous index state")
            return
        for repo, info in sorted(state.get("repos", {}).items()):
            print(f"  {repo}: HEAD={info.get('head','?')[:12]} at {info.get('time','?')}")
        print(f"  Last full index: {state.get('last_full', 'never')}")
        return

    # Discover repos via discover.py (auto-detection from .gitmodules)
    discovered = discover_repos(include_state=False)
    repos = {}
    for name, info in discovered.items():
        if info["initialized"] and info["path"] and info["path"].exists():
            repos[name] = info["path"]

    changed = []
    unchanged = []
    synced = []
    for name, path in sorted(repos.items()):
        # Sync with origin first so a lagging submodule is not falsely "unchanged".
        if not args.no_fetch:
            sync_status, sync_detail = fetch_and_sync(path, apply=True)
            if sync_status == "fast-forwarded":
                synced.append((name, sync_detail))
                print(f"  {name:35s} SYNCED     {sync_detail}")
            elif sync_status in ("behind", "detached", "no-upstream", "error"):
                print(f"  {name:35s} WARN       {sync_status}: {sync_detail}")
        head_sha, head_ts = get_git_head(path)
        prev_sha = state.get("repos", {}).get(name, {}).get("head")
        status = "CHANGED" if (head_sha and head_sha != prev_sha) else "unchanged"
        if args.force or (head_sha and head_sha != prev_sha):
            changed.append(name)
        else:
            unchanged.append(name)
        print(f"  {name:35s} {status}  head={head_sha[:12] if head_sha else 'N/A'}")

    if synced:
        print(f"\n  Synced {len(synced)} repo(s) with origin: "
              + ", ".join(n for n, _ in synced))

    if not changed:
        print(f"\nAll {len(repos)} repos unchanged. Nothing to index.")
        if args.force:
            print("  (--force overrides: forcing full reindex)")
            changed = list(repos.keys())
        else:
            return

    print(f"\n=== Indexing {len(changed)} changed repos ===")
    if args.dry_run:
        print(f"  Would index: {', '.join(changed)}")
        return

    # Run main indexer on changed repos
    cmd = [sys.executable, str(INDEXER)]
    for repo in changed:
        cmd += ["--repo", repo]
    
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(WIKI_SUPER), timeout=600)
    
    if result.returncode != 0:
        print(f"  ERROR: indexer failed with code {result.returncode}")
        sys.exit(1)

    # Update state
    new_state = state.copy()
    new_state["repos"] = new_state.get("repos", {})
    for name, path in repos.items():
        head_sha, head_ts = get_git_head(path)
        if head_sha:
            new_state["repos"][name] = {"head": head_sha, "indexed": timestamp}
    new_state["last_index"] = timestamp
    if args.force:
        new_state["last_full"] = timestamp
    save_state(new_state)

    print(f"\n=== Done ===")
    print(f"  Indexed: {len(changed)} repos ({', '.join(changed)})")
    print(f"  Unchanged: {len(unchanged)} repos")

if __name__ == "__main__":
    main()
