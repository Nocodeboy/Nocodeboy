#!/usr/bin/env python3
"""Global Observer — Ebola (Bundibugyo) in DR Congo, update of 24 Sep 2026.

Every figure on screen is taken from the sources listed in NOTES.md:
DRC Ministry of Health via ECDC (update 23 Sep 2026 14:45, data to 21 Sep) and WHO DON617 (10 Sep, data to 7 Sep).
"""
import json, math, sys
sys.path.insert(0, ".tesseract-work")
from golib import *          # noqa: F401,F403  (layer/animation helpers and brand palette)
import golib
from shapely.geometry import shape as geom
from shapely.ops import unary_union

_text1 = golib.text
def text(name, s, x, y, size, color, start, end, parent=None, h=None, **kw):
    """Like golib.text, but a string with line breaks becomes a group of single-line layers."""
    if "\n" not in s:
        return _text1(name, s, x, y, size, color, start, end, parent, h=h, **kw)
    lines = s.split("\n"); lh = size * 1.28
    grp = group(name, start, end, parent)
    for i, ln in enumerate(lines):
        _text1(f"{name} line {i+1}", ln, x, y + i * lh, size, color, 0, end - start, grp, h=int(lh), **kw)
    return grp

TOTAL = 81.0
# presenter clip: Magnific lip-sync by default; PRESENTER_FILE / PRESENTER_TOOL switch to another take (e.g. JoggAI)
import os, subprocess
PRESENTER_FILE = os.environ.get("PRESENTER_FILE", "Sources/presenter/anchor-intro-veed.mp4")
PRESENTER_TOOL = os.environ.get("PRESENTER_TOOL", "Magnific lip-sync")
_pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                                 "-of", "json", PRESENTER_FILE], capture_output=True, text=True).stdout)
PW, PH = _pr["streams"][0]["width"], _pr["streams"][0]["height"]
PDUR = int(float(_pr["format"]["duration"]) * 1000)
PSCALE = round(100 * max(1080 / PW, 1920 / PH), 2)
VO = [("vo1", 3.6, 11.18), ("vo2", 15.2, 12.80), ("vo3", 28.4, 4.55), ("vo4", 33.4, 14.99),
      ("vo5", 48.8, 12.72), ("vo6", 62.0, 7.18), ("vo7", 69.6, 8.72)]
VOS = {v[0]: v[1] for v in VO}
CUTS = [3.4, 13.6, 33.3, 48.7, 61.9, 69.5]   # wipe midpoints; presenter cut before her closing smile
_b = [0.0] + CUTS + [TOTAL]
SCENES = {n: (_b[i], _b[i + 1]) for i, n in enumerate(["ident", "anchor", "figures", "map", "vaccine", "risk", "outro"])}
CHROME_START = 3.25
TAG = "UPDATE"

# ---------------------------------------------------------------- captions from measured word timings
WORDS = json.load(open(".tesseract-work/words.json"))
FIX = {"Itri": "Ituri", "Sudhu": "Sud-Ubangi,", "Bangi,": "", "Bondi": "Bundibugyo.", "Bugio.": "",
       "Organisation": "Organization", "watch,": "watch:", "evening,": "evening."}
def phrases(vid, maxlen=44):
    ws = []
    for w in WORDS[vid]:
        t = FIX.get(w["w"], w["w"])
        if w["w"].startswith(",") and ws:        # "7" ",773" -> "7,773"
            ws[-1]["w"] += w["w"]; ws[-1]["e"] = w["e"]; continue
        if t == "":
            ws[-1]["e"] = w["e"]; continue
        if ws and ws[-1]["w"][-1] in ".:" and t[0].islower() and t != "the":
            t = t[0].upper() + t[1:]
        ws.append({"w": t, "s": w["s"], "e": w["e"]})
    # sentences first, then split long ones near the middle at a word gap
    sents, cur = [], []
    for w in ws:
        cur.append(w)
        if w["w"][-1] in ".:": sents.append(cur); cur = []
    if cur: sents.append(cur)
    out = []
    def split(chunk):
        txt = " ".join(x["w"] for x in chunk)
        if len(txt) <= maxlen or len(chunk) < 4:
            out.append(chunk); return
        best, bi = 1e9, 1
        for i in range(2, len(chunk) - 1):
            left = len(" ".join(x["w"] for x in chunk[:i]))
            score = abs(left - len(txt) / 2) - (12 if chunk[i - 1]["w"][-1] == "," else 0)
            if score < best: best, bi = score, i
        split(chunk[:bi]); split(chunk[bi:])
    for s_ in sents: split(s_)
    return [(p[0]["s"], p[-1]["e"], " ".join(x["w"] for x in p)) for p in out]
CAPS = [(vid, s, e, t) for vid, _, _ in VO for (s, e, t) in phrases(vid)]

