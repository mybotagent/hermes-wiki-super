#!/usr/bin/env python3
"""
Auto-Discovery: Parse .gitmodules → all submodules, auto-namespace.

Reads .gitmodules from hermes-wiki-super, determines all submodule repos
(initialized and uninitialized), auto-generates compact 2-char namespaces,
and provides helpers for indexer.py and index_incremental.py.

Usage:
  python3 discover.py                    # list all discovered repos
  python3 discover.py --init-new         # git submodule update --init new ones
  python3 discover.py --check            # exit 0 if no change, 1 if new/removed
"""
import os, sys, subprocess, configparser, re
from pathlib import Path

WIKI_SUPER = Path(os.path.expanduser("~/hermes-wiki-super"))
GITMODULES = WIKI_SUPER / ".gitmodules"
STATE_FILE = Path(__file__).parent / ".index_state.json"
EXTRA_REPOS = {
    "trade-pipeline": Path(os.path.expanduser("~/trade-pipeline")),
}

def parse_gitmodules(path=None):
    """Parse .gitmodules and return {name: path, url} dict."""
    path = path or GITMODULES
    repos = {}
    if not path.exists():
        return repos
    cfg = configparser.ConfigParser()
    cfg.read(str(path))
    for section in cfg.sections():
        if section.startswith("submodule "):
            # section name = 'submodule "path"', extract path
            raw_name = section.split('"')[1] if '"' in section else section
            # Strip wiki/ prefix for clean repo name
            name = os.path.basename(raw_name.rstrip("/"))
            repos[name] = {
                "path": raw_name,
                "url": cfg[section].get("url", ""),
            }
    return repos

def auto_namespace(repo_name: str, existing=None) -> str:
    """Generate compact 2-char namespace from repo_name.
    
    Preserves known mappings for backward compatibility, then generates
    new ones from meaningful initials.
    
    Known mappings (preserved):
      hermes-wiki=hw, trade-pipeline=tp, hermes-wiki-claude-code=cc,
      hermes-wiki-codex=cx, harness-engineering-wiki=he, hermes-logs=hl,
      hermes-wiki-quant=hq, ai-job-analysis=aj, ai-marketing-wiki=am,
      hermes-prompts=hp, hermes-slash-commands=hs, hermes-wiki-schedule=hsd,
      subagents-library=sl
    
    New repos: first letter of each word, max 2 chars.
    If collision, append digit: hw → hw2 → hw3
    """
    existing = existing or set()
    name = repo_name.lower()
    
    # Known mappings (backward compatible)
    known = {
        "hermes-wiki": "hw", "trade-pipeline": "tp",
        "hermes-wiki-claude-code": "cc", "hermes-wiki-codex": "cx",
        "harness-engineering-wiki": "he", "hermes-logs": "hl",
        "hermes-wiki-quant": "hq", "ai-job-analysis": "aj",
        "ai-marketing-wiki": "am", "hermes-prompts": "hp",
        "hermes-slash-commands": "hs", "hermes-wiki-schedule": "hsd",
        "subagents-library": "sl",
    }
    if name in known:
        ns = known[name]
        if ns in existing:
            # If known ns is taken by something else, append digit
            for i in range(2, 10):
                if f"{ns}{i}" not in existing:
                    return f"{ns}{i}"
        return ns
    
    # Auto-generate: initials of meaningful words
    # Remove common prefixes
    clean = name
    for prefix in ["hermes-wiki-", "hermes-", "wiki-"]:
        if clean.startswith(prefix):
            clean = clean[len(prefix):]
            break
    
    # Split by - and take first letter of each word
    words = [w for w in re.split(r'[-_\s]+', clean) if w and len(w) > 1]
    if not words:
        words = [w for w in re.split(r'[-_\s]+', clean) if w]
    if not words:
        words = [name[:3], name[3:6]]
    
    ns = "".join(w[0] for w in words[:2])
    if len(ns) < 2:
        ns = (name[:1] + "x") if len(name) < 2 else name[:2]
    
    # Handle collisions
    if ns in existing:
        for i in range(2, 10):
            candidate = f"{ns}{i}"
            if candidate not in existing:
                return candidate
        return f"{ns}x"
    
    return ns

