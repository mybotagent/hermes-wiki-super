# add-wiki

사용자가 내용을 주면 Claude가 Karpathy LLM Wiki 패턴으로 적합한 서브모듈 레포를 찾거나 새로 만들어서 저장한다.

참고: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## 사용법

```
/add-wiki <내용 또는 주제>
```

내용만 적으면 Claude가 자동으로 레포 판단 → 페이지 작성 → push까지 완료한다.

---

## Claude가 수행할 단계

### 1단계 — 기존 서브모듈 목록 파악

```bash
cat "/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super/.gitmodules"
ls "/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super/wiki/"
```

### 2단계 — 레포 결정 (내용 분석)

`$ARGUMENTS`의 주제/카테고리를 파악해서:

- 기존 서브모듈 중 **가장 적합한 곳** 선택
- 어디에도 맞지 않으면 **새 레포 이름 결정** (kebab-case)

결정 이유를 한 줄로 먼저 사용자에게 설명한다.

현재 서브모듈 참고:
- `hermes-wiki` — Hermes 메인 위키 (일반)
- `hermes-wiki-claude-code` — Claude Code 관련
- `hermes-wiki-codex` — Codex / 슬래시 커맨드
- `hermes-wiki-schedule` — 스케줄/루틴
- `harness-engineering-wiki` — 엔지니어링/개발
- `ai-job-analysis` — AI 채용/직무
- `ai-marketing-wiki` — AI 마케팅
- `hermes-logs` — 로그/기록 (타임스탬프 파일)
- `hermes-slash-commands` — 슬래시 커맨드
- `subagents-library` — 서브에이전트

### 3단계 — Karpathy 방식으로 페이지 작성

내용을 위키 페이지로 변환할 때 다음 규칙을 따른다:

#### 페이지 형식
```markdown
---
tags: ["<주제태그>", "<카테고리태그>"]
related: ["<관련페이지경로>"]
created: YYYY-MM-DD
---

# <제목>

> <한 줄 요약 — 이 페이지가 무엇인지>

## <섹션>

<내용 — 구글 1페이지에 없는 고유 인사이트만. 설치법/기초 설명 금지>

## Related

- [[관련페이지]] — <한 줄 설명>
```

#### 품질 규칙 (AGENTS.md 기반)
- **Unique insight only**: 고유한 분석, 사용자 환경 특화 정보만
- **Concise**: 1~5KB, 핵심만
- **[[wikilinks]]** 로 교차 참조
- **No trivial content**: 기초 튜토리얼, 설치 가이드 금지

#### 파일명
- kebab-case, 주제 반영
- 예: `ltv-strategy.md`, `ai-automation-patterns.md`

### 4단계 — index.md 및 log.md 업데이트

레포 안의 `index.md`에 새 페이지 항목 추가:
```markdown
- [페이지제목](경로/파일명.md) — <한 줄 요약>
```

`log.md`에 변경 이력 append:
```markdown
## [YYYY-MM-DD] ingest | <페이지제목>
<무엇을 추가했는지 한 줄>
```

(index.md나 log.md가 없으면 새로 생성)

### 5단계A — 기존 서브모듈에 push

```bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
WIKI_PATH="wiki/<결정된레포>"

cd "$SUPER_ROOT/$WIKI_PATH"
git add -A
git commit -m "wiki: add <파일명> $(date '+%Y-%m-%d')"
git push

cd "$SUPER_ROOT"
git add "$WIKI_PATH"
git commit -m "sync: update <레포명> ref $(date '+%Y-%m-%d')"
git push
```

### 5단계B — 새 레포 생성 후 push

```bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
WIKI_NAME="<결정된레포이름>"
WIKI_PATH="wiki/$WIKI_NAME"
GITHUB_USER="mybotagent"
REMOTE_URL="https://github.com/$GITHUB_USER/$WIKI_NAME.git"

# 1. GitHub private 레포 생성
gh repo create "$GITHUB_USER/$WIKI_NAME" --private --description "Wiki: $WIKI_NAME"

# 2. 로컬 초기화
mkdir -p "$SUPER_ROOT/$WIKI_PATH"
cd "$SUPER_ROOT/$WIKI_PATH"
git init
git branch -M main

# 3. 페이지 파일, index.md, log.md 작성 (Write 도구로)

# 4. 첫 커밋 & push
git add -A
git commit -m "init: create $WIKI_NAME"
git remote add origin "$REMOTE_URL"
git push -u origin main

# 5. 슈퍼 레포에 서브모듈 등록
cd "$SUPER_ROOT"
git submodule add "$REMOTE_URL" "$WIKI_PATH"
git add .gitmodules "$WIKI_PATH"
git commit -m "feat: add $WIKI_NAME as submodule"
git push
```

---

## 완료 후 출력

- 어떤 레포에 넣었는지 (기존 / 신규)
- 생성된 파일 경로
- index.md / log.md 업데이트 여부
- push 성공 여부
