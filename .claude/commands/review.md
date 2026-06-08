# review

리뷰 주기에 따라 wiki 활동을 집계·분석하고, Monthly/Quarterly에서는 Re-align(카테고리 가중치·검색어·전략 재조정)을 실행한다.

## 사용법

```
/review daily      — 오늘 활동 스캔 + 미처리 Clippings 확인 (15분)
/review weekly     — 주간 합산 + 목표 대비 현황 (30분)
/review monthly    — 월간 분석 + Re-align 실행 (1시간)
/review quarterly  — 분기 심층 분석 + Deep Re-align (2시간)
```

인자 없이 `/review` 만 실행하면 `daily`로 동작한다.

---

## 공통 — 0단계: 데이터 수집 (모든 주기)

```bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
TODAY=$(date '+%Y-%m-%d')

# 1. 미처리 Clippings 확인
echo "=== Unprocessed Clippings ==="
ls "$SUPER_ROOT/Clippings/" | grep -v "^processed$" || echo "(없음)"

# 2. 주기별 git log 범위 설정 (daily=1d / weekly=7d / monthly=30d / quarterly=90d)
echo "=== Recent Wiki Activity ==="
cd "$SUPER_ROOT"
git log --oneline --since="<주기>" | grep "^.*sync: update"

# 3. log.md 있는 레포 목록에서 최근 항목 수집
for repo in ai-job-analysis ai-marketing-wiki harness-engineering-wiki hermes-prompts hermes-wiki-claude-code hermes-wiki-quant; do
  logfile="$SUPER_ROOT/wiki/$repo/log.md"
  [ -f "$logfile" ] && echo "--- $repo ---" && grep "^## \[" "$logfile" | tail -5
done
```

---

## DAILY — 일간 루틴

### 1단계: 미처리 Clippings 처리

Clippings/ 에 미처리 파일이 있으면:
→ `/process-clippings` 실행 권고 또는 자동 실행

없으면 "Clippings 클린" 확인 후 종료.

### 2단계: 오늘의 wiki 활동 요약

오늘 날짜 기준 추가된 wiki 페이지 목록 출력.

### 3단계: 오늘의 핵심 인사이트 1개

오늘 추가된 페이지들에서 LTV 관점 가장 중요한 인사이트 1문장 추출.

### 출력 형식

```
📅 Daily Review — YYYY-MM-DD

📥 Clippings: <처리됨 N개 / 미처리 N개>
📚 오늘 추가된 페이지: <N개>
  - [레포] 파일명 — 한 줄 요약

💡 오늘의 핵심 인사이트:
  <LTV 관점 1문장>
```

---

## WEEKLY — 주간 루틴

### 1단계: 공통 데이터 수집 (git since 7d)

### 2단계: 카테고리별 수집 현황 집계

지난 7일간 log.md 변경 기반으로 카테고리별 추가 건수 집계:

| 카테고리 | 레포 | 이번 주 추가 | 목표 가중치 |
|---------|------|------------|-----------|
| AI & 자동화 | harness-engineering-wiki, hermes-wiki-claude-code | N개 | 30% |
| 퀀트 & 금융 | hermes-wiki-quant | N개 | 25% |
| 뉴스레터 & 콘텐츠 | ai-marketing-wiki | N개 | 20% |
| 솔로프리너 | hermes-wiki | N개 | 15% |
| LTV & 고객관계 | hermes-wiki | N개 | 10% |

목표 대비 실제 비율 계산 → 과다/부족 카테고리 강조 표시.

### 3단계: 주간 요약 저장

아래 형식으로 hermes-logs에 저장:

```markdown
# Weekly Review — YYYY-MM-DD (W<주차>)

## 수집 현황
<카테고리별 표>

## 주요 인사이트
- <상위 3개>

## 다음 주 포커스
- 부족한 카테고리: <카테고리명>
- 추천 검색어: <키워드 3개>
```

