# Append Audio layers and a ducking envelope on the music bed (lower under narration).
import json
d = json.load(open(".tesseract-work/editable.json"))
a = json.load(open(".tesseract-work/audio_layers.json"))
d["composition"]["layers"].extend(a["layers"])
json.dump(d, open(".tesseract-work/editable.json", "w"))
