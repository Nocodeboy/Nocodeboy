# Global Observer — Piloto de telediario (FORMAT TEST)

> **Todo el contenido es ficticio.** Meridia no existe; las cifras, partidos y fuentes son inventados para probar el formato. El vídeo lleva `FORMAT TEST · FICTIONAL DATA` en pantalla todo el tiempo y en el ticker. **No publicar.**

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `MeridiaPilot.mp4` | Máster 1080×1920, 30 fps, H.264 + AAC, 50,5 s |
| `MeridiaPilot.tsrct` | Proyecto editable de Tesseract (todas las capas nativas, fuentes y audio empaquetados) |
| `Previews/Filmstrip.png`, `Previews/poster.jpg` | Revisión visual y póster |
| `Sources/` | Locución original (Kokoro, voz `bf_emma`), música procedural, efectos |
| `.tesseract-work/build.py` | Generador: escaleta, rótulos, animaciones, subtítulos y mezcla en un solo sitio |
| `.tesseract-work/assemble.sh` | Reconstruye el `.tsrct` desde cero (`bash .tesseract-work/assemble.sh`) |

## Escaleta

| Tiempo | Bloque | Grafismo |
|---|---|---|
| 0,0–3,4 | Cabecera | Cuadrado de marca, anillos de señal, wordmark que se cierra, sting |
| 3,4–9,9 | Apertura | Globo wireframe girando, marcador pulsante en Meridia, titular MERIDIA / VOTES |
| 9,9–18,5 | Participación | Anillo y contador 0→71 %, histórico de participación (2004 destacado) |
| 18,5–27,6 | Resultados | Barra de escrutinio 0→60 %, barras de partidos con cifras que cuentan, línea de mayoría 50 % |
| 27,6–33,4 | Mapa | Mapa de teselas por distrito; 3 distritos del norte cambian de color con pulso y contorno |
| 33,4–40,9 | Próximos pasos | Línea de tiempo que se dibuja, reloj con agujas girando, nodos que aparecen al ritmo de la locución |
| 40,9–50,5 | What to watch + cierre | Dos claves numeradas, firma @GLOBALOBSHQ con anillos (espejo de la cabecera) |

Siempre en pantalla: barra superior con LIVE pulsante, chapa `DEVELOPING`, aviso de prueba, barra de progreso, ticker inferior, subtítulos en la zona segura (1650–1780 px) y cortinillas de marca en cada corte.

## Guion (inglés)

1. Good evening. This is Global Observer. Polls have just closed in Meridia, and the first official count is coming in.
2. The national electoral commission reports turnout of seventy-one per cent, the highest since the country's first multiparty vote in two thousand and four.
3. With sixty per cent of districts counted, the opposition Coastal Alliance leads on forty-four per cent. The governing Unity Party follows on thirty-eight.
4. The swing is sharpest in the northern highlands, where three districts have changed hands for the first time.
5. The commission expects final results within forty-eight hours. International observers will publish their first assessment tomorrow.
6. What to watch: whether the Alliance crosses fifty per cent, or a coalition decides who governs. This is Global Observer.

## Datos (ficticios)

| Dato | Valor | Fuente |
|---|---|---|
| Participación | 71 % | Ficticia (comisión electoral inventada) |
| Escrutado | 60 % de distritos | Ficticia |
| Coastal Alliance | 44 % | Ficticia |
| Unity Party | 38 % | Ficticia |
| Otros | 18 % | Ficticia |
| Histórico participación | 2004: 74 · 2008: 63 · 2012: 59 · 2016: 57 · 2021: 64 · 2026: 71 | Ficticia |

## Créditos

- Tipografía: Barlow Condensed Bold y SemiBold (SIL OFL, google/fonts), la de la marca.
- Voz: Kokoro v1.0 (Apache-2.0), voz `bf_emma`, generada en local.
- Música: pista procedural propia (placeholder), 100 BPM en la menor.
- Efectos: generados en local con el ayudante de sonido de Tesseract.

## Comprobaciones hechas

- Render completo sin errores; `ffmpeg` decodifica limpio.
- Sonoridad integrada **−16,1 LUFS**, pico **−4,5 dBFS** (objetivo de marca: −16 LUFS, ≤ −1,5 dBTP).
- Fotogramas revisados en cabecera, cada bloque y cada corte (sin transparencias entre escenas, sin textos fuera de encuadre, subtítulos sin colisiones).
- **No escuchado:** no puedo reproducir audio en este entorno. Revisa la voz y la música de oído.

## Limitaciones de esta prueba

- **Sin presentador en vídeo ni voz de Magnific.** Generé en Magnific dos retratos de presentadora, las seis locuciones con la voz "Charlotte Harrington", una pista musical y un sting. La red de este entorno bloquea el CDN de Magnific (`pikaso.cdnpk.net`), así que no pude traerlos. Están en tu cuenta de Magnific (proyecto Personal).
- **Sin noticia real:** la red también bloquea las fuentes primarias (USGS, OCHA, Wikimedia), así que no se podía verificar nada.

## Cómo pasar de piloto a pieza real

1. En el entorno de la nube, añade a la red permitida `pikaso.cdnpk.net` y las fuentes que uses (p. ej. `earthquake.usgs.gov`, `www.unocha.org`, `commons.wikimedia.org`, `api.reliefweb.int`).
2. `global-newsroom` aprueba la historia → se reescriben `script.json`, los textos y las cifras de `build.py`.
3. Voz de Magnific → sustituir los WAV de `Sources/voice/`; los tiempos de subtítulos salen de las pausas (`silencedetect`).
4. Presentador: `video_speak` de Magnific con el retrato y la locución de la entradilla → capa de vídeo en el bloque de apertura.
5. `bash .tesseract-work/assemble.sh` y exportar:
   `tsrct export --project MeridiaPilot.tsrct --output MeridiaPilot.mp4 --encoder-backend external-ffmpeg-command --ffmpeg-path "$(command -v ffmpeg)"`

Una corrección (cifra, topónimo, titular) es cambiar el texto en `build.py`, reconstruir y exportar: unos 2–3 minutos, sin rehacer nada a mano.

## Copy para X (borrador, solo de ejemplo)

> FORMAT TEST — fictional data. Meridia votes: turnout 71%, the highest since 2004. With 60% of districts counted, the Coastal Alliance leads on 44%, the Unity Party on 38%. What to watch: a majority, or coalition talks.
