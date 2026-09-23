# Local narration with Kokoro (Apache-2.0). One WAV per script line for exact timing.
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
M = "/tmp/claude-0/-home-user-Nocodeboy/b62ffa48-66bc-5b14-8620-eec2e1822f42/scratchpad/kokoro"
k = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
script = json.load(open(".tesseract-work/script.json"))
voice = sys.argv[1] if len(sys.argv) > 1 else "bf_emma"
only = sys.argv[2:]  # optional line ids
for line in script:
    if only and line["id"] not in only: continue
    audio, sr = k.create(line["text"], voice=voice, speed=line.get("speed", 1.0), lang="en-gb")
    out = f"Sources/voice/{line['id']}.wav"
    sf.write(out, audio, sr)
    print(out, round(len(audio) / sr, 2))
