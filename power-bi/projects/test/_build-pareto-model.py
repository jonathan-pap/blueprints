"""Build the Pareto-Model-Test page — the model-measure Pareto variant.

Contrast with _build-pareto.py (the base recipe, pure visual calculations):
here the cumulative is a MODEL measure ([Cumulative %]), the green/red split and the
bar color are model measures too, and a CARD shows '# Products to 80%' — the number a
visual calc can't feed. Requires the 5 measures added to _Measures.tmdl.

  category = financials[Product]      value = _Measures[Total Sales]
  lines    = _Measures[Cumulative Green] / [Cumulative Red]   (secondary axis, 0-100%)
  bars     = colored by _Measures[Pareto Bar Color]
  card     = _Measures[# Products to 80%]
  slicer   = financials[Segment]      (normal/related -> ALLSELECTED keeps it responsive)

Idempotent. Run from projects/test/ with Power BI Desktop CLOSED, then reopen.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "test.Report" / "definition" / "pages"

PAGE = "67c5721b95aa4918a024"
TITLE = "52ab9b2a0f0c416b"
SLICER = "da5f91585d7a4329bfb7"
COMBO = "f597da10173e4576aee2"
CARD = "13636021f8704bd4a7e4"

VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json"
VC7 = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"


def w(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def measure(prop, entity="_Measures"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def y_proj(prop, entity="_Measures"):
    return {"field": measure(prop, entity), "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}


# ── page ───────────────────────────────────────────────────────────────────────
w(PAGES / PAGE / "page.json", {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
    "name": PAGE, "displayName": "Pareto-Model-Test",
    "width": 1280, "height": 720, "displayOption": "FitToPage",
})

# ── title ──────────────────────────────────────────────────────────────────────
w(PAGES / PAGE / "visuals" / TITLE / "visual.json", {
    "$schema": VC7, "name": TITLE,
    "position": {"x": 24, "y": 24, "width": 1232, "height": 56, "z": 0},
    "visual": {"visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [
            {"value": "Pareto-Model-Test  —  model-measure variant (cumulative is a real measure → also feeds the card)",
             "textStyle": {"fontSize": "18pt"}}]}]}}]},
        "visualContainerObjects": {k: [{"properties": {"show": lit("false")}}] for k in ("title", "background", "border")},
        "drillFilterOtherVisuals": True}})

# ── normal Segment slicer (proves ALLSELECTED stays responsive) ────────────────
w(PAGES / PAGE / "visuals" / SLICER / "visual.json", {
    "$schema": VC7, "name": SLICER,
    "position": {"x": 24, "y": 96, "width": 240, "height": 360, "z": 0, "tabOrder": 1},
    "visual": {"visualType": "listSlicer",
        "query": {"queryState": {"Values": {"projections": [
            {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "financials"}}, "Property": "Segment"}},
             "queryRef": "financials.Segment", "nativeQueryRef": "Segment"}]}}},
        "objects": {}, "drillFilterOtherVisuals": True,
        "visualContainerObjects": {"title": [{"properties": {
            "show": lit("true"), "text": lit("'Segment (normal slicer)'")}}]}}})

# ── '# Products to 80%' card (the visual-calc version can't do this) ───────────
w(PAGES / PAGE / "visuals" / CARD / "visual.json", {
    "$schema": VC7, "name": CARD,
    "position": {"x": 24, "y": 472, "width": 240, "height": 216, "z": 0, "tabOrder": 2},
    "visual": {"visualType": "card",
        "query": {"queryState": {"Values": {"projections": [y_proj("# Products to 80%")]}}},
        "visualContainerObjects": {"title": [{"properties": {
            "show": lit("true"), "text": lit("'Products = first 80% of sales'")}}]},
        "drillFilterOtherVisuals": True}})

# ── model-measure Pareto combo ─────────────────────────────────────────────────
w(PAGES / PAGE / "visuals" / COMBO / "visual.json", {
    "$schema": VC, "name": COMBO,
    "position": {"x": 288, "y": 96, "z": 0, "height": 592, "width": 968, "tabOrder": 0},
    "visual": {
        "visualType": "lineStackedColumnComboChart",
        "query": {
            "queryState": {
                "Category": {"projections": [
                    {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "financials"}}, "Property": "Product"}},
                     "queryRef": "financials.Product", "nativeQueryRef": "Product", "active": True}]},
                "Y": {"projections": [y_proj("Total Sales")]},
                "Y2": {"projections": [y_proj("Cumulative Green"), y_proj("Cumulative Red")]},
            },
            "sortDefinition": {"sort": [{"field": measure("Total Sales"), "direction": "Descending"}],
                               "isDefaultSort": True},
        },
        "objects": {
            "dataPoint": [
                # columns: colored per-bar by the model color measure (wildcard selector)
                {"properties": {"fill": {"solid": {"color": {"expr": measure("Pareto Bar Color")}}}},
                 "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}},
                # line series colors (override the wildcard for these two metadata series)
                {"properties": {"fill": {"solid": {"color": lit("'#1E9790'")}}},
                 "selector": {"metadata": "_Measures.Cumulative Green"}},
                {"properties": {"fill": {"solid": {"color": lit("'#ED4D55'")}}},
                 "selector": {"metadata": "_Measures.Cumulative Red"}},
            ],
            "lineStyles": [{"properties": {
                "showMarker": lit("true"), "markerShape": lit("'circle'"), "markerSize": lit("6D")}}],
            "labels": [{"properties": {"show": lit("true"), "fontSize": lit("9D")}}],
            "valueAxis": [{"properties": {
                "secStart": lit("0D"), "secEnd": lit("1D"),
                "secTitleText": lit("'Cumulative %'"), "alignZeros": lit("false")}}],
            "legend": [{"properties": {"show": lit("false")}}],
            "categoryAxis": [{"properties": {"innerPadding": lit("12L")}}],
        },
        "visualContainerObjects": {"title": [{"properties": {"show": lit("false")}}]},
        "drillFilterOtherVisuals": True,
    }})

# ── register the page ──────────────────────────────────────────────────────────
pj = PAGES / "pages.json"
meta = json.loads(pj.read_text(encoding="utf-8"))
if PAGE not in meta["pageOrder"]:
    meta["pageOrder"].append(PAGE)
meta["activePageName"] = PAGE
pj.write_text(json.dumps(meta, indent=2), encoding="utf-8")

print(f"Built Pareto-Model-Test page {PAGE}:")
for nm, vid in [("title", TITLE), ("slicer", SLICER), ("card", CARD), ("combo", COMBO)]:
    print(f"  {nm:7} {vid}")