def discover_repos(include_state=True):
    """Discover all repos: submodules + extras.
    
    Returns: {name: {"path": Path, "namespace": str, "initialized": bool, "status": str}}
    """
    submodules = parse_gitmodules()
    repos = {}
    existing_ns = set()
    
    # Check initialized submodules (have .git file or dir)
    for name, info in submodules.items():
        repo_path = WIKI_SUPER / info["path"]
        has_git = (repo_path / ".git").exists()  # file for submodules, dir for clones
        ns = auto_namespace(name, existing_ns)
        existing_ns.add(ns)
        repos[name] = {
            "path": repo_path,
            "namespace": ns,
            "initialized": has_git,
            "source": "submodule",
        }
    
    # Extra repos
    for name, path in EXTRA_REPOS.items():
        if path.exists():
            ns = auto_namespace(name, existing_ns)
            existing_ns.add(ns)
            repos[name] = {
                "path": path,
                "namespace": ns,
                "initialized": True,
                "source": "extra",
            }
    
    # Compare with state if requested
    if include_state:
        import json
        state = {}
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text())
        tracked = set(state.get("repos", {}).keys())
        discovered = set(repos.keys())
        
        for name in repos:
            if name not in tracked:
                repos[name]["status"] = "new"
            else:
                repos[name]["status"] = "tracked"
        
        for name in tracked:
            if name not in repos:
                repos[name] = {"status": "removed", "path": None, "namespace": "", "initialized": False, "source": "unknown"}
    
    return repos

def get_namespace_map(repos=None):
    """Return {repo_name: namespace} dict."""
    if repos is None:
        repos = discover_repos(include_state=False)
    return {name: info["namespace"] for name, info in repos.items()}

def init_new_repos(repos=None):
    """git submodule update --init for uninitialized submodules."""
    if repos is None:
        repos = discover_repos(include_state=False)
    new = [name for name, info in repos.items() if info["source"] == "submodule" and not info["initialized"]]
    if not new:
        return []
    result = subprocess.run(
        ["git", "submodule", "update", "--init"] + new,
        cwd=str(WIKI_SUPER), capture_output=True, text=True, timeout=120
    )
    return new if result.returncode == 0 else []

def main():
    import argparse, json
    parser = argparse.ArgumentParser(description="Wiki repo auto-discovery")
    parser.add_argument("--init-new", action="store_true", help="Init uninitialized submodules")
    parser.add_argument("--check", action="store_true", help="Check for new/removed repos (exit code)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()
    
    repos = discover_repos()
    
    if args.init_new:
        inited = init_new_repos(repos)
        if inited:
            print(f"Initialized: {', '.join(inited)}")
            repos = discover_repos()  # re-discover
    
    if args.check:
        changes = [n for n, i in repos.items() if i.get("status") in ("new", "removed")]
        if changes:
            print(f"Changes detected: {', '.join(changes)}")
            sys.exit(1)
        print("All repos tracked, no changes")
        sys.exit(0)
    
    if args.json:
        output = {}
        for name, info in sorted(repos.items()):
            output[name] = {
                "ns": info["namespace"],
                "init": info["initialized"],
                "source": info["source"],
                "status": info.get("status", "unknown"),
                "path": str(info["path"]) if info["path"] else None,
            }
        print(json.dumps(output, indent=2))
    else:
        print(f"{'Repo':35s} {'NS':4s} {'Init':5s} {'Status':10s} {'Path'}")
        print("-" * 80)
        for name, info in sorted(repos.items()):
            init_s = "✅" if info["initialized"] else "❌"
            print(f"{name:35s} {info['namespace']:4s} {init_s:5s} {info.get('status','?'):10s} {str(info['path'] or '')[:30]}")

if __name__ == "__main__":
    main()
