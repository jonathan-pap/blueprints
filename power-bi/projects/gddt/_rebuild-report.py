"""Full report rebuild for gddt.

Deletes all existing pages, then rebuilds the four numbered pages from scratch
with an explicit non-overlap layout. Every visual rectangle is tracked and
checked against every other visual on the same page before write.

Pages:
  1. 01-Summary    Where the data stands today (header, hero, KPIs, trend, breakdowns)
  2. 02-Groups     Per-group scorecard grid (5 cards, dimension bars per group)
  3. 03-Datasets   Dataset-level table
  4. 04-Scoring    Grading model + leaderboard

Palette (editorial):
  ink     #15171C   paper   #F7F5EF   rule   #D8D5CC   mute   #8F8E87
  good    #2D6948   warn    #B46C1A   bad    #A23A2A
"""
import json
import os
import shutil
import uuid

ROOT = "gddt.Report/definition/pages"
SCHEMA_PAGE   = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_VIS    = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"
SCHEMA_PAGES  = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json"

INK  = "#15171C"; PAPER = "#F7F5EF"; RULE = "#D8D5CC"; MUTE = "#8F8E87"
GOOD = "#2D6948"; WARN  = "#B46C1A"; BAD  = "#A23A2A"

PAGE_W = 1320
GUTTER = 40   # left/right page margin

# ---------- json primitives ----------
def lit(v): return {"expr": {"Literal": {"Value": v}}}
def lit_s(v): return lit(f"'{v}'")
def lit_b(v): return lit("true" if v else "false")
def lit_n(v): return lit(f"{v}D")

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)

# ---------- layout ----------
class Layout:
    def __init__(self, page_w, page_h, page_name):
        self.w = page_w; self.h = page_h; self.name = page_name
        self.placed = []

    def add(self, name, x, y, w, h):
        if x < 0 or y < 0 or x + w > self.w or y + h > self.h:
            raise ValueError(f"[{self.name}] {name} out of bounds: ({x},{y},{w},{h}) page {self.w}x{self.h}")
        for px, py, pw, ph, pname in self.placed:
            if x < px + pw and x + w > px and y < py + ph and y + h > py:
                raise ValueError(f"[{self.name}] {name} overlaps {pname}: "
                                 f"({x},{y},{w},{h}) vs ({px},{py},{pw},{ph})")
        self.placed.append((x, y, w, h, name))
        return x, y, w, h


# ---------- visual builders ----------
def vc_objects(*, title=False, bg=None, border=False, pad=(0, 0, 0, 0)):
    o = {
        "title": [{"properties": {"show": lit_b(title)}}],
        "border": [{"properties": {"show": lit_b(border)}}],
        "padding": [{"properties": {
            "top":    lit_n(pad[0]),
            "right":  lit_n(pad[1]),
            "bottom": lit_n(pad[2]),
            "left":   lit_n(pad[3]),
        }}],
    }
    if bg:
        o["background"] = [{"properties": {
            "show": lit_b(True),
            "color": {"solid": {"color": lit_s(bg)}},
        }}]
    else:
        o["background"] = [{"properties": {"show": lit_b(False)}}]
    return o


def textbox(name, text_runs, x, y, w, h, *, align="left", bg=None, border=False, pad=(8, 12, 8, 12), z=1):
    """text_runs = list of (value, font_size_pt, family, color, bold)"""
    runs = []
    for value, size, family, color, bold in text_runs:
        ts = {"fontSize": f"{size}pt", "fontFamily": family, "color": color}
        if bold:
            ts["fontWeight"] = "bold"
        runs.append({"value": value, "textStyle": ts})

    return {
        "path": f"{name}/visual.json",
        "data": {
            "name": name,
            "visual": {
                "visualType": "textbox",
                "query": {"queryState": {}},
                "objects": {"general": [{"properties": {"paragraphs": [
                    {"textRuns": runs, "horizontalTextAlignment": align}
                ]}}]},
                "drillFilterOtherVisuals": True,
                "visualContainerObjects": vc_objects(bg=bg, border=border, pad=pad),
            },
            "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
            "$schema": SCHEMA_VIS,
        },
    }


def shape(name, x, y, w, h, *, fill, z=0):
    """Filled rectangle. Use for dividers/bands."""
    return {
        "path": f"{name}/visual.json",
        "data": {
            "name": name,
            "visual": {
                "visualType": "basicShape",
                "query": {"queryState": {}},
                "objects": {
                    "shape": [{"properties": {"tileShape": lit_s("rectangle")}}],
                    "fill": [{"properties": {
                        "show": lit_b(True),
                        "fillColor": {"solid": {"color": lit_s(fill)}},
                        "transparency": lit_n(0),
                    }}],
                    "line": [{"properties": {"show": lit_b(False)}}],
                },
                "drillFilterOtherVisuals": True,
                "visualContainerObjects": vc_objects(),
            },
            "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
            "$schema": SCHEMA_VIS,
        },
    }


def measure_field(prop, entity="_Measures"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def column_field(prop, entity):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def group_filter(group_value):
    return {"filters": [{
        "name": f"Filter_group_{group_value.replace(' ', '_')}",
        "type": "Categorical",
        "field": column_field("group", "expected"),
        "filter": {
            "Version": 2,
            "From": [{"Name": "e", "Entity": "expected", "Type": 0}],
            "Where": [{"Condition": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "group"}}],
                "Values": [[{"Literal": {"Value": f"'{group_value}'"}}]],
            }}}],
        },
        "howCreated": "User",
    }]}


