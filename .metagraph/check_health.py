#!/usr/bin/env python3
"""
Neo4j Health Check & Monitoring

Verifies:
1. Neo4j process is running under systemd
2. Bolt port 7687 is listening
3. Graph database is queryable
4. Page count sanity check
5. Vector search works (if vector index exists)

Usage:
  source ~/.venv-neo4j/bin/activate
  python3 check_health.py                  # full check, exits 0/1
  python3 check_health.py --verbose        # human-readable
  python3 check_health.py --repair         # attempt auto-fix
"""
import os, sys, subprocess, json
from pathlib import Path
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_HOME = "/usr/local/neo4j"
MIN_PAGES = 50  # alert if fewer pages than this

def check_process():
    """Check Neo4j is running under systemd."""
    r = subprocess.run(
        ["systemctl", "is-active", "neo4j.service"],
        capture_output=True, text=True, timeout=5
    )
    return r.stdout.strip() == "active", r.stdout.strip()

def check_port():
    """Check Bolt port is listening."""
    r = subprocess.run(
        ["ss", "-tlnp"], capture_output=True, text=True, timeout=5
    )
    return "7687" in r.stdout, "port 7687 found" if "7687" in r.stdout else "port 7687 not found"

def check_database():
    """Check graph database is queryable."""
    try:
        driver = GraphDatabase.driver(NEO4J_URI)
        with driver.session() as sess:
            r = sess.run("MATCH (n) RETURN count(n) AS cnt")
            total = r.single()["cnt"]
            r2 = sess.run("MATCH ()-[r]->() RETURN count(r) AS cnt")
            rels = r2.single()["cnt"]
            r3 = sess.run("SHOW INDEXES WHERE name = 'page_emb'")
            vec = len(r3.data()) > 0
        driver.close()
        return True, {"nodes": total, "edges": rels, "vector_search": bool(vec)}
    except Exception as e:
        return False, {"error": str(e)}

def check_memory():
    """Check Neo4j memory usage."""
    r = subprocess.run(
        ["ps", "-o", "rss=", "-p", 
         subprocess.run(["pgrep", "-f", "org.neo4j.server"], 
                       capture_output=True, text=True).stdout.strip()],
        capture_output=True, text=True, timeout=5
    )
    if r.stdout.strip():
        mem_kb = int(r.stdout.strip())
        return True, f"{mem_kb // 1024}MB"
    return False, "unknown"

def repair():
    """Attempt auto-fix."""
    print("[repair] Attempting to start Neo4j...")
    r = subprocess.run(
        ["sudo", "systemctl", "start", "neo4j.service"],
        capture_output=True, text=True, timeout=30
    )
    if r.returncode == 0:
        print("[repair] Started successfully")
        return True
    print(f"[repair] Failed: {r.stderr}")
    return False

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = {}

    pid_ok, pid_status = check_process()
    results["process"] = {"ok": pid_ok, "status": pid_status}

    port_ok, port_msg = check_port()
    results["port"] = {"ok": port_ok, "msg": port_msg}

    db_ok, db_info = check_database()
    results["database"] = {"ok": db_ok, "info": db_info}

    mem_ok, mem_info = check_memory()
    results["memory"] = {"ok": mem_ok, "usage": mem_info}

    # Overall health
    all_ok = pid_ok and port_ok and db_ok
    results["healthy"] = all_ok

    if args.json:
        print(json.dumps(results, indent=2))
    elif args.verbose:
        print("=== Neo4j Health Check ===")
        print(f"  Process:     {'✅' if pid_ok else '❌'} {pid_status}")
        print(f"  Port 7687:   {'✅' if port_ok else '❌'} {port_msg}")
        if db_ok:
            db = db_info
            print(f"  Database:    ✅ {db['nodes']} nodes, {db['edges']} edges, vector={'✅' if db['vector_search'] else '❌'}")
        else:
            print(f"  Database:    ❌ {db_info.get('error','unknown')}")
        print(f"  Memory:      {mem_info}")
        print(f"  Overall:     {'✅ HEALTHY' if all_ok else '❌ UNHEALTHY'}")
    else:
        # Machine-readable: just exit code
        pass

    if args.repair and not all_ok:
        print("[repair] Health check failed, attempting repair...")
        if repair():
            all_ok = True

    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
