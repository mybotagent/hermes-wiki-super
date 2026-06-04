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

1. Obsidian 볼트 폴더에 clone
   ```bash
   git clone --recurse-submodules https://github.com/mybotagent/hermes-wiki-super.git \
     ~/Documents/Obsidian\ Vault/hermes-wiki-super
   ```

2. **양방향 sync 스크립트 생성**
   
   > ⚠️ Obsidian Git 플러그인은 루트 레포만 감지하므로, submodule 내부 수정은 별도 스크립트가 필요함.
   
   ```bash
   # ~/Documents/Obsidian\ Vault/hermes-wiki-super/sync.sh
   #!/bin/bash
   cd ~/Documents/Obsidian\ Vault/hermes-wiki-super

   # 1️⃣ 내려받기 (pull) — Hermes/다른 기기에서 수정한 내용 반영
   git pull
   git submodule update --remote

   # 2️⃣ 올리기 (push) — Obsidian에서 수정한 내용 자동 커밋+푸시
   git submodule foreach 'git add -A && git diff --cached --quiet || (git commit -m "obsidian: auto-sync $(date +%Y-%m-%d_%H:%M)" && git push)'

   # 3️⃣ super repo ref 갱신 + 푸시
   git add -A
   git diff --cached --quiet || (git commit -m "sync: update submodule refs $(date +%Y-%m-%d_%H:%M)" && git push)
   ```
   
   ```bash
   chmod +x ~/Documents/Obsidian\ Vault/hermes-wiki-super/sync.sh
   ```

3. **cron 등록 (10분마다 자동 sync)**
   ```bash
   crontab -e
   */10 * * * * ~/Documents/Obsidian\ Vault/hermes-wiki-super/sync.sh >> ~/Documents/Obsidian\ Vault/hermes-wiki-super/sync.log 2>&1
   ```

4. **Obsidian Git 플러그인**
   - 설치: 커뮤니티 플러그인 → "Obsidian Git"
   - 설정: `Pull on startup: ON`

### 동작 방식

| 상황 | 스크립트 동작 |
|:----|:----------|
| Hermes가 wiki에 푸시 | → pull 받아서 Obsidian에 최신 반영 ✅ |
| Obsidian에서 수정 | → 해당 submodule만 자동 커밋+푸시 ✅ |
| 아무 변화 없음 | → 조용히 종료 (로그만 남음) ✅ |
| 충돌 발생 | → 드묾, 발생 시 수동 해결 |

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
