#!/usr/bin/env python3
"""Global Observer bulletin pilot (FORMAT TEST, fictional data) as native Tesseract layers.

Writes .tesseract-work/actions.json (visual layers + animation) and
.tesseract-work/audio_layers.json (Audio layers appended through checkout/commit).
All times below are seconds unless a name ends in _ms.
"""
import json, math
from PIL import ImageFont

W, H = 1080, 1920
TOTAL = 50.5
FONT_DIR = ".tesseract-work/fonts"
BOLD, SEMI = "Bold Condensed", "SemiBold Condensed"
FAM = "Barlow Condensed"

def c(r, g, b, a=1.0): return [round(r / 255, 4), round(g / 255, 4), round(b / 255, 4), a]
INK = c(9, 12, 17); PAPER = c(244, 246, 249); AMBER = c(232, 173, 62)
ALERT = c(211, 56, 42); DEV = c(214, 122, 42); SLATE = c(124, 136, 152); LINE = c(34, 40, 50)
SOFT = c(196, 206, 220)
ALLIANCE = c(64, 160, 196); UNITY = c(150, 112, 196); UNCOUNTED = c(52, 60, 76)

# ---------------------------------------------------------------- narration
VO = [  # id, start (s), duration (s)
    ("vo1", 3.4, 6.08), ("vo2", 10.0, 8.19), ("vo3", 18.7, 8.62),
    ("vo4", 27.8, 5.31), ("vo5", 33.6, 7.04), ("vo6", 41.1, 7.04),
]
VOS = {v[0]: v[1] for v in VO}
# captions: (vo id, start, end within the clip, text) - start/end from measured pauses
CAPS = [
    ("vo1", 0.00, 2.00, "Good evening. This is Global Observer."),
    ("vo1", 2.50, 4.08, "Polls have just closed in Meridia,"),
    ("vo1", 4.08, 6.08, "and the first official count is coming in."),
    ("vo2", 0.00, 1.75, "The national electoral commission"),
    ("vo2", 1.75, 3.80, "reports turnout of 71 per cent,"),
    ("vo2", 4.32, 8.19, "the highest since the country's first multiparty vote in 2004."),
    ("vo3", 0.00, 2.03, "With 60 per cent of districts counted,"),
    ("vo3", 2.45, 5.59, "the opposition Coastal Alliance leads on 44 per cent."),
    ("vo3", 6.22, 8.62, "The governing Unity Party follows on 38."),
    ("vo4", 0.00, 2.23, "The swing is sharpest in the northern highlands,"),
    ("vo4", 2.64, 5.31, "where three districts have changed hands for the first time."),
    ("vo5", 0.00, 3.12, "The commission expects final results within 48 hours."),
    ("vo5", 3.73, 7.04, "International observers will publish their first assessment tomorrow."),
    ("vo6", 0.00, 0.76, "What to watch:"),
    ("vo6", 0.95, 3.02, "whether the Alliance crosses 50 per cent,"),
    ("vo6", 3.21, 5.08, "or a coalition decides who governs."),
    ("vo6", 5.64, 7.04, "This is Global Observer."),
]
# scenes: name, start, end (they overlap the wipes that hide each cut)
CUTS = [3.4, 9.9, 18.5, 27.6, 33.4, 40.9]  # wipe midpoints (full cover)
# scenes switch exactly at full cover, so an outgoing scene never shows through an incoming one
_b = [0.0] + CUTS + [TOTAL]
SCENES = [(n, _b[i], _b[i + 1]) for i, n in enumerate(["ident", "open", "turnout", "results", "map", "next", "outro"])]
CHROME_START = 3.25

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

# ================================================================ background (whole programme)
bg = group("Background", 0, TOTAL)
rect("Ink base", 0, 0, W, H, INK, 0, TOTAL, bg)
# soft vertical light: gradient rect
gi = nid()
A.append({"type": "createFxRectLayer", "compositionId": "main", "layerId": gi, "name": "Studio light",
          "insertIndex": 0, "parentLayerId": bg, "activeRange": rng(0, TOTAL), "transform": tf(),
          "rect": {"size": [W, H], "fillColor": [0, 0, 0, 0],
                   "fillPaint": {"type": "gradient", "gradientType": "radial", "start": [540, 620], "end": [540, 1900],
                                 "stops": [{"offset": 0, "color": c(28, 38, 56, 1)}, {"offset": 1, "color": c(9, 12, 17, 0)}]}}})
