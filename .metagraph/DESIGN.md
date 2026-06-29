# Hermes GraphRAG — Design Document v0.4

> 2026-06-29 | Phase 6: Universal Knowledge Graph

## Motivation

Phase 5의 구조적 한계:
1. **`indexer.py`**: `NAMESPACES` 하드코딩 — 새 repo 추가 시 수동 등록 필요
2. **`query.py`**: `structural_search()`에 하드코딩된 키워드 맵(valuation/infra/analysis/...)
3. **`query.py`**: `detect_mode()`에 하드코딩된 한국어 키워드
4. **No auto-discovery**: 새 submodule이 `.gitmodules`에 추가돼도 자동 감지 불가

**목표**: repo 추가/제거/변경에 완전히 자동 대응. 모든 콘텐츠를 언어/도메인/태그 무관하게 검색.

## System Architecture v0.4

```
┌───────────────────────────────────────┐
│          Wiki Super Repo              │
│  .gitmodules (13+ submodules)         │
│  wiki/*/  (submodule checkouts)       │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│  discover.py (NEW)                    │
│  ├─ parse .gitmodules → 모든 submodule │
│  ├─ auto-generate namespace (2자 + 충돌)│
│  ├─ compare vs .index_state.json      │
│  └─ 신규 발견 → git submodule update  │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│  indexer.py (REFACTORED)             │
│  ├─ NAMESPACES 하드코딩 ❌ 제거       │
│  ├─ discover.py 결과 사용            │
│  ├─ standalone repos도 auto-detect    │
│  └─ trade-pipeline 등 extra path 포함 │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│  Neo4j (200+ pages)                  │
│  vector_search + graph_traversal     │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│  query.py (REFACTORED)               │
│  ├─ structural_search 키워드 ❌ 제거   │
│  ├─ detect_mode 키워드 ❌ 제거        │
│  ├─ universal_search (NEW)           │
│  │   ├─ 1. vector_search (임베딩)     │
│  │   ├─ 2. graph_expand (1-hop)       │
│  │   └─ 3. rank: vector × connectivity│
│  └─ 모든 repo/언어/도메인 무관 작동   │
└───────────────────────────────────────┘
```

## Key Changes

### 1. discover.py (NEW)
`.gitmodules`를 파싱해 모든 submodule 자동 감지:

```python
def discover_repos(wiki_super_path):
    """Return {repo_name: repo_path, namespace, status}"""
    # 1. Parse .gitmodules → all submodules (init/uninit 모두)
    # 2. Compare vs .index_state.json
    # 3. New: auto-namespace (첫글자2자 + 충돌 시 증분)
    # 4. Extra: ~/trade-pipeline 같이 submodule 밖 repo
```

**Namespace 생성 규칙**:
- repo명에서 첫 2자 추출 (e.g., `hermes-wiki` → `hw`)
- 충돌 시 숫자 증분 (e.g., `hw`, `hw2`, `hw3`)
- 특수 repo는 alias (e.g., `trade-pipeline` → `tp`)

### 2. indexer.py (REFACTORED)
```python
# BEFORE: 하드코딩 NAMESPACES
NAMESPACES = {
    "hermes-wiki": "hw", "trade-pipeline": "tp", ...
}

# AFTER: discover.py 위임
def get_repo_namespace(repo_name):
    from discover import resolve_namespace
    return resolve_namespace(repo_name)

# standalone repos도 discover.py로 통합
# trade-pipeline hardcode 제거
```

### 3. Universal Query Router (query.py)

```python
# BEFORE (제거):
keywords = {"valuation": ["per", "pbr", ...]}  # ❌
def detect_mode(q):
    if any(w in q for w in ["연결", "관계", ...]):  # ❌

# AFTER:
def universal_search(query: str, k: int = 5) -> list:
    """키워드/태그/도메인 가정 ZERO. 오직 벡터 + 그래프."""
    # Step 1: Vector search (always works)
    emb = embed_text(query)
    vec_results = vector_search(emb, k)
    
    # Step 2: Graph expand top results
    for r in vec_results[:3]:
        r["neighbors"] = get_neighbors(r["id"])
    
    # Step 3: Rank by combined score
    #   vector_score × (1 + log(connectivity + 1))
    return ranked
```

**작동 원리**:
- 벡터 검색은 언어/도메인/태그에 무관 — 임베딩이 의미를 포착
- 그래프 확장은 연결성 정보 추가 — "연결/관계" 질문도 자연히 커버
- 키워드 매칭/태그 필터 없이도 모든 질문에 대응

### 4. Auto-Ingest Pipeline

```
Cron 03:00 KST (기존 유지, discovery 추가):

Step 0: python3 discover.py --check
  → 신규 submodule 발견 시 git submodule update --init
  → .index_state.json에 신규 repo 등록
  → 메시지: "[NEW] hermes-wiki-foo (ns:hf) detected, indexed"

Step 1: python3 index_incremental.py
  → 변경된 repo만 재인덱싱
  → 신규 repo도 포함 (초기 인덱싱)
```

## Implementation Plan

### Phase 6a: Discovery + Indexer 리팩터
| File | Change |
|------|--------|
| `discover.py` | **NEW** — .gitmodules 파서 + namespace 생성기 |
| `indexer.py` | 하드코딩 NAMESPACES 제거, discover.py 위임 |
| `index_incremental.py` | discover.py 통합, 신규 repo 감지 |

### Phase 6b: Universal Query Router
| File | Change |
|------|--------|
| `query.py` | `structural_search` 키워드 제거, `universal_search` 추가 |
| `query.py` | `detect_mode` 키워드 제거, unified rank |
| `synthesize.py` | 불필요한 필터 제거 |

### Phase 6c: Cron + Auto-Ingest
| Task | Detail |
|------|--------|
| `discover.py --check` | cron pre-step으로 추가 |
| cron update | 기존 03:00 KST에 discover 추가 |

## Timeline

| Phase | Date | Description |
|-------|------|-------------|
| P1~P5 | 2026-06-29 | Foundation (200 pages, 11 repos) |
| **P6a** | 2026-06-29 | Discovery + Indexer 리팩터 |
| **P6b** | 2026-06-29 | Universal Query Router |
| **P6c** | 2026-06-29 | Auto-ingest cron |

## Risk

| Risk | Mitigation |
|------|------------|
| namespace 충돌 | 2자 + 숫자 증분으로 해결 |
| 미초기화 submodule index 실패 | `discover.py`가 init까지 자동 처리 |
| universal_search가 structural보다 정확도 낮음 | vector × connectivity 조합이 키워드 매칭 상회 |