def card(name, measure, x, y, w, h, *,
         font=24, family="Georgia", color=INK, bold=True, align="left",
         bg=None, border=False, group_value=None, z=2, label=False):
    """Single-measure card visual."""
    label_props = {
        "fontSize": lit_n(font),
        "color": {"solid": {"color": lit_s(color)}},
        "fontFamily": lit_s(family),
        "bold": lit_b(bold),
        "horizontalAlignment": lit_s(align),
    }
    v = {
        "name": name,
        "visual": {
            "visualType": "card",
            "query": {"queryState": {"Values": {"projections": [{
                "queryRef": f"_Measures.{measure}",
                "field": measure_field(measure),
                "nativeQueryRef": measure,
            }]}}},
            "objects": {
                "labels": [{"properties": label_props}],
                "categoryLabels": [{"properties": {"show": lit_b(label)}}],
            },
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": vc_objects(bg=bg, border=border, pad=(4, 8, 4, 8)),
        },
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }
    if group_value:
        v["filterConfig"] = group_filter(group_value)
    return {"path": f"{name}/visual.json", "data": v}


def column_chart(name, *, category_field, value_fields, x, y, w, h,
                 visual_type="columnChart", title=False, bg=None, z=1,
                 fill_color=None, series_colors=None, show_labels=True):
    """Column chart. visual_type: 'columnChart' (clustered), 'stackedColumnChart',
    'clusteredColumnChart', 'hundredPercentStackedColumnChart'.
    fill_color: single color for all bars (overrides theme).
    series_colors: list aligned with value_fields — one color per measure (per-series selector).
    """
    projections_cat = [{
        "queryRef": f"{category_field[0]}.{category_field[1]}",
        "field": column_field(category_field[1], category_field[0]),
        "nativeQueryRef": category_field[1],
        "active": True,
    }]
    projections_val = []
    for ent, m in value_fields:
        projections_val.append({
            "queryRef": f"{ent}.{m}",
            "field": measure_field(m, ent),
            "nativeQueryRef": m,
        })

    objects = {
        "legend":       [{"properties": {
            "show": lit_b(len(value_fields) > 1),
            "position": lit_s("Bottom"),
            "fontSize": lit_n(9),
            "fontFamily": lit_s("Segoe UI"),
            "labelColor": {"solid": {"color": lit_s(MUTE)}},
        }}],
        "categoryAxis": [{"properties": {
            "fontSize": lit_n(9), "fontFamily": lit_s("Segoe UI"),
            "labelColor": {"solid": {"color": lit_s(MUTE)}},
        }}],
        "valueAxis":    [{"properties": {
            "fontSize": lit_n(9), "fontFamily": lit_s("Segoe UI"),
            "labelColor": {"solid": {"color": lit_s(MUTE)}},
            "gridlineColor": {"solid": {"color": lit_s(RULE)}},
        }}],
        "labels": [{"properties": {
            "show": lit_b(show_labels),
            "fontSize": lit_n(8),
            "fontFamily": lit_s("Consolas"),
            "color": {"solid": {"color": lit_s(INK)}},
        }}],
    }

    if series_colors:
        dp = []
        for (ent, m), color in zip(value_fields, series_colors):
            dp.append({
                "selector": {"metadata": f"{ent}.{m}"},
                "properties": {"fill": {"solid": {"color": lit_s(color)}}},
            })
        objects["dataPoint"] = dp
    elif fill_color:
        objects["dataPoint"] = [{"properties": {
            "fill": {"solid": {"color": lit_s(fill_color)}},
        }}]

    return {"path": f"{name}/visual.json", "data": {
        "name": name,
        "visual": {
            "visualType": visual_type,
            "query": {"queryState": {
                "Category": {"projections": projections_cat},
                "Y": {"projections": projections_val},
            }},
            "objects": objects,
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": vc_objects(title=title, bg=bg, border=False),
        },
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }}


def table_ex(name, *, fields, x, y, w, h, sort_by=None, sort_desc=True, group_value=None,
             column_headers=True, totals=False, z=1):
    """fields = list of dicts: {entity, prop, kind: 'col'|'measure'}"""
    projections = []
    for f in fields:
        if f["kind"] == "col":
            field_obj = column_field(f["prop"], f["entity"])
        else:
            field_obj = measure_field(f["prop"], f["entity"])
        projections.append({
            "queryRef": f"{f['entity']}.{f['prop']}",
            "field": field_obj,
            "nativeQueryRef": f["prop"],
        })

    qs = {"Values": {"projections": projections}}
    if sort_by:
        ent, prop, kind = sort_by
        field_obj = (column_field(prop, ent) if kind == "col" else measure_field(prop, ent))
        qs_sort = {
            "sort": [{"field": field_obj, "direction": "Descending" if sort_desc else "Ascending"}],
            "isDefaultSort": True,
        }
    else:
        qs_sort = None

    data = {
        "name": name,
        "visual": {
            "visualType": "tableEx",
            "query": {"queryState": qs},
            "objects": {
                "columnHeaders": [{"properties": {"show": lit_b(column_headers), "fontFamily": lit_s("Segoe UI"), "fontSize": lit_n(9), "fontColor": {"solid": {"color": lit_s(MUTE)}}}}],
                "values":        [{"properties": {"fontFamily": lit_s("Segoe UI"), "fontSize": lit_n(10), "fontColor": {"solid": {"color": lit_s(INK)}}}}],
                "total":         [{"properties": {"show": lit_b(totals)}}],
                "grid":          [{"properties": {"gridVertical": lit_b(False), "gridHorizontalColor": {"solid": {"color": lit_s(RULE)}}}}],
            },
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": vc_objects(bg=None, border=False, pad=(4, 8, 4, 8)),
        },
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }
    if qs_sort:
        data["visual"]["query"]["sortDefinition"] = qs_sort
    if group_value:
        data["filterConfig"] = group_filter(group_value)
    return {"path": f"{name}/visual.json", "data": data}


