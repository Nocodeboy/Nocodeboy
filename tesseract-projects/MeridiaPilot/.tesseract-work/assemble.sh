#!/bin/bash
# Rebuild MeridiaPilot.tsrct from the sources: fonts, audio, visual actions, audio layers.
set -euo pipefail
cd "$(dirname "$0")/.."
T="${XDG_DATA_HOME:-$HOME/.local/share}/Tesseract/bin/tsrct"
P=.tesseract-work/build.tsrct
python3 .tesseract-work/build.py
rm -f "$P"; "$T" project create --project "$P" >/dev/null
for f in Bold SemiBold; do "$T" project import-font --project "$P" --file .tesseract-work/fonts/BarlowCondensed-$f.ttf >/dev/null 2>&1; done
for v in 1 2 3 4 5 6; do "$T" project import-asset --project "$P" --file .tesseract-work/audio/vo$v-master.wav --asset-id vo-vo$v --kind audio >/dev/null; done
"$T" project import-asset --project "$P" --file Sources/music/news-bed-procedural.wav --asset-id music-bed --kind audio >/dev/null
for s in riser:ident-riser impact:ident-impact whoosh:wipe-whoosh ping:outro-ping; do "$T" project import-asset --project "$P" --file Sources/sfx/${s#*:}.wav --asset-id sfx-${s%%:*} --kind audio >/dev/null; done
# duration first (seconds), then the visual batch, then audio layers
"$T" project checkout --project "$P" --output .tesseract-work/editable.json >/dev/null
python3 -c "
import json; d=json.load(open('.tesseract-work/editable.json')); d['duration']=50.5
json.dump(d,open('.tesseract-work/editable.json','w'))"
"$T" project commit --project "$P" --file .tesseract-work/editable.json >/dev/null
"$T" project apply --project "$P" --actions .tesseract-work/actions.json
"$T" project checkout --project "$P" --output .tesseract-work/editable.json >/dev/null
python3 .tesseract-work/add_audio.py
"$T" project commit --project "$P" --file .tesseract-work/editable.json
"$T" project apply --project "$P" --actions .tesseract-work/audio_actions.json
mv "$P" MeridiaPilot.tsrct
echo built MeridiaPilot.tsrct
