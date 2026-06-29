#!/usr/bin/env python3
"""
Wiki -> Neo4j Indexer
Scans hermes-wiki-super submodules, extracts frontmatter + wikilinks,
generates embeddings, and MERGEs into Neo4j.

Usage:
  source ~/.venv-neo4j/bin/activate
  python3 indexer.py                           # scan all
  python3 indexer.py --repo hermes-wiki         # single repo
  python3 indexer.py --dry-run                  # dry run (no writes)
"""
import os, re, sys, argparse
from pathlib import Path
from datetime import date
from neo4j import GraphDatabase

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from embed import embed_batch

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
WIKI_SUPER = os.path.expanduser("~/hermes-wiki-super")

NAMESPACES = {
    "hermes-wiki": "hw", "trade-pipeline": "tp",
    "hermes-wiki-claude-code": "cc", "hermes-wiki-codex": "cx",
    "harness-engineering-wiki": "he", "subagents-library": "sl",
    "hermes-logs": "hl", "hermes-wiki-quant": "hq",
    "ai-job-analysis": "aj", "ai-marketing-wiki": "am",
    "hermes-prompts": "hp", "hermes-slash-commands": "hs",
    "hermes-wiki-schedule": "hsd",
}

def get_repo_namespace(repo_name):
    return NAMESPACES.get(repo_name, repo_name[:2])

def find_wiki_pages(repo_path):
    pages = []
    for f in Path(repo_path).rglob("*.md"):
        rel = f.relative_to(repo_path)
        parts = rel.parts
        if any(p.startswith(".") for p in parts): continue
        if parts[0] in ("logs", "raw", ".git", "subagents-library"): continue
        pages.append(f)
    return pages

def parse_frontmatter(content):
    fm = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text, body = parts[1], parts[2]
            for line in fm_text.strip().split("\n"):
                line = line.strip()
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if val.startswith("[") and val.endswith("]"):
                        val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
                    fm[key] = val
    return fm, body

def extract_wikilinks(body):
    return re.findall(r'\[\[([^\]]+)\]\]', body)

def extract_page_title(path, frontmatter):
    if "title" in frontmatter: return frontmatter["title"]
    return path.stem.replace("-", " ").title()

def get_page_summary(body, max_len=200):
    for line in body.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            if len(line) > 30: return line[:max_len]
    return ""

def get_tags(frontmatter):
    tags = frontmatter.get("tags", frontmatter.get("tag", []))
    return tags if isinstance(tags, list) else [tags]

def get_related(frontmatter):
    related = frontmatter.get("related", [])
    return related if isinstance(related, list) else [related]

def scan_repo(repo_name, repo_path, dry_run=False):
    pages, links, refs = [], [], []
    ns = get_repo_namespace(repo_name)
    print(f"\n--- Scanning: {repo_name} ({ns}:) ---")
    md_files = find_wiki_pages(repo_path)
    print(f"  Found {len(md_files)} markdown files")

    page_path_to_id = {}
    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        fm, body = parse_frontmatter(content)
        rel_path = str(f.relative_to(repo_path))
        page_id = f"{ns}:{rel_path.replace('/', ':').replace('.md', '')}"
        page_path_to_id[rel_path] = page_id

        pages.append({
            "id": page_id, "repo": repo_name, "path": rel_path,
            "title": extract_page_title(f, fm),
            "tags": get_tags(fm),
            "summary": get_page_summary(body),
            "updated": fm.get("updated", fm.get("created", str(date.today()))),
            "confidence": fm.get("confidence", "medium"),
            "text": f"{extract_page_title(f, fm)}: {get_page_summary(body)}",
        })
        for r in get_related(fm):
            r_id = f"{ns}:{r.replace('.md', '').replace('/', ':')}"
            refs.append((page_id, r_id, "related"))

    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        _, body = parse_frontmatter(content)
        rel_path = str(f.relative_to(repo_path))
        from_id = page_path_to_id[rel_path]
        for wl in extract_wikilinks(body):
            wl_clean = wl.split("|")[0]
            wl_id = f"{ns}:{wl_clean.replace('/', ':')}"
            links.append((from_id, wl_id, "wikilink"))

    if not dry_run:
        write_to_neo4j(pages, links, refs)

    print(f"  Pages: {len(pages)}, Wikilinks: {len(links)}, Related: {len(refs)}")
    return pages, links, refs

def write_to_neo4j(pages, links, refs):
    driver = GraphDatabase.driver(NEO4J_URI)
    # Generate embeddings
    texts = [p["text"] for p in pages]
    print(f"  Generating {len(texts)} embeddings...")
    embs = embed_batch(texts)
    for i, emb in enumerate(embs):
        pages[i]["embedding"] = emb

    with driver.session() as sess:
        for p in pages:
            sess.run("""
                MERGE (n:Page {id: $id})
                SET n.repo = $repo, n.path = $path,
                    n.title = $title, n.tags = $tags,
                    n.summary = $summary, n.updated = $updated,
                    n.confidence = $confidence,
                    n.embedding = $embedding
            """, p)
        for from_id, to_id, ltype in links + refs:
            try:
                sess.run("""
                    MATCH (a:Page {id: $from_id})
                    MATCH (b:Page {id: $to_id})
                    MERGE (a)-[r:LINKS {type: $type}]->(b)
                """, {"from_id": from_id, "to_id": to_id, "type": ltype})
            except: pass
    driver.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="Scan single repo only")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    wiki_super = Path(WIKI_SUPER)
    repos = {}
    for item in wiki_super.iterdir():
        if not item.is_dir() or item.name.startswith("."): continue
        if (item / ".git").exists() or (item / "index.md").exists():
            repos[item.name] = item
        if item.name == "wiki":
            for sub in item.iterdir():
                if sub.is_dir() and ((sub / ".git").exists() or (sub / "index.md").exists()):
                    repos[sub.name] = sub

    # Standalone repos outside wiki_super
    standalone = {
        "trade-pipeline": os.path.expanduser("~/trade-pipeline"),
    }
    for name, path in standalone.items():
        if Path(path).exists():
            repos[name] = Path(path)

    print(f"Found {len(repos)} repos")
    total_pages = total_links = total_refs = 0
    for repo_name, repo_path in sorted(repos.items()):
        if args.repo and repo_name != args.repo: continue
        p, l, r = scan_repo(repo_name, repo_path, args.dry_run)
        total_pages += len(p); total_links += len(l); total_refs += len(r)

    print(f"\n=== Summary ===")
    print(f"  Pages: {total_pages}, Links: {total_links}, Refs: {total_refs}")
    if args.dry_run: print("  (dry run)")

if __name__ == "__main__":
    main()
