# hermes-wiki-super

mybotagent 계정의 모든 wiki 레포를 **submodule**로 모은 super 저장소.

> **하나만 clone하면 모든 wiki 레포가 따라온다**

## 사용법

```bash
# 처음 클론
git clone --recurse-submodules https://github.com/mybotagent/hermes-wiki-super.git

# 이후 최신 상태로 업데이트
cd hermes-wiki-super
git pull
git submodule update --remote
```

## Obsidian 연동

1. Obsidian 볼트 폴더에 위 명령어로 clone
2. Obsidian Git 플러그인: `Pull on startup: ON`
3. (선택) cron에 등록: `*/10 * * * * cd /path/to/hermes-wiki-super && git pull && git submodule update --remote`

## 모바일 (iOS) — Working Copy

1. Working Copy에서 `hermes-wiki-super` clone
2. 서브모듈은 Working Copy에서 알아서 관리 가능
3. 주기적으로 Pull

## 포함된 레포

| 경로 | 레포 | 설명 |
|:----|:----|:------|
| `wiki/hermes-wiki` | hermes-wiki | 메인 위키 (INDEX repo) |
| `wiki/hermes-wiki-portfolio` | hermes-wiki-portfolio | 포트폴리오/증시 분석 |
| `wiki/hermes-wiki-schedule` | hermes-wiki-schedule | 일정/경제지표 |
| `wiki/hermes-wiki-claude-code` | hermes-wiki-claude-code | Claude Code CLI |
| `wiki/hermes-wiki-codex` | hermes-wiki-codex | Codex CLI |
| `wiki/hermes-logs` | hermes-logs | 변경 로그 |
| `code/stock-analysis-toolkit` | stock-analysis-toolkit | 주식 분석 스크립트 |
| `wiki/subagents-library` | subagents-library | Sub-agent 카탈로그 |
| `wiki/harness-engineering-wiki` | harness-engineering-wiki | Harness Engineering 강의 |
| `wiki/ai-job-analysis` | ai-job-analysis | AI Agent 직업 분석 |
| `wiki/hermes-slash-commands` | hermes-slash-commands | 슬래시 명령어 문서 |
