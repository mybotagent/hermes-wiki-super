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
   
   > ⚠️ 주의사항 두 가지:
   > 1. `*/10`을 터미널에 바로 치면 zsh가 glob 패턴으로 오해함 — 아래 명령어를 **통째로 복붙**할 것
   > 2. `~/Documents/Obsidian Vault/` 경로에 **띄어쓰기**가 있음 — crontab에서 인식 못 할 수 있으므로 **절대경로 + 큰따옴표**를 권장
   
   ```bash
   # 등록 (절대경로 + 띄어쓰기 문제 해결)
   (crontab -l 2>/dev/null; echo "*/10 * * * * /Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super/sync.sh >> /Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super/sync.log 2>&1") | crontab -
   
   # 확인
   crontab -l
   ```
   
   > 터미널에 **한 줄로** 복붙해서 실행하면 끝. vi/nano 안 열어도 됨.
   
   > ⏱️ `*/1`(1분)은 너무 잦음. sync.sh가 submodule을 전부 체크하므로 `*/10`(10분) 권장.

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

---

## 포함된 레포

| 경로 | 레포 | 설명 |
|:----|:----|:------|
| `wiki/hermes-wiki` | hermes-wiki | 메인 위키 (INDEX repo) |
| `wiki/hermes-wiki-schedule` | hermes-wiki-schedule | 일정/경제지표 |
| `wiki/hermes-wiki-claude-code` | hermes-wiki-claude-code | Claude Code CLI |
| `wiki/hermes-wiki-codex` | hermes-wiki-codex | Codex CLI |
| `wiki/hermes-logs` | hermes-logs | 변경 로그 |
| `wiki/subagents-library` | subagents-library | Sub-agent 카탈로그 |
| `wiki/harness-engineering-wiki` | harness-engineering-wiki | Harness Engineering 강의 |
| `wiki/hermes-slash-commands` | hermes-slash-commands | 슬래시 명령어 문서 |
| `wiki/ai-agent-wiki` | ai-agent-wiki | AI Agent 위키 |
| `wiki/ai-marketing-wiki` | ai-marketing-wiki | AI 마케팅 위키 |
| `wiki/hermes-prompts` | hermes-prompts | 프롬프트 모음 |
| `wiki/hermes-wiki-quant` | hermes-wiki-quant | 퀀트/매크로 |
