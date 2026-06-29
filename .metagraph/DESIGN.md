# Hermes GraphRAG — Design Document v0.3

> 2026-06-29 | Phase 5 완료: 운영 자동화

## System Architecture

```
┌─────────────────────────────────┐
│    11 Wiki Repos (hermes-*)     │
│  ├─ hermes-wiki (34 pages)      │
│  ├─ trade-pipeline (24 pages)   │
│  ├─ hermes-logs (30 pages)      │
│  ├─ harness-engineering (26)    │
│  ├─ ai-marketing (20 pages)     │
│  ├─ hermes-prompts (18 pages)   │
│  ├─ claude-code (18 pages)      │
│  ├─ hermes-wiki-quant (10)      │
│  ├─ codex (9 pages)             │
│  ├─ ai-job-analysis (8 pages)   │
│  └─ slash-commands (3 pages)    │
└─────────┬───────────────────────┘
          │ git HEAD diff (daily 03:00 KST)
          ▼
┌─────────────────────────────────┐
│   .metagraph/indexer.py         │
│   .metagraph/index_incremental  │ ← 증분 모드
│   .metagraph/link_cross_repo.py │ ← 크로스-레포 링크
└─────────┬───────────────────────┘
          │ MERGE
          ▼
┌─────────────────────────────────┐
│  Neo4j Community 5.26.0         │
│  ┌───────────┐ ┌──────────┐   │
│  │ 200 Pages  │ │ 376 Edges│   │
│  │ (384d vec) │ │251 wiki+ │   │
│  │            │ │125 cross │   │
│  └───────────┘ └──────────┘   │
│  Vector Index: page_emb        │
│  Bolt: localhost:7687          │
│  Heap: 512MB / Cache: 256MB   │
│  systemd: enabled (boot auto)  │
└─────────┬───────────────────────┘
          │ QUERY (Hermes Skill)
          ▼
┌─────────────────────────────────┐
│  Query Router (auto-detect)     │
│  ├─ Semantic (vector)           │
│  ├─ Structural (Cypher GRAPH)   │
│  └─ Hybrid (multi-hop)          │
└─────────┬───────────────────────┘
          │ Synthesize → 한글
          ▼
┌─────────────────────────────────┐
│      Hermes Agent Response      │
└─────────────────────────────────┘
```

## Key Decisions

### Phase 1-3 (Foundation)
- **Neo4j Community (local)** — 비용 0, 포트폴리오 가치 최대
- **BAAI/bge-m3 (384d)** — DeepSeek embedding API 없음 → 무료 오픈소스
- **Query Router** — semantic/structural/hybrid 자동 분기 (규칙 기반, LLM 불필요)
- **11 Repos** — 200 pages, 376 edges (125 cross-repo)

### Phase 4 (Cross-repo)
- Namespace registry (hw:, tp:, he:, etc.)
- Cross-repo wikilink resolution: `hw:cron-jobs` → 다른 repo의 `[[cron-jobs]]` 연결
- 13개 submodule 중 11개 checkout/인덱싱 완료 (2개 미초기화)

### Phase 5 (Operations) ← NEW
- **systemd** → 부팅 시 Neo4j 자동 시작, 실패 시 자동 재시작
- **Incremental Indexer** → git HEAD 변경 감지, 변경된 repo만 재인덱싱
- **Health Check cron** → 매일 08:00 KST, silent when healthy
- **Incremental Index cron** → 매일 03:00 KST, 자동 증분 인덱싱

## Operations

### 크론 작업

| Job ID | Name | Schedule (KST) | Type | Description |
|--------|------|---------------|------|-------------|
| 65ef8dbdfa5d | neo4j-health-check | 08:00 daily | no_agent | Silent when healthy, alert on failure |
| 972c64d3f4da | neo4j-incremental-index | 03:00 daily | agent | Report changed repos + pages count |

### 복구 절차

```bash
# 1. 상태 확인
systemctl status neo4j.service

# 2. 재시작
sudo systemctl restart neo4j.service

# 3. 수동 헬스 체크
source ~/.venv-neo4j/bin/activate
python3 ~/hermes-wiki-super/.metagraph/check_health.py --verbose
```

### 메모리 (1.9GB RAM 서버)

| Component | Usage |
|-----------|-------|
| Neo4j Heap | 512MB |
| Page Cache | 256MB |
| JVM overhead | ~100MB |
| Total | ~900MB |
| Swap | 1.9GB available |

## Future Considerations

1. **Incremental 인덱스 크론 개선** — 파일 단위 변경 감지 (현재: repo HEAD 단위)
2. **스킬 Hermes Agent 등록** — 현재 수동 호출, Hermes Agent skill로 통합
3. **Neo4j 인증 설정** — auth off (로컬 전용, 필요 시)
4. **미초기화 submodule** — hermes-wiki-schedule, subagents-library (새 repo 추가 시)

## Files

### Input / Source
- `~/hermes-wiki-super/wiki/*/` — 11 wiki repos (submodules)

### Scripts (.metagraph/)
| Script | Purpose |
|--------|---------|
| `create_schema.py` | Neo4j schema + Vector Index init |
| `embed.py` | bge-m3 embedding (384d) |
| `indexer.py` | Full indexer (all repos) |
| `index_incremental.py` | Incremental (changed repos only) |
| `link_cross_repo.py` | Cross-repo wikilink resolver |
| `check_health.py` | Health check + auto-repair |
| `skill/query.py` | Query Router |
| `skill/synthesize.py` | Result synthesizer |

### Config / State
| File | Purpose |
|------|---------|
| `.index_state.json` | Per-repo HEAD tracking |
| `/etc/systemd/system/neo4j.service` | Systemd unit |
| `/usr/local/neo4j/conf/neo4j.conf` | Neo4j config |

## Timeline

| Phase | Date | Pages | Edges | Repos |
|-------|------|-------|-------|-------|
| P1: Schema + Graph (initial) | 2026-06-29 | 64 | 78 | 2 |
| P2: Vectors | 2026-06-29 | 64 | 78 | 2 |
| P3: Hermes Skill | 2026-06-29 | 64 | 78 | 2 |
| P4: Cross-repo Expansion | 2026-06-29 | 200 | 376 | 11 |
| P5: Operations Automation | 2026-06-29 | 200 | 376 | 11 |
