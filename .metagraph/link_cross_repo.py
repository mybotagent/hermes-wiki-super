#!/usr/bin/env python3
"""
Cross-repo link builder.
Creates :LINKS relationships between pages in different repos
that share common tags. Run after indexer.py.
"""
from neo4j import GraphDatabase
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")

def link_cross_repo():
    driver = GraphDatabase.driver(NEO4J_URI)
    with driver.session() as s:
        result = s.run("""
            MATCH (a:Page), (b:Page)
            WHERE a.repo < b.repo AND a.id < b.id
            UNWIND a.tags AS tag
            UNWIND b.tags AS btag
            WITH a, b, tag WHERE tag = btag
            WITH a, b, collect(tag) AS common
            WHERE size(common) > 0
            WITH a, b, common
            MERGE (a)-[r:LINKS {type: 'cross-repo'}]->(b)
            SET r.tags = common
            RETURN count(*) AS created
        """)
        created = result.single()["created"]
        
        total = s.run("""
            MATCH (a:Page)-[r:LINKS]->(b:Page)
            WHERE a.repo <> b.repo
            RETURN count(*) AS cnt
        """).single()["cnt"]
        
        print(f"Created: {created} | Total cross-repo links: {total}")
    driver.close()

if __name__ == "__main__":
    link_cross_repo()
