#!/usr/bin/env python3
"""VOICEVOX でテキストを WAV にする（標準ライブラリのみ）。

  synth.py "テキスト" -s 3 -o out.wav [--speed 1.1 --pitch 0 --intonation 1.2 --volume 1.0]
  synth.py --file lines.tsv -o outdir/      # TSV: <ファイル名>\t<speaker>\t<テキスト>
  synth.py --speakers                       # 話者とスタイルIDの一覧
"""
import argparse, json, os, sys, urllib.parse, urllib.request, wave

HOST = os.environ.get("VOICEVOX_HOST", "http://localhost:50021")


def req(path, data=None, method="GET"):
    r = urllib.request.Request(HOST + path, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as res:
        return res.read()


def synth(text, speaker, out, a):
    q = json.loads(req(f"/audio_query?speaker={speaker}&text={urllib.parse.quote(text)}", b"", "POST"))
    q["speedScale"], q["pitchScale"] = a.speed, a.pitch
    q["intonationScale"], q["volumeScale"] = a.intonation, a.volume
    wav = req(f"/synthesis?speaker={speaker}", json.dumps(q).encode(), "POST")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "wb").write(wav)
    with wave.open(out) as w:
        sec = w.getnframes() / w.getframerate()
    print(f"{out}\t{sec:.2f}s")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("text", nargs="?")
    p.add_argument("-s", "--speaker", type=int, default=3)
    p.add_argument("-o", "--out", default="out.wav")
    p.add_argument("--file")
    p.add_argument("--speakers", action="store_true")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--pitch", type=float, default=0.0)
    p.add_argument("--intonation", type=float, default=1.0)
    p.add_argument("--volume", type=float, default=1.0)
    a = p.parse_args()
    try:
        req("/version")
    except Exception:
        sys.exit(f"VOICEVOX エンジンに繋がらない: {HOST}（アプリを起動して）")
    if a.speakers:
        for sp in json.loads(req("/speakers")):
            print(sp["name"], " / ".join(f'{s["name"]}={s["id"]}' for s in sp["styles"]))
    elif a.file:
        for line in open(a.file, encoding="utf-8"):
            if not line.strip() or line.startswith("#"):
                continue
            name, spk, text = line.rstrip("\n").split("\t", 2)
            synth(text, int(spk), os.path.join(a.out, name), a)
    elif a.text:
        synth(a.text, a.speaker, a.out, a)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
