#!/bin/bash
SUPER_ROOT="/Users/sanghee/Documents/Obsidian Vault/hermes-wiki-super"
CLIPPINGS=$(ls "$SUPER_ROOT/Clippings/" 2>/dev/null | grep -v "^processed$" | wc -l | tr -d ' ')
if [ "$CLIPPINGS" -gt 0 ]; then
  echo "📥 미처리 Clippings ${CLIPPINGS}개 대기 중 (/process-clippings로 처리 가능)"
fi
