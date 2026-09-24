#!/usr/bin/env python3
"""Shared helpers for Global Observer bulletins built as native Tesseract layers.

Writes .tesseract-work/actions.json (visual layers + animation) and
.tesseract-work/audio_layers.json (Audio layers appended through checkout/commit).
All times below are seconds unless a name ends in _ms.
"""
import json, math
from PIL import ImageFont

W, H = 1080, 1920
FONT_DIR = ".tesseract-work/fonts"
BOLD, SEMI = "Bold Condensed", "SemiBold Condensed"
FAM = "Barlow Condensed"

def c(r, g, b, a=1.0): return [round(r / 255, 4), round(g / 255, 4), round(b / 255, 4), a]
INK = c(9, 12, 17); PAPER = c(244, 246, 249); AMBER = c(232, 173, 62)
ALERT = c(211, 56, 42); DEV = c(214, 122, 42); SLATE = c(124, 136, 152); LINE = c(34, 40, 50)
SOFT = c(196, 206, 220)
ALLIANCE = c(64, 160, 196); UNITY = c(150, 112, 196); UNCOUNTED = c(52, 60, 76)

A = []           # actions
_next_id = [1]
def nid():
    _next_id[0] += 1
    return _next_id[0]
def ms(s): return int(round(s * 1000))
def rng(start, end): return {"start": ms(start), "duration": ms(end - start)}
def tf(x=0, y=0, ax=0, ay=0, sx=100, sy=100, rot=0, op=100):
    return {"anchorPoint": [ax, ay], "position": [x, y], "scale": [sx, sy], "rotation": rot, "opacity": op}

EASE_OUT = {"type": "cubicBezier", "x1": 0.16, "y1": 1, "x2": 0.3, "y2": 1}
EASE_IN = {"type": "cubicBezier", "x1": 0.7, "y1": 0, "x2": 0.84, "y2": 0}
EASE_IO = {"type": "cubicBezier", "x1": 0.65, "y1": 0, "x2": 0.35, "y2": 1}
LIN = {"type": "linear"}

def group(name, start, end, parent=None, **t):
    i = nid()
    a = {"type": "createFxGroupLayer", "compositionId": "main", "layerId": i, "name": name,
         "activeRange": rng(start, end), "transform": tf(**t), "insertIndex": 0}
    if parent: a["parentLayerId"] = parent
    A.append(a); return i

def rect(name, x, y, w, h, fill, start, end, parent=None, round_=0, ax=0, ay=0, stroke=None, sw=0, op=100, dashes=None):
    i = nid()
    r = {"size": [w, h], "fillColor": fill, "roundness": round_}
    if stroke:
        r.update({"strokeEnabled": True, "strokeColor": stroke, "strokeWidth": sw})
        if dashes: r["strokeDashes"] = dashes
    if fill is None:
        r["fillColor"] = [0, 0, 0, 0]; r["fillEnabled"] = False
    a = {"type": "createFxRectLayer", "compositionId": "main", "layerId": i, "name": name, "insertIndex": 0,
         "activeRange": rng(start, end), "transform": tf(x, y, ax, ay, op=op), "rect": r}
    if parent: a["parentLayerId"] = parent
    A.append(a); return i

def text(name, s, x, y, size, color, start, end, parent=None, style=BOLD, w=952, h=None, just="left",
         track=0, valign=None, op=100, box=True):
    i = nid()
    st = {"text": s, "fontFamily": FAM, "fontStyle": style, "fontSize": size, "fillColor": color,
          "strokeWidth": 0, "justification": just, "tracking": track}
    if box:
        st.update({"boxText": True, "boxPosition": [0, 0], "boxSize": [w, h or int(size * 1.35)]})
        if valign: st["verticalAlign"] = valign
    a = {"type": "createFxTextLayer", "compositionId": "main", "layerId": i, "name": name, "insertIndex": 0,
         "activeRange": rng(start, end), "transform": tf(x, y, op=op), "sourceText": st}
    if parent: a["parentLayerId"] = parent
    A.append(a); return i

def stroke_style(color, width, cap="round", dashes=None, opacity=1.0):
    s = {"paint": {"type": "solid", "color": color}, "width": width, "cap": cap, "join": "round",
         "miterLimit": 4, "blendMode": "normal", "opacity": opacity}
    if dashes: s["dashes"] = dashes
    return s

def fill_style(color):
    return {"paint": {"type": "solid", "color": color}, "fillRule": "nonZeroWinding", "opacity": 1, "blendMode": "normal"}

def shape(name, x, y, start, end, parent=None, path=None, ellipse=None, strokes=(), fills=(), trim=None, rot=0, op=100):
    i = nid()
    sh = {"path": {"commands": path or []}, "fills": list(fills), "strokes": list(strokes)}
    if ellipse: sh["ellipse"] = {"position": [0, 0], "size": ellipse}
    if trim is not None: sh["trim"] = {"start": 0, "end": trim, "mode": "simultaneously"}
    a = {"type": "createFxShapeLayer", "compositionId": "main", "layerId": i, "name": name, "insertIndex": 0,
         "activeRange": rng(start, end), "transform": tf(x, y, rot=rot, op=op), "shape": sh}
    if parent: a["parentLayerId"] = parent
    A.append(a); return i

def kf(layer, prop, keys):
    """keys: list of (t seconds in layer time, value, easing)."""
    A.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
              "property": {"layerId": layer, "propertyType": prop},
              "keyframes": [{"id": f"L{layer}-{prop}-{n}", "layerTime": ms(t),
                             "value": {"type": "float", "value": v}, "easing": e}
                            for n, (t, v, e) in enumerate(keys)]})

def script(layer, prop, code):
    A.append({"type": "setFxPropertyAnimator", "compositionId": "main",
              "property": {"layerId": layer, "propertyType": prop}, "dependencies": [],
              "animator": {"type": "jsScript", "layerTimeJsCode": code}})

def enter(layer, t0, y, dy=40, dur=0.45, fade=True):
    """Rise + fade in at layer time t0 (layer is positioned at its final y)."""
    kf(layer, "positionY", [(t0, y + dy, LIN), (t0 + dur, y, EASE_OUT)])
    if fade: kf(layer, "opacity", [(t0, 0, LIN), (t0 + dur * 0.7, 100, EASE_OUT)])

def fade_in(layer, t0, dur=0.35):
    kf(layer, "opacity", [(t0, 0, LIN), (t0 + dur, 100, EASE_OUT)])

def width_px(s, size, style="SemiBold", track=0):
    f = ImageFont.truetype(f"{FONT_DIR}/BarlowCondensed-{style}.ttf", size)
    return f.getlength(s) + track * len(s)

