#!/bin/bash
# Cron wrapper: Neo4j health check — silent when healthy, alert on failure
# Runs daily at 08:00 KST

source ~/.venv-neo4j/bin/activate
cd ~/hermes-wiki-super/.metagraph
python3 check_health.py 2>&1
RC=$?
if [ $RC -eq 0 ]; then
  # Healthy → silent (no-agent mode)
  exit 0
else
  echo "❌ Neo4j Health Check FAILED"
  python3 check_health.py --verbose 2>&1
  exit 1
fi