```bash
cd "$SUPER_ROOT/wiki/hermes-logs"
# Write 도구로 YYYY-WNN-weekly-review.md 저장
git add -A && git commit -m "log: weekly review $TODAY" && git push

cd "$SUPER_ROOT"
git add wiki/hermes-logs
git commit -m "sync: update hermes-logs ref $TODAY" && git push
```

### 출력 형식

```
📊 Weekly Review — YYYY-MM-DD

카테고리별 수집:
  ✅ AI & 자동화:      N개 (목표 30% → 실제 XX%)
  ⚠️  퀀트 & 금융:     N개 (목표 25% → 실제 XX%) ← 부족
  ✅ 뉴스레터 & 콘텐츠: N개 (목표 20% → 실제 XX%)
  ...

다음 주 포커스: <부족 카테고리>
저장됨: wiki/hermes-logs/YYYY-WNN-weekly-review.md
```

---

## MONTHLY — 월간 + Re-align

### 1단계: 공통 데이터 수집 (git since 30d)

### 2단계: 월간 집계

지난 4주 weekly-review 파일들 + log.md 전체 집계:

```bash
# 이번 달 weekly review 파일 목록
ls "$SUPER_ROOT/wiki/hermes-logs/" | grep "$(date '+%Y-%m')"

# 카테고리별 총 추가 건수, 페이지 목록
for repo in ai-job-analysis ai-marketing-wiki harness-engineering-wiki hermes-prompts hermes-wiki-claude-code hermes-wiki-quant; do
  grep "^## \[$(date '+%Y')" "$SUPER_ROOT/wiki/$repo/log.md" 2>/dev/null
done
```

### 3단계: ⚙️ Re-align 실행

Re-align은 4개 서브파이프라인으로 구성된다:

#### [RA-1] 성과 측정
```
□ 이번 달 총 수집 건수: <N>개 (목표: 주간 25개 × 4 = 100개)
□ A급 심층 분석 비율: <N>% (목표: 50%+)
□ Clippings 처리율: <N>% (목표: 100%)
□ 카테고리별 목표 달성률: <표>
```

#### [RA-2] 갭 분석
현재 수집 패턴 vs 목표 가중치 비교:
- **과다 카테고리** (목표 대비 +10%p 이상): 다음 달 검색 빈도 줄임
- **부족 카테고리** (목표 대비 -10%p 이상): 다음 달 검색 키워드 보강
- **신규 트렌드**: log.md에서 이번 달 처음 등장한 태그/주제 발굴

#### [RA-3] 검색어 업데이트
CLAUDE.md의 주간 검색 계획 기반, 성과가 낮은 검색어를 교체:
- 기존 검색어 성과 평가 (수집된 A급 콘텐츠 수 기준)
- 신규 검색어 3-5개 제안 (이번 달 log.md 태그 기반)
- 최종 확정된 검색어 목록 사용자에게 제시 후 승인 요청

#### [RA-4] 전략 문서 업데이트
사용자 승인 후 hermes-wiki-schedule에 다음 달 계획 저장:

```markdown
# YYYY년 MM월 실행 계획 (Re-aligned)

## 카테고리 가중치 (Re-aligned)
| 카테고리 | 이전 | 조정 후 | 이유 |
|---------|------|---------|------|
| AI & 자동화 | 30% | XX% | <이유> |
...

## 이번 달 주간 검색어

### 월요일: AI & 자동화
- <업데이트된 검색어 3개>
...

## 다음 달 포커스 키워드
<신규 트렌드 3개>
```

```bash
cd "$SUPER_ROOT/wiki/hermes-wiki-schedule"
# Write 도구로 YYYY-MM-monthly-plan.md 저장
git add -A && git commit -m "plan: monthly realign $TODAY" && git push

cd "$SUPER_ROOT"
git add wiki/hermes-wiki-schedule wiki/hermes-logs
git commit -m "sync: monthly review + realign $TODAY" && git push
```

