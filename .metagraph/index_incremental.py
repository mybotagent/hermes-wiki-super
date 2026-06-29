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

    # Discover repos
    # Check both root and wiki/ subdirectory for submodules
    repos = {}
    search_dirs = [WIKI_SUPER]
    wiki_dir = WIKI_SUPER / "wiki"
    if wiki_dir.exists():
        search_dirs.append(wiki_dir)
    for base in search_dirs:
        for item in sorted(base.iterdir()):
            if not item.is_dir() or item.name.startswith("."):
                continue
            # git can be a dir (full clone) or file (submodule link)
            if (item / ".git").exists():
                repos[item.name] = item
    if (Path(os.path.expanduser("~/trade-pipeline"))).exists():
        repos["trade-pipeline"] = Path(os.path.expanduser("~/trade-pipeline"))

    changed = []
    unchanged = []
    for name, path in sorted(repos.items()):
        head_sha, head_ts = get_git_head(path)
        prev_sha = state.get("repos", {}).get(name, {}).get("head")
        status = "CHANGED" if (head_sha and head_sha != prev_sha) else "unchanged"
        if args.force or (head_sha and head_sha != prev_sha):
            changed.append(name)
        else:
            unchanged.append(name)
        print(f"  {name:35s} {status}  head={head_sha[:12] if head_sha else 'N/A'}")

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
