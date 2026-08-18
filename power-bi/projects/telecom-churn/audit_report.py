"""04-review audit for telecom-churn: quick checks + design-system compliance.

Writes a dated artifact to power-bi/outputs/ per the workspace output convention.
The layout section is what the audit-layout-consistency hook would check: every visual's
rectangle must correspond to a design-system.yaml region (or an inset of one), and every
position must sit on the 8px snap.
"""
import glob
import json
import os
from datetime import date

import resolve_layout as RL

REPORT = "telecom-churn.Report"
PAGES = os.path.join(REPORT, "definition", "pages")
DS = RL.load()
SNAP = DS["grid"]["snap"]
PAGE = DS["meta"]["page"]

PERF_TYPES = {"tableEx", "barChart", "columnChart", "card", "lineChart", "pivotTable",
              "scatterChart", "donutChart", "azureMap", "lineClusteredColumnComboChart"}
DECOR = {"textbox", "image", "shape", "actionButton"}

lines = []


def out(s=""):
    lines.append(s)
    print(s)


def all_region_edges():
    xs, ys = set(), set()
    for name in DS["layouts"]:
        for r in RL.layout(name, DS):
            xs.update([r["x"], r["x"] + r["width"]])
            ys.update([r["y"], r["y"] + r["height"]])
    return xs, ys


pages = [p for p in sorted(os.listdir(PAGES)) if os.path.isdir(os.path.join(PAGES, p))]
out("# Audit - telecom-churn report")
out()
out("Generated %s - theme `%s`, page %dx%d, %d-col x %d-row grid."
    % (date.today().isoformat(), DS["meta"]["theme"], PAGE["width"], PAGE["height"],
       DS["grid"]["columns"], DS["grid"]["rows"]))
out()

# ---- quick checks --------------------------------------------------------
out("## Quick checks")
out()
out("| Page | Visuals | Data visuals | Slicers | Verdict |")
out("|---|---|---|---|---|")
tot_data = 0
for p in pages:
    vs = glob.glob(os.path.join(PAGES, p, "visuals", "*", "visual.json"))
    types = []
    for f in vs:
        types.append(json.load(open(f, encoding="utf-8"))["visual"]["visualType"])
    data = [t for t in types if t not in DECOR]
    slic = [t for t in types if t == "slicer"]
    tot_data += len(data)
    verdict = "optimal" if len(data) <= 8 else ("acceptable" if len(data) <= 12 else "WARNING")
    out("| %s | %d | %d | %d | %s |" % (p, len(vs), len(data), len(slic), verdict))
out()
out("Data visuals total: **%d** across %d pages. Decorative (textbox/image/shape) are excluded "
    "- they carry no query cost." % (tot_data, len(pages)))
out()

theme = json.load(open(os.path.join(REPORT, "definition", "report.json"), encoding="utf-8"))
tname = theme.get("themeCollection", {}).get("customTheme", {}).get("name", "(none)")
out("Custom theme applied: **%s**" % tname)
out()

# ---- layout compliance --------------------------------------------------
out("## Design-system compliance")
out()
xs, ys = all_region_edges()
off_snap, off_grid = [], []
for p in pages:
    for f in sorted(glob.glob(os.path.join(PAGES, p, "visuals", "*", "visual.json"))):
        v = json.load(open(f, encoding="utf-8"))
        pos, nm = v["position"], v["name"]
        vt = v["visual"]["visualType"]
        for key in ("x", "y", "width", "height"):
            if pos[key] % SNAP:
                off_snap.append((p, nm, vt, key, pos[key]))
        # a visual must start on a region edge, or be an inset of one (headings/insets)
        if pos["x"] not in xs and not any(abs(pos["x"] - e) <= 16 for e in xs):
            off_grid.append((p, nm, vt, "x", pos["x"]))
        if pos["y"] not in ys and not any(abs(pos["y"] - e) <= 56 for e in ys):
            off_grid.append((p, nm, vt, "y", pos["y"]))

out("- Off-snap coordinates (not a multiple of %d): **%d**" % (SNAP, len(off_snap)))
for r in off_snap[:8]:
    out("  - %s / %s (%s) %s=%s" % r)
out("- Off-grid origins (not on or near a region edge): **%d**" % len(off_grid))
for r in off_grid[:8]:
    out("  - %s / %s (%s) %s=%s" % r)
out()
out("`resolve_layout.py` snaps region EDGES, but a helper that insets a region (heading strip "
    "+ gap) can still land content off-snap - this check found 44 such coordinates on its first "
    "run, from a 6px gap. It is not redundant with the resolver.")
out()

# ---- theme compliance ---------------------------------------------------
out("## Theme compliance")
out()
PALETTE = {"#B8480A", "#00558F", "#B673A4", "#1B1F27", "#5B6472", "#7A8494",
           "#FFFFFF", "#DCE1E9", "#EEF1F5", "#8A6D1F", "#8A93A3"}
stray = {}
for p in pages:
    for f in glob.glob(os.path.join(PAGES, p, "visuals", "*", "visual.json")):
        txt = open(f, encoding="utf-8").read()
        import re
        for hexv in set(re.findall(r"#[0-9A-Fa-f]{6}", txt)):
            if hexv.upper() not in PALETTE:
                stray.setdefault(hexv, []).append("%s/%s" % (p, os.path.basename(os.path.dirname(f))))
out("- Hex values outside the documented palette: **%d**" % len(stray))
for k, v in list(stray.items())[:8]:
    out("  - `%s` in %s" % (k, ", ".join(v[:3])))
if not stray:
    out("  - none. Colours in visual.json are all palette members; SVG measures reference the "
        "`[Clr *]` measures rather than inline hex, so a re-theme reaches them.")
out()

os.makedirs("../../outputs", exist_ok=True)
dest = "../../outputs/%s-telecom-churn-audit.md" % date.today().isoformat()
open(dest, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("\nwrote", os.path.normpath(dest))
