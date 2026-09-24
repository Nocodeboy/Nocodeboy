#!/bin/bash
# Rebuild the bulletin from sources into GO-Ebola-DRC-2026-09-24.tsrct
set -euo pipefail
cd "$(dirname "$0")/.."
T="${XDG_DATA_HOME:-$HOME/.local/share}/Tesseract/bin/tsrct"
P=.tesseract-work/build.tsrct
python3 .tesseract-work/build.py > .tesseract-work/build.log
rm -f "$P"; "$T" project create --project "$P" >/dev/null
for f in Bold SemiBold; do "$T" project import-font --project "$P" --file .tesseract-work/fonts/BarlowCondensed-$f.ttf >/dev/null 2>&1; done
for v in 1 2 3 4 5 6 7; do "$T" project import-asset --project "$P" --file .tesseract-work/audio/vo$v-master.wav --asset-id vo-vo$v --kind audio >/dev/null; done
"$T" project import-asset --project "$P" --file .tesseract-work/audio/news-bed-81s.wav --asset-id music-bed --kind audio >/dev/null
"$T" project import-asset --project "$P" --file .tesseract-work/audio/ident-sting.wav --asset-id sfx-sting --kind audio >/dev/null
"$T" project import-asset --project "$P" --file .tesseract-work/audio/wipe-whoosh.wav --asset-id sfx-whoosh --kind audio >/dev/null
"$T" project import-video --project "$P" --file "${PRESENTER_FILE:-Sources/presenter/anchor-intro-veed.mp4}" --asset-id presenter >/dev/null
"$T" project checkout --project "$P" --output .tesseract-work/editable.json >/dev/null
python3 -c "
import json; d=json.load(open('.tesseract-work/editable.json')); d['duration']=81.0
json.dump(d,open('.tesseract-work/editable.json','w'))"
"$T" project commit --project "$P" --file .tesseract-work/editable.json >/dev/null
"$T" project apply --project "$P" --actions .tesseract-work/actions.json >/dev/null
"$T" project checkout --project "$P" --output .tesseract-work/editable.json >/dev/null
python3 - <<'PY'
import json
d = json.load(open(".tesseract-work/editable.json")); m = json.load(open(".tesseract-work/media.json"))
L = d["composition"]["layers"]
bg = [i for i, l in enumerate(L) if l.get("id") == m["background"]][0]
L.insert(bg, m["video"])            # just in front of the background, behind every scene group
L.extend(m["media"])
json.dump(d, open(".tesseract-work/editable.json", "w"))
json.dump(m["audio_actions"], open(".tesseract-work/audio_actions.json", "w"))
PY
"$T" project commit --project "$P" --file .tesseract-work/editable.json >/dev/null
"$T" project apply --project "$P" --actions .tesseract-work/audio_actions.json >/dev/null
OUT="${OUT:-GO-Ebola-DRC-2026-09-24}"
mv "$P" "$OUT.tsrct"
echo "built $OUT.tsrct"
