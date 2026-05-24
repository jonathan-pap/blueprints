"""Wipe ALL report pages and rebuild a comprehensive 'all native visuals' gallery.

Strategy: harvest one known-good instance of each native visualType already present in the
report (preferring the Demo-* pages for clean bindings), then re-lay them into fresh
no-overlap gallery pages grouped by family. Reusing existing visual bodies keeps every
role binding valid — only `name` + `position` change.

DESTRUCTIVE: deletes every existing page (incl. the recipe test pages — rebuild those by
re-running _build-pareto.py / _build-pareto-model.py / _build-avt.py). Model is untouched.

Run from projects/test/ with Power BI Desktop CLOSED, then reopen.
"""
import json
import math
import shutil
import uuid
import pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "test.Report" / "definition" / "pages"

PAGE_W, PAGE_H = 1280, 720
M, G, TITLE_H, TOP = 16, 12, 40, 16

SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json"
SCHEMA_VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"

# gallery: (page title, columns, [visualType, ...])
GALLERY = [
    ("Native · Column & Bar", 3,
     ["columnChart", "clusteredColumnChart", "hundredPercentStackedColumnChart",
      "barChart", "clusteredBarChart", "hundredPercentStackedBarChart"]),
    ("Native · Line, Area & Combo", 4,
     ["lineChart", "areaChart", "stackedAreaChart", "hundredPercentStackedAreaChart",
      "ribbonChart", "lineClusteredColumnComboChart", "lineStackedColumnComboChart"]),
    ("Native · Part-to-Whole & Flow", 3,
     ["pieChart", "donutChart", "treemap", "funnel", "waterfallChart", "scatterChart"]),
    ("Native · Cards, KPI & Gauge", 3,
     ["card", "cardVisual", "multiRowCard", "kpi", "gauge"]),
    ("Native · Tables & Slicers", 3,
     ["tableEx", "pivotTable", "slicer", "listSlicer", "advancedSlicerVisual"]),
    ("Native · Report Elements", 2,
     ["textbox", "shape", "actionButton", "bookmarkNavigator"]),
]


def vid20():
    return uuid.uuid4().hex[:20]


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


# ── 1. harvest one source body per visualType (prefer Demo-* pages) ───────────
sources = {}
for vf in PAGES.glob("*/visuals/*/visual.json"):
    try:
        d = json.loads(vf.read_text(encoding="utf-8"))
    except Exception:
        continue
    vt = d.get("visual", {}).get("visualType")
    if not vt:
        continue
    prefer = "Demo-" in str(vf)
    # keep the first; replace only if the new one is from a Demo- page and the held one isn't
    if vt not in sources or (prefer and not sources[vt][1]):
        sources[vt] = (d, prefer)

print(f"harvested {len(sources)} distinct visualTypes")

# ── 2. snapshot the old page list, then build new pages ───────────────────────
old_pages = [p for p in PAGES.iterdir() if p.is_dir()]


def grid(n, cols):
    rows = math.ceil(n / cols)
    content_top = TOP + TITLE_H + 12
    content_h = PAGE_H - content_top - M
    tw = (PAGE_W - 2 * M - (cols - 1) * G) / cols
    th = (content_h - (rows - 1) * G) / rows
    out = []
    for i in range(n):
        r, c = divmod(i, cols)
        out.append((M + c * (tw + G), content_top + r * (th + G), tw, th))
    return out


def title_visual(text):
    name = vid20()
    return name, {
        "$schema": SCHEMA_VC, "name": name,
        "position": {"x": M, "y": TOP, "width": PAGE_W - 2 * M, "height": TITLE_H, "z": 0},
        "visual": {"visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [
                {"value": text, "textStyle": {"fontSize": "18pt"}}]}]}}]},
            "visualContainerObjects": {k: [{"properties": {"show": lit("false")}}]
                                       for k in ("title", "background", "border")},
            "drillFilterOtherVisuals": True}}


built_pages = []
for pi, (title, cols, types) in enumerate(GALLERY):
    present = [t for t in types if t in sources]
    missing = [t for t in types if t not in sources]
    if missing:
        print(f"  [{title}] skipped (not in report): {missing}")
    page_id = vid20()
    pdir = PAGES / page_id
    (pdir / "visuals").mkdir(parents=True, exist_ok=True)

    # title
    tname, tvis = title_visual(title)
    (pdir / "visuals" / tname).mkdir(parents=True, exist_ok=True)
    (pdir / "visuals" / tname / "visual.json").write_text(json.dumps(tvis, indent=2), encoding="utf-8")

    # tiles
    slots = grid(len(present), cols)
    for t, (x, y, w, h) in zip(present, slots):
        body = json.loads(json.dumps(sources[t][0]))   # deep copy
        name = vid20()
        body["name"] = name
        body.pop("parentGroupName", None)
        body["position"] = {"x": round(x, 2), "y": round(y, 2), "z": 0,
                            "width": round(w, 2), "height": round(h, 2), "tabOrder": 0}
        # label each tile with its visualType via the container title
        vco = body["visual"].setdefault("visualContainerObjects", {})
        vco["title"] = [{"properties": {"show": lit("true"), "text": lit(f"'{t}'"),
                                        "fontSize": lit("9D")}}]
        (pdir / "visuals" / name).mkdir(parents=True, exist_ok=True)
        (pdir / "visuals" / name / "visual.json").write_text(json.dumps(body, indent=2), encoding="utf-8")

    page = {"$schema": SCHEMA_PAGE, "name": page_id, "displayName": title,
            "width": PAGE_W, "height": PAGE_H, "displayOption": "FitToPage"}
    (pdir / "page.json").write_text(json.dumps(page, indent=2), encoding="utf-8")
    built_pages.append(page_id)
    print(f"  built '{title}': {len(present)} visuals")

# ── 3. delete the old pages ───────────────────────────────────────────────────
for p in old_pages:
    shutil.rmtree(p)
print(f"deleted {len(old_pages)} old pages")

# ── 4. rewrite pages.json ─────────────────────────────────────────────────────
(PAGES / "pages.json").write_text(json.dumps(
    {"$schema": SCHEMA_PAGES, "pageOrder": built_pages, "activePageName": built_pages[0]},
    indent=2), encoding="utf-8")
print(f"pages.json -> {len(built_pages)} gallery pages")