def matrix(name, *, row_fields, column_fields, value_fields,
           x, y, w, h, z=1,
           value_bg_measure=None, value_fg_measure=None,
           column_subtotals=False, row_subtotals=False, totals=False):
    """Matrix (pivotTable) with optional measure-bound cell background/foreground colors.
    *_fields = list of dicts: {entity, prop, kind: 'col'|'measure'}
    value_bg_measure / value_fg_measure = ('_Measures', 'Cell Color BG') etc.
    """
    def projections(fields):
        out = []
        for f in fields:
            if f["kind"] == "col":
                field_obj = column_field(f["prop"], f["entity"])
            else:
                field_obj = measure_field(f["prop"], f["entity"])
            out.append({
                "queryRef": f"{f['entity']}.{f['prop']}",
                "field": field_obj,
                "nativeQueryRef": f["prop"],
            })
        return out

    qs = {
        "Rows":    {"projections": projections(row_fields)},
        "Columns": {"projections": projections(column_fields)},
        "Values":  {"projections": projections(value_fields)},
    }

    value_props = {
        "fontFamily": lit_s("Segoe UI"),
        "fontSize":   lit_n(9),
        "fontColor":  {"solid": {"color": lit_s(INK)}},
    }
    if value_bg_measure is not None:
        ent, prop = value_bg_measure
        value_props["backColor"] = {"solid": {"color": {"expr": {
            "Measure": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}
        }}}}
    if value_fg_measure is not None:
        ent, prop = value_fg_measure
        value_props["fontColor"] = {"solid": {"color": {"expr": {
            "Measure": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": prop}
        }}}}

    objects = {
        "columnHeaders": [{"properties": {
            "fontFamily": lit_s("Consolas"), "fontSize": lit_n(9),
            "fontColor": {"solid": {"color": lit_s(MUTE)}},
        }}],
        "rowHeaders": [{"properties": {
            "fontFamily": lit_s("Segoe UI"), "fontSize": lit_n(10),
            "fontColor": {"solid": {"color": lit_s(INK)}},
        }}],
        "values": [{"properties": value_props}],
        "subTotals": [{"properties": {
            "columnSubtotals": lit_b(column_subtotals),
            "rowSubtotals":    lit_b(row_subtotals),
        }}],
        "total": [{"properties": {"show": lit_b(totals)}}],
        "grid": [{"properties": {
            "gridVerticalColor":   {"solid": {"color": lit_s(RULE)}},
            "gridHorizontalColor": {"solid": {"color": lit_s(RULE)}},
        }}],
    }

    return {"path": f"{name}/visual.json", "data": {
        "name": name,
        "visual": {
            "visualType": "pivotTable",
            "query": {"queryState": qs},
            "objects": objects,
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": vc_objects(bg=None, border=False, pad=(4, 8, 4, 8)),
        },
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }}


def year_slicer(name, x, y, w, h, *, z=1):
    """Slicer on dim_calendar[Year]."""
    return {"path": f"{name}/visual.json", "data": {
        "name": name,
        "visual": {
            "visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [{
                "queryRef": "dim_calendar.Year",
                "field": column_field("Year", "dim_calendar"),
                "nativeQueryRef": "Year",
            }]}}},
            "objects": {
                "general": [{"properties": {"orientation": lit_s("horizontal")}}],
                "items":   [{"properties": {"fontFamily": lit_s("Segoe UI"), "fontSize": lit_n(9)}}],
            },
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": vc_objects(bg=PAPER, border=False, pad=(4, 8, 4, 8)),
        },
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }}


# ---------- page-level helpers ----------
def write_page(page_dir, page_name, display_name, w, h, visuals):
    full_dir = os.path.join(ROOT, page_dir)
    os.makedirs(full_dir, exist_ok=True)
    write_json(os.path.join(full_dir, "page.json"), {
        "$schema": SCHEMA_PAGE,
        "name": page_name,
        "displayName": display_name,
        "width": w,
        "height": h,
        "displayOption": "FitToWidth",
    })
    vis_dir = os.path.join(full_dir, "visuals")
    os.makedirs(vis_dir, exist_ok=True)
    for v in visuals:
        write_json(os.path.join(vis_dir, v["path"]), v["data"])


def hash_name():
    return uuid.uuid4().hex[:20]


# ---------- header builder (shared) ----------
def build_header(layout, *, eyebrow, title, meta, with_year_slicer=True):
    """Build the editorial header band. Returns list of visuals.
    Layout consumed:  top 0..160
    """
    items = []
    cx = GUTTER
    cw = layout.w - 2 * GUTTER

    # eyebrow row (24px high)
    items.append(textbox("hdr-eyebrow",
        [(eyebrow, 9, "Consolas", MUTE, False)],
        *layout.add("hdr-eyebrow", cx, 24, cw, 22), pad=(0, 0, 0, 0)))

    # title row (44px high)
    items.append(textbox("hdr-title",
        [(title, 28, "Georgia", INK, True)],
        *layout.add("hdr-title", cx, 50, cw - 220, 50), pad=(0, 0, 0, 0)))

    # year slicer (right of title)
    if with_year_slicer:
        items.append(year_slicer("hdr-year",
            *layout.add("hdr-year", cx + cw - 200, 56, 200, 38)))

    # meta row (20px high)
    items.append(textbox("hdr-meta",
        [(meta, 9, "Consolas", MUTE, False)],
        *layout.add("hdr-meta", cx, 108, cw, 22), pad=(0, 0, 0, 0)))

    # divider rule
    items.append(shape("hdr-rule",
        *layout.add("hdr-rule", cx, 140, cw, 1), fill=RULE))

    return items


