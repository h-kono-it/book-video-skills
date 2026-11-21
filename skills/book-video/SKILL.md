---
name: book-video
description: 自作の技術同人誌（Vivliostyle）や Web サービスの解説動画・宣伝動画を、ずんだもん（＋四国めたんなど）の掛け合いやナレーションで作る。「この本の解説動画を作りたい」「新刊の宣伝動画」「告知用のショート動画」「60秒で」「テンポ速めで」「ずんだもんだけで」など、動画づくりや動画のパラメータ指定の依頼で使う。構成→台本→素材→合成→書き出しまでを指揮し、音声は voicevox-voice、画面収録は web-capture スキルに任せる。
---

# 本・サービスの解説／宣伝動画

## 全体像

```
~/workspace/book-videos/
├── _template/        Remotion + VOICEVOX テンプレート（拡張版）。直接編集しない
└── <slug>/           動画1本につき1プロジェクト
```

プロジェクト内の `CLAUDE.md` の冒頭に、ブリーフ・合成の書式（`bg` / `telop` / `marks`）・npm スクリプトがまとまっている。**台本の正本は `config/script.yaml`、指示の正本は `config/brief.yaml`。**

担当の切り分け:
- 音声の生成・読みの修正・辞書 → **voicevox-voice**
- Playwright による録画・スクショ → **web-capture**
- それ以外（ブリーフ、構成、台本、素材の配置、合成、確認、書き出し）→ このスキル

## 指示できるパラメータ（config/brief.yaml）

ユーザーの言葉をこの表に当てはめる。言及がない項目は既定値のままにする。

| key | 既定 | 値 | ユーザーの言い方の例 |
|---|---|---|---|
| `kind` | promo | `promo` 宣伝 / `explainer` 解説 | 「宣伝」「告知」/「解説」「紹介」 |
| `length` | promo 60 / explainer 300 | 目標の秒数（±10% に収める） | 「1分」「30秒のショート」「5分くらい」 |
| `tempo` | normal | `slow` / `normal` / `fast` / `{ speed, pauseScale }` | 「ゆっくり」「テンポよく」「早口で」 |
| `aspect` | landscape | `landscape` / `portrait` / `square` | 「縦型」「ショート」「TikTok」→ portrait |
| `cast` | `[zundamon, metan]` | 先頭が説明役。1人ならソロのナレーション | 「ずんだもんだけ」「つむぎも出して」 |
| `cast[].style` / `voice` | ノーマル / なし | VOICEVOX のスタイル名、`pitch` `intonation` `speed` | 「あまあまボイスで」「抑揚強め」「少し低く」 |
| `subtitles` | true | true / false | 「字幕なし」 |
| `audience` | 中級者 | 自由記述 | 「Java初心者向け」 |
| `tone` | ゆるめ | ゆるめ / まじめ / ハイテンション | 「真面目に」「ノリよく」 |
| `scope` | all | 扱う章（原稿のファイル名） | 「21と25の章だけ」 |
| `se` | few | none / few / normal | 「効果音なし」 |
| `bgm` | off | ファイル名 / off | 「BGMつけて」（素材はユーザーが用意する） |
| `cta` | 空欄 | event / space / price / url | 頒布情報。**推測で埋めない** |

テンポの中身: `slow` = 話速 1.0・間 ×1.4、`normal` = 1.15・×1.0、`fast` = 1.3・×0.6。

同梱の立ち絵があるのはずんだもんと四国めたんだけ。ほかの話者は `{ id: tsumugi, speaker: 春日部つむぎ, style: ノーマル, image: null }` のように指定して、立ち絵なし（声と字幕だけ）にするか、ユーザーに立ち絵の素材（`public/images/<id>/mouth_open.png`・`mouth_close.png`）を用意してもらう。

## 1. ヒアリング

指示から決まらない項目のうち、**題材・kind・cta だけ**を AskUserQuestion で聞く。そのほかは既定値で進め、ブリーフを見せるときに「ここは既定値にした」と伝える。

## 2. プロジェクトを作り、ブリーフを反映する

```bash
~/.claude/skills/book-video/scripts/new-video.sh <slug> [book_dir]
cd ~/workspace/book-videos/<slug>
# config/brief.yaml を書く
npm run apply-brief
```