### 출력 형식

```
📈 Monthly Review + Re-align — YYYY-MM

성과:
  수집: N개 (목표 100개 → XX%)
  A급 분석: N% (목표 50%)
  Clippings 처리율: N%

Re-align 결과:
  ✅ 유지: AI & 자동화 30%
  ⬆️  증가: 퀀트 & 금융 25% → 30% (부족했음)
  ⬇️  감소: 뉴스레터 20% → 15% (과다)
  🆕 신규 키워드: <3개>

저장됨:
  wiki/hermes-logs/YYYY-MM-monthly-review.md
  wiki/hermes-wiki-schedule/YYYY-MM-monthly-plan.md
```

---

## QUARTERLY — 분기 + Deep Re-align

### 1단계: 공통 데이터 수집 (git since 90d)

### 2단계: 분기 집계

지난 3개월의 monthly-review 파일 3개 합산.

### 3단계: ⚙️ Deep Re-align 실행

월간 Re-align보다 넓은 범위:

#### [DRA-1] 분기 성과 종합
- 3개월 누적 수집량, 카테고리 분포
- 가장 많이 교차 참조된 위키 페이지 (링크 히트맵)
- LTV 공식 관점 평가: 어떤 인사이트가 실제 비즈니스에 적용됐나?

#### [DRA-2] 위키 생태계 점검
```bash
# 각 레포의 페이지 수, 마지막 업데이트 확인
for repo in "$SUPER_ROOT/wiki"/*/; do
  count=$(ls "$repo" | grep "\.md$" | wc -l | tr -d ' ')
  last=$(cd "$repo" && git log --oneline -1 --format="%ar" 2>/dev/null || echo "N/A")
  echo "$(basename $repo): $count pages, last: $last"
done
```
- 30일 이상 업데이트 없는 레포 → "정체 레포" 표시
- 가장 활발한 레포 → 다음 분기 집중 투자

#### [DRA-3] 전략 방향 재검토
사용자에게 3가지 질문:
1. "이번 분기에서 가장 LTV에 기여한 인사이트는?"
2. "다음 분기에 새로 탐색하고 싶은 주제/분야는?"
3. "제거하거나 줄이고 싶은 카테고리는?"

답변 기반으로 다음 분기 전략 문서 작성.

#### [DRA-4] 시스템 개선 제안
수집 파이프라인 자체 평가:
- process-clippings 사용 빈도 vs Clippings 폴더 누적량
- 활용되지 않은 위키 레포 → 통합/폐기 제안
- 새 위키 레포 필요성 평가

#### [DRA-5] 분기 계획 저장

hermes-wiki-schedule에 저장:
```markdown
# YYYY Q<N> 분기 계획 (Deep Re-aligned)

## 분기 성과 요약
...

## 전략 방향 변경
...

## 카테고리 가중치 (분기 기준)
...

## 시스템 개선 사항
...
```

### 출력 형식

```
🔭 Quarterly Deep Re-align — YYYY Q<N>

분기 성과:
  총 수집: N개
  활성 레포: N/12개
  정체 레포: <목록>

Deep Re-align:
  전략 변경: <요약>
  새 카테고리: <있으면>
  폐기 제안: <있으면>
  시스템 개선: <N개 항목>

저장됨: wiki/hermes-wiki-schedule/YYYY-QN-quarterly-plan.md
```

---

## Re-align 파이프라인 요약

```
[수집 집계] → [갭 분석] → [검색어 업데이트] → [전략 문서 저장] → [push]
     ↑                                                              ↓
     └──────────── 다음 주기 수집 가이드로 피드백 ←─────────────────┘
```

- **Daily**: 수집 상태 확인만
- **Weekly**: 수집 현황 → 다음 주 포커스 조정
- **Monthly**: 전체 Re-align → 가중치·검색어·계획 업데이트
- **Quarterly**: Deep Re-align → 전략 방향·위키 생태계 재설계
