#!/usr/bin/env python3
"""Neo4j wiki KB: Create schema constraints and indexes."""
import os, sys
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
driver = GraphDatabase.driver(NEO4J_URI)

def run(query):
    with driver.session() as sess:
        sess.run(query)
    print(f"  \u2713 {query[:100]}")

print("=== Creating Neo4j Schema ===")

run("CREATE CONSTRAINT page_id IF NOT EXISTS FOR (p:Page) REQUIRE p.id IS UNIQUE")
run("CREATE CONSTRAINT page_path IF NOT EXISTS FOR (p:Page) REQUIRE (p.repo, p.path) IS UNIQUE")

run("CREATE RANGE INDEX page_tags IF NOT EXISTS FOR (p:Page) ON (p.tags)")
run("CREATE RANGE INDEX page_repo IF NOT EXISTS FOR (p:Page) ON (p.repo)")
run("CREATE RANGE INDEX page_updated IF NOT EXISTS FOR (p:Page) ON (p.updated)")

# Vector index (Neo4j 5.18+)
try:
    run('CREATE VECTOR INDEX page_emb IF NOT EXISTS FOR (p:Page) ON (p.embedding) OPTIONS {indexConfig: {`vector.dimensions`: 1536, `vector.similarity_function`: "cosine"}}')
except Exception as e:
    print(f"  ! Vector index skip: {e}")

print()
print("=== Schema Verification ===")
with driver.session() as sess:
    for r in sess.run("SHOW CONSTRAINTS"):
        print(f"  CONSTRAINT: {r['name']} ({r['type']})")
    for r in sess.run("SHOW RANGE INDEXES"):
        print(f"  RANGE INDEX: {r['name']} ({r['type']})")
    for r in sess.run("SHOW VECTOR INDEXES"):
        print(f"  VECTOR INDEX: {r['name']} (dim={r.get('dimensions')})")

driver.close()
print("\nSchema OK!")
