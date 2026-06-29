# Hermes GraphRAG — .metagraph/

Neo4j 기반 지식 그래프 + 벡터 검색 엔진. Hermes Wiki 11개 repo를 통합 검색.

## 구조

```
.metagraph/
├── create_schema.py      # Neo4j 스키마 + Vector Index 초기화
├── embed.py              # BAAI/bge-m3 임베딩 생성 (384d)
├── indexer.py            # 전체 인덱서 (all repos)
├── index_incremental.py  # 증분 인덱서 (변경된 repo만)
├── link_cross_repo.py    # 크로스-레포 [[wikilink]] 해석기
├── check_health.py       # 헬스 체크 + 자동 복구
├── cron_health.sh        # 헬스 체크 크론 래퍼
├── skill/
│   ├── SKILL.md          # Hermes Agent 스킬 정의
│   ├── query.py          # Query Router (semantic/structural/hybrid)
│   └── synthesize.py     # 결과 → 자연어 합성
└── .index_state.json     # 증분 인덱스 상태 파일
```

## 크론

| 작업 | 시간 (KST) | 설명 |
|------|-----------|------|
| 헬스 체크 | 매일 08:00 | 상태 이상 시만 알림 (silent when healthy) |
| 증분 인덱스 | 매일 03:00 | git HEAD 변경된 repo만 재인덱싱 |

## 지원 레포 (11개)

| 네임스페이스 | 레포 | 페이지 |
|-------------|------|-------|
| hw | hermes-wiki | 34 |
| tp | trade-pipeline | 24 |
| he | harness-engineering-wiki | 26 |
| am | ai-marketing-wiki | 20 |
| hp | hermes-prompts | 18 |
| cc | hermes-wiki-claude-code | 18 |
| hq | hermes-wiki-quant | 10 |
| cx | hermes-wiki-codex | 9 |
| hl | hermes-logs | 30 |
| aj | ai-job-analysis | 8 |
| hs | hermes-slash-commands | 3 |

## 사용

```bash
source ~/.venv-neo4j/bin/activate

# 헬스 체크
python3 check_health.py --verbose

# 전체 재인덱싱
python3 indexer.py

# 증분 인덱싱
python3 index_incremental.py

# 쿼리 (스킬)
python3 skill/query.py "PER이 뭐야?"
# → 복합 쿼리면 hybrid 모드 자동
python3 skill/query.py "CRON에 연결된 페이지 찾아줘"
```
