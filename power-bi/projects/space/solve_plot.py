"""Solve the scatter's plot rect in page units, self-calibrating off the ribbon.

The ribbon is a known object: its container rect is known in page units, and the SVG draws
its bands at known fractions of that rect. Measuring those bands in the screenshot therefore
gives the raw-px <-> page-unit mapping without needing to find the canvas edges. Node centres
then convert to page units, and inverting the pinned axis window gives the plot rect.
"""
import sys
from collections import defaultdict

from PIL import Image

PNG = sys.argv[1]

# what the ribbon visual is CURRENTLY set to
RIB = {"x": 125, "y": 173, "w": 1095, "h": 520}
# what the LIVE measure actually emits (NOT what is on disk - reload does not re-read it)
VB_W, VB_H = 1200, 430
BAND_Y = [61, 164, 266, 369]
BAND_X0, BAND_X1 = 89, 1111

X_START, X_END = -1.4, 17.4
Y_START, Y_END = -3.6, 0.6
PER_ROW = 17

CYAN, AMBER = (76, 201, 240), (242, 169, 59)
near = lambda c, t: all(abs(c[i] - t[i]) <= 38 for i in range(3))

im = Image.open(PNG).convert("RGB")
W, H = im.size
px = im.load()
lum = lambda c: c[0] + c[1] + c[2]

# ---- node centres, grouped into rows --------------------------------------
pts = [(X, Y) for Y in range(H) for X in range(0, W, 2)
       if near(px[X, Y], CYAN) or near(px[X, Y], AMBER)]
rows = defaultdict(list)
for X, Y in pts:
    rows[Y // 120].append((X, Y))
bands = [v for v in rows.values() if len(v) > 400]
bands.sort(key=lambda v: sum(y for _, y in v) / len(v))
row_y = [(min(y for _, y in v) + max(y for _, y in v)) / 2 for v in bands]
print("node row centres (raw px):", [round(v, 1) for v in row_y])

# columns of the widest row
widest = max(bands, key=lambda v: max(x for x, _ in v) - min(x for x, _ in v))
cy = (min(y for _, y in widest) + max(y for _, y in widest)) // 2
xs = [X for X in range(W) if near(px[X, cy], CYAN) or near(px[X, cy], AMBER)]
g = []
for X in xs:
    if g and X - g[-1][-1] <= 3:
        g[-1].append(X)
    else:
        g.append([X])
cols = [(q[0] + q[-1]) / 2 for q in g if len(q) > 10]
print("node cols on that row: n=%d  first=%.1f last=%.1f" % (len(cols), cols[0], cols[-1]))

# ---- ribbon bands, in raw px ---------------------------------------------
# vertical: thin horizontal features, counted only in the gaps between bubbles
cand = []
for Y in range(40, H - 40):
    n = sum(1 for X in range(int(cols[0]), int(cols[-1]), 3)
            if lum(px[X, Y]) > lum(px[X, Y - 9]) + 24 and lum(px[X, Y]) > lum(px[X, Y + 9]) + 24)
    cand.append((n, Y))
best = sorted(cand, reverse=True)[:60]
cl = []
for _, Y in sorted(best, key=lambda t: t[1]):
    if cl and Y - cl[-1][-1] <= 8:
        cl[-1].append(Y)
    else:
        cl.append([Y])
rib_y = [sum(c) / len(c) for c in cl if len(c) >= 2]
print("ribbon band ys (raw px):", [round(v, 1) for v in rib_y])

# ---- mapping, from the ribbon's known geometry ---------------------------
if len(rib_y) < 2:
    sys.exit("need two ribbon bands")
pa = RIB["y"] + BAND_Y[0] / VB_H * RIB["h"]
pb = RIB["y"] + BAND_Y[len(rib_y) - 1] / VB_H * RIB["h"]
scale = (rib_y[-1] - rib_y[0]) / (pb - pa)
oy = rib_y[0] - pa * scale
print("\nscale %.4f px/page-unit   page y=0 at raw %.1f" % (scale, oy))

# horizontal origin from the ribbon band's own ends
line_y = int(rib_y[0])
dots = [X for X in range(W)
        if lum(px[X, line_y]) > lum(px[X, line_y - 9]) + 22
        and lum(px[X, line_y]) > lum(px[X, line_y + 9]) + 22]
lo_raw, hi_raw = min(dots), max(dots)
page_x0 = RIB["x"] + BAND_X0 / VB_W * RIB["w"]
ox = lo_raw - page_x0 * scale
print("ribbon band starts raw %.1f -> page x %.1f ; page x=0 at raw %.1f" % (lo_raw, page_x0, ox))

to_px = lambda v, o: (v - o) / scale

# ---- solve the plot rect -------------------------------------------------
n = len(row_y)
f0 = (Y_END - 0) / (Y_END - Y_START)
f1 = (Y_END + (n - 1)) / (Y_END - Y_START)
py0, py1 = to_px(row_y[0], oy), to_px(row_y[-1], oy)
plot_h = (py1 - py0) / (f1 - f0)
plot_y = py0 - f0 * plot_h

g0 = (0 - X_START) / (X_END - X_START)
g1 = ((PER_ROW - 1) - X_START) / (X_END - X_START)
px0, px1 = to_px(cols[0], ox), to_px(cols[-1], ox)
plot_w = (px1 - px0) / (g1 - g0)
plot_x = px0 - g0 * plot_w

print("\nnode col0 page x=%.1f  col16 page x=%.1f" % (px0, px1))
print("node row0 page y=%.1f  row%d page y=%.1f" % (py0, n - 1, py1))
print("\n--- ribbon should be ---")
print('{"x": %d, "y": %d, "width": %d, "height": %d}'
      % (round(plot_x), round(plot_y), round(plot_w), round(plot_h)))
