"""Build the Pareto-Test page in the test report.

Battle-tests recipes/pareto-chart on the test model:
  category  = financials[Product]      (the bars)
  value     = _Measures[Total Sales]   (magnitude + cumulative)
Plus a NORMAL slicer on financials[Segment] to prove the Pareto re-ranks when filtered
(it binds to real, related fields — not a disconnected table).

Idempotent: rewrites the page folder and re-registers it in pages.json.
Run from projects/test/ with Power BI Desktop CLOSED, then reopen to view.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
REPORT = ROOT / "test.Report" / "definition"
PAGES = REPORT / "pages"
RECIPE_TEMPLATE = (
    ROOT.parent.parent
    / "02-build" / "recipes" / "pareto-chart" / "templates" / "pareto-combo.visual.json"
)

PAGE_ID = "dd17952c1a9747e0a957"
TITLE = "257125c057ac47cc"
SLICER = "249f039712ec4654894f"
PARETO = "b2507e3edf4947618f07"

# ── recipe tokens for the test model ──────────────────────────────────────────
TOK = {
    "<VISUAL_NAME_CHART>": PARETO,
    "<CHART_X>": "300", "<CHART_Y>": "96", "<CHART_Z>": "0",
    "<CHART_HEIGHT>": "592", "<CHART_WIDTH>": "956", "<CHART_TAB_ORDER>": "0",
    "<CATEGORY_TABLE>": "financials", "<CATEGORY_COLUMN>": "Product",
    "<MEASURE_TABLE>": "_Measures", "<VALUE_MEASURE>": "Total Sales",
    "<THRESHOLD>": "0.8",
    "<VITAL_COLOR>": "#1E9790", "<TRIVIAL_COLOR>": "#ED4D55",
    "<VITAL_LABEL_COLOR>": "#C1DEC1", "<TRIVIAL_LABEL_COLOR>": "#efb5b9",
}


def w(path: pathlib.Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


# ── page ──────────────────────────────────────────────────────────────────────
w(PAGES / PAGE_ID / "page.json", {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
    "name": PAGE_ID, "displayName": "Pareto-Test",
    "width": 1280, "height": 720, "displayOption": "FitToPage",
})

# ── title ─────────────────────────────────────────────────────────────────────
w(PAGES / PAGE_ID / "visuals" / TITLE / "visual.json", {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
    "name": TITLE,
    "position": {"x": 24, "y": 24, "width": 1232, "height": 56, "z": 0},
    "visual": {
        "visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [
            {"value": "Pareto-Test  —  Total Sales by Product (slice Segment → it re-ranks)",
             "textStyle": {"fontSize": "20pt"}}]}]}}]},
        "visualContainerObjects": {
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
        },
        "drillFilterOtherVisuals": True,
    },
})

# ── normal slicer on financials[Segment] (real column → it filters the Pareto) ─
w(PAGES / PAGE_ID / "visuals" / SLICER / "visual.json", {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
    "name": SLICER,
    "position": {"x": 24, "y": 96, "width": 260, "height": 592, "z": 0, "tabOrder": 1},
    "visual": {
        "visualType": "listSlicer",
        "query": {"queryState": {"Values": {"projections": [{
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "financials"}},
                                 "Property": "Segment"}},
            "queryRef": "financials.Segment", "nativeQueryRef": "Segment"}]}}},
        "objects": {},
        "drillFilterOtherVisuals": True,
        "visualContainerObjects": {"title": [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "text": {"expr": {"Literal": {"Value": "'Segment (normal slicer)'"}}}}}]},
    },
})

# ── Pareto combo: recipe template, token-substituted ─────────────────────────
raw = RECIPE_TEMPLATE.read_text(encoding="utf-8")
for k, v in TOK.items():
    raw = raw.replace(k, v)
leftover = [t for t in TOK if t in raw]
assert not leftover, f"unsubstituted tokens: {leftover}"
pareto = json.loads(raw)  # also validates the JSON
w(PAGES / PAGE_ID / "visuals" / PARETO / "visual.json", pareto)

# ── register the page ─────────────────────────────────────────────────────────
pj = PAGES / "pages.json"
meta = json.loads(pj.read_text(encoding="utf-8"))
if PAGE_ID not in meta["pageOrder"]:
    meta["pageOrder"].append(PAGE_ID)
meta["activePageName"] = PAGE_ID
pj.write_text(json.dumps(meta, indent=2), encoding="utf-8")

print(f"Built Pareto-Test page {PAGE_ID}:")
print("  title  ", TITLE)
print("  slicer ", SLICER, "(financials[Segment], normal/related)")
print("  pareto ", PARETO, "(financials[Product] x _Measures[Total Sales])")
print("  pareto visualType:", pareto["visual"]["visualType"])
