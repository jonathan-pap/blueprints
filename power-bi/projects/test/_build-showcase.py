"""Build the Recipe-Showcase page: all 4 disconnected-selection-emphasis variants in a 2x2 grid.
TL time-window · TR numeric band · BL comparison period · BR category spotlight.
"""
import json, os

PAGE = "ee2fb4ec20df418f8422"
DIR = f"test.Report/definition/pages/{PAGE}"
SVIS = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json"

def lit(v): return {"expr": {"Literal": {"Value": v}}}
def litb(v): return lit("true" if v else "false")

def wr(name, data):
    p = f"{DIR}/visuals/{name}/visual.json"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)

def col(entity, prop): return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
def mea(prop): return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": prop}}
def pos(x, y, w, h, z=0, tab=0): return {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": tab}

def title_obj(text, show=True):
    return {"title": [{"properties": {"show": litb(show), "text": lit(f"'{text}'")}}]}

# ---------- slicers ----------
def slicer_base(name, entity, prop, p, title):
    return {
        "$schema": SVIS, "name": name, "position": p,
        "visual": {
            "visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [
                {"field": col(entity, prop), "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop, "active": True}]}}},
            "objects": {}, "visualContainerObjects": title_obj(title), "drillFilterOtherVisuals": True,
        },
    }

def date_slicer(name, entity, prop, p, start_disp, end_disp, start_flt, end_flt, flt, title):
    v = slicer_base(name, entity, prop, p, title)
    v["visual"]["objects"] = {
        "data": [{"properties": {"startDate": lit(start_disp), "endDate": lit(end_disp), "mode": lit("'Between'")}}],
        "general": [{"properties": {"filter": {"filter": {
            "Version": 2, "From": [{"Name": "d", "Entity": entity, "Type": 0}],
            "Where": [{"Condition": {"And": {
                "Left": {"Comparison": {"ComparisonKind": 2, "Left": col_src("d", prop), "Right": {"Literal": {"Value": start_flt}}}},
                "Right": {"Comparison": {"ComparisonKind": 3, "Left": col_src("d", prop), "Right": {"Literal": {"Value": end_flt}}}}}}}]}}}}],
        "header": [{"properties": {"show": litb(False)}}],
        "date": [{"properties": {"textSize": lit("9D")}}],
    }
    v["filterConfig"] = {"filters": [{"name": flt, "field": col(entity, prop), "type": "Categorical"}]}
    return v

def col_src(src, prop): return {"Column": {"Expression": {"SourceRef": {"Source": src}}, "Property": prop}}

def numeric_slicer(name, entity, prop, p, lo, hi, flt, title):
    v = slicer_base(name, entity, prop, p, title)
    v["visual"]["objects"] = {
        "data": [{"properties": {"mode": lit("'Between'")}}],
        "general": [{"properties": {"filter": {"filter": {
            "Version": 2, "From": [{"Name": "d", "Entity": entity, "Type": 0}],
            "Where": [{"Condition": {"And": {
                "Left": {"Comparison": {"ComparisonKind": 2, "Left": col_src("d", prop), "Right": {"Literal": {"Value": f"{lo}L"}}}},
                "Right": {"Comparison": {"ComparisonKind": 3, "Left": col_src("d", prop), "Right": {"Literal": {"Value": f"{hi}L"}}}}}}}]}}}}],
        "header": [{"properties": {"show": litb(False)}}],
    }
    v["filterConfig"] = {"filters": [{"name": flt, "field": col(entity, prop), "type": "Categorical"}]}
    return v

def list_slicer(name, entity, prop, p, values, single, flt, title, str_vals=True):
    v = slicer_base(name, entity, prop, p, title)
    lits = [[{"Literal": {"Value": (f"'{x}'" if str_vals else f"{x}L")}}] for x in values]
    v["visual"]["objects"] = {
        "selection": [{"properties": {"singleSelect": litb(single)}}],
        "general": [{"properties": {"filter": {"filter": {
            "Version": 2, "From": [{"Name": "d", "Entity": entity, "Type": 0}],
            "Where": [{"Condition": {"In": {"Expressions": [col_src("d", prop)], "Values": lits}}}]}}}}],
        "header": [{"properties": {"show": litb(False)}}],
    }
    v["filterConfig"] = {"filters": [{"name": flt, "field": col(entity, prop), "type": "Categorical"}]}
    return v

# ---------- charts ----------
def ref_line(line_id, name_label, value_expr, transp, shade_page=False):
    props = {
        "show": litb(True), "displayName": lit(f"'{name_label}'"),
        "value": value_expr,
        "shadeShow": litb(True), "shadeRegion": lit("'before'"), "position": lit("'back'"),
        "shadeTransparency": lit(f"{transp}D"), "width": lit("1D"),
    }
    if shade_page:
        props["shadeColor"] = {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": 0, "Percent": 0}}}}}
    return {"properties": props, "selector": {"id": line_id}}

def agg_value(entity, prop, fn):
    return {"expr": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}, "Function": fn}}}

