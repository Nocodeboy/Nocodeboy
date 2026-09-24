# Global Observer — Ébola en la RDC (UPDATE) · 24/09/2026

**ID editorial:** GOH-2026-08-22-001 (actualización) · **Etiqueta:** `UPDATE` · **Estado:** vídeo listo, **pendiente de aprobación para publicar**

| Archivo | Qué es |
|---|---|
| `GO-Ebola-DRC-2026-09-24.mp4` | Máster 1080×1920, 30 fps, H.264 + AAC, 81 s |
| `GO-Ebola-DRC-2026-09-24.tsrct` | Proyecto editable de Tesseract (capas nativas, fuentes, audio y presentadora empaquetados) |
| `Previews/…-preview.mp4`, `Previews/Filmstrip.png`, `Previews/poster.jpg` | Copia ligera, revisión visual y póster |
| `Sources/` | Voz (Magnific), presentadora (Magnific), música y sting (Magnific), retratos, mapa (geoBoundaries) |
| `.tesseract-work/build.py` + `assemble.sh` | Generador y reconstrucción completa (`bash .tesseract-work/assemble.sh`) |

## Guion (inglés, locución)

1. Good evening. This is Global Observer. The Ebola outbreak in the Democratic Republic of the Congo has now passed seven thousand seven hundred confirmed cases.
2. The country's health ministry reports seven thousand, seven hundred and seventy-three confirmed cases, and three thousand, seven hundred and fifty-nine deaths, with data up to the twenty-first of September.
3. That is about one thousand more confirmed cases than two weeks earlier.
4. The virus has now been confirmed in sixty-three health zones across seven provinces. Ituri remains the hardest hit. The latest province, Sud-Ubangi, lies in the far north-west, on the border with the Central African Republic.
5. There is no approved vaccine or treatment for this strain, Bundibugyo. A vaccine developed for a related strain is being tested; the World Health Organization says about two thousand people have received it.
6. The WHO rates the risk as very high in Congo, high for neighbouring countries, and low globally.
7. What to watch: the next WHO update, and whether cases appear beyond the seven affected provinces. This is Global Observer.

## Datos en pantalla y fuentes

