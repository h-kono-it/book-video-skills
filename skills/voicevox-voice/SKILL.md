---
name: voicevox-voice
description: VOICEVOX でセリフやナレーションを音声合成する。「音声を生成して」「読み上げて」「ずんだもんに喋らせて」「発音がおかしい」「読みを直して」「話者を変えたい」など、音声づくり・読み修正・ユーザー辞書の登録をするときに使う。動画の台本づくりや合成は book-video スキルの担当で、このスキルは音声だけを扱う。
---

# VOICEVOX 音声合成

音声だけを担当する。動画プロジェクト（`~/workspace/book-videos/<slug>/`）の中でも外でも使える。

## 0. エンジンの確認

```bash
curl -s -m 2 localhost:50021/version || echo "VOICEVOX が起動していない"
```

起動していなければ、VOICEVOX アプリ（https://voicevox.hiroshiba.jp/ ）を起動してもらう。アプリが入っていなければ、ユーザーにインストールを頼む（Homebrew の cask はない）。生成中にアプリを終了しないこと。

## 1. 動画プロジェクトの中で使うとき

- 台本の正本は `config/script.yaml`。話者 ID は `config/characters.yaml` の `speakerId` にある（ずんだもん=3、四国めたん=2）
- 一括生成は `npm run voices`。`public/voices/NN_<character>.wav` と `durations.json` が更新され、`src/data/script.ts` に尺が反映される
- `npm run voices` は毎回すべての行を作り直す（尺の整合が保たれるので、1行だけ直した場合もこれでよい）

## 2. 単発で使うとき / プロジェクトの外

```bash
S=~/.claude/skills/voicevox-voice/scripts
python3 $S/synth.py --speakers                         # 話者・スタイル ID 一覧
python3 $S/synth.py "こんにちはなのだ" -s 3 -o /tmp/a.wav --speed 1.1
python3 $S/synth.py --file lines.tsv -o out/            # TSV: ファイル名\t話者ID\tテキスト
```

## 3. 読み（発音）の直し方：優先順位

1. **ユーザー辞書**（推奨）: `~/.claude/skills/voicevox-voice/dict.tsv` に「表記・読み・アクセント核」を追記し、`python3 $S/register-dict.py` を実行して登録する。こうすると台本は英語表記のままで読みだけが直り、`displayText` を二重管理せずに済む。登録した辞書は VOICEVOX 側に残るので、毎回登録し直す必要はない
2. **その行だけの言い換え**: `text` にカタカナを書き、`displayText` に字幕用の表記を入れる
3. 数字・記号: 「Java 21」→「ジャバ ニジュウイチ」、「→」「/」は読まれ方が不安定なので、言葉に開く

直したあとは、該当行だけを再生成して確かめる。

## 4. 聞きやすさの目安

- 1行あたり 40 文字以内。長いセリフは2行に分ける
- 動画側で 1.2 倍速再生しているので（`video-settings.yaml` の `playbackRate`）、`speedScale` は 1.0 のままにする
- 掛け合いの間（`pauseAfter`）は 10〜20 フレーム。話題の区切りは 30 フレーム

## 5. クレジット（必須）

VOICEVOX の音声を使った動画には、使った話者ごとに「VOICEVOX:ずんだもん」「VOICEVOX:四国めたん」の形式でクレジットを入れる。動画の最後と、投稿の概要欄の両方に入れる。商用利用（同人誌の宣伝・頒布）もクレジットがあれば可能だが、キャラクターごとの規約は話者ごとに異なるため、新しい話者を使うときは公式の利用規約を確認すること。