def build_footnote(layout, *, text, y):
    cx = GUTTER
    cw = layout.w - 2 * GUTTER
    items = [
        shape("footnote-rule", *layout.add("footnote-rule", cx, y, cw, 1), fill=RULE),
        textbox("footnote", [(text, 8, "Consolas", MUTE, False)],
                *layout.add("footnote", cx, y + 8, cw, 20), pad=(0, 0, 0, 0)),
    ]
    return items


# ---------- PAGE 1: SUMMARY ----------
def build_page_1_summary():
    h = 1500   # extended to fit Daily Flow section
    L = Layout(PAGE_W, h, "01-Summary")
    visuals = []

    visuals += build_header(L,
        eyebrow="GROUP DATA DELIVERY TRACKER  ·  2026",
        title="Where the data stands today",
        meta="As of 2026-05-19  ·  5 active groups  ·  deadline = 15th of the period month")

    # Section: HERO — big # Files Overdue with narrative. No score/grade.
    cx = GUTTER
    cw = PAGE_W - 2 * GUTTER
    band_y = 170
    visuals.append(textbox("hero-eyebrow",
        [("AS OF TODAY", 9, "Consolas", MUTE, False)],
        *L.add("hero-eyebrow", cx, band_y, cw, 18), pad=(0, 0, 0, 0)))

    visuals.append(card("hero-overdue", "# Files Overdue",
        *L.add("hero-overdue", cx, band_y + 24, 300, 100),
        font=64, family="Georgia", color=BAD, bold=True, align="left"))

    visuals.append(textbox("hero-narrative",
        [("files past their deadline and not yet delivered.", 14, "Georgia", INK, False),
         ("\n\n", 4, "Consolas", INK, False),
         ("Deadline is the 15th of each period's own month. Files arriving after the 15th count as late; files for periods that haven't started yet are pending.",
          11, "Georgia", MUTE, False)],
        *L.add("hero-narrative", cx + 320, band_y + 28, cw - 320, 90), pad=(0, 0, 0, 0)))

    # KPI band: 6 cards across, y = 340..470
    visuals.append(textbox("kpi-eyebrow",
        [("AT A GLANCE", 9, "Consolas", MUTE, False)],
        *L.add("kpi-eyebrow", cx, 340, cw, 18), pad=(0, 0, 0, 0)))

    kpi_y = 364
    kpi_h = 100
    kpis = [
        ("kpi-expected",  "# Expected",      "FILES EXPECTED"),
        ("kpi-delivered", "# Delivered",     "DELIVERED"),
        ("kpi-overdue",   "# Files Overdue", "OVERDUE"),
        ("kpi-ontime",    "# On Time",       "ON TIME"),
        ("kpi-gold",      "# Reached Gold",  "REACHED GOLD"),
        ("kpi-due",       "# Due By Today",  "DUE BY TODAY"),
    ]
    gap = 8
    kpi_w = (cw - gap * (len(kpis) - 1)) // len(kpis)
    for i, (name, measure, label) in enumerate(kpis):
        kx = cx + i * (kpi_w + gap)
        visuals.append(textbox(f"{name}-label",
            [(label, 8, "Consolas", MUTE, False)],
            *L.add(f"{name}-label", kx, kpi_y, kpi_w, 16), pad=(0, 0, 0, 0)))
        visuals.append(card(name, measure,
            *L.add(name, kx, kpi_y + 18, kpi_w, kpi_h - 18),
            font=28, family="Georgia", bold=True, align="left"))

    # Monthly trend: y = 490..760
    trend_top = 490
    visuals.append(textbox("trend-eyebrow",
        [("MONTHLY DELIVERY TREND", 9, "Consolas", MUTE, False)],
        *L.add("trend-eyebrow", cx, trend_top, cw, 18), pad=(0, 0, 0, 0)))
    visuals.append(shape("trend-rule",
        *L.add("trend-rule", cx, trend_top + 22, cw, 1), fill=RULE))
    # Stacked column: 5 delivery states per month, editorial palette.
    # Reached Gold (green) → DQ Found (warn) → Schema Failed (bad) → Overdue (pink) → Pending (paper-2 tan)
    visuals.append(column_chart("trend-chart",
        visual_type="columnChart",
        category_field=("dim_calendar", "MonthName"),
        value_fields=[
            ("_Measures", "# Reached Gold"),
            ("_Measures", "# Records Found in Inspection - Failed DQ"),
            ("_Measures", "# Schema Failed - Quarantine"),
            ("_Measures", "# Files Overdue"),
            ("_Measures", "# Files Pending"),
        ],
        series_colors=[GOOD, WARN, BAD, "#E8C0B5", "#EBE8DF"],
        x=cx, y=trend_top + 32,
        w=cw, h=230,
        show_labels=True,
    ))
    L.add("trend-chart", cx, trend_top + 32, cw, 230)

    # Daily Flow section — receipts per day. y = 790..1060
    daily_top = 790
    visuals.append(textbox("daily-eyebrow",
        [("DAILY DELIVERY FLOW", 9, "Consolas", MUTE, False)],
        *L.add("daily-eyebrow", cx, daily_top, cw - 360, 18), pad=(0, 0, 0, 0)))
    visuals.append(textbox("daily-window",
        [("WINDOW: 1ST → 15TH OF EACH PERIOD", 9, "Consolas", MUTE, False)],
        *L.add("daily-window", cx + cw - 340, daily_top, 340, 18), pad=(0, 0, 0, 0), align="right"))
    visuals.append(shape("daily-rule",
        *L.add("daily-rule", cx, daily_top + 22, cw, 1), fill=RULE))

    # Small KPI band — current Day-of cardinal markers
    k_y = daily_top + 36
    k_h = 50
    k_items = [
        ("daily-kpi-quarter", "Day of Quarter",  "DAY OF QUARTER"),
        ("daily-kpi-semester","Day of Semester", "DAY OF HALF-YEAR"),
        ("daily-kpi-year",    "Day of Year",     "DAY OF YEAR"),
    ]
    k_w = 220
    k_gap = 20
    for i, (name, measure, label) in enumerate(k_items):
        kx = cx + i * (k_w + k_gap)
        visuals.append(textbox(f"{name}-label",
            [(label, 8, "Consolas", MUTE, False)],
            *L.add(f"{name}-label", kx, k_y, k_w, 14), pad=(0, 0, 0, 0)))
        visuals.append(card(name, measure,
            *L.add(name, kx, k_y + 16, k_w, k_h - 16),
            font=22, family="Georgia", bold=True, align="left"))

    # Daily column chart — # Received Today per dim_calendar[Date]
    chart_y = daily_top + 100
    visuals.append(column_chart("daily-chart",
        visual_type="columnChart",
        category_field=("dim_calendar", "Date"),
        value_fields=[("_Measures", "# Received Today")],
        fill_color=INK,
        x=cx, y=chart_y,
        w=cw, h=160,
    ))
    L.add("daily-chart", cx, chart_y, cw, 160)

    # Two-panel: dataset breakdown + group standings. y = 1080..1360
    panel_top = 1080
    panel_h = 280
    panel_gap = 20
    panel_w = (cw - panel_gap) // 2

    visuals.append(textbox("panel-l-eyebrow",
        [("DATASETS WITH MOST DELAY", 9, "Consolas", MUTE, False)],
        *L.add("panel-l-eyebrow", cx, panel_top, panel_w, 18), pad=(0, 0, 0, 0)))
    visuals.append(shape("panel-l-rule",
        *L.add("panel-l-rule", cx, panel_top + 22, panel_w, 1), fill=RULE))
    visuals.append(table_ex("panel-l-table",
        fields=[
            {"entity": "expected", "prop": "dataset_name", "kind": "col"},
            {"entity": "_Measures", "prop": "# Files Overdue", "kind": "measure"},
            {"entity": "_Measures", "prop": "# Expected", "kind": "measure"},
        ],
        x=cx, y=panel_top + 32, w=panel_w, h=panel_h - 32,
        sort_by=("_Measures", "# Files Overdue", "measure")))
    L.add("panel-l-table", cx, panel_top + 32, panel_w, panel_h - 32)

    rx = cx + panel_w + panel_gap
    visuals.append(textbox("panel-r-eyebrow",
        [("GROUP DELIVERY", 9, "Consolas", MUTE, False)],
        *L.add("panel-r-eyebrow", rx, panel_top, panel_w, 18), pad=(0, 0, 0, 0)))
    visuals.append(shape("panel-r-rule",
        *L.add("panel-r-rule", rx, panel_top + 22, panel_w, 1), fill=RULE))
    visuals.append(table_ex("panel-r-table",
        fields=[
            {"entity": "expected", "prop": "group", "kind": "col"},
            {"entity": "_Measures", "prop": "# Expected", "kind": "measure"},
            {"entity": "_Measures", "prop": "# Delivered", "kind": "measure"},
            {"entity": "_Measures", "prop": "# Files Overdue", "kind": "measure"},
            {"entity": "_Measures", "prop": "# Reached Gold", "kind": "measure"},
        ],
        x=rx, y=panel_top + 32, w=panel_w, h=panel_h - 32,
        sort_by=("_Measures", "# Files Overdue", "measure")))
    L.add("panel-r-table", rx, panel_top + 32, panel_w, panel_h - 32)

    # Footnote
    visuals += build_footnote(L,
        text="Source: expected.csv  ·  fct_delivery (active deliveries only)  ·  Overdue = no delivery + deadline (15th of period month) has passed  ·  Daily flow uses fct_delivery[received_date]",
        y=h - 80)

    return ("01-Summary", "fe1a126ffb0c5ea8", "01-Summary", PAGE_W, h, visuals)


