# Word timestamps for each narration clip (timings from the model; caption text is ours).
import json, glob
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8")
out = {}
for f in sorted(glob.glob("Sources/voice/vo*.mp3")):
    segs, _ = m.transcribe(f, word_timestamps=True, vad_filter=False, beam_size=5)
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in (s.words or [])]
    key = f.split("/")[-1][:-4]; out[key] = words
    print(key, " ".join(f"{x['w']}[{x['s']}]" for x in words))
json.dump(out, open(".tesseract-work/words.json", "w"), indent=0)
