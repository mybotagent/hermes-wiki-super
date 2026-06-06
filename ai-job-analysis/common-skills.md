# AI/LLM 직무 공통 필수 스킬 분석 2026

> 출처: 사람인·잡코리아·원티드 채용공고 + NotebookLM Gemini 2.5 분석 (45개 소스 기반)
> 작성일: 2026-06-06

---

## 필수 스킬 빈도 분석

### 1순위 — 거의 모든 공고에서 요구 (90% 이상)

| 스킬 | 설명 |
|------|------|
| **Python** | 프로덕션 수준 숙련도 필수. 텍스트 전처리, ML 파이프라인 포함 |
| **LLM API 활용** | OpenAI GPT, Anthropic Claude, Azure OpenAI, Google Gemini 중 하나 이상 |
| **LangChain / LangGraph** | 오케스트레이션 프레임워크. LangGraph는 에이전트 워크플로우 필수 |
| **RAG 파이프라인** | 청킹 전략, 임베딩, 하이브리드 검색, 리랭커 포함 |
| **벡터 DB** | Pinecone, pgvector, Weaviate, Elasticsearch, Qdrant 중 하나 이상 |

### 2순위 — 중간 이상 공고에서 요구 (50~89%)

| 스킬 | 설명 |
|------|------|
| **프롬프트 엔지니어링** | Chain-of-Thought, Few-shot, 구조화된 출력 설계 |
| **FastAPI** | LLM 백엔드 서비스 구축 |
| **Docker / Kubernetes** | 컨테이너 배포 및 운영 |
| **클라우드 (AWS/Azure/GCP)** | AI 서비스 연동 및 인프라 경험 |
| **Transformer 아키텍처 이해** | BERT, GPT 구조 이해. 직접 학습 불필요 |

### 3순위 — 우대사항 (30~49%)

| 스킬 | 설명 |
|------|------|
| **Fine-tuning (LoRA, QLoRA)** | sLLM 경량화 미세조정 경험 |
| **PyTorch** | 모델 학습/평가 경험 (연구직 필수, 응용직 우대) |
| **HuggingFace** | 오픈소스 모델 활용 |
| **vLLM / TGI** | LLM 인퍼런스 최적화 |
| **MCP (Model Context Protocol)** | 에이전트 도구 연결 서버 구축 |
| **Eval 프레임워크** | RAGAS, LangSmith, LLM-as-judge |

---

## 직무 유형별 핵심 스킬 매핑

```
LLM 애플리케이션 엔지니어
├── Python ★★★
├── LLM API (OpenAI/Claude) ★★★
├── RAG + 벡터DB ★★★
├── LangChain/LangGraph ★★★
└── FastAPI ★★

AI Agent 엔지니어
├── LangGraph / AutoGen / CrewAI ★★★
├── Tool Use / Function Calling ★★★
├── MCP 서버 구축 ★★★
├── 멀티에이전트 오케스트레이션 ★★
└── 메모리 아키텍처 설계 ★★

LLM Research Engineer (연구직)
├── PyTorch ★★★
├── 분산학습 (DDP, Slurm) ★★★
├── Fine-tuning (LoRA, RLHF, DPO) ★★★
├── 논문 작성/발표 ★★
└── GPU 클러스터 운영 ★★

AI 데이터/어시스턴트 (신입 진입 최적)
├── 생성형 AI 사용 경험 ★★★
├── 한국어 텍스트 처리 능력 ★★★
├── 어노테이션 / 데이터 품질 관리 ★★
└── LLM 결과 평가 능력 ★★
```

---

## 신입 로드맵 (6개월 기준)

### Phase 1 — 기본기 (1~2개월)
- [ ] Python 프로덕션 수준 (비동기, 패키징, 테스트)
- [ ] OpenAI/Claude API 직접 호출 → Tool Use 루프 구현
- [ ] RAG 파이프라인 처음부터 구현 (프레임워크 없이)

### Phase 2 — 심화 (3~4개월)
- [ ] LangGraph로 멀티스텝 에이전트 구축
- [ ] RAGAS로 시스템 성능 수치화
- [ ] FastAPI로 API 서비스화
- [ ] GitHub 포트폴리오 공개

### Phase 3 — 취업 준비 (5~6개월)
- [ ] 기술 블로그 (실패 경험 + 해결 과정 필수)
- [ ] 카카오·네이버 인턴 → 정규직 전환 목표
- [ ] 사람인/잡코리아 '신입 가능' 필터 지원

---

> **핵심 인사이트**: 후보자의 76%가 프로덕션 배포 경험이 부족. 실제 작동하는 RAG 또는 에이전트 1개만 GitHub에 올려도 강력한 경쟁력.
