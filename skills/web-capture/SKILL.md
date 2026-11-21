---
name: web-capture
description: Playwright で Web サービスの操作を録画したり、スクリーンショットを撮ったりして動画の素材を作る。「画面を録画して」「デモを収録して」「スクショ紙芝居にしたい」「このアプリの操作動画の素材がほしい」と言われたときに使う。録画した素材を動画に合成するのは book-video スキルの担当。
---

# Web 画面の収録（Playwright）

動画プロジェクト（`~/workspace/book-videos/<slug>/`）の中で実行する。収録スクリプトの本体はテンプレートの `scripts/capture.ts` にある。

## 手順

1. **何を見せるかを先に決める**: 台本のシーンごとに「この画面で、この操作を、何秒くらい」と書き出す。録画は台本に合わせて撮る（逆にすると尺が合わない）
2. **シナリオを書く**: `captures/<name>.ts`（雛形は `captures/example.ts`）
   - 区切りごとに `await mark("ラベル")` を呼ぶ。録画上の秒数が `public/content/rec/<name>.marks.json` に出るので、台本の `bg.startFrom` にそのまま使う
   - 紙芝居にする場面では `await shot("ラベル")` を呼ぶ → `public/content/shots/<name>/<ラベル>.png`
   - 人が見て追える速さで操作する: `page.mouse.move(x, y, { steps: 25 })` でカーソルをゆっくり動かし、操作のあとに `pause(800〜1500)` を入れる。入力は `locator.pressSequentially(text, { delay: 60 })`
   - ローカルのサービスなら、起動しているかを先に確認する（`curl -s -o /dev/null -w '%{http_code}' <url>`）
3. **実行する**: `npm run capture -- captures/<name>.ts`
4. **確認する**: `npx remotion ffprobe public/content/rec/<name>.webm` で尺を見る。スクショは Read で目視する
5. 撮り直しはシナリオを直して再実行する（同じ名前で上書きされる）

## options

```ts
export const options = { width: 1920, height: 1080, record: true, deviceScaleFactor: 1, colorScheme: "light" };
```

- 横型動画では 1920x1080 のまま。縦型のショート動画でスマホ画面を見せたいときは `width: 1080, height: 1920`（または 390x844 に `deviceScaleFactor: 3`）
- スクショだけ欲しいときは `record: false`

## 気をつけること

- ログインが必要なサービスで、本番の認証情報をシナリオに直書きしない。テスト用アカウントを環境変数（`process.env.DEMO_PASSWORD`）から渡す
- 画面に個人情報・実データ・トークンが映らないか、収録後にスクショで確認する
- 疑似カーソル（赤い丸）が自動で入る。消したいときは `scripts/capture.ts` の `FAKE_CURSOR` を外す