# dot grid: dashed horizontal strokes with round caps read as dots
dots = []
for row in range(0, H // 40 + 1):
    y = row * 40 + 20
    dots += [{"type": "moveTo", "x": 0, "y": y}, {"type": "lineTo", "x": W, "y": y}]
dg = shape("Dot grid", 0, 0, 0, TOTAL, bg, path=dots,
           strokes=[stroke_style(c(120, 140, 170, 0.16), 3, cap="round", dashes=[0.1, 39.9])])

# ================================================================ scene 0: ident
s0, e0 = SCENES[0][1], SCENES[0][2]
g = group("S0 Ident", s0, e0)
rect("Ident black", 0, 0, W, H, INK, 0, e0 - s0, g)
for k in range(3):  # signal rings
    ring = shape(f"Signal ring {k+1}", 540, 860, 0, e0 - s0, g, ellipse=[10, 10],
                 strokes=[stroke_style(c(232, 173, 62, 0.9), 4 - k)])
    d = 0.25 + k * 0.22
    script(ring, "ellipseSize", f"var t=input.time.seconds-{d}; if(t<0) return [0,0]; var p=Math.min(1,t/1.6); var e=1-Math.pow(1-p,3); var s=40+e*{900 + k * 260}; return [s,s];")
    kf(ring, "opacity", [(d, 100, LIN), (d + 1.6, 0, EASE_OUT)])
sq = rect("Brand square", 540, 860, 60, 120, AMBER, 0, e0 - s0, g, ax=30, ay=60)
kf(sq, "scaleX", [(0.05, 0, LIN), (0.45, 100, EASE_OUT)])
kf(sq, "scaleY", [(0.05, 0, LIN), (0.45, 100, EASE_OUT)])
kf(sq, "positionX", [(0.9, 540, LIN), (1.4, 128, EASE_IO)])
kf(sq, "rotation", [(0.05, -90, LIN), (0.6, 0, EASE_OUT)])
wm = text("Wordmark", "GLOBAL OBSERVER", 176, 792, 124, PAPER, 0, e0 - s0, g, w=880, track=6)
kf(wm, "opacity", [(1.15, 0, LIN), (1.6, 100, EASE_OUT)])
kf(wm, "tracking", [(1.15, 40, LIN), (1.9, 6, EASE_OUT)])
tl = text("Tagline", "GLOBAL NEWS, WITHOUT THE BLIND SPOTS", 180, 960, 40, SLATE, 0, e0 - s0, g, style=SEMI, w=860, track=5)
enter(tl, 1.7, 960, dy=20)
ev = text("Ident edition", "EVENING BULLETIN  ·  FORMAT TEST", 180, 1030, 32, AMBER, 0, e0 - s0, g, style=SEMI, w=860, track=6)
fade_in(ev, 2.0)

# ================================================================ chrome (top bar, chips, ticker, progress)
ch = group("Chrome", CHROME_START, TOTAL)
cd = TOTAL - CHROME_START
top = group("Top bar", 0, cd, ch)
rect("Top bar plate", 0, 0, W, 132, c(9, 12, 17, 0.88), 0, cd, top)
rect("Top bar rule", 0, 131, W, 2, LINE, 0, cd, top)
rect("Top mark", 64, 52, 18, 36, AMBER, 0, cd, top)
text("Top brand", "GLOBAL OBSERVER", 100, 44, 46, PAPER, 0, cd, top, w=500, track=3.5)
live = group("LIVE marker", 0, cd, top)
rect("LIVE pill", 836, 46, 180, 48, c(211, 56, 42, 1), 0, cd, live, round_=24)
dot = shape("LIVE dot", 870, 70, 0, cd, live, ellipse=[16, 16], fills=[fill_style(PAPER)])
script(dot, "opacity", "var p=(input.time.seconds%1.2)/1.2; return 35+65*(0.5+0.5*Math.cos(p*2*Math.PI));")
text("LIVE label", "LIVE", 890, 48, 36, PAPER, 0, cd, live, w=110, track=4)
# progress bar (brand): 7 px, fills across the programme
rect("Progress track", 0, 0, W, 7, c(26, 32, 41, 0.55), 0, cd, top)
pb = rect("Progress", 0, 0, W, 7, c(232, 173, 62, 0.98), 0, cd, top)
script(pb, "scaleX", f"return Math.min(100, 100*input.time.seconds/{cd:.3f});")
kf(top, "positionY", [(0, -140, LIN), (0.5, 0, EASE_OUT)])
# chips row: editorial tag + format-test warning (always visible)
chips = group("Chips", 0, cd, ch)
tag = "DEVELOPING"; tw = width_px(tag, 34, "Bold", 3)
rect("Tag chip", 64, 160, tw + 44, 56, DEV, 0, cd, chips)
text("Tag label", tag, 86, 162, 34, PAPER, 0, cd, chips, w=tw + 30, track=3)
warn = "FORMAT TEST · FICTIONAL DATA"; ww = width_px(warn, 28, "SemiBold", 2.5)
rect("Test chip", W - 64 - ww - 36, 164, ww + 36, 48, None, 0, cd, chips, stroke=c(150, 162, 180, 1), sw=2)
text("Test label", warn, W - 64 - ww - 18, 170, 28, SOFT, 0, cd, chips, style=SEMI, w=ww + 10, track=2.5)
kf(chips, "opacity", [(0.3, 0, LIN), (0.7, 100, EASE_OUT)])
# ticker (footer band): scrolling text under a fixed label
tk = group("Ticker", 0, cd, ch)
rect("Ticker band", 0, 1802, W, 118, c(9, 12, 17, 0.96), 0, cd, tk)
rect("Ticker rule", 0, 1802, W, 2, LINE, 0, cd, tk)
item = ("MERIDIA: TURNOUT 71%, HIGHEST SINCE 2004   •   COASTAL ALLIANCE 44%, UNITY PARTY 38% WITH 60% OF DISTRICTS COUNTED   •   "
        "FINAL RESULTS EXPECTED WITHIN 48 HOURS   •   FORMAT TEST — FICTIONAL COUNTRY AND DATA   •   ")
iw = width_px(item, 36, "SemiBold", 1.5)
crawl = text("Ticker crawl", item + item + item, 300, 1838, 36, SOFT, 0, cd, tk, style=SEMI, w=int(iw * 3 + 400), h=56, track=1.5)
script(crawl, "positionX", f"return 300 - ((input.time.seconds*140) % {iw:.1f});")
rect("Ticker label plate", 0, 1804, 292, 116, c(9, 12, 17, 1), 0, cd, tk)
rect("Ticker label", 64, 1832, 204, 60, AMBER, 0, cd, tk)
text("Ticker label text", "MERIDIA VOTES", 76, 1836, 34, INK, 0, cd, tk, w=190, track=2)
kf(tk, "positionY", [(0, 130, LIN), (0.5, 0, EASE_OUT)])

# ================================================================ captions
cg = group("Captions", CHROME_START, TOTAL)
for vid, a, b, s in CAPS:
    t0 = VOS[vid] + a - CHROME_START; t1 = VOS[vid] + b - CHROME_START + 0.08
    lines = 1 if width_px(s, 50, "SemiBold", 0.8) < 880 else 2
    ph = 84 if lines == 1 else 144
    y = 1778 - ph
    rect("Caption plate", 48, y, 984, ph, c(9, 12, 17, 0.74), t0, t1, cg, round_=10)
    text("Caption", s, 80, y + 10, 50, PAPER, t0, t1, cg, style=SEMI, w=920, h=ph - 20, just="center",
         valign="center", track=0.8)

# ================================================================ scene 1: opening (globe + headline)
n, s1, e1 = SCENES[1]; d1 = e1 - s1
g = group("S1 Opening", s1, e1)
glob = group("Globe", 0, d1, g, x=540, y=640)
R = 300
shape("Globe halo", 0, 0, 0, d1, glob, ellipse=[2 * R + 60, 2 * R + 60], fills=[fill_style(c(40, 60, 90, 0.25))])
shape("Globe rim", 0, 0, 0, d1, glob, ellipse=[2 * R, 2 * R], strokes=[stroke_style(c(150, 170, 200, 0.8), 3)])
TILT = math.radians(18)
for k, lat in enumerate([-60, -30, 0, 30, 60]):
    la = math.radians(lat); wv = 2 * R * math.cos(la); hv = max(2, wv * math.sin(TILT))
    li = shape(f"Latitude {lat}", 0, -R * math.sin(la) * math.cos(TILT), 0, d1, glob, ellipse=[wv, hv],
               strokes=[stroke_style(c(120, 140, 170, 0.45), 2)])
NM = 8
for k in range(NM):
    col = c(232, 173, 62, 0.95) if k == 0 else c(120, 150, 190, 0.55)
    m = shape(f"Meridian {k+1}", 0, 0, 0, d1, glob, ellipse=[2 * R, 2 * R], strokes=[stroke_style(col, 3 if k == 0 else 2)])
    script(m, "ellipseSize", f"var a=input.time.seconds*0.45+{k * math.pi / NM:.4f}; return [Math.max(1,{2 * R}*Math.abs(Math.cos(a))),{2 * R}];")
kf(glob, "scaleX", [(0.0, 70, LIN), (0.8, 100, EASE_OUT)])
kf(glob, "scaleY", [(0.0, 70, LIN), (0.8, 100, EASE_OUT)])
kf(glob, "opacity", [(0.0, 0, LIN), (0.5, 100, EASE_OUT)])
# Meridia marker (fictional location) with pulses
mk = group("Meridia marker", 0, d1, glob, x=70, y=40)
for k in range(2):
    p = shape(f"Marker pulse {k+1}", 0, 0, 0, d1, mk, ellipse=[20, 20], strokes=[stroke_style(ALERT, 3)])
    script(p, "ellipseSize", f"var q=((input.time.seconds+{k * 0.8})%1.6)/1.6; var s=20+q*120; return [s,s];")
    script(p, "opacity", f"var q=((input.time.seconds+{k * 0.8})%1.6)/1.6; return 100*(1-q);")
shape("Marker dot", 0, 0, 0, d1, mk, ellipse=[26, 26], fills=[fill_style(ALERT)], strokes=[stroke_style(PAPER, 3)])
shape("Marker leader", 0, 0, 0, d1, mk, path=[{"type": "moveTo", "x": 18, "y": -10}, {"type": "lineTo", "x": 120, "y": -70}, {"type": "lineTo", "x": 290, "y": -70}],
      strokes=[stroke_style(c(200, 210, 225, 0.9), 2, cap="butt")], trim=100)
kf(A[-1]["layerId"], "trimEnd", [(0.9, 0, LIN), (1.5, 100, EASE_OUT)])
ml = text("Marker label", "MERIDIA", 130, -128, 48, PAPER, 0, d1, mk, w=260, track=3)
fade_in(ml, 1.4)
ms_ = text("Marker sub", "FICTIONAL STATE", 130, -60, 26, SLATE, 0, d1, mk, style=SEMI, w=260, track=2)
fade_in(ms_, 1.6)
kf(mk, "opacity", [(0.6, 0, LIN), (0.9, 100, EASE_OUT)])
# headline block
k1 = text("Kicker", "ELECTION NIGHT", 64, 1010, 44, AMBER, 0, d1, g, style=SEMI, track=6)
enter(k1, 1.0, 1010)
r1 = rect("Kicker rule", 64, 1074, 560, 4, AMBER, 0, d1, g)
kf(r1, "scaleX", [(1.1, 0, LIN), (1.7, 100, EASE_OUT)])
h1 = text("Headline", "MERIDIA", 58, 1090, 200, PAPER, 0, d1, g, track=2, h=220)
enter(h1, 1.2, 1090, dy=60)
h1b = text("Headline 2", "VOTES", 58, 1270, 200, AMBER, 0, d1, g, track=2, h=220)
enter(h1b, 1.35, 1270, dy=60)
sb = text("Headline sub", "Polls closed · first official count coming in", 64, 1500, 46, SOFT, 0, d1, g, style=SEMI, track=1)
enter(sb, 1.6, 1500)

# ================================================================ scene 2: turnout
n, s2, e2 = SCENES[2]; d2 = e2 - s2
g = group("S2 Turnout", s2, e2)
kt = text("Kicker", "TURNOUT", 64, 270, 44, AMBER, 0, d2, g, style=SEMI, track=6)
enter(kt, 0.35, 270)
rg = group("Turnout ring", 0, d2, g, x=540, y=650)
shape("Ring track", 0, 0, 0, d2, rg, ellipse=[440, 440], strokes=[stroke_style(c(40, 48, 62, 1), 26, cap="butt")])
ring = shape("Ring value", 0, 0, 0, d2, rg, ellipse=[440, 440], strokes=[stroke_style(AMBER, 26, cap="butt")], trim=0, rot=-90)
T0, T1 = 1.6, 3.9   # count lands on "seventy-one per cent"
script(ring, "trimEnd", f"var p=Math.max(0,Math.min(1,(input.time.seconds-{T0})/{T1 - T0})); return 71*(1-Math.pow(1-p,3));")
num = text("Turnout number", "0%", -300, -120, 190, PAPER, 0, d2, rg, w=600, h=230, just="center")
script(num, "textContent", f"var p=Math.max(0,Math.min(1,(input.time.seconds-{T0})/{T1 - T0})); return Math.round(71*(1-Math.pow(1-p,3)))+'%';")
text("Turnout unit", "OF REGISTERED VOTERS", -300, 92, 34, SLATE, 0, d2, rg, style=SEMI, w=600, just="center", track=3)
kf(rg, "opacity", [(0.3, 0, LIN), (0.8, 100, EASE_OUT)])
kf(rg, "scaleX", [(0.3, 85, LIN), (0.9, 100, EASE_OUT)]); kf(rg, "scaleY", [(0.3, 85, LIN), (0.9, 100, EASE_OUT)])
# history chart
hist = [("2004", 74), ("2008", 63), ("2012", 59), ("2016", 57), ("2021", 64), ("2026", 71)]
hc = group("Turnout history", 0, d2, g)
HT0 = 4.4  # "the highest since..."
ht = text("History title", "TURNOUT BY ELECTION", 64, 1000, 40, PAPER, 0, d2, hc, track=3)
enter(ht, HT0, 1000)
base_y, maxh, bw, gap = 1490, 330, 128, 36
x0 = (W - (len(hist) * bw + (len(hist) - 1) * gap)) / 2
rect("History baseline", 64, base_y, W - 128, 2, LINE, 0, d2, hc)
for i, (yr, v) in enumerate(hist):
    x = x0 + i * (bw + gap); h = maxh * v / 80
    col = AMBER if yr == "2026" else (c(150, 162, 180, 1) if yr == "2004" else c(58, 68, 86, 1))
    b = rect(f"Bar {yr}", x, base_y, bw, h, col, 0, d2, hc, ay=h)
    t_ = HT0 + 0.2 + i * 0.12
    kf(b, "scaleY", [(t_, 0, LIN), (t_ + 0.55, 100, EASE_OUT)])
    lv = text(f"Value {yr}", f"{v}%", x - 20, base_y - h - 56, 40, PAPER if yr in ("2026", "2004") else SOFT, 0, d2, hc,
              w=bw + 40, just="center")
    fade_in(lv, t_ + 0.45)
    ly = text(f"Year {yr}", yr, x - 20, base_y + 12, 32, AMBER if yr == "2026" else SLATE, 0, d2, hc, style=SEMI, w=bw + 40, just="center", track=2)
    fade_in(ly, t_ + 0.2)
note = text("History note", "HIGHEST SINCE 2004", 64, 1052, 30, AMBER, 0, d2, hc, style=SEMI, track=4)
fade_in(note, HT0 + 1.4)

# ================================================================ scene 3: results
n, s3, e3 = SCENES[3]; d3 = e3 - s3
g = group("S3 Results", s3, e3)
k3 = text("Kicker", "FIRST OFFICIAL COUNT", 64, 270, 44, AMBER, 0, d3, g, style=SEMI, track=6)
enter(k3, 0.35, 270)
cnt = text("Counted label", "DISTRICTS COUNTED", 64, 340, 34, SLATE, 0, d3, g, style=SEMI, track=3)
fade_in(cnt, 0.5)
rect("Counted track", 64, 396, W - 128, 18, c(40, 48, 62, 1), 0, d3, g)
cb = rect("Counted fill", 64, 396, W - 128, 18, PAPER, 0, d3, g)
kf(cb, "scaleX", [(0.6, 0, LIN), (2.3, 60, EASE_OUT)])
cp = text("Counted value", "0%", W - 64 - 200, 330, 52, PAPER, 0, d3, g, w=200, just="right")
script(cp, "textContent", "var p=Math.max(0,Math.min(1,(input.time.seconds-0.6)/1.7)); return Math.round(60*(1-Math.pow(1-p,3)))+'%';")
FULL = W - 128  # 50 % of the vote = full width
maj_x = 64 + FULL
rows = [("COASTAL ALLIANCE", "Opposition", 44, ALLIANCE, 4.1), ("UNITY PARTY", "Governing", 38, UNITY, 7.2),
        ("OTHERS", "", 18, c(70, 80, 98, 1), 8.0)]
y = 520
for name, sub, v, col, tstart in rows:
    big = name != "OTHERS"
    nm = text(f"{name} name", name, 64, y, 56 if big else 40, PAPER, 0, d3, g, track=2)
    enter(nm, tstart - 0.5 if big else tstart, y, dy=20)
    if sub:
        sl = text(f"{name} sub", sub.upper(), 64 + width_px(name, 56, "Bold", 2) + 24, y + 18, 30, SLATE, 0, d3, g, style=SEMI, w=300, track=3)
        fade_in(sl, tstart - 0.3)
    bh = 110 if big else 56
    by = y + (74 if big else 56)
    rect(f"{name} track", 64, by, FULL, bh, c(24, 30, 40, 1), 0, d3, g)
    bar = rect(f"{name} bar", 64, by, FULL * v / 50, bh, col, 0, d3, g)
    kf(bar, "scaleX", [(tstart, 0, LIN), (tstart + 1.2, 100, EASE_OUT)])
    vv = text(f"{name} value", "0%", 64 + 24, by + (4 if big else 2), 96 if big else 48, INK if big else PAPER, 0, d3, g, w=300)
    script(vv, "textContent", f"var p=Math.max(0,Math.min(1,(input.time.seconds-{tstart})/1.2)); return Math.round({v}*(1-Math.pow(1-p,3)))+'%';")
    fade_in(vv, tstart + 0.15, 0.2)
    y = by + bh + (70 if big else 40)
# majority line
mj = shape("Majority line", maj_x, 500, 0, d3, g, path=[{"type": "moveTo", "x": 0, "y": 0}, {"type": "lineTo", "x": 0, "y": y - 500}],
           strokes=[stroke_style(AMBER, 3, cap="butt", dashes=[14, 10])], trim=100)
kf(mj, "trimEnd", [(2.6, 0, LIN), (3.4, 100, EASE_OUT)])
ml = text("Majority label", "50% MAJORITY", maj_x - 300, y + 10, 32, AMBER, 0, d3, g, style=SEMI, w=300, just="right", track=3)
fade_in(ml, 3.2)
src3 = text("Results source", "SOURCE: FICTIONAL ELECTORAL COMMISSION — FORMAT TEST", 64, 1560, 26, SLATE, 0, d3, g, style=SEMI, track=2)
fade_in(src3, 1.0)

# ================================================================ scene 4: tile map
n, s4, e4 = SCENES[4]; d4 = e4 - s4
g = group("S4 Map", s4, e4)
k4 = text("Kicker", "THE SWING", 64, 270, 44, AMBER, 0, d4, g, style=SEMI, track=6)
enter(k4, 0.3, 270)
t4 = text("Map title", "NORTHERN HIGHLANDS", 64, 322, 96, PAPER, 0, d4, g, track=2, h=120)
enter(t4, 0.45, 322)
GRID = ["..AAU....", ".AAUUU...", ".AAAUUU..", "AAA.UUU..", ".AAAAUUU.", "..AA.UUUU", "...AAUU..", "....AU..."]
FLIP = {(0, 3), (1, 3), (1, 4)}           # Unity -> Alliance tonight
UNC = {(2, 1), (3, 5), (4, 7), (5, 2), (5, 8), (6, 6), (7, 4), (4, 1), (2, 6), (6, 3), (3, 2)}  # not yet counted
pitch, ts_ = 110, 98
mx0 = (W - 9 * pitch) / 2 + 6; my0 = 470
mp = group("Tile map", 0, d4, g)
FT = 3.2  # "changed hands" lands
for r_, row in enumerate(GRID):
    for c_, ch_ in enumerate(row):
        if ch_ == ".": continue
        x = mx0 + c_ * pitch; yy = my0 + r_ * pitch
        if (r_, c_) in UNC: col = UNCOUNTED
        elif (r_, c_) in FLIP: col = UNITY
        else: col = ALLIANCE if ch_ == "A" else UNITY
        tl_ = rect(f"District {r_}-{c_}", x + ts_ / 2, yy + ts_ / 2, ts_, ts_, col, 0, d4, mp, round_=12, ax=ts_ / 2, ay=ts_ / 2)
        dl = 0.5 + (r_ + c_) * 0.035
        kf(tl_, "scaleX", [(dl, 0, LIN), (dl + 0.35, 100, EASE_OUT)]); kf(tl_, "scaleY", [(dl, 0, LIN), (dl + 0.35, 100, EASE_OUT)])
        if (r_, c_) in FLIP:
            ft = FT + 0.15 * len([f for f in FLIP if f < (r_, c_)])
            ua, al = UNITY, ALLIANCE
            script(tl_, "fillColor", f"var p=Math.max(0,Math.min(1,(input.time.seconds-{ft})/0.35)); "
                   f"return [{ua[0]}+({al[0]}-{ua[0]})*p,{ua[1]}+({al[1]}-{ua[1]})*p,{ua[2]}+({al[2]}-{ua[2]})*p,1];")
            kf(tl_, "scaleX", [(dl, 0, LIN), (dl + 0.35, 100, EASE_OUT), (ft, 100, LIN), (ft + 0.15, 118, EASE_OUT), (ft + 0.45, 100, EASE_IO)])
            kf(tl_, "scaleY", [(dl, 0, LIN), (dl + 0.35, 100, EASE_OUT), (ft, 100, LIN), (ft + 0.15, 118, EASE_OUT), (ft + 0.45, 100, EASE_IO)])
# outline around the flipped region (draw-on)
ox, oy = mx0 + 3 * pitch - 12, my0 - 12
outline = [{"type": "moveTo", "x": 0, "y": 0}, {"type": "lineTo", "x": pitch + 14, "y": 0},
           {"type": "lineTo", "x": pitch + 14, "y": pitch}, {"type": "lineTo", "x": 2 * pitch + 14, "y": pitch},
           {"type": "lineTo", "x": 2 * pitch + 14, "y": 2 * pitch + 14}, {"type": "lineTo", "x": 0, "y": 2 * pitch + 14},
           {"type": "close"}]
oo = shape("Swing outline", ox, oy, 0, d4, mp, path=outline, strokes=[stroke_style(AMBER, 5, cap="round")], trim=0)
kf(oo, "trimEnd", [(FT - 0.9, 0, LIN), (FT - 0.1, 100, EASE_OUT)])
cl = text("Swing callout", "3 DISTRICTS\nCHANGE HANDS", ox + 2 * pitch + 44, oy + 20, 44, AMBER, 0, d4, mp, w=360, track=2, h=120)
enter(cl, FT - 0.2, oy + 20, dy=16)
# legend
ly = 1400
for i, (lab, col) in enumerate([("COASTAL ALLIANCE", ALLIANCE), ("UNITY PARTY", UNITY), ("NOT YET COUNTED", UNCOUNTED)]):
    lx = 64 + i * 330
    rect(f"Legend swatch {i}", lx, ly + 6, 30, 30, col, 0, d4, g, round_=6)
    lt = text(f"Legend {i}", lab, lx + 44, ly, 32, SOFT, 0, d4, g, style=SEMI, w=280, track=2)
    fade_in(lt, 1.0 + i * 0.1)
src4 = text("Map note", "SCHEMATIC TILE MAP · FICTIONAL DATA", 64, 1470, 26, SLATE, 0, d4, g, style=SEMI, track=2)
fade_in(src4, 1.2)

# ================================================================ scene 5: what happens next (timeline + clock)
n, s5, e5 = SCENES[5]; d5 = e5 - s5
g = group("S5 Next", s5, e5)
k5 = text("Kicker", "WHAT HAPPENS NEXT", 64, 270, 44, AMBER, 0, d5, g, style=SEMI, track=6)
enter(k5, 0.3, 270)
clk = group("Clock", 0, d5, g, x=W - 180, y=330)
shape("Clock face", 0, 0, 0, d5, clk, ellipse=[160, 160], strokes=[stroke_style(SOFT, 5)])
hh = shape("Clock hour", 0, 0, 0, d5, clk, path=[{"type": "moveTo", "x": 0, "y": 0}, {"type": "lineTo", "x": 0, "y": -42}], strokes=[stroke_style(PAPER, 7)])
mh = shape("Clock minute", 0, 0, 0, d5, clk, path=[{"type": "moveTo", "x": 0, "y": 0}, {"type": "lineTo", "x": 0, "y": -64}], strokes=[stroke_style(AMBER, 5)])
script(mh, "rotation", "return input.time.seconds*360*0.6;")
script(hh, "rotation", "return input.time.seconds*30*0.6;")
kf(clk, "opacity", [(0.3, 0, LIN), (0.7, 100, EASE_OUT)])
steps = [("NOW", "Count continues", "60% of districts declared", 0.5, 300),
         ("TOMORROW", "Observers report", "First assessment from international missions", 4.35, 0),
         ("WITHIN 48 HOURS", "Final results", "Electoral commission publishes the full count", 0.9, 0)]
# chronological order top to bottom; reveal follows the narration
reveal = {"NOW": 0.6, "WITHIN 48 HOURS": 1.0, "TOMORROW": 4.4}
ty0, tstep = 560, 330
spine = shape("Timeline spine", 110, ty0, 0, d5, g, path=[{"type": "moveTo", "x": 0, "y": 0}, {"type": "lineTo", "x": 0, "y": 2 * tstep}],
              strokes=[stroke_style(c(58, 68, 86, 1), 6, cap="round")], trim=0)
kf(spine, "trimEnd", [(0.4, 0, LIN), (1.4, 100, EASE_OUT)])
for i, (when, what, detail, _, _x) in enumerate([steps[0], steps[1], steps[2]]):
    yy = ty0 + i * tstep; tr = reveal[when]
    nd = shape(f"Node {when}", 110, yy, 0, d5, g, ellipse=[44, 44], fills=[fill_style(AMBER if i == 0 else INK)],
               strokes=[stroke_style(AMBER, 6)])
    kf(nd, "scaleX", [(tr, 0, LIN), (tr + 0.4, 100, EASE_OUT)]); kf(nd, "scaleY", [(tr, 0, LIN), (tr + 0.4, 100, EASE_OUT)])
    w_ = text(f"When {when}", when, 170, yy - 40, 40, AMBER, 0, d5, g, style=SEMI, w=800, track=4)
    enter(w_, tr + 0.1, yy - 40, dy=16)
    t_ = text(f"What {when}", what, 170, yy + 4, 76, PAPER, 0, d5, g, w=860, h=100)
    enter(t_, tr + 0.2, yy + 4, dy=20)
    dd = text(f"Detail {when}", detail, 170, yy + 100, 36, SOFT, 0, d5, g, style=SEMI, w=860, h=100)
    enter(dd, tr + 0.35, yy + 100, dy=16)
    if i == 0:  # the live step pulses
        pp = shape("Now pulse", 110, yy, 0, d5, g, ellipse=[44, 44], strokes=[stroke_style(AMBER, 3)])
        script(pp, "ellipseSize", "var q=(input.time.seconds%1.4)/1.4; var s=44+q*70; return [s,s];")
        script(pp, "opacity", "var q=(input.time.seconds%1.4)/1.4; return input.time.seconds<1?0:100*(1-q);")

# ================================================================ scene 6: what to watch + sign-off
n, s6, e6 = SCENES[6]; d6 = e6 - s6
g = group("S6 Outro", s6, e6)
wt = group("What to watch", 0, 6.2, g)
a1 = text("WTW line 1", "WHAT TO", 64, 290, 150, PAPER, 0, 6.2, wt, track=3, h=170)
enter(a1, 0.3, 290, dy=50)
a2 = text("WTW line 2", "WATCH NEXT", 64, 440, 150, AMBER, 0, 6.2, wt, track=3, h=170)
enter(a2, 0.45, 440, dy=50)
r6 = rect("WTW rule", 64, 640, 560, 4, LINE, 0, 6.2, wt)
kf(r6, "scaleX", [(0.6, 0, LIN), (1.2, 100, EASE_OUT)])
items = [("01", "Does the Alliance pass 50%?", "A majority lets it govern alone", 0.9),
         ("02", "Or do coalition talks decide?", "Below 50%, alliances pick the government", 3.1)]
for i, (num_, head, sub, t_) in enumerate(items):
    yy = 780 + i * 300
    nn = text(f"Item {num_} number", num_, 64, yy, 70, AMBER, 0, 6.2, wt, w=110, track=2)
    enter(nn, t_, yy, dy=24)
    hd = text(f"Item {num_} head", head, 180, yy + 2, 72, PAPER, 0, 6.2, wt, w=840, h=96, track=1)
    enter(hd, t_ + 0.1, yy + 2, dy=24)
    sd = text(f"Item {num_} sub", sub, 180, yy + 100, 42, SLATE, 0, 6.2, wt, style=SEMI, w=840, track=1)
    enter(sd, t_ + 0.25, yy + 100, dy=16)
kf(wt, "opacity", [(5.4, 100, LIN), (5.9, 0, EASE_IN)])
so = group("Sign-off", 5.7, d6, g)
sd6 = d6 - 5.7
for k in range(3):
    ring = shape(f"Sign-off ring {k+1}", 540, 900, 0, sd6, so, ellipse=[10, 10], strokes=[stroke_style(c(232, 173, 62, 0.8), 3 - k)])
    d = 0.1 + k * 0.25
    script(ring, "ellipseSize", f"var t=input.time.seconds-{d}; if(t<0) return [0,0]; var p=Math.min(1,t/2.2); var e=1-Math.pow(1-p,3); var s=60+e*{700 + k * 240}; return [s,s];")
    kf(ring, "opacity", [(d, 90, LIN), (d + 2.2, 0, EASE_OUT)])
sq2 = rect("Sign-off mark", 540, 760, 44, 88, AMBER, 0, sd6, so, ax=22, ay=44)
kf(sq2, "scaleY", [(0.05, 0, LIN), (0.4, 100, EASE_OUT)])
h6 = text("Sign-off handle", "@GLOBALOBSHQ", 90, 840, 120, PAPER, 0, sd6, so, w=900, just="center", track=6, h=150)
enter(h6, 0.25, 840, dy=30)
kf(h6, "tracking", [(0.25, 24, LIN), (1.2, 6, EASE_OUT)])
tg = text("Sign-off tagline", "Global news, without the blind spots.", 90, 1000, 46, SLATE, 0, sd6, so, style=SEMI, w=900, just="center")
enter(tg, 0.6, 1000, dy=20)
sr = text("Sign-off sources", "SOURCES: FICTIONAL — FORMAT TEST, NOT FOR PUBLICATION", 90, 1110, 28, AMBER, 0, sd6, so, style=SEMI, w=900, just="center", track=3)
fade_in(sr, 0.9)

# ================================================================ wipes (cortinilla) above scenes, below chrome
wp = group("Wipes", 0, TOTAL)
for k, cut in enumerate(CUTS):
    t0, t1 = cut - 0.3, cut + 0.3
    wg = group(f"Wipe {k+1}", t0, t1, wp)
    pn = rect("Wipe panel", 0, 0, W + 60, H, c(14, 18, 26, 1), 0, 0.6, wg)
    rect("Wipe edge", W + 60, 0, 64, H, AMBER, 0, 0.6, wg)
    rect("Wipe edge 2", -64, 0, 64, H, AMBER, 0, 0.6, wg)
    rect("Wipe mark", 570 - 214, 925, 26, 52, AMBER, 0, 0.6, wg)
    text("Wipe wordmark", "GLOBAL OBSERVER", 570 - 176, 916, 66, PAPER, 0, 0.6, wg, w=460, track=3.5)
    kf(wg, "positionX", [(0, -W - 120, LIN), (0.26, -30, EASE_IN), (0.34, -30, LIN), (0.6, W + 60, EASE_OUT)])
# every create prepends (last created is frontmost); bring chrome, then captions, above scenes and wipes
for lid in (ch, cg):
    A.append({"type": "moveFxCompositionLayer", "compositionId": "main", "layerId": lid, "insertIndex": 0})

json.dump(A, open(".tesseract-work/actions.json", "w"), indent=0)

# ================================================================ audio layers (document JSON)
aud = []
aid = 900
def audio(name, asset, start, dur, vol, src_dur=None):
    global aid; aid += 1
    aud.append({"type": "Audio", "id": aid, "name": name, "activeRange": {"start": ms(start), "duration": ms(dur)},
                "sourceRange": {"start": 0, "duration": ms(dur)}, "sourceIntrinsicDuration": ms(src_dur or dur),
                "source": {"assetId": asset}, "volume": vol, "captionsEnabled": False})
    return aid
for vid, st, du in VO:
    audio(f"Narration {vid}", f"vo-{vid}", st, du, 0.75)
music_id = audio("Music bed (procedural placeholder)", "music-bed", 0, TOTAL, 0.5, 51.0)
audio("Ident riser", "sfx-riser", 2.1, 1.1, 0.55)
audio("Ident impact", "sfx-impact", 3.15, 0.4, 0.8)
for k, cut in enumerate(CUTS[1:]):
    audio(f"Wipe whoosh {k+2}", "sfx-whoosh", cut - 0.3, 0.45, 0.35)
audio("Outro ping", "sfx-ping", VOS["vo6"] + 5.55, 0.48, 0.4)
json.dump({"layers": aud, "music_id": music_id, "vo": VO}, open(".tesseract-work/audio_layers.json", "w"), indent=1)
# music ducking: bed at 0.55 in the ident/gaps, 0.16 under narration, 0.3 s ramps
segs = ",".join(f"[{st:.2f},{st + du:.2f}]" for _, st, du in VO)
duck = ("var t=input.time.seconds; var hi=0.55, lo=0.13, r=0.3; var v=hi; var S=[" + segs + "];"
        "for(var i=0;i<S.length;i++){var a=S[i][0]-r, b=S[i][1]+r;"
        " if(t>=a&&t<=b){var k=Math.min(1,(t-a)/r,(b-t)/r); v=Math.min(v,hi+(lo-hi)*Math.max(0,k));}}"
        f" if(t>{TOTAL - 2.5}) v=v*Math.max(0,({TOTAL}-t)/2.5); return v;")
json.dump([{"type": "setFxPropertyAnimator", "compositionId": "main", "property": {"layerId": music_id, "propertyType": "volume"},
            "dependencies": [], "animator": {"type": "jsScript", "layerTimeJsCode": duck}}], open(".tesseract-work/audio_actions.json", "w"))
print(f"{len(A)} actions, {_next_id[0]} visual ids, {len(aud)} audio layers")