def measure_value(prop):
    return {"expr": mea(prop)}

def band_line(name, axis_entity, axis_col, value_measure, calc_name, calc_expr, end_value, start_value, p, title, harvest_measures):
    return {
        "$schema": SVIS, "name": name, "position": p,
        "visual": {
            "visualType": "lineChart",
            "query": {"queryState": {
                "Category": {"projections": [{"field": col(axis_entity, axis_col), "queryRef": f"{axis_entity}.{axis_col}", "nativeQueryRef": axis_col, "active": True}]},
                "Tooltips": {"projections": [
                    {"field": mea(m), "queryRef": f"_Measures.{m}", "nativeQueryRef": m} for m in harvest_measures
                ]},
                "Y": {"projections": [
                    {"field": mea(value_measure), "queryRef": f"_Measures.{value_measure}", "nativeQueryRef": value_measure},
                    {"field": {"NativeVisualCalculation": {"Language": "dax", "Expression": calc_expr, "Name": calc_name}}, "queryRef": "select", "nativeQueryRef": calc_name},
                ]},
            }, "sortDefinition": {"sort": [{"field": col(axis_entity, axis_col), "direction": "Ascending"}], "isDefaultSort": True}},
            "objects": {
                "valueAxis": [{"properties": {"show": litb(False)}}],
                "xAxisReferenceLine": [
                    ref_line("1", "end", end_value, 85),
                    ref_line("2", "start", start_value, 0, shade_page=True),
                ],
                "lineStyles": [
                    {"properties": {"strokeShow": litb(False), "markerSize": lit("4D")}, "selector": {"metadata": "select"}},
                    {"properties": {"showMarker": litb(False)}, "selector": {"metadata": f"_Measures.{value_measure}"}},
                ],
                "labels": [
                    {"properties": {"show": litb(True), "fontSize": lit("8D")}},
                    {"properties": {"showSeries": litb(False)}, "selector": {"metadata": f"_Measures.{value_measure}"}},
                ],
                "categoryAxis": [{"properties": {"fontSize": lit("9D")}}],
                "legend": [{"properties": {"show": litb(False)}}],
            },
            "visualContainerObjects": title_obj(title),
            "drillFilterOtherVisuals": True,
        },
    }

def spotlight_bar(name, cat_entity, cat_col, value_measure, color_measure, p, title):
    return {
        "$schema": SVIS, "name": name, "position": p,
        "visual": {
            "visualType": "barChart",
            "query": {"queryState": {
                "Category": {"projections": [{"field": col(cat_entity, cat_col), "queryRef": f"{cat_entity}.{cat_col}", "nativeQueryRef": cat_col, "active": True}]},
                "Y": {"projections": [{"field": mea(value_measure), "queryRef": f"_Measures.{value_measure}", "nativeQueryRef": value_measure}]},
            }, "sortDefinition": {"sort": [{"field": mea(value_measure), "direction": "Descending"}], "isDefaultSort": True}},
            "objects": {
                "dataPoint": [{
                    "properties": {"fill": {"solid": {"color": {"expr": mea(color_measure)}}}},
                    "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}
                }],
                "categoryAxis": [{"properties": {"fontSize": lit("9D")}}],
                "valueAxis": [{"properties": {"show": litb(False)}}],
                "legend": [{"properties": {"show": litb(False)}}],
            },
            "visualContainerObjects": title_obj(title),
            "drillFilterOtherVisuals": True,
        },
    }

