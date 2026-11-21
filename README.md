# book-video-skills

技術同人誌や Web サービスの解説・宣伝動画を、ずんだもん（＋四国めたんなど）の掛け合いで作るための [Claude Code](https://claude.com/claude-code) 用 user skills。
「この本の宣伝動画を1分で、テンポ速めで」のように頼むと、構成案 → 台本 → 音声 → 合成 → 書き出しまで進める。

| skill | 役割 |
|---|---|
| `book-video` | 指揮役。ブリーフ（尺・テンポ・声・キャスト・縦横）、構成、台本、合成、確認、書き出し |
| `voicevox-voice` | VOICEVOX による音声合成と、読みのユーザー辞書（`dict.tsv`） |
| `web-capture` | Playwright による Web 画面の録画・スクショ |

## 必要なもの

- 動画テンプレート [book-video-template](https://github.com/h-kono-it/book-video-template)（[remotion-voicevox-template](https://github.com/nyanko3141592/remotion-voicevox-template) の拡張版）
- [VOICEVOX](https://voicevox.hiroshiba.jp/)（起動しておく）
- Node.js 20+、`brew install poppler imagemagick`
- macOS（`new-video.sh` は APFS の `cp -c` を使う）

## インストール

```bash
# テンプレート（スキルは ~/workspace/book-videos/_template を前提にしている）
mkdir -p ~/workspace/book-videos
git clone https://github.com/h-kono-it/book-video-template ~/workspace/book-videos/_template
(cd ~/workspace/book-videos/_template && npm install && npx playwright install chromium)

# スキル
git clone https://github.com/h-kono-it/book-video-skills ~/workspace/book-video-skills
for s in ~/workspace/book-video-skills/skills/*; do ln -s "$s" ~/.claude/skills/$(basename "$s"); done

# 読み辞書を VOICEVOX に登録
python3 ~/workspace/book-video-skills/skills/voicevox-voice/scripts/register-dict.py
```

置き場所を変える場合は `skills/book-video/scripts/new-video.sh` の `BASE` と、各 SKILL.md のパスを書き換える。

## 使い方

Claude Code で、たとえばこう頼む。

- 「`~/workspace/my-book` を X で宣伝する動画を作って。1分くらいで、テンポ速めで」
- 「縦型の30秒ショートで、ずんだもんだけで」
- 「このアプリの操作をデモする解説動画を作りたい」（web-capture で収録する）

## 注意

- VOICEVOX の音声を使った動画には、話者ごとに「VOICEVOX:ずんだもん」のようなクレジットが必要。キャラクターごとの利用規約も確認すること
- 表紙・イラスト・BGM などの素材は、権利を確認したものだけを使う

## License

MIT
