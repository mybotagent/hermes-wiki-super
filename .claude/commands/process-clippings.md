# process-clippings

`Clippings/` 디렉터리 안의 파일들을 읽어 add-wiki 패턴으로 적합한 위키 서브모듈에 재배치한다.

## 사용법

```
/process-clippings
/process-clippings <파일명>   # 특정 파일만 처리
```

인자 없이 실행하면 `Clippings/` 디렉터리의 모든 파일을 처리한다.  
파일명을 지정하면 해당 파일만 처리한다.

---

## Claude가 수행할 단계

### 0단계 — 처리 대상 파일 목록 확인

```bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
ls "$SUPER_ROOT/Clippings/"
```

`$ARGUMENTS`가 있으면 해당 파일만, 없으면 모든 파일을 순서대로 처리한다.

---

### 각 파일에 대해 아래 단계 반복

#### 1단계 — 파일 읽기 및 주제 분석

파일의 frontmatter와 본문을 읽어 다음을 파악한다:
- **title**: 제목
- **source**: 원본 URL
- **tags**: 기존 태그
- **핵심 주제**: 어떤 분야에 속하는가

#### 2단계 — 레포 결정 (add-wiki 기준)

현재 서브모듈 참고:
- `hermes-wiki` — Hermes 메인 위키 (일반)
- `hermes-wiki-claude-code` — Claude Code 관련
- `hermes-wiki-codex` — Codex / 슬래시 커맨드
- `hermes-wiki-schedule` — 스케줄/루틴
- `harness-engineering-wiki` — 엔지니어링/개발
- `ai-job-analysis` — AI 채용/직무 분석
- `ai-marketing-wiki` — AI 마케팅
- `hermes-logs` — 로그/기록
- `hermes-slash-commands` — 슬래시 커맨드
- `subagents-library` — 서브에이전트

기존 서브모듈 목록을 먼저 확인:
```bash
cat "/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super/.gitmodules"
```

결정 이유를 한 줄로 사용자에게 설명한다. 어디에도 맞지 않으면 새 레포 이름 결정(kebab-case).

#### 3단계 — Karpathy 방식으로 위키 페이지 작성

클리핑 원문에서 **고유 인사이트만 추출**하여 위키 페이지로 변환:

```markdown
---
tags: ["<주제태그>", "<카테고리태그>"]
related: ["<관련페이지경로>"]
source: "<원본URL>"
created: YYYY-MM-DD
---

# <제목>

> <한 줄 요약>

## <핵심 섹션>

<인사이트 — 구글 1페이지에 없는 고유 분석만. 원문 전사 금지>

## Related

- [[관련페이지]] — <한 줄 설명>
```

**품질 규칙:**
- Unique insight only: 원문 요약이 아닌 핵심 인사이트 추출
- Concise: 1~5KB, 핵심만 (클리핑 원문 길이에 관계없이)
- `[[wikilinks]]` 로 교차 참조
- 파일명: kebab-case (예: `data-science-roadmap-2026.md`)

#### 4단계 — index.md 및 log.md 업데이트

레포 안의 `index.md`에 새 페이지 항목 추가:
```markdown
- [페이지제목](경로/파일명.md) — <한 줄 요약>
```

`log.md`에 변경 이력 append:
```markdown
## [YYYY-MM-DD] ingest | <페이지제목>
Clippings/<원본파일명> 에서 변환
```

#### 5단계 — 위키 레포에 push

**기존 서브모듈인 경우:**
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

**새 레포가 필요한 경우:**
```bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
WIKI_NAME="<결정된레포이름>"
GITHUB_USER="mybotagent"

gh repo create "$GITHUB_USER/$WIKI_NAME" --private --description "Wiki: $WIKI_NAME"
mkdir -p "$SUPER_ROOT/wiki/$WIKI_NAME"
cd "$SUPER_ROOT/wiki/$WIKI_NAME"
git init && git branch -M main
# Write 도구로 파일 작성
git add -A
git commit -m "init: create $WIKI_NAME"
git remote add origin "https://github.com/$GITHUB_USER/$WIKI_NAME.git"
git push -u origin main

cd "$SUPER_ROOT"
git submodule add "https://github.com/$GITHUB_USER/$WIKI_NAME.git" "wiki/$WIKI_NAME"
git add .gitmodules "wiki/$WIKI_NAME"
git commit -m "feat: add $WIKI_NAME as submodule"
git push
```

#### 6단계 — 처리 완료된 클리핑 아카이브

위키 push 성공 후 원본 클리핑 파일을 `Clippings/processed/` 폴더로 이동:
```bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
mkdir -p "$SUPER_ROOT/Clippings/processed"
mv "$SUPER_ROOT/Clippings/<파일명>" "$SUPER_ROOT/Clippings/processed/"
```

삭제하지 않고 `processed/` 폴더에 보관하여 원본을 보존한다.

---

## 완료 후 출력 (파일당)

각 파일 처리 후:
- 원본 파일명
- 배치된 레포 (기존 / 신규)
- 생성된 위키 페이지 경로
- push 성공 여부
- 아카이브 경로

여러 파일 처리 시 마지막에 처리 요약표 출력:
```
| 파일 | 레포 | 상태 |
|------|------|------|
| ... | ... | ✅/❌ |
```
