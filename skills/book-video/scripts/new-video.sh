#!/usr/bin/env bash
# テンプレートから新しい動画プロジェクトを作る
#   new-video.sh <slug> [book_dir]
# 例: new-video.sh java-ge-promo ~/workspace/vivliostyle-java-tech-book-2026-v2
set -euo pipefail
SLUG="${1:?usage: new-video.sh <slug> [book_dir]}"
BOOK="${2:-}"
BASE="$HOME/workspace/book-videos"
TPL="$BASE/_template"
DEST="$BASE/$SLUG"

[ -e "$DEST" ] && { echo "既に存在する: $DEST" >&2; exit 1; }
# APFS の clonefile で node_modules ごと一瞬でコピー（容量もほぼ食わない）
cp -cR "$TPL" "$DEST"
cd "$DEST"
rm -rf .git out public/voices/*.wav public/content/book public/content/rec public/content/shots book-outline.md
echo '{}' > public/voices/durations.json
cat > config/script.yaml <<'EOF'
# 台本。編集後 npm run voices → npm run sync
[]
EOF
git init -q && git add -A && git commit -q -m "init from _template"

if [ -n "$BOOK" ]; then
  echo "BOOK_DIR=$BOOK" > .book
  bash scripts/import-book.sh "$BOOK"
fi
echo "created: $DEST"
