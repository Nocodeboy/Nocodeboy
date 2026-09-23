# SetupPreview: Tesseract install check

- Intent: a 3 s portrait (1080×1920) title card that shows the CLI can render text, shape and keyframe motion, and audio.
- Revision: v1. `SetupPreview.tsrct` is the source for `SetupPreview.mp4`.
- Layers: 1 background rect, 2 accent bar (scaleX wipe 0–500 ms), 3 title (fade in and rise 250–700 ms), 4 subtitle (fade 600–950 ms), and title/subtitle fade out 2600–2950 ms. Layer 10 is the procedural `air-whoosh` SFX at 0 ms, volume 0.5.
- Font: Archivo Black (SIL OFL, `.tesseract-work/fonts/OFL.txt`) from google/fonts. It is embedded in the .tsrct file.
- Checks: still preview, filmstrip, and export probe (h264 1080×1920 30 fps, 3.0 s, AAC). The audio peaks at −18.2 dB within the first 0.5 s. I checked the audio by measurement only; I did not listen to it.
- Export command (the Linux bundle has no H.264 encoder):
  `tsrct export --project SetupPreview.tsrct --output SetupPreview.mp4 --encoder-backend external-ffmpeg-command --ffmpeg-path "$(command -v ffmpeg)"`
