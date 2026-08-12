"""Add the SVG micro-chart gallery to the test report (appends to the native gallery).

1. Splices the SVG measures from _svg-measures.fragment into _Measures.tmdl (idempotent,
   CRLF-preserving) — re-run safely if Power BI Desktop clobbers the model on save.
2. Builds two SVG showcase pages (tableEx with dataCategory=ImageUrl measures):
     - 'SVG · per-product micro-charts'  (Product rows: bullet, lollipop, overlapping,
        dumbbell, ibcs, status pill / progress, target bar, discount, sparkline, heatmap)
     - 'SVG · distribution (per segment)' (Segment rows: boxplot, jitter)

Run from projects/test/ with Power BI Desktop CLOSED, then reopen.
"""
import json
import shutil
import pathlib

ROOT = pathlib.Path(__file__).parent
SM = ROOT / "test.SemanticModel" / "definition" / "tables" / "_Measures.tmdl"
FRAG = ROOT / "_svg-measures.fragment"
PAGES = ROOT / "test.Report" / "definition" / "pages"

PG1 = "f59408ed7db1478596ad"
PG2 = "417008f5e69249979f16"
SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json"
VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"

# ── 1. splice measures (idempotent, preserve newline) ─────────────────────────
raw = SM.read_bytes().decode("utf-8")
if "'Product Target'" in raw:
    print("SVG measures already present — skipping splice")
else:
    nl = "\r\n" if "\r\n" in raw else "\n"
    frag = FRAG.read_text(encoding="utf-8").replace("\r\n", "\n")
    frag = frag.replace("\n", nl)
    lines = raw.splitlines(keepends=True)
    idx = next(i for i, ln in enumerate(lines) if ln.strip() == "column _")
    lines.insert(idx, frag if frag.endswith(nl) else frag + nl)
    SM.write_bytes("".join(lines).encode("utf-8"))
    print(f"spliced SVG measures before 'column _' (newline={nl!r})")

import uuid


def vid():
    return uuid.uuid4().hex[:20]


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def col(entity, prop, measure=False):
    kind = "Measure" if measure else "Column"
    return {"field": {kind: {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
            "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}


def title(page_dir, text):
    name = vid()
    (page_dir / "visuals" / name).mkdir(parents=True, exist_ok=True)
    (page_dir / "visuals" / name / "visual.json").write_text(json.dumps({
        "$schema": VC, "name": name,
        "position": {"x": 16, "y": 16, "width": 1248, "height": 40, "z": 0},
        "visual": {"visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [
                {"value": text, "textStyle": {"fontSize": "18pt"}}]}]}}]},
            "visualContainerObjects": {k: [{"properties": {"show": lit("false")}}]
                                       for k in ("title", "background", "border")},
            "drillFilterOtherVisuals": True}}, indent=2), encoding="utf-8")


def table(page_dir, pos, cols, ih, iw, tt):
    name = vid()
    (page_dir / "visuals" / name).mkdir(parents=True, exist_ok=True)
    (page_dir / "visuals" / name / "visual.json").write_text(json.dumps({
        "$schema": VC, "name": name, "position": pos,
        "visual": {"visualType": "tableEx",
            "query": {"queryState": {"Values": {"projections": cols}}},
            "objects": {"grid": [{"properties": {"imageHeight": lit(f"{ih}D"), "imageWidth": lit(f"{iw}D")}}]},
            "visualContainerObjects": {"title": [{"properties": {
                "show": lit("true"), "text": lit(f"'{tt}'"), "fontSize": lit("10D")}}]},
            "drillFilterOtherVisuals": True}}, indent=2), encoding="utf-8")


def fresh(page_id):
    d = PAGES / page_id
    if d.exists():
        shutil.rmtree(d)
    (d / "visuals").mkdir(parents=True, exist_ok=True)
    return d


M = "_Measures"
F = "financials"

# ── Page 1: per-product micro-charts (two tables) ─────────────────────────────
p1 = fresh(PG1)
title(p1, "SVG · per-product micro-charts (DAX-measure SVG in table cells)")
# comparison family (Total Sales vs Product Target)
table(p1, {"x": 16, "y": 64, "width": 1248, "height": 300, "z": 0, "tabOrder": 0},
      [col(F, "Product"), col(M, "Total Sales", True),
       col(M, "Sales Bullet SVG", True), col(M, "Sales Lollipop SVG", True),
       col(M, "Sales Overlapping Bars SVG", True), col(M, "Sales Dumbbell SVG", True),
       col(M, "Sales IBCS Bar SVG", True), col(M, "Profit Pill SVG", True)],
      ih=28, iw=110, tt="vs target / prior-year")
# single-value family
table(p1, {"x": 16, "y": 372, "width": 1248, "height": 316, "z": 0, "tabOrder": 1},
      [col(F, "Product"), col(M, "Profit % SVG", True), col(M, "Profit Target Bar SVG", True),
       col(M, "Discount % SVG", True), col(M, "Sales Sparkline SVG", True), col(M, "Heatmap SVG", True)],
      ih=34, iw=150, tt="single-value / trend")
(p1 / "page.json").write_text(json.dumps({"$schema": SCHEMA_PAGE, "name": PG1,
    "displayName": "SVG · per-product micro-charts", "width": 1280, "height": 720,
    "displayOption": "FitToPage"}, indent=2), encoding="utf-8")

# ── Page 2: distribution (per segment) ────────────────────────────────────────
p2 = fresh(PG2)
title(p2, "SVG · distribution per segment (boxplot + jitter across products)")
table(p2, {"x": 16, "y": 64, "width": 760, "height": 360, "z": 0, "tabOrder": 0},
      [col(F, "Segment"), col(M, "Total Sales", True),
       col(M, "Sales Boxplot SVG", True), col(M, "Sales Jitter SVG", True)],
      ih=30, iw=120, tt="distribution of product Total Sales within each segment")
(p2 / "page.json").write_text(json.dumps({"$schema": SCHEMA_PAGE, "name": PG2,
    "displayName": "SVG · distribution (per segment)", "width": 1280, "height": 720,
    "displayOption": "FitToPage"}, indent=2), encoding="utf-8")

# ── register pages (append, dedup) ────────────────────────────────────────────
pj = PAGES / "pages.json"
meta = json.loads(pj.read_text(encoding="utf-8"))
meta["$schema"] = SCHEMA_PAGES   # pin to 1.0.0 (offline CLI lacks Desktop's 1.1.0 schema)
for pid in (PG1, PG2):
    if pid not in meta["pageOrder"]:
        meta["pageOrder"].append(pid)
meta["activePageName"] = PG1
pj.write_text(json.dumps(meta, indent=2), encoding="utf-8")
print(f"built SVG pages; report now has {len(meta['pageOrder'])} pages")
