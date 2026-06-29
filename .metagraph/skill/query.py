#!/usr/bin/env python3
"""
Wiki Knowledge Search — Universal Query Router v2

하드코딩 키워드/태그 ZERO. 오직 벡터 + 그래프 조합.
모든 repo/언어/도메인에 무관하게 작동.

Usage:
  python3 query.py "클로드 코드 활용법"
  python3 query.py "PER 분석 방법"
  python3 query.py "cron jobs에 연결된 페이지"
  python3 query.py --top-k 10 "밸류에이션"
"""
import os, sys, argparse, textwrap
sys.path.insert(0, os.path.expanduser("~/.venv-neo4j/lib/python*/site-packages"))
sys.path.insert(0, os.path.expanduser("~/hermes-wiki-super/.metagraph"))

from neo4j import GraphDatabase
from embed import embed_text

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
TOP_K = 5

# ──────────────────────────────────────────────
# Vector Search (always works, any domain)
# ──────────────────────────────────────────────

def vector_search(query: str, k: int = TOP_K) -> list:
    """Pure vector similarity. Language/domain agnostic."""
    emb = embed_text(query)
    with GraphDatabase.driver(NEO4J_URI).session() as s:
        results = s.run("""
            CALL db.index.vector.queryNodes('page_emb', $k, $emb)
            YIELD node, score
            RETURN node.id AS id, node.title AS title,
                   node.repo AS repo, node.path AS path,
                   node.summary AS summary, score
        """, emb=emb, k=k)
        return [dict(r) for r in results]

# ──────────────────────────────────────────────
# Graph Context (neighborhood expand)
# ──────────────────────────────────────────────

def get_neighbors(page_id: str, max_n: int = 5) -> list:
    """1-hop neighborhood for any page. No keyword assumptions."""
    with GraphDatabase.driver(NEO4J_URI).session() as s:
        results = s.run("""
            MATCH (p:Page {id: $id})-[r:LINKS]-(neighbor:Page)
            RETURN DISTINCT neighbor.id AS id, neighbor.title AS title,
                   neighbor.repo AS repo, neighbor.path AS path,
                   neighbor.summary AS summary,
                   r.type AS rel_type
            LIMIT $max_n
        """, id=page_id, max_n=max_n)
        return [dict(r) for r in results]

def get_connected_pages(query: str, k: int = TOP_K) -> list:
    """
    Graph connectivity search — finds the most connected pages via
    keyword matching on title/summary. No hardcoded tag categories.
    """
    with GraphDatabase.driver(NEO4J_URI).session() as s:
        # Match pages whose title or summary contains query words
        # Rank by connectivity (number of neighbors)
        q = query.lower()
        results = s.run("""
            MATCH (p:Page)
            OPTIONAL MATCH (p)-[r:LINKS]-(neighbor:Page)
            WITH p, count(DISTINCT neighbor) AS connections
            WHERE connections > 0
              AND (toLower(p.title) CONTAINS $q
                   OR toLower(p.summary) CONTAINS $q
                   OR toLower(p.repo) CONTAINS $q)
            RETURN p.id AS id, p.title AS title,
                   p.repo AS repo, p.path AS path,
                   p.summary AS summary,
                   connections
            ORDER BY connections DESC
            LIMIT $k
        """, q=q, k=k)
        return [dict(r) for r in results]

# ──────────────────────────────────────────────
# Universal Search (no keywords, no tags, no assumptions)
# ──────────────────────────────────────────────

def universal_search(query: str, k: int = TOP_K) -> dict:
    """
    Zero keyword, zero tag, zero domain assumption search.
    
    Strategy:
    1. Vector search (always) — semantic matching on any language
    2. Graph expand top results — find connected pages
    3. Keyword-fallback connectivity — find pages mentioning query terms
    4. Fuse + deduplicate — combined ranking
    
    No hardcoded keywords. No tag categories. No domain assumptions.
    """
    # Step 1: Vector search (primary)
    vec_results = vector_search(query, k)
    vec_ids = {r["id"] for r in vec_results}
    
    # Step 2: Graph connectivity search (secondary)
    conn_results = get_connected_pages(query, k)
    
    # Step 3: Fuse results — vector first, then connectivity
    fused = []
    seen = set()
    
    for r in vec_results:
        if r["id"] not in seen:
            seen.add(r["id"])
            r["match_type"] = "semantic"
            # Enrich with neighbors
            r["neighbors"] = get_neighbors(r["id"])
            fused.append(r)
    
    for r in conn_results:
        if r["id"] not in seen:
            seen.add(r["id"])
            r["match_type"] = "graph"
            r["neighbors"] = get_neighbors(r["id"])
            fused.append(r)
    
    for r in fused[:3]:
        if "neighbors" not in r or not r["neighbors"]:
            r["neighbors"] = get_neighbors(r["id"])
    
    return {
        "question": query,
        "mode": "universal",
        "total": len(fused),
        "results": fused[:k],
    }

# ──────────────────────────────────────────────
# Query Interface
# ──────────────────────────────────────────────

def query_kb(question: str) -> dict:
    """Main query entry point. Always uses universal search."""
    return universal_search(question)

# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Universal Wiki Knowledge Search")
    parser.add_argument("query", nargs="?", help="질문 (모든 언어/도메인)")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    args = parser.parse_args()
    
    if not args.query:
        while True:
            try:
                q = input("\n❓ 질문 (q=종료): ").strip()
                if q.lower() in ("q", "quit", "exit"): break
                if not q: continue
                result = query_kb(q)
                print(format_results(result, json_output=args.json))
            except KeyboardInterrupt:
                break
        return
    
    result = query_kb(args.query)
    # Override top-k if requested
    if args.top_k != TOP_K:
        result["results"] = result["results"][:args.top_k]
        result["total"] = len(result["results"])
    print(format_results(result, json_output=args.json))

def format_results(data: dict, json_output=False) -> str:
    if json_output:
        import json
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)
    
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"📌 {data['question']}")
    lines.append(f"🔍 Mode: {data['mode']}  |  검색결과: {data['total']}건")
    lines.append('='*60)
    
    for i, r in enumerate(data["results"], 1):
        lines.append(f"\n{i}. [{r['repo']}] {r['title']}")
        lines.append(f"   📄 {r['path']}")
        if r.get("score"):
            lines.append(f"   🎯 유사도: {r['score']:.3f}")
        if r.get("connections"):
            lines.append(f"   🔗 연결: {r['connections']}개")
        if r.get("match_type"):
            lines.append(f"   🏷 매칭: {r['match_type']}")
        summary = (r.get("summary") or "")[:150]
        if summary:
            lines.append(f"   {summary}...")
        neighbors = r.get("neighbors", [])
        if neighbors:
            n_titles = [n["title"] for n in neighbors[:5]]
            lines.append(f"   └ 연결페이지: {', '.join(n_titles)}")
    
    lines.append(f"\n{'='*60}")
    return "\n".join(lines)

if __name__ == "__main__":
    main()
