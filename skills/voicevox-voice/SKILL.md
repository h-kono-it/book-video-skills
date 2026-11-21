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

- 台本は `config/script.yaml`。声は `config/characters.yaml` の `speakerId`（VOICEVOX のスタイル ID）と `voice`（speed / pitch / intonation / volume）で決まり、全体の話速 `video-settings.yaml` の `voice.speed` が掛かる。行ごとに `voice:` で上書きもできる
- 声の変更は、`config/brief.yaml` の `cast` / `tempo` を書き換えて `npm run apply-brief` を実行する（スタイル名から ID への変換には VOICEVOX の起動が必要）
- 生成は `npm run voices`。テキスト・話者・声パラメータが変わった行だけを作り直す（`-- --all` で全行）。尺は `public/voices/durations.json` に入り、台本から消えた行の wav は掃除される
- スタイル名の一覧は `python3 $S/synth.py --speakers` で確認する

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
- テンポは `speedScale`（話速）で決める。`playbackRate` は 1.0 のままにする（再生を速めると、声が早口になるだけで間が詰まらない）。話速 1.3 を超えると聞き取りにくくなる
- 掛け合いの間（`pauseAfter`）は 10〜20 フレーム。話題の区切りは 30 フレーム

## 5. クレジット（必須）

VOICEVOX の音声を使った動画には、使った話者ごとに「VOICEVOX:ずんだもん」「VOICEVOX:四国めたん」の形式でクレジットを入れる。動画の最後と、投稿の概要欄の両方に入れる。商用利用（同人誌の宣伝・頒布）もクレジットがあれば可能だが、キャラクターごとの規約は話者ごとに異なるため、新しい話者を使うときは公式の利用規約を確認すること。
