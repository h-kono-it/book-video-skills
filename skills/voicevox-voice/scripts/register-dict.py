#!/usr/bin/env python3
"""dict.tsv の単語を VOICEVOX のユーザー辞書に登録/更新する（同じ表記は上書き）。

  register-dict.py [dict.tsv]
TSV: <表記>\t<読み(カタカナ)>\t<アクセント核位置(0=平板)>  # 行頭 # はコメント
"""
import json, os, sys, urllib.parse, urllib.request

HOST = os.environ.get("VOICEVOX_HOST", "http://localhost:50021")
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "dict.tsv")


def call(p, method="GET"):
    r = urllib.request.Request(HOST + p, data=b"" if method != "GET" else None, method=method)
    with urllib.request.urlopen(r, timeout=30) as res:
        body = res.read()
        return json.loads(body) if body else None


existing = {v["surface"]: k for k, v in (call("/user_dict") or {}).items()}
n = 0
for line in open(path, encoding="utf-8"):
    if not line.strip() or line.startswith("#"):
        continue
    surface, pron, accent = (line.rstrip("\n").split("\t") + ["0"])[:3]
    qs = urllib.parse.urlencode({"surface": surface, "pronunciation": pron, "accent_type": int(accent or 0)})
    # VOICEVOX は surface を全角に正規化して保存するので、既存判定は両方で見る
    uid = existing.get(surface) or existing.get(surface.translate({i: i + 0xFEE0 for i in range(0x21, 0x7F)}))
    if uid:
        call(f"/user_dict_word/{uid}?{qs}", "PUT")
    else:
        call(f"/user_dict_word?{qs}", "POST")
    n += 1
print(f"registered {n} words")
