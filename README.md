# book-video-skills

技術同人誌や Web サービスの解説・宣伝動画（ずんだもん＆四国めたん）を Claude Code で作るための user skills。

| skill | 役割 |
|---|---|
| `book-video` | 指揮役。構成 → 台本 → 合成 → 書き出し |
| `voicevox-voice` | VOICEVOX による音声合成、読みの辞書（`dict.tsv`） |
| `web-capture` | Playwright による画面の録画・スクショ |

動画テンプレートは `~/workspace/book-videos/_template`（[remotion-voicevox-template](https://github.com/nyanko3141592/remotion-voicevox-template) の拡張版）を前提にしている。

## インストール

```bash
git clone <this repo> ~/workspace/book-video-skills
for s in ~/workspace/book-video-skills/skills/*; do ln -s "$s" ~/.claude/skills/$(basename "$s"); done
```