# ---------- PAGE 2: GROUPS ----------
def build_page_2_groups():
    h = 1100
    L = Layout(PAGE_W, h, "02-Groups")
    visuals = []

    visuals += build_header(L,
        eyebrow="GROUP DATA DELIVERY TRACKER  ·  GROUPS",
        title="Group delivery check",
        meta="Five active groups  ·  one card per group  ·  raw counts only, no scoring")

    # 4-wide grid: 4 cards × 300 + 3 gaps × 16 + 2 margins = 1320 → margin = 36.
    card_w = 300
    card_h = 380
    gap = 16
    margin_x = (PAGE_W - 4 * card_w - 3 * gap) // 2
    grid_top = 170

    active = [
        ("mammoet",      "Mammoet",      (0, 0)),
        ("nutreco",      "Nutreco",      (1, 0)),
        ("kiwa",         "Kiwa",         (2, 0)),
        ("shv-holdings", "SHV Holdings", (3, 0)),
        ("shv-energy",   "SHV Energy",   (0, 1)),
    ]

    for slug, group_value, (col, row) in active:
        cx = margin_x + col * (card_w + gap)
        cy = grid_top + row * (card_h + gap)

        # Header — group name + meta line. No score, no grade chip.
        visuals.append(textbox(f"c-{slug}-name",
            [(group_value, 18, "Georgia", INK, True)],
            *L.add(f"c-{slug}-name", cx, cy, 300, 36), pad=(6, 12, 4, 14), bg=PAPER, z=1))

        visuals.append(card(f"c-{slug}-meta", "Card Meta",
            *L.add(f"c-{slug}-meta", cx, cy + 36, 300, 24),
            font=9, family="Consolas", bold=False, align="left", color=MUTE,
            bg=PAPER, group_value=group_value, z=1))

        # Divider rule
        visuals.append(shape(f"c-{slug}-rule",
            *L.add(f"c-{slug}-rule", cx, cy + 62, 300, 2), fill=RULE, z=1))

        # 4 stat rows: Expected / Delivered / Overdue / Reached Gold.
        # Each row: label (left) + value card (right).
        stats = [
            ("expected",  "# Expected",      "Expected",        INK),
            ("delivered", "# Delivered",     "Delivered",       GOOD),
            ("overdue",   "# Files Overdue", "Overdue",         BAD),
            ("gold",      "# Reached Gold",  "Reached Gold",    GOOD),
        ]
        row_h = 56
        row_y = cy + 70
        for stat_slug, measure_name, label, val_color in stats:
            # Label (left half)
            visuals.append(textbox(f"c-{slug}-{stat_slug}-lbl",
                [(label, 10, "Consolas", MUTE, False)],
                *L.add(f"c-{slug}-{stat_slug}-lbl", cx + 14, row_y + 14, 160, 28), pad=(0, 0, 0, 0), z=1))
            # Value card (right half)
            visuals.append(card(f"c-{slug}-{stat_slug}",
                measure_name,
                *L.add(f"c-{slug}-{stat_slug}", cx + 180, row_y + 6, 110, 44),
                font=22, family="Georgia", color=val_color, bold=True, align="right",
                group_value=group_value, z=1))
            # Thin separator
            visuals.append(shape(f"c-{slug}-{stat_slug}-sep",
                *L.add(f"c-{slug}-{stat_slug}-sep", cx + 14, row_y + row_h - 1, 272, 1), fill=RULE, z=1))
            row_y += row_h

    visuals += build_footnote(L,
        text="Counts scoped per group via visual-level filter  ·  Delivered = at least one active delivery for the expected file",
        y=h - 60)

    return ("02-Groups", "edc6b6af2663e6b4", "02-Groups", PAGE_W, h, visuals)


