#!/bin/bash
# ============================================================
# sync.sh — hermes-wiki-super 양방향 자동 동기화 스크립트
# 사용법: cron에 등록해서 10분마다 실행
#   crontab -e
#   */10 * * * * /ABSOLUTE/PATH/hermes-wiki-super/sync.sh >> /ABSOLUTE/PATH/hermes-wiki-super/sync.log 2>&1
#   ※ ~/Documents/Obsidian Vault/처럼 띄어쓰기 있는 경로는 절대경로+큰따옴표로 감쌀 것
#   ※ zsh에서 */10 glob 오류 → crontab -e로 직접 입력하거나 echo로 등록
# ============================================================

cd "$(dirname "$0")"

echo "=== Sync started: $(date) ==="

# 1️⃣ 내려받기 (pull) — Hermes/다른 기기에서 수정한 내용 반영
echo ">>> Pulling super repo..."
git pull
echo ">>> Updating submodules..."
git submodule update --remote

# 2️⃣ 올리기 (push) — Obsidian/로컬에서 수정한 내용 자동 커밋+푸시
echo ">>> Checking submodules for local changes..."
git submodule foreach 'git add -A && if ! git diff --cached --quiet; then git commit -m "obsidian: auto-sync $(date +%Y-%m-%d_%H:%M)" && git push && echo "  ✅ Pushed $name" || echo "  ❌ Failed $name"; else echo "  ➖ No changes in $name"; fi'

# 3️⃣ super repo ref 갱신 + 푸시
echo ">>> Updating super repo refs..."
git add -A
if ! git diff --cached --quiet; then
    git commit -m "sync: update submodule refs $(date +%Y-%m-%d_%H:%M)"
    git push
    echo "✅ Super refs updated and pushed"
else
    echo "➖ No super repo ref changes"
fi

echo "=== Sync completed: $(date) ==="
