"""Build the AvT-Variance-Test page — the actual-vs-target-variance recipe.

Battle-tests recipes/actual-vs-target-variance on the test model:
  actual = _Measures[Total Sales]   target = _Measures[Sales Target] (synthetic, flat budget)
  axis   = financials[Month Name]   (sorted by Month Number)
Page filtered to Year = 2014 so all 12 months show and the narrative pins to one year.

Requires the AvT measures in _Measures.tmdl, the MonthKey column on financials,
compatibilityLevel 1601, and Month Name sortByColumn. Run from projects/test/ with
Power BI Desktop CLOSED, then reopen.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "test.Report" / "definition" / "pages"
RECIPE_TEMPLATE = (
    ROOT.parent.parent
    / "02-build" / "recipes" / "actual-vs-target-variance"
    / "templates" / "actual-vs-target.visual.json"
)

PAGE = "4e8c34e9d7f146459626"
TITLE = "3bb6160412e54a26"
CHART = "19a72d6971894c0b89ec"

TOK = {
    "<VISUAL_NAME_CHART>": CHART,
    "<CHART_X>": "24", "<CHART_Y>": "96", "<CHART_Z>": "0",
    "<CHART_HEIGHT>": "560", "<CHART_WIDTH>": "1232", "<CHART_TAB_ORDER>": "0",
    "<AXIS_TABLE>": "financials", "<AXIS_COLUMN>": "Month Name",
    "<MEASURE_TABLE>": "_Measures", "<ACTUAL_MEASURE>": "Total Sales",
    "<TARGET_MEASURE>": "Sales Target",
    "<POS_COLOR>": "#1B7F4A", "<NEG_COLOR>": "#B00020",
}

VC7 = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"


def w(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


# ── page (filtered to Year = 2014) ─────────────────────────────────────────────
page_filter = {"filters": [{
    "name": "filter_year_2014", "type": "Categorical",
    "field": {"Column": {"Expression": {"SourceRef": {"Entity": "financials"}}, "Property": "Year"}},
    "filter": {"Version": 2, "From": [{"Name": "f", "Entity": "financials", "Type": 0}],
               "Where": [{"Condition": {"In": {
                   "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "Year"}}],
                   "Values": [[{"Literal": {"Value": "2014L"}}]]}}}]},
    "howCreated": "User"}]}

page = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
    "name": PAGE, "displayName": "AvT-Variance-Test",
    "width": 1280, "height": 720, "displayOption": "FitToPage",
    "filterConfig": page_filter,
}
w(PAGES / PAGE / "page.json", page)

# ── title ──────────────────────────────────────────────────────────────────────
w(PAGES / PAGE / "visuals" / TITLE / "visual.json", {
    "$schema": VC7, "name": TITLE,
    "position": {"x": 24, "y": 24, "width": 1232, "height": 56, "z": 0},
    "visual": {"visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [
            {"value": "AvT-Variance-Test  —  error bars as directional variance connectors (green=beat, red=miss)",
             "textStyle": {"fontSize": "18pt"}}]}]}}]},
        "visualContainerObjects": {k: [{"properties": {"show": lit("false")}}] for k in ("title", "background", "border")},
        "drillFilterOtherVisuals": True}})

# ── variance chart: recipe template, token-substituted ────────────────────────
raw = RECIPE_TEMPLATE.read_text(encoding="utf-8")
for k, v in TOK.items():
    raw = raw.replace(k, v)
leftover = [t for t in TOK if t in raw]
assert not leftover, f"unsubstituted tokens: {leftover}"
chart = json.loads(raw)
w(PAGES / PAGE / "visuals" / CHART / "visual.json", chart)

# ── register the page ──────────────────────────────────────────────────────────
pj = PAGES / "pages.json"
meta = json.loads(pj.read_text(encoding="utf-8"))
if PAGE not in meta["pageOrder"]:
    meta["pageOrder"].append(PAGE)
meta["activePageName"] = PAGE
pj.write_text(json.dumps(meta, indent=2), encoding="utf-8")

print(f"Built AvT-Variance-Test page {PAGE}:")
print("  title", TITLE)
print("  chart", CHART, "(financials[Month Name] x Total Sales vs Sales Target)")
print("  chart visualType:", chart["visual"]["visualType"])
print("  Y series:", [p["field"]["Measure"]["Property"] for p in chart["visual"]["query"]["queryState"]["Y"]["projections"]])