# ---------- PAGE 3: DATASETS ----------
def build_page_3_datasets():
    h = 1100
    L = Layout(PAGE_W, h, "03-Datasets")
    visuals = []

    visuals += build_header(L,
        eyebrow="GROUP DATA DELIVERY TRACKER  ·  DATASETS",
        title="Dataset-level delivery detail",
        meta="One row per dataset  ·  sorted by overdue then expected")

    cx = GUTTER
    cw = PAGE_W - 2 * GUTTER

    # Filter band: group slicer + year slicer side by side
    fy = 170
    visuals.append(textbox("ds-slicer-label",
        [("FILTER", 8, "Consolas", MUTE, False)],
        *L.add("ds-slicer-label", cx, fy, 80, 16), pad=(0, 0, 0, 0)))

    # KPI band
    kpi_y = 200
    kpi_h = 100
    kpis = [
        ("d-kpi-datasets",  "# Datasets",   "DATASETS"),
        ("d-kpi-contracts", "# Contracts",  "CONTRACTS"),
        ("d-kpi-expected",  "# Expected",   "EXPECTED"),
        ("d-kpi-delivered", "# Delivered",  "DELIVERED"),
        ("d-kpi-overdue",   "# Files Overdue", "OVERDUE"),
    ]
    gap = 8
    kpi_w = (cw - gap * (len(kpis) - 1)) // len(kpis)
    for i, (name, measure, label) in enumerate(kpis):
        kx = cx + i * (kpi_w + gap)
        visuals.append(textbox(f"{name}-label",
            [(label, 8, "Consolas", MUTE, False)],
            *L.add(f"{name}-label", kx, kpi_y, kpi_w, 16), pad=(0, 0, 0, 0)))
        visuals.append(card(name, measure,
            *L.add(name, kx, kpi_y + 18, kpi_w, kpi_h - 18),
            font=24, family="Georgia", bold=True, align="left"))

    # Big table
    table_top = 330
    table_h = h - table_top - 80

    visuals.append(textbox("ds-table-eyebrow",
        [("ALL DATASETS", 9, "Consolas", MUTE, False)],
        *L.add("ds-table-eyebrow", cx, table_top, cw, 18), pad=(0, 0, 0, 0)))
    visuals.append(shape("ds-table-rule",
        *L.add("ds-table-rule", cx, table_top + 22, cw, 1), fill=RULE))
    visuals.append(table_ex("ds-table",
        fields=[
            {"entity": "expected",  "prop": "group",           "kind": "col"},
            {"entity": "expected",  "prop": "dataset_name",    "kind": "col"},
            {"entity": "expected",  "prop": "frequency",       "kind": "col"},
            {"entity": "_Measures", "prop": "# Expected",      "kind": "measure"},
            {"entity": "_Measures", "prop": "# Delivered",     "kind": "measure"},
            {"entity": "_Measures", "prop": "# On Time",       "kind": "measure"},
            {"entity": "_Measures", "prop": "# Files Overdue", "kind": "measure"},
            {"entity": "_Measures", "prop": "# Reached Gold",  "kind": "measure"},
        ],
        x=cx, y=table_top + 32, w=cw, h=table_h - 32,
        sort_by=("_Measures", "# Files Overdue", "measure"), totals=True))
    L.add("ds-table", cx, table_top + 32, cw, table_h - 32)

    visuals += build_footnote(L,
        text="Active deliveries only  ·  counts scoped per dataset's filter context",
        y=h - 60)

    return ("03-Datasets", "8f6ea4df68c76d61", "03-Datasets", PAGE_W, h, visuals)