def textbox(name, runs, p):
    paras = [{"textRuns": [{"value": t, "textStyle": ({"fontWeight": "bold"} if b else {}) | {"fontSize": f"{s}pt"}}], "horizontalTextAlignment": "left"} for (t, s, b) in runs]
    return {"$schema": SVIS, "name": name, "position": p,
            "visual": {"visualType": "textbox", "query": {"queryState": {}},
                       "objects": {"general": [{"properties": {"paragraphs": paras}}]}, "drillFilterOtherVisuals": True}}

# ---------- layout ----------
QW, QH = 616, 318
TL, TR, BL, BR = (16, 56), (648, 56), (16, 386), (648, 386)
def quad(origin):
    x, y = origin
    return (x, y, QW, 48), (x, y + 52, QW, QH - 52)  # slicer rect, chart rect

# header
wr("f641bd20eec6496d96e6", textbox("f641bd20eec6496d96e6",
   [("Disconnected Selection Emphasis — all 4 variants", 16, True),
    ("each slicer is a disconnected table; selection drives emphasis, not filtering", 9, False)],
   pos(16, 8, 1248, 44)))

# V1 — time window (TL)
s, c = quad(TL)
wr("96a6685142d340eaa904", date_slicer("96a6685142d340eaa904", "financials Date Slicer", "Date",
   pos(*s, z=1, tab=1), "datetime'2014-01-01T01:00:00'", "datetime'2014-06-01T01:00:00'",
   "datetime'2014-01-01T00:00:00'", "datetime'2014-06-02T00:00:00'", "f1a", "1 · Time window"))
wr("8af2a5f079da40328dd9", band_line("8af2a5f079da40328dd9", "financials", "Date", "Total Sales",
   "Data Labels Window", "\r\nIF (\r\n    [Date] >= [Window Start Date]\r\n        && [Date] <= [Window End Date],\r\n    [Total Sales]\r\n)",
   agg_value("financials Date Slicer", "Date", 4), agg_value("financials Date Slicer", "Date", 3),
   pos(*c), "Total Sales — time window", ["Window Start Date", "Window End Date"]))

# V2 — numeric band (TR)
s, c = quad(TR)
wr("8558c614a50645e0abb3", numeric_slicer("8558c614a50645e0abb3", "Price Slicer", "Sale Price",
   pos(*s, z=1, tab=1), 20, 300, "f2a", "2 · Numeric band"))
wr("52d876bf1f3445cb9f95", band_line("52d876bf1f3445cb9f95", "financials", "Sale Price", "Total Sales",
   "Labels In Band", "\r\nIF (\r\n    [Sale Price] >= [Price Low]\r\n        && [Sale Price] <= [Price High],\r\n    [Total Sales]\r\n)",
   agg_value("Price Slicer", "Sale Price", 4), agg_value("Price Slicer", "Sale Price", 3),
   pos(*c), "Total Sales by Sale Price — band", ["Price Low", "Price High"]))

# V3 — comparison period (BL)
s, c = quad(BL)
wr("94a2391eae714b52b387", list_slicer("94a2391eae714b52b387", "Year Slicer", "Year",
   pos(*s, z=1, tab=1), [2014], True, "f3a", "3 · Comparison period", str_vals=False))
wr("24cea914dc9d4a90b56b", band_line("24cea914dc9d4a90b56b", "financials", "Date", "Total Sales",
   "Labels In Year", "\r\nIF (\r\n    [Date] >= [Year Start]\r\n        && [Date] <= [Year End],\r\n    [Total Sales]\r\n)",
   measure_value("Year End"), measure_value("Year Start"),
   pos(*c), "Total Sales — selected year shaded", ["Year Start", "Year End", "Selected Year"]))

# V4 — category spotlight (BR)
s, c = quad(BR)
wr("9092198a395748cb89ad", list_slicer("9092198a395748cb89ad", "Product Slicer", "Product",
   pos(*s, z=1, tab=1), ["Paseo", "VTT"], False, "f4a", "4 · Category spotlight", str_vals=True))
wr("29d11573e28f4042bdf4", spotlight_bar("29d11573e28f4042bdf4", "financials", "Product", "Total Sales",
   "Spotlight Color", pos(*c), "Total Sales by Product — spotlight"))

print("showcase page built: 1 header + 4 slicers + 4 charts")