`book_dir` を渡すと、表紙・裏表紙・PDF の全ページ（`public/content/book/pages/p-NNN.png`）と見出し一覧 `book-outline.md` を取り込む。

## 3. 構成案 → ユーザーの承認

`book-outline.md` と原稿（`<book>/src/*.md`、`scope` の範囲）を読み、**シーン表**を作ってユーザーに見せる。各シーンの秒数の合計は `length` に合わせる。**承認されるまで台本は書かない。**

| # | 秒 | 内容 | 背景 | テロップ |
|---|---|---|---|---|

尺の目安: 1行は、話速 1.0 で約 7 文字/秒。60 秒なら 10〜14 行、5 分なら 50〜70 行。

### explainer の型
1. つかみ（10 秒）: 読者が抱えていそうな悩みや問いを投げかける
2. 本の紹介: 表紙の画像に `title` テロップを重ねる
3. 章ごとに 1 シーン: 要点を1つに絞る。背景はその章の代表ページ、`label` で章名を出す。コード例のページは `marks` で注目箇所を囲む
4. まとめ → 頒布情報 → クレジット

### promo の型
1. フック（3 秒以内）: `emphasis` テロップで問いや数字を出す
2. 本の紹介: 表紙に `kenBurns: in`
3. 推しポイントを3つ: 各 1〜2 行。背景はそのポイントが載っているページ
4. 頒布情報: `title` と `note` で、最後の 5 秒以上は画面に出したままにする
5. クレジット

ページを選ぶときは `public/content/book/pages/` を Read で実際に見て、図やコードのあるページを選ぶ。

## 4. 台本（config/script.yaml）

- 口調は `tone` に合わせる。ずんだもんは「〜なのだ」、めたんは「〜わ」「〜かしら？」。ソロのときは、ずんだもんが視聴者に語りかける形にする
- **原稿に書いてあることだけを話す**。本にない主張や数字は足さない。宣伝で誇張しない
- 1行は 40 文字以内。専門用語の読みは voicevox-voice の辞書に任せ、`text` は表記どおりに書く
- `pauseAfter` は特別な間（話題の区切り = 30 など）を取りたい行にだけ書く。それ以外は既定値に `pauseScale` が掛かる
- `bg` は場面が変わる行にだけ書く。`telop` と `marks` は、ここぞという行にだけ使う
- 最後に、VOICEVOX のクレジットを出す: `telop: { text: "VOICEVOX:ずんだもん / VOICEVOX:四国めたん", style: note, position: bottom }`（cast の全員分）

**書いたらすぐ `npm run duration` を実行し**、見積もりが `length` の ±10% に入るまで行数を調整する。

## 5. 音声 → 尺の調整 → 見た目の確認

1. voicevox-voice スキルの手順で、辞書の登録と `npm run voices` を行う
2. `npm run duration` で実際の尺を確認する。外れていれば、まず行を足すか削り、それでも足りない分を `tempo` で微調整する（`{ speed: 1.2, pauseScale: 0.8 }` のように数値で指定できる）→ `npm run apply-brief` → `npm run voices`
3. **静止画で確認する**: `npm run duration` が出す各行の開始フレームを使い、シーンの切り替わり目ごとに `npx remotion still src/index.ts Main out/check-<n>.png --frame=<N>` を出して Read で目視する。見るのは、テロップと字幕・キャラの重なり、`marks` の位置、文字のはみ出し
4. ユーザーに見てもらうときは `npm start` で Remotion Studio（http://localhost:3000 ）を案内する

## 6. 書き出し

```bash
npx remotion render src/index.ts Main out/<slug>.mp4
```

書き出したら、尺とファイルの場所を伝える。投稿用の概要欄の文面（本の紹介、頒布情報、VOICEVOX のクレジット）も一緒に用意する。

## 素材と権利のチェック（書き出し前に必ず）

- VOICEVOX のクレジット（cast の全員分）が、動画の最後と概要欄の両方に入っているか
- キャラクター画像: テンプレートに同梱の画像は、作者から改変・再配布の許可が出ている。差し替える場合は、その素材の規約を確認する
- 表紙・本文: ユーザー自身の著作物なので使ってよい。ただし共著の本や、表紙を外部のイラストレーターに依頼している本は、動画への使用について確認する
- BGM・効果音は、配布元の規約を確認したものだけを `public/bgm`・`public/se` に置く
- Web 録画に個人情報・実データ・トークンが映っていないか