# ---------- PAGE 4: DAILY MATRIX ----------
def build_page_4_daily():
    h = 1100
    L = Layout(PAGE_W, h, "04-Daily")
    visuals = []

    visuals += build_header(L,
        eyebrow="GROUP DATA DELIVERY TRACKER  ·  DAILY",
        title="Daily receipts — month × day",
        meta="Rows = month  ·  columns = day of month  ·  green = within delivery window (1–15)  ·  red = outside window (16+)")

    cx = GUTTER
    cw = PAGE_W - 2 * GUTTER

    # Legend strip
    leg_y = 170
    visuals.append(textbox("daily-legend-in",
        [("■ ", 11, "Segoe UI", GOOD, True),
         ("IN WINDOW  (days 1–15)", 9, "Consolas", MUTE, False)],
        *L.add("daily-legend-in", cx, leg_y, 280, 22), pad=(0, 0, 0, 0)))
    visuals.append(textbox("daily-legend-out",
        [("■ ", 11, "Segoe UI", BAD, True),
         ("OUTSIDE WINDOW  (days 16+)", 9, "Consolas", MUTE, False)],
        *L.add("daily-legend-out", cx + 300, leg_y, 320, 22), pad=(0, 0, 0, 0)))
    visuals.append(textbox("daily-legend-note",
        [("Cells show count of active deliveries received on that calendar day.", 9, "Consolas", MUTE, False)],
        *L.add("daily-legend-note", cx + cw - 540, leg_y, 540, 22), pad=(0, 0, 0, 0), align="right"))

    # Matrix
    mat_top = 210
    mat_h = h - mat_top - 80
    visuals.append(shape("daily-mat-rule",
        *L.add("daily-mat-rule", cx, mat_top - 8, cw, 1), fill=RULE))
    visuals.append(matrix("daily-matrix",
        row_fields=[
            {"entity": "dim_calendar", "prop": "MonthName", "kind": "col"},
        ],
        column_fields=[
            {"entity": "dim_calendar", "prop": "DayOfMonth", "kind": "col"},
        ],
        value_fields=[
            {"entity": "_Measures", "prop": "# Received Today", "kind": "measure"},
        ],
        value_bg_measure=("_Measures", "Cell Color BG"),
        value_fg_measure=("_Measures", "Cell Color FG"),
        x=cx, y=mat_top, w=cw, h=mat_h,
        column_subtotals=False, row_subtotals=False, totals=True,
    ))
    L.add("daily-matrix", cx, mat_top, cw, mat_h)

    visuals += build_footnote(L,
        text="Counts use fct_delivery[received_date] via USERELATIONSHIP; calendar slicers in the header scope by Year.  Months sorted by Month#; days run 1–31.",
        y=h - 60)

    return ("04-Daily", "4f14e8b6930a22c6", "04-Daily", PAGE_W, h, visuals)