| Dato | Valor | Fuente | Fecha |
|---|---|---|---|
| Casos confirmados RDC | 7.773 | Ministerio de Salud RDC vía [ECDC](https://www.ecdc.europa.eu/en/ebola-outbreak-democratic-republic-congo-and-uganda) | actualización 23/09 14:45, datos a 21/09 |
| Muertes | 3.759 | ídem | ídem |
| Zonas de salud / provincias | 63 de 167 / 7 de 26 | ídem | ídem |
| Provincia más afectada | Ituri | ídem | ídem |
| Casos a 7/09 | 6.757 | [OMS DON617](https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON617) | publicado 10/09 |
| Aumento en dos semanas | +1.016 (7.773 − 6.757) | cálculo propio sobre las dos cifras anteriores | 7/09 → 21/09 |
| Vacuna / tratamiento aprobados | ninguno | OMS DON617 | 10/09 |
| Vacunados en ensayo (rVSV-ZEBOV / Ervebo) | 2.007 | OMS DON617 | datos a 7/09 |
| Riesgo OMS | muy alto nacional · alto países limítrofes · bajo global | OMS DON617 | 10/09 |
| Sud-Ubangi, última provincia | 1 caso, 1 muerte | ECDC (lista de provincias) | 23/09 |

**Cadena de evidencia:** un solo grupo de independencia (Ministerio de Salud de la RDC, retransmitido por la OMS y el ECDC); fuente primaria autorizada, cumple el umbral. Sin cifras tempranas sin atribuir.

## Escaleta

| Tiempo | Bloque |
|---|---|
| 0,0–3,4 | Cabecera Global Observer (sting de Magnific) |
| 3,4–13,6 | Presentadora (IA, lip-sync de Magnific), etalonaje frío, faldón `UPDATE · EBOLA OUTBREAK: DR CONGO`, chapa "AI-GENERATED PRESENTER" |
| 13,6–33,3 | Cifras: contadores 7.773 / 3.759, "data to 21 September", comparativa 7/09 vs 21/09 y "+1,016 in two weeks" |
| 33,3–48,7 | Mapa de las 26 provincias: se encienden las 7 afectadas, Ituri en rojo, Sud-Ubangi con pulso, República Centroafricana; contadores 63 zonas / 7 provincias |
| 48,7–61,9 | Sin vacuna ni tratamiento aprobados; ensayo rVSV-ZEBOV, 2.007 vacunados |
| 61,9–69,5 | Evaluación de riesgo de la OMS (tres medidores) |
| 69,5–81,0 | What to watch (dos puntos) y firma con fuentes |

## Créditos

- Presentadora y voz: generadas con IA en Magnific (retrato Seedream 5 Pro, voz ElevenLabs "Charlotte Harrington", lip-sync Veed Fabric 1.0). Rotulado en pantalla y en la firma.
- Música ("Ticking Time in the Global Spotlight") y sting: Magnific (ElevenLabs Music / SFX).
- Mapa: geoBoundaries COD ADM1 (datos de OpenStreetMap, ODbL).
- Tipografía: Barlow Condensed (SIL OFL).
- Tiempos de subtítulos: faster-whisper (texto corregido a mano: Ituri, Sud-Ubangi, Bundibugyo).

## Comprobaciones hechas

- Render completo; decodifica limpio. 1080×1920, 30 fps, 81,0 s, AAC.
- Sonoridad **−16,3 LUFS**, pico **−3,2 dBFS** (objetivo de marca −16 LUFS, ≤ −1,5 dBTP).
- Fotogramas revisados en cada bloque y en cada corte: sin escenas superpuestas, textos dentro de la zona segura, subtítulos sin choques con el faldón.
- Voz y vídeo de la presentadora sincronizados (desfase medido: 0 ms).
- **No escuchado por mí:** revisa de oído la voz, la música y la mezcla.

## A revisar antes de publicar

- La presentadora esboza una sonrisa al decir "Good evening". La regla de marca permite la entradilla con etalonaje frío en historias de víctimas. El cierre sonriente ya queda fuera, porque corto a las cifras antes.
- ¿Mantener la chapa "AI-GENERATED PRESENTER"? La recomiendo por transparencia.
- Las cifras caducan con el próximo informe del ECDC o de la OMS. Si sale uno antes de publicar, se actualizan en `build.py` y se reconstruye en unos 3 minutos.

## Copy para X (borrador, requiere aprobación)

> UPDATE: Ebola in DR Congo has reached 7,773 confirmed cases and 3,759 deaths (data to 21 Sep), per the health ministry via ECDC. 63 health zones in seven provinces are affected. No approved vaccine or treatment exists for the Bundibugyo strain. Sources: ECDC, WHO
> [character count: 263]

## Ficha técnica

H.264 1080×1920 30 fps · AAC 48 kHz · 81 s · exportado con Tesseract 0.2.0 (renderizado por software, FFmpeg externo con libx264).

## Versiones de presentadora (A/B/C)

Mismo audio, grafismo y mezcla en las tres; solo cambia el clip de la entradilla (`PRESENTER_FILE` en `assemble.sh`).

| Versión | Archivo | Presentadora | Coste de la entradilla | Notas |
|---|---|---|---|---|
| A | `GO-Ebola-DRC-2026-09-24.mp4` | Retrato propio + Veed Fabric 1.0 (Magnific) | 2.860 cr Magnific | Expresiva, gestos con las manos; sonrisa final (cortada) |
| B | `GO-Ebola-DRC-2026-09-24-JOGG.mp4` | Avatar público JoggAI "Harper" (1201) con nuestro audio | créditos JoggAI (cuenta rcabrerovaras) | Sobria, plató azul; avatar no exclusivo |
| C | `GO-Ebola-DRC-2026-09-24-C.mp4` | Retrato propio → clip en reposo Kling 2.5 → Veed Sync 2 (Magnific) | 280 + 1.540 = 1.820 cr Magnific | Seria, sin sonrisa, misma cara que A; 720p reescalado |

JoggAI con nuestro retrato no fue posible: la animación de foto (Motion 2.0 Pro) falló dos veces por "Task timeout" y el lip-sync por API no está incluido en el plan de esa cuenta (código 17005).