# ================================================================ background
bg = group("Background", 0, TOTAL)
rect("Ink base", 0, 0, W, H, INK, 0, TOTAL, bg)
gi = nid()
A.append({"type": "createFxRectLayer", "compositionId": "main", "layerId": gi, "name": "Studio light", "insertIndex": 0,
          "parentLayerId": bg, "activeRange": rng(0, TOTAL), "transform": tf(),
          "rect": {"size": [W, H], "fillColor": [0, 0, 0, 0],
                   "fillPaint": {"type": "gradient", "gradientType": "radial", "start": [540, 700], "end": [540, 1900],
                                 "stops": [{"offset": 0, "color": c(26, 36, 54, 1)}, {"offset": 1, "color": c(9, 12, 17, 0)}]}}})
dots = []
for row in range(0, H // 40 + 1):
    dots += [{"type": "moveTo", "x": 0, "y": row * 40 + 20}, {"type": "lineTo", "x": W, "y": row * 40 + 20}]
shape("Dot grid", 0, 0, 0, TOTAL, bg, path=dots, strokes=[stroke_style(c(120, 140, 170, 0.14), 3, dashes=[0.1, 39.9])])

# ================================================================ ident (same as the pilot, sting from Magnific)
s0, e0 = SCENES["ident"]
g = group("S0 Ident", s0, e0)
rect("Ident black", 0, 0, W, H, INK, 0, e0, g)
for k in range(3):
    ring = shape(f"Signal ring {k+1}", 540, 860, 0, e0, g, ellipse=[10, 10], strokes=[stroke_style(c(232, 173, 62, 0.9), 4 - k)])
    d = 0.25 + k * 0.22
    script(ring, "ellipseSize", f"var t=input.time.seconds-{d}; if(t<0) return [0,0]; var p=Math.min(1,t/1.6); var e=1-Math.pow(1-p,3); var s=40+e*{900 + k * 260}; return [s,s];")
    kf(ring, "opacity", [(d, 100, LIN), (d + 1.6, 0, EASE_OUT)])
sq = rect("Brand square", 540, 860, 60, 120, AMBER, 0, e0, g, ax=30, ay=60)
kf(sq, "scaleX", [(0.05, 0, LIN), (0.45, 100, EASE_OUT)]); kf(sq, "scaleY", [(0.05, 0, LIN), (0.45, 100, EASE_OUT)])
kf(sq, "positionX", [(0.9, 540, LIN), (1.4, 128, EASE_IO)]); kf(sq, "rotation", [(0.05, -90, LIN), (0.6, 0, EASE_OUT)])
wm = text("Wordmark", "GLOBAL OBSERVER", 176, 792, 124, PAPER, 0, e0, g, w=880, track=6)
kf(wm, "opacity", [(1.15, 0, LIN), (1.6, 100, EASE_OUT)]); kf(wm, "tracking", [(1.15, 40, LIN), (1.9, 6, EASE_OUT)])
tl = text("Tagline", "GLOBAL NEWS, WITHOUT THE BLIND SPOTS", 180, 960, 40, SLATE, 0, e0, g, style=SEMI, w=860, track=5)
enter(tl, 1.7, 960, dy=20)

# ================================================================ scene: anchor (video layer added in the document JSON)
s1, e1 = SCENES["anchor"]; d1 = e1 - s1
g = group("S1 Anchor overlays", s1, e1)
ANCHOR_GROUP = g
rect("Cold grade", 0, 0, W, H, c(8, 22, 48, 0.20), 0, d1, g)
li = nid()
A.append({"type": "createFxRectLayer", "compositionId": "main", "layerId": li, "name": "Lower gradient", "insertIndex": 0,
          "parentLayerId": g, "activeRange": rng(0, d1), "transform": tf(0, 1180),
          "rect": {"size": [W, 740], "fillColor": [0, 0, 0, 0],
                   "fillPaint": {"type": "gradient", "gradientType": "linear", "start": [0, 0], "end": [0, 420],
                                 "stops": [{"offset": 0, "color": c(9, 12, 17, 0)}, {"offset": 1, "color": c(9, 12, 17, 0.96)}]}}})
lt = group("Lower third", 0, d1, g)
tw = width_px(TAG, 34, "Bold", 3)
rect("LT tag", 64, 1400, tw + 40, 56, DEV, 0, d1, lt)
text("LT tag label", TAG, 84, 1402, 34, PAPER, 0, d1, lt, w=tw + 30, track=3)
text("LT title", "EBOLA OUTBREAK: DR CONGO", 64, 1470, 76, PAPER, 0, d1, lt, track=2, h=96)
text("LT sub", "Confirmed cases pass 7,700 · Health ministry via ECDC", 64, 1566, 38, SOFT, 0, d1, lt, style=SEMI, track=1)
kf(lt, "positionY", [(0.5, 60, LIN), (1.0, 0, EASE_OUT)]); kf(lt, "opacity", [(0.5, 0, LIN), (0.9, 100, EASE_OUT)])
ai = "AI-GENERATED PRESENTER"; aw = width_px(ai, 26, "SemiBold", 2.5)
rect("AI chip", W - 64 - aw - 32, 236, aw + 32, 44, c(9, 12, 17, 0.7), 0, d1, g, stroke=c(150, 162, 180, 1), sw=2)
text("AI chip label", ai, W - 64 - aw - 16, 241, 26, SOFT, 0, d1, g, style=SEMI, w=aw + 10, track=2.5)

# ================================================================ chrome
ch = group("Chrome", CHROME_START, TOTAL); cd = TOTAL - CHROME_START
top = group("Top bar", 0, cd, ch)
rect("Top bar plate", 0, 0, W, 132, c(9, 12, 17, 0.88), 0, cd, top)
rect("Top bar rule", 0, 131, W, 2, LINE, 0, cd, top)
rect("Top mark", 64, 52, 18, 36, AMBER, 0, cd, top)
text("Top brand", "GLOBAL OBSERVER", 100, 44, 46, PAPER, 0, cd, top, w=500, track=3.5)
text("Top date", "24 SEP 2026", W - 64 - 300, 52, 32, SLATE, 0, cd, top, style=SEMI, w=300, just="right", track=2.5)
rect("Progress track", 0, 0, W, 7, c(26, 32, 41, 0.55), 0, cd, top)
pb = rect("Progress", 0, 0, W, 7, c(232, 173, 62, 0.98), 0, cd, top)
script(pb, "scaleX", f"return Math.min(100, 100*input.time.seconds/{cd:.3f});")
kf(top, "positionY", [(0, -140, LIN), (0.5, 0, EASE_OUT)])
chips = group("Chips", 0, cd, ch)
rect("Tag chip", 64, 160, tw + 44, 56, DEV, 0, cd, chips)
text("Tag label", TAG, 86, 162, 34, PAPER, 0, cd, chips, w=tw + 30, track=3)
desk = "HEALTH · DR CONGO"; dw = width_px(desk, 30, "SemiBold", 3)
text("Desk label", desk, 64 + tw + 70, 168, 30, SLATE, 0, cd, chips, style=SEMI, w=dw + 20, track=3)
kf(chips, "opacity", [(0.3, 0, LIN), (0.7, 100, EASE_OUT)])
tk = group("Ticker", 0, cd, ch)
rect("Ticker band", 0, 1802, W, 118, c(9, 12, 17, 0.96), 0, cd, tk)
rect("Ticker rule", 0, 1802, W, 2, LINE, 0, cd, tk)
item = ("EBOLA IN DR CONGO: 7,773 CONFIRMED CASES AND 3,759 DEATHS, DATA TO 21 SEP   •   63 HEALTH ZONES IN 7 PROVINCES AFFECTED   •   "
        "NO APPROVED VACCINE OR TREATMENT FOR BUNDIBUGYO VIRUS   •   WHO RISK: VERY HIGH NATIONAL, HIGH REGIONAL, LOW GLOBAL   •   "
        "SOURCES: DRC HEALTH MINISTRY VIA ECDC (23 SEP), WHO (10 SEP)   •   ")
iw = width_px(item, 36, "SemiBold", 1.5)
crawl = text("Ticker crawl", item * 3, 300, 1838, 36, SOFT, 0, cd, tk, style=SEMI, w=int(iw * 3 + 400), h=56, track=1.5)
script(crawl, "positionX", f"return 300 - ((input.time.seconds*130) % {iw:.1f});")
rect("Ticker label plate", 0, 1804, 292, 116, c(9, 12, 17, 1), 0, cd, tk)
rect("Ticker label", 64, 1832, 204, 60, AMBER, 0, cd, tk)
text("Ticker label text", "EBOLA · DRC", 76, 1836, 34, INK, 0, cd, tk, w=190, track=2)
kf(tk, "positionY", [(0, 130, LIN), (0.5, 0, EASE_OUT)])

# ================================================================ captions (High over the presenter, Main elsewhere)
cg = group("Captions", CHROME_START, TOTAL)
for i_, (vid, a, b, s) in enumerate(CAPS):
    t0 = VOS[vid] + a; t1 = VOS[vid] + b + 0.12
    if i_ + 1 < len(CAPS):
        t1 = min(t1, VOS[CAPS[i_ + 1][0]] + CAPS[i_ + 1][1] - 0.02)
    two = width_px(s, 50, "SemiBold", 0.8) >= 880
    ph = 144 if two else 84
    y = (1350 - ph) if t0 < CUTS[1] else (1778 - ph)   # above the lower third while the presenter is on screen
    rect("Caption plate", 48, y, 984, ph, c(9, 12, 17, 0.74), t0 - CHROME_START, t1 - CHROME_START, cg, round_=10)
    text("Caption", s, 80, y + 10, 50, PAPER, t0 - CHROME_START, t1 - CHROME_START, cg, style=SEMI, w=920, h=ph - 20,
         just="center", valign="center", track=0.8)

def at(vid, sec, scene):
    """Local scene time of a moment in a narration clip."""
    return VOS[vid] + sec - SCENES[scene][0]

def counter(layer, value, t0, dur, suffix=""):
    script(layer, "textContent", f"var p=Math.max(0,Math.min(1,(input.time.seconds-{t0})/{dur})); var v=Math.round({value}*(1-Math.pow(1-p,3)));"
           f" return v.toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ',')+'{suffix}';")

# ================================================================ scene: figures
s2, e2 = SCENES["figures"]; d2 = e2 - s2
g = group("S2 Figures", s2, e2)
k2 = text("Kicker", "DR CONGO · CONFIRMED CASES", 64, 270, 44, AMBER, 0, d2, g, style=SEMI, track=6)
enter(k2, 0.4, 270)
r2 = rect("Kicker rule", 64, 336, 620, 4, AMBER, 0, d2, g); kf(r2, "scaleX", [(0.5, 0, LIN), (1.1, 100, EASE_OUT)])
tc = at("vo2", 1.5, "figures")
big = text("Cases number", "0", 56, 360, 260, PAPER, 0, d2, g, w=980, h=280, track=-1)
counter(big, 7773, tc, 2.4); fade_in(big, tc - 0.2, 0.2)
lab = text("Cases label", "CONFIRMED CASES", 64, 640, 56, AMBER, 0, d2, g, track=3); enter(lab, tc + 0.6, 640, dy=20)
td = at("vo2", 6.5, "figures")
rect("Deaths rule", 64, 740, W - 128, 2, LINE, 0, d2, g)
dn = text("Deaths number", "0", 60, 770, 170, PAPER, 0, d2, g, w=560, h=200, track=-1)
counter(dn, 3759, td, 1.8); fade_in(dn, td - 0.2, 0.2)
dl = text("Deaths label", "DEATHS", 600, 830, 64, c(226, 96, 82), 0, d2, g, w=400, track=4); enter(dl, td + 0.5, 830, dy=20)
tdt = at("vo2", 9.8, "figures")
note = text("Data note", "DATA TO 21 SEPTEMBER 2026", 64, 975, 38, SOFT, 0, d2, g, style=SEMI, track=3); fade_in(note, tdt)
src = text("Figures source", "SOURCE: DRC MINISTRY OF HEALTH VIA ECDC, UPDATED 23 SEP · 7 SEP FIGURE: WHO", 64, 1590, 26, SLATE, 0, d2, g, style=SEMI, track=2)
fade_in(src, 1.0)
# comparison (vo3): two weeks of growth
tb = at("vo3", 0.2, "figures")
cmp_ = group("Two-week comparison", 0, d2, g)
text("Compare title", "CONFIRMED CASES, TWO WEEKS APART", 64, 1080, 36, PAPER, 0, d2, cmp_, track=3)
MAXV = 8000; BW = W - 128
for i, (lbl, v, col, dt) in enumerate([("7 SEP", 6757, c(90, 102, 124), 0.0), ("21 SEP", 7773, AMBER, 0.35)]):
    y = 1150 + i * 130
    text(f"Bar {lbl} date", lbl, 64, y, 34, SLATE if i == 0 else AMBER, 0, d2, cmp_, style=SEMI, w=200, track=3)
    rect(f"Bar {lbl} track", 64, y + 46, BW, 64, c(24, 30, 40), 0, d2, cmp_)
    bar = rect(f"Bar {lbl}", 64, y + 46, BW * v / MAXV, 64, col, 0, d2, cmp_)
    kf(bar, "scaleX", [(tb + dt, 0, LIN), (tb + dt + 0.9, 100, EASE_OUT)])
    val = text(f"Bar {lbl} value", f"{v:,}", 84, y + 48, 50, INK, 0, d2, cmp_, w=300); fade_in(val, tb + dt + 0.6, 0.2)
badge_t = at("vo3", 2.9, "figures")
bw_ = width_px("+1,016 IN TWO WEEKS", 44, "Bold", 2) + 48
bd = rect("Growth badge", W - 64 - bw_, 1416, bw_, 70, c(211, 56, 42), 0, d2, cmp_)
bt = text("Growth badge text", "+1,016 IN TWO WEEKS", W - 64 - bw_ + 24, 1422, 44, PAPER, 0, d2, cmp_, w=bw_, track=2)
for l_ in (bd, bt): fade_in(l_, badge_t, 0.25)
kf(cmp_, "opacity", [(tb - 0.4, 0, LIN), (tb, 100, EASE_OUT)])

# ================================================================ scene: map of provinces
s3, e3 = SCENES["map"]; d3 = e3 - s3
g = group("S3 Map", s3, e3)
k3 = text("Kicker", "WHERE THE VIRUS HAS BEEN CONFIRMED", 64, 262, 40, AMBER, 0, d3, g, style=SEMI, track=5)
enter(k3, 0.35, 262)
geo = json.load(open("Sources/geo/geoBoundaries-COD-ADM1_simplified.geojson"))
feats = {f["properties"]["shapeName"]: geom(f["geometry"]).simplify(0.03, preserve_topology=True) for f in geo["features"]}
minx, miny, maxx, maxy = unary_union(list(feats.values())).bounds
BOX_X, BOX_Y, BOX_W = 70, 330, 940
kx = math.cos(math.radians((miny + maxy) / 2)); sc = BOX_W / ((maxx - minx) * kx)
def pj(lon, lat): return ((lon - minx) * kx * sc + BOX_X, (maxy - lat) * sc + BOX_Y)
AFFECTED = ["Ituri", "North Kivu", "Upper Uele", "Tshopo", "Lower Uele", "South Kivu", "Sud-Ubangi"]
LIGHT = {n: at("vo4", 3.7, "map") + i * 0.18 for i, n in enumerate(AFFECTED[:-1])}
LIGHT["Sud-Ubangi"] = at("vo4", 8.9, "map")
BASE = c(30, 37, 50); WARM = c(214, 122, 42); HOT = c(211, 56, 42)
mp = group("Province map", 0, d3, g)
for name, gm in feats.items():
    polys = gm.geoms if gm.geom_type == "MultiPolygon" else [gm]
    cmds = []
    for p in polys:
        pts = [pj(x, y) for x, y in p.exterior.coords]
        cmds.append({"type": "moveTo", "x": round(pts[0][0], 1), "y": round(pts[0][1], 1)})
        cmds += [{"type": "lineTo", "x": round(x, 1), "y": round(y, 1)} for x, y in pts[1:]]
        cmds.append({"type": "close"})
    lid = shape(f"Province {name}", 0, 0, 0, d3, mp, path=cmds, fills=[fill_style(BASE)],
                strokes=[stroke_style(c(96, 110, 134, 0.9), 2, cap="round")])
    if name in LIGHT:
        tgt = HOT if name == "Ituri" else WARM
        t_ = LIGHT[name]
        script(lid, "fillColor", f"var p=Math.max(0,Math.min(1,(input.time.seconds-{t_:.2f})/0.4)); "
               f"return [{BASE[0]}+({tgt[0]}-{BASE[0]})*p,{BASE[1]}+({tgt[1]}-{BASE[1]})*p,{BASE[2]}+({tgt[2]}-{BASE[2]})*p,1];")
kf(mp, "opacity", [(0.2, 0, LIN), (0.8, 100, EASE_OUT)])
kf(mp, "scaleX", [(0.2, 94, LIN), (1.0, 100, EASE_OUT)]); kf(mp, "scaleY", [(0.2, 94, LIN), (1.0, 100, EASE_OUT)])
# labels and markers
def centroid(n):
    p = feats[n].representative_point(); return pj(p.x, p.y)
ix, iy = centroid("Ituri"); ti = at("vo4", 5.7, "map")
lab = text("Ituri label", "ITURI", ix - 190, iy - 40, 40, PAPER, 0, d3, mp, w=160, just="right", track=2); fade_in(lab, ti)
lab2 = text("Ituri sub", "HARDEST HIT", ix - 190, iy + 4, 26, c(255, 190, 170), 0, d3, mp, style=SEMI, w=160, just="right", track=2); fade_in(lab2, ti + 0.15)
sx_, sy_ = centroid("Sud-Ubangi"); ts = LIGHT["Sud-Ubangi"]
mk = group("Sud-Ubangi marker", 0, d3, mp, x=sx_, y=sy_)
for k in range(2):
    pr = shape(f"Pulse {k+1}", 0, 0, 0, d3, mk, ellipse=[20, 20], strokes=[stroke_style(PAPER, 3)])
    script(pr, "ellipseSize", f"var q=((input.time.seconds+{k * 0.8})%1.6)/1.6; var s=20+q*110; return [s,s];")
    script(pr, "opacity", f"return input.time.seconds<{ts:.2f}?0:100*(1-((input.time.seconds+{k * 0.8})%1.6)/1.6);")
shape("Sud-Ubangi dot", 0, 0, 0, d3, mk, ellipse=[22, 22], fills=[fill_style(PAPER)])
kf(mk, "opacity", [(ts - 0.1, 0, LIN), (ts + 0.2, 100, EASE_OUT)])
sl = text("Sud-Ubangi label", "SUD-UBANGI", sx_ + 28, sy_ - 8, 40, PAPER, 0, d3, mp, w=320, track=2); fade_in(sl, ts + 0.2)
sl2 = text("Sud-Ubangi sub", "LATEST PROVINCE", sx_ + 28, sy_ + 36, 26, AMBER, 0, d3, mp, style=SEMI, w=320, track=2); fade_in(sl2, ts + 0.35)
tcar = at("vo4", 12.8, "map")
car = text("CAR label", "CENTRAL AFRICAN REPUBLIC", 70, BOX_Y - 6, 30, SOFT, 0, d3, mp, style=SEMI, w=600, track=3)
fade_in(car, tcar)
arrow = shape("CAR arrow", sx_ - 10, BOX_Y + 36, 0, d3, mp, path=[{"type": "moveTo", "x": 0, "y": sy_ - BOX_Y - 60}, {"type": "lineTo", "x": 0, "y": 0}],
              strokes=[stroke_style(SOFT, 3, cap="round", dashes=[8, 8])], trim=0)
kf(arrow, "trimEnd", [(tcar, 0, LIN), (tcar + 0.6, 100, EASE_OUT)])
# counters below the map
tz = at("vo4", 1.8, "map"); tpv = at("vo4", 3.7, "map")
mapb = BOX_Y + (maxy - miny) * sc
zc = text("Zones number", "0", 64, mapb + 30, 110, PAPER, 0, d3, g, w=260, h=130); counter(zc, 63, tz, 0.9); fade_in(zc, tz - 0.1, 0.2)
text("Zones label", "HEALTH ZONES\nOF 167", 250, mapb + 50, 34, SOFT, 0, d3, g, style=SEMI, w=250, h=90, track=2)
pc = text("Provinces number", "0", 560, mapb + 30, 110, AMBER, 0, d3, g, w=200, h=130); counter(pc, 7, tpv, 0.9); fade_in(pc, tpv - 0.1, 0.2)
text("Provinces label", "PROVINCES\nOF 26", 690, mapb + 50, 34, SOFT, 0, d3, g, style=SEMI, w=250, h=90, track=2)
ms3 = text("Map source", "SOURCE: ECDC, 23 SEP · MAP DATA: OPENSTREETMAP CONTRIBUTORS (ODbL) VIA GEOBOUNDARIES", 64, 1600, 24, SLATE, 0, d3, g, style=SEMI, track=1.5)
fade_in(ms3, 1.0)

# ================================================================ scene: vaccine and treatment
s4, e4 = SCENES["vaccine"]; d4 = e4 - s4
g = group("S4 Vaccine", s4, e4)
k4 = text("Kicker", "STRAIN: BUNDIBUGYO VIRUS", 64, 270, 44, AMBER, 0, d4, g, style=SEMI, track=6); enter(k4, 0.35, 270)
tv = at("vo5", 0.3, "vaccine")
for i, lbl in enumerate(["APPROVED VACCINE", "APPROVED TREATMENT"]):
    y = 380 + i * 190
    row = group(f"Row {lbl}", 0, d4, g)
    text(f"{lbl} label", lbl, 64, y, 40, SOFT, 0, d4, row, style=SEMI, track=4)
    text(f"{lbl} value", "NONE", 64, y + 44, 110, PAPER, 0, d4, row, track=3, h=120)
    x_ = shape(f"{lbl} strike", 64 + 390, y + 70, 0, d4, row, path=[{"type": "moveTo", "x": 0, "y": 0}, {"type": "lineTo", "x": 70, "y": 70},
               {"type": "moveTo", "x": 70, "y": 0}, {"type": "lineTo", "x": 0, "y": 70}], strokes=[stroke_style(c(226, 96, 82), 12)], trim=0)
    kf(x_, "trimEnd", [(tv + 0.6 + i * 0.3, 0, LIN), (tv + 1.0 + i * 0.3, 100, EASE_OUT)])
    enter(row, tv + i * 0.3, 0, dy=30)
tt = at("vo5", 4.2, "vaccine")
tr = group("Trial panel", 0, d4, g)
rect("Trial panel plate", 64, 800, W - 128, 560, c(18, 24, 34, 0.9), 0, d4, tr, round_=8)
rect("Trial panel accent", 64, 800, 8, 560, AMBER, 0, d4, tr)
text("Trial kicker", "IN A CLINICAL TRIAL", 104, 830, 36, AMBER, 0, d4, tr, style=SEMI, track=4)
text("Trial name", "rVSV-ZEBOV (ERVEBO)", 104, 876, 72, PAPER, 0, d4, tr, track=1, h=90)
text("Trial note", "Developed for the Zaire strain, not for Bundibugyo", 104, 966, 38, SOFT, 0, d4, tr, style=SEMI, w=880)
tn = at("vo5", 10.0, "vaccine")
vn = text("Vaccinated number", "0", 104, 1050, 170, PAPER, 0, d4, tr, w=600, h=200, track=-1); counter(vn, 2007, tn, 1.2); fade_in(vn, tn - 0.2, 0.2)
text("Vaccinated label", "PEOPLE VACCINATED\nAS OF 7 SEPTEMBER", 560, 1100, 36, SOFT, 0, d4, tr, style=SEMI, w=420, h=100, track=2)
kf(tr, "opacity", [(tt, 0, LIN), (tt + 0.4, 100, EASE_OUT)]); kf(tr, "positionY", [(tt, 40, LIN), (tt + 0.5, 0, EASE_OUT)])
s4s = text("Vaccine source", "SOURCE: WHO DISEASE OUTBREAK NEWS, 10 SEP 2026", 64, 1400, 26, SLATE, 0, d4, g, style=SEMI, track=2); fade_in(s4s, 1.0)

# ================================================================ scene: WHO risk assessment
s5, e5 = SCENES["risk"]; d5 = e5 - s5
g = group("S5 Risk", s5, e5)
k5 = text("Kicker", "WHO RISK ASSESSMENT", 64, 270, 44, AMBER, 0, d5, g, style=SEMI, track=6); enter(k5, 0.35, 270)
rows = [("DR CONGO", "VERY HIGH", 5, HOT, at("vo6", 2.0, "risk")),
        ("NEIGHBOURING COUNTRIES", "HIGH", 4, WARM, at("vo6", 3.8, "risk")),
        ("GLOBAL", "LOW", 1, c(120, 136, 160), at("vo6", 5.6, "risk"))]
for i, (who, lvl, n, col, t_) in enumerate(rows):
    y = 400 + i * 330
    rg = group(f"Risk {who}", 0, d5, g)
    text(f"{who} label", who, 64, y, 44, SOFT, 0, d5, rg, style=SEMI, track=4)
    text(f"{who} level", lvl, 64, y + 52, 110, PAPER if n > 1 else SOFT, 0, d5, rg, track=2, h=120)
    for s_ in range(5):
        seg = rect(f"{who} seg {s_+1}", 64 + s_ * 192, y + 190, 180, 36, col if s_ < n else c(34, 42, 56), 0, d5, rg)
        if s_ < n: kf(seg, "opacity", [(t_ + 0.1 + s_ * 0.08, 0, LIN), (t_ + 0.25 + s_ * 0.08, 100, EASE_OUT)])
    enter(rg, t_ - 0.3, 0, dy=30)
s5s = text("Risk source", "SOURCE: WHO DISEASE OUTBREAK NEWS, 10 SEP 2026", 64, 1400, 26, SLATE, 0, d5, g, style=SEMI, track=2); fade_in(s5s, 1.0)

# ================================================================ scene: what to watch + sign-off
s6, e6 = SCENES["outro"]; d6 = e6 - s6
g = group("S6 Outro", s6, e6)
SO = at("vo7", 6.4, "outro")
wt = group("What to watch", 0, SO + 0.6, g)
a1 = text("WTW 1", "WHAT TO", 64, 290, 150, PAPER, 0, SO + 0.6, wt, track=3, h=170); enter(a1, 0.3, 290, dy=50)
a2 = text("WTW 2", "WATCH NEXT", 64, 440, 150, AMBER, 0, SO + 0.6, wt, track=3, h=170); enter(a2, 0.45, 440, dy=50)
for i, (num_, head, sub, t_) in enumerate([("01", "The next WHO update", "Case and death counts, vaccination figures", at("vo7", 1.0, "outro")),
                                           ("02", "Cases beyond seven provinces", "Any confirmed case in a new province", at("vo7", 3.0, "outro"))]):
    yy = 780 + i * 300
    nn = text(f"Item {num_} number", num_, 64, yy, 70, AMBER, 0, SO + 0.6, wt, w=110, track=2); enter(nn, t_, yy, dy=24)
    hd = text(f"Item {num_} head", head, 180, yy + 2, 72, PAPER, 0, SO + 0.6, wt, w=840, h=96, track=1); enter(hd, t_ + 0.1, yy + 2, dy=24)
    sd = text(f"Item {num_} sub", sub, 180, yy + 100, 42, SLATE, 0, SO + 0.6, wt, style=SEMI, w=840, track=1); enter(sd, t_ + 0.25, yy + 100, dy=16)
kf(wt, "opacity", [(SO, 100, LIN), (SO + 0.5, 0, EASE_IN)])
so = group("Sign-off", SO + 0.3, d6, g); sd6 = d6 - SO - 0.3
for k in range(3):
    ring = shape(f"Sign-off ring {k+1}", 540, 780, 0, sd6, so, ellipse=[10, 10], strokes=[stroke_style(c(232, 173, 62, 0.8), 3 - k)])
    d = 0.1 + k * 0.25
    script(ring, "ellipseSize", f"var t=input.time.seconds-{d}; if(t<0) return [0,0]; var p=Math.min(1,t/2.2); var e=1-Math.pow(1-p,3); var s=60+e*{700 + k * 240}; return [s,s];")
    kf(ring, "opacity", [(d, 90, LIN), (d + 2.2, 0, EASE_OUT)])
sq2 = rect("Sign-off mark", 540, 640, 44, 88, AMBER, 0, sd6, so, ax=22, ay=44); kf(sq2, "scaleY", [(0.05, 0, LIN), (0.4, 100, EASE_OUT)])
h6 = text("Sign-off handle", "@GLOBALOBSHQ", 90, 720, 120, PAPER, 0, sd6, so, w=900, just="center", track=6, h=150); enter(h6, 0.25, 720, dy=30)
tg = text("Sign-off tagline", "Global news, without the blind spots.", 90, 880, 46, SLATE, 0, sd6, so, style=SEMI, w=900, just="center"); enter(tg, 0.6, 880, dy=20)
srcs = ("SOURCES\nDRC Ministry of Health via ECDC — update of 23 Sep 2026 (data to 21 Sep)\n"
        "WHO Disease Outbreak News DON617 — 10 Sep 2026 (data to 7 Sep)\n"
        "Map data: OpenStreetMap contributors (ODbL) via geoBoundaries\nPresenter AI-generated (" + PRESENTER_TOOL + "), voice Magnific")
sr = text("Sign-off sources", srcs, 90, 1020, 30, SOFT, 0, sd6, so, style=SEMI, w=900, h=240, just="center", track=1); fade_in(sr, 0.9)

# ================================================================ wipes
wp = group("Wipes", 0, TOTAL)
for k, cut in enumerate(CUTS):
    wg = group(f"Wipe {k+1}", cut - 0.3, cut + 0.3, wp)
    rect("Wipe panel", 0, 0, W + 60, H, c(14, 18, 26), 0, 0.6, wg)
    rect("Wipe edge", W + 60, 0, 64, H, AMBER, 0, 0.6, wg)
    rect("Wipe edge 2", -64, 0, 64, H, AMBER, 0, 0.6, wg)
    rect("Wipe mark", 570 - 214, 925, 26, 52, AMBER, 0, 0.6, wg)
    text("Wipe wordmark", "GLOBAL OBSERVER", 570 - 176, 916, 66, PAPER, 0, 0.6, wg, w=460, track=3.5)
    kf(wg, "positionX", [(0, -W - 120, LIN), (0.26, -30, EASE_IN), (0.34, -30, LIN), (0.6, W + 60, EASE_OUT)])
for lid in (ch, cg):
    A.append({"type": "moveFxCompositionLayer", "compositionId": "main", "layerId": lid, "insertIndex": 0})
json.dump(A, open(".tesseract-work/actions.json", "w"), indent=0)

# ================================================================ media layers for the document JSON
aid = [900]
media = []
def audio(name, asset, start, dur, vol, src_start=0.0, src_dur=None):
    aid[0] += 1
    media.append({"type": "Audio", "id": aid[0], "name": name, "activeRange": {"start": ms(start), "duration": ms(dur)},
                  "sourceRange": {"start": ms(src_start), "duration": ms(dur)}, "sourceIntrinsicDuration": ms(src_dur or dur),
                  "source": {"assetId": asset}, "volume": vol, "captionsEnabled": False})
    return aid[0]
for vid, st, du in VO:
    audio(f"Narration {vid}", f"vo-{vid}", st, du, 0.75)
music = audio("Music bed (Magnific)", "music-bed", 0, TOTAL, 0.5, 0, 81.0)
audio("Ident sting (Magnific)", "sfx-sting", 0.15, 3.0, 0.42, 0, 3.03)
for k, cut in enumerate(CUTS[1:]):
    audio(f"Wipe whoosh {k+2}", "sfx-whoosh", cut - 0.3, 0.45, 0.3)
video = {"type": "Video", "id": 950, "name": f"AI presenter ({PRESENTER_TOOL})",
         "activeRange": {"start": ms(s1), "duration": ms(e1 - s1)}, "sourceRange": {"start": ms(s1 - VOS['vo1'] + 0.0) if s1 > VOS['vo1'] else 0, "duration": ms(e1 - s1)},
         "sourceIntrinsicDuration": PDUR, "volume": None,
         # source scaled to cover 1080x1920 (the layer keeps the source size)
         "transform": {"anchorPoint": [PW / 2, PH / 2], "position": [540, 960], "scale": [PSCALE, PSCALE], "rotation": 0, "opacity": 100},
         "source": {"assetId": "presenter", "fit": "cover"}}
# presenter starts talking with vo1: layer placed so source time 0 == vo1 start
video["activeRange"] = {"start": ms(VOS["vo1"]), "duration": ms(e1 - VOS["vo1"])}
video["sourceRange"] = {"start": 0, "duration": ms(e1 - VOS["vo1"])}
segs = ",".join(f"[{st:.2f},{st + du:.2f}]" for _, st, du in VO)
duck = ("var t=input.time.seconds; var hi=0.5, lo=0.12, r=0.3; var v=hi; var S=[" + segs + "];"
        "for(var i=0;i<S.length;i++){var a=S[i][0]-r, b=S[i][1]+r; if(t>=a&&t<=b){var k=Math.min(1,(t-a)/r,(b-t)/r); v=Math.min(v,hi+(lo-hi)*Math.max(0,k));}}"
        f" if(t>{TOTAL - 3}) v=v*Math.max(0,({TOTAL}-t)/3); return v;")
json.dump({"media": media, "video": video, "anchor_group": ANCHOR_GROUP, "background": bg,
           "audio_actions": [{"type": "setFxPropertyAnimator", "compositionId": "main", "property": {"layerId": music, "propertyType": "volume"},
                              "dependencies": [], "animator": {"type": "jsScript", "layerTimeJsCode": duck}}]},
          open(".tesseract-work/media.json", "w"), indent=1)
print(f"{len(A)} actions · {len(CAPS)} captions · total {TOTAL}s")
for c_ in CAPS: print(" ", c_)