# ---------- PAGE 4-OLD: SCORING (unused) ----------
def build_page_4_scoring():
    h = 1280
    L = Layout(PAGE_W, h, "04-Scoring")
    visuals = []

    visuals += build_header(L,
        eyebrow="GROUP DATA DELIVERY TRACKER  ·  HOW WE SCORE",
        title="The Group Health Score",
        meta="Composite weighted across five dimensions, minus an overdue penalty, capped 0–100")

    cx = GUTTER
    cw = PAGE_W - 2 * GUTTER

    # Formula box (single textbox with PAPER bg, no separate shape)
    fy = 170
    visuals.append(textbox("s-formula-eyebrow",
        [("THE FORMULA", 9, "Consolas", MUTE, False)],
        *L.add("s-formula-eyebrow", cx, fy, cw, 18), pad=(0, 0, 0, 0)))
    visuals.append(textbox("s-formula-text",
        [("Score = ", 14, "Georgia", INK, False),
         ("0.25 ", 14, "Consolas", GOOD, True), ("Reliable  +  ", 14, "Georgia", INK, False),
         ("0.15 ", 14, "Consolas", GOOD, True), ("OnTime  +  ", 14, "Georgia", INK, False),
         ("0.25 ", 14, "Consolas", GOOD, True), ("Quality  +  ", 14, "Georgia", INK, False),
         ("0.10 ", 14, "Consolas", GOOD, True), ("Recovery  +  ", 14, "Georgia", INK, False),
         ("0.15 ", 14, "Consolas", GOOD, True), ("Discipline  −  ", 14, "Georgia", INK, False),
         ("0.10 ", 14, "Consolas", BAD, True),  ("Overdue", 14, "Georgia", INK, False)],
        *L.add("s-formula-text", cx, fy + 24, cw, 90), pad=(28, 24, 28, 24), bg=PAPER, z=1))

    # Dimensions panel — 5 rows
    dp_top = fy + 130   # 300
    visuals.append(textbox("s-dims-eyebrow",
        [("THE FIVE DIMENSIONS", 9, "Consolas", MUTE, False)],
        *L.add("s-dims-eyebrow", cx, dp_top, cw, 18), pad=(0, 0, 0, 0)))
    visuals.append(shape("s-dims-rule",
        *L.add("s-dims-rule", cx, dp_top + 22, cw, 1), fill=RULE))

    dims = [
        ("Reliable",   "Delivered / Due-by-today",          "0.25"),
        ("On Time",    "On-time / Delivered",                "0.15"),
        ("Quality",    "Reached Gold / Delivered",           "0.25"),
        ("Recovery",   "Any delivery effort (binary 0/100)", "0.10"),
        ("Discipline", "1 − (scope-quarantine / delivered)", "0.15"),
    ]
    row_h = 60
    row_y = dp_top + 32
    for name, formula, weight in dims:
        visuals.append(textbox(f"s-dim-{name.lower().replace(' ', '')}-name",
            [(name, 13, "Georgia", INK, True)],
            *L.add(f"s-dim-{name.lower().replace(' ', '')}-name", cx, row_y, 200, 28), pad=(0, 0, 0, 0)))
        visuals.append(textbox(f"s-dim-{name.lower().replace(' ', '')}-form",
            [(formula, 10, "Consolas", MUTE, False)],
            *L.add(f"s-dim-{name.lower().replace(' ', '')}-form", cx + 210, row_y + 4, cw - 360, 22), pad=(0, 0, 0, 0)))
        visuals.append(textbox(f"s-dim-{name.lower().replace(' ', '')}-wt",
            [("w = " + weight, 11, "Consolas", INK, True)],
            *L.add(f"s-dim-{name.lower().replace(' ', '')}-wt", cx + cw - 140, row_y + 4, 140, 22), pad=(0, 0, 0, 0), align="right"))
        visuals.append(shape(f"s-dim-{name.lower().replace(' ', '')}-rule",
            *L.add(f"s-dim-{name.lower().replace(' ', '')}-rule", cx, row_y + 34, cw, 1), fill=RULE))
        row_y += row_h
    # row_y is now end of dimensions panel = dp_top + 32 + 5*60 = 332 + 300 = 632 + offset

    # Grade bands  -- y ~ 670
    gb_top = row_y + 30
    visuals.append(textbox("s-bands-eyebrow",
        [("GRADE BANDS", 9, "Consolas", MUTE, False)],
        *L.add("s-bands-eyebrow", cx, gb_top, cw, 18), pad=(0, 0, 0, 0)))

    bands = [
        ("A", "90 – 100", GOOD),
        ("B", "75 – 89",  GOOD),
        ("C", "60 – 74",  WARN),
        ("D", "40 – 59",  WARN),
        ("F", " < 40",    BAD),
    ]
    band_y = gb_top + 28
    chip_w = (cw - 4 * 16) // 5
    for i, (letter, rng, color) in enumerate(bands):
        bx = cx + i * (chip_w + 16)
        # Single textbox per chip — colored bg, both runs inside
        visuals.append(textbox(f"s-band-{letter}",
            [(letter, 32, "Georgia", PAPER, True),
             ("\n", 6, "Consolas", PAPER, False),
             (rng,  10, "Consolas", PAPER, False)],
            *L.add(f"s-band-{letter}", bx, band_y, chip_w, 80),
            align="left", pad=(8, 12, 8, 14), bg=color, z=1))

    # Leaderboard
    lb_top = band_y + 110
    visuals.append(textbox("s-leader-eyebrow",
        [("LEADERBOARD", 9, "Consolas", MUTE, False)],
        *L.add("s-leader-eyebrow", cx, lb_top, cw, 18), pad=(0, 0, 0, 0)))
    visuals.append(shape("s-leader-rule",
        *L.add("s-leader-rule", cx, lb_top + 22, cw, 1), fill=RULE))
    visuals.append(table_ex("s-leader-table",
        fields=[
            {"entity": "expected", "prop": "group", "kind": "col"},
            {"entity": "_Measures", "prop": "Reliability", "kind": "measure"},
            {"entity": "_Measures", "prop": "Punctuality", "kind": "measure"},
            {"entity": "_Measures", "prop": "Quality", "kind": "measure"},
            {"entity": "_Measures", "prop": "Recovery", "kind": "measure"},
            {"entity": "_Measures", "prop": "Discipline", "kind": "measure"},
            {"entity": "_Measures", "prop": "Score", "kind": "measure"},
            {"entity": "_Measures", "prop": "Grade", "kind": "measure"},
        ],
        x=cx, y=lb_top + 32, w=cw, h=h - lb_top - 100,
        sort_by=("_Measures", "Score", "measure"), totals=False))
    L.add("s-leader-table", cx, lb_top + 32, cw, h - lb_top - 100)

    visuals += build_footnote(L,
        text="Overdue Share penalty = (overdue / due-by-today) × 100  ·  Final score clamped to 0–100",
        y=h - 60)

    return ("04-Scoring", "4f14e8b6930a22c6", "04-Scoring", PAGE_W, h, visuals)


# ---------- MAIN ----------
def main():
    # 1) Wipe existing pages
    if os.path.exists(ROOT):
        for item in os.listdir(ROOT):
            full = os.path.join(ROOT, item)
            if os.path.isdir(full):
                shutil.rmtree(full)
            elif item == "pages.json":
                os.remove(full)
    print("wiped all existing pages")

    # 2) Build pages — scoring/grading removed; this is a delivery check, not a graded scorecard
    builders = [build_page_1_summary, build_page_2_groups, build_page_3_datasets, build_page_4_daily]
    page_order = []
    for b in builders:
        page_dir, page_name, display, w, h, visuals = b()
        write_page(page_dir, page_name, display, w, h, visuals)
        page_order.append(page_name)
        print(f"  built {display}: {len(visuals)} visuals, {w}x{h}")

    # 3) pages.json
    write_json(os.path.join(ROOT, "pages.json"), {
        "$schema": SCHEMA_PAGES,
        "pageOrder": page_order,
        "activePageName": page_order[0],
    })
    print(f"wrote pages.json (active = {page_order[0]})")
    print("done.")


if __name__ == "__main__":
    main()
