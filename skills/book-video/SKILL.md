---
name: book-video
description: 自作の技術同人誌（Vivliostyle）や Web サービスの解説動画・宣伝動画を、ずんだもん＆四国めたんの掛け合いで作る。「この本の解説動画を作りたい」「新刊の宣伝動画」「告知用のショート動画」「紹介動画を作って」と言われたときに使う。構成→台本→素材→合成→書き出しまでを指揮し、音声は voicevox-voice、画面収録は web-capture スキルに任せる。
---

# 本・サービスの解説／宣伝動画

## 全体像

```
~/workspace/book-videos/
├── _template/        Remotion + VOICEVOX テンプレート（拡張版）。直接編集しない
└── <slug>/           動画1本につき1プロジェクト
```

合成の書式（`bg` / `telop` / `marks`）と npm スクリプトは、プロジェクト内の `CLAUDE.md` の冒頭にある。**台本の正本は `config/script.yaml`**。

担当の切り分け:
- 音声の生成・読みの修正・辞書 → **voicevox-voice**
- Playwright による録画・スクショ → **web-capture**
- それ以外（構成、台本、素材の配置、合成、確認、書き出し）→ このスキル

## 1. ヒアリング（最初に一度だけ、まとめて聞く）

AskUserQuestion で、決まっていないものだけ聞く。

- **題材**: 本のリポジトリのパス（`~/workspace/vivliostyle-*` など）／Web サービスの URL
- **種類**:
  - `explainer` 解説: 横 1920x1080、3〜8 分。章ごとに要点を掛け合いで話す
  - `promo` 宣伝: 30〜60 秒。横（YouTube・X）か縦 1080x1920（ショート・TikTok）か
- **頒布情報**: イベント名、日付、スペース番号、価格、BOOTH などの URL。**推測で埋めない。わからなければ空欄のまま確認する**
- **背景の方針**: 本のページ／スクショ紙芝居／Playwright 録画／混在

## 2. プロジェクトを作る

```bash
~/.claude/skills/book-video/scripts/new-video.sh <slug> [book_dir]
cd ~/workspace/book-videos/<slug>
```

`book_dir` を渡すと、表紙・裏表紙・PDF の全ページ（`public/content/book/pages/p-NNN.png`）と見出し一覧 `book-outline.md` を取り込む。PDF がなければ、本のリポジトリで先にビルドしてもらう。縦型にする場合は、CLAUDE.md の「縦型」の設定を適用する。

## 3. 構成案 → ユーザーの承認

`book-outline.md` と原稿（`<book>/src/*.md`）を読み、**シーン表**を作ってユーザーに見せる。**承認されるまで台本は書かない。**

| # | 尺 | 内容 | 背景 | テロップ |
|---|---|---|---|---|

### explainer の型
1. つかみ（10 秒）: 読者が抱えていそうな悩みや問いを、めたんが投げかける
2. 本の紹介: 表紙の画像に `title` テロップを重ねる
3. 章ごとに 1 シーン: 章の要点を1つに絞って話す。背景はその章の代表ページ、`label` で章名を出す。コード例のページは `marks` で注目箇所を囲む
4. まとめ → 頒布情報 → クレジット

### promo の型（60 秒なら 10〜14 行が目安）
1. フック（3 秒以内）: `emphasis` テロップで問いや数字を出す（例:「Java 18〜27 を1冊で」）
2. 本の紹介: 表紙に `kenBurns: in`
3. 推しポイントを3つ: 各 1〜2 行。背景はそのポイントが載っているページ
4. 頒布情報: イベント・スペース・価格を `title` と `note` で、最後の 5 秒以上は画面に出したままにする
5. クレジット

ページを選ぶときは `public/content/book/pages/` を Read で実際に見て、文字が多すぎないページ・図やコードがあるページを選ぶ。

## 4. 台本（config/script.yaml）

- ずんだもん（説明役）は「〜なのだ」、めたん（聞き役・ツッコミ）は「〜わ」「〜かしら？」
- **原稿に書いてあることだけを話す**。本にない主張や数字は足さない。宣伝で誇張しない
- 1行は 40 文字以内。専門用語の読みは voicevox-voice の辞書に任せ、`text` は表記どおりに書く（辞書で直らない行だけ `displayText` を使う）
- `bg` は場面が変わる行にだけ書く（次の `bg` までその背景が続く）。`telop` と `marks` は、ここぞという行にだけ使う
- 表情の差分と効果音は控えめにする（効果音は 1 本あたり 5〜10 個まで）
- 最後の行のあと、画面にクレジットを出す: `telop: { text: "VOICEVOX:ずんだもん / VOICEVOX:四国めたん", style: note, position: bottom }`

## 5. 音声 → 確認

1. voicevox-voice スキルの手順で、辞書の登録と `npm run voices` を行う
2. `npm run sync`
3. **静止画で確認する**: シーンの切り替わり目ごとに `npx remotion still src/index.ts Main out/check-<n>.png --frame=<N>` を出し、Read で目視する。見るのは、テロップと字幕・キャラが重なっていないか、`marks` の位置が合っているか、文字が画面からはみ出していないか
   - フレーム番号は `src/data/script.ts` の各行の `ceil(durationInFrames/1.2) + ceil(pauseAfter/1.2)` を足し合わせて求める
4. ユーザーに見てもらうときは `npm start` で Remotion Studio（http://localhost:3000 ）を案内する

## 6. 書き出し

```bash
npx remotion render src/index.ts Main out/<slug>.mp4
```

書き出したら、尺とファイルの場所を伝える。投稿用の概要欄の文面（本の紹介、頒布情報、VOICEVOX のクレジット）も一緒に用意する。

## 素材と権利のチェック（書き出し前に必ず）

- VOICEVOX のクレジット（話者ごと）が、動画の最後と概要欄の両方に入っているか
- キャラクター画像: テンプレートに同梱の画像は、作者から改変・再配布の許可が出ている。差し替える場合は、その素材の規約を確認する
- 表紙・本文: ユーザー自身の著作物なので使ってよい。ただし共著の本や、表紙を外部のイラストレーターに依頼している本は、動画への使用について確認する
- BGM・効果音は、配布元の規約を確認したものだけを `public/bgm`・`public/se` に置く
- Web 録画に個人情報・実データ・トークンが映っていないか
