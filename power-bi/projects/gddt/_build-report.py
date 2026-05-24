"""Theme-clean 5-level report build for gddt (per BRIEF.md).

L0 Health · L1 Where's the problem · L2 Pipeline funnel · L2.5 Daily ops · L3 File detail.

Visuals carry data + position + native title only (no color/font/background
overrides) so the registered theme drives styling. Exceptions are deliberate:
the L0 stack uses CurrentState (single state per file) so it partitions to Expected.
"""
import json
import os
import shutil

ROOT = "gddt.Report/definition/pages"
SCHEMA_PAGE  = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_VIS   = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"
SCHEMA_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json"

PAGE_W, PAGE_H, GUTTER = 1280, 720, 16

def lit(v): return {"expr": {"Literal": {"Value": v}}}
def lit_s(v): return lit(f"'{v}'")
def lit_b(v): return lit("true" if v else "false")

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)


class Layout:
    def __init__(self, w, h, name):
        self.w, self.h, self.name = w, h, name
        self.placed = []
    def add(self, name, x, y, w, h):
        if x < 0 or y < 0 or x + w > self.w or y + h > self.h:
            raise ValueError(f"[{self.name}] {name} OOB ({x},{y},{w},{h})")
        for px, py, pw, ph, pn in self.placed:
            if x < px + pw and x + w > px and y < py + ph and y + h > py:
                raise ValueError(f"[{self.name}] {name} overlaps {pn}")
        self.placed.append((x, y, w, h, name))
        return x, y, w, h


def measure_field(prop, entity="_Measures"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
def column_field(prop, entity):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
def projection(f):
    field = column_field(f["prop"], f["entity"]) if f["kind"] == "col" else measure_field(f["prop"], f["entity"])
    return {"queryRef": f"{f['entity']}.{f['prop']}", "field": field, "nativeQueryRef": f["prop"]}
def title_obj(text):
    return {"title": [{"properties": {"show": lit_b(True), "text": lit_s(text)}}]}


def _wrap(name, vtype, qs, x, y, w, h, title, objects=None, page_local=None):
    v = {
        "name": name,
        "visual": {"visualType": vtype, "query": {"queryState": qs}, "drillFilterOtherVisuals": True},
        "position": {"x": x, "y": y, "z": 1, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }
    if objects:
        v["visual"]["objects"] = objects
    if title:
        v["visual"]["visualContainerObjects"] = title_obj(title)
    return {"path": f"{name}/visual.json", "data": v}


def card(name, measure, x, y, w, h, *, title=None):
    qs = {"Values": {"projections": [projection({"entity": "_Measures", "prop": measure, "kind": "measure"})]}}
    return _wrap(name, "card", qs, x, y, w, h, title)


def chart(name, *, vtype="columnChart", category, values, x, y, w, h, title=None,
          legend=None, series_colors=None, show_labels=False):
    qs = {"Category": {"projections": [projection(category) | {"active": True}]},
          "Y": {"projections": [projection(v) for v in values]}}
    if legend:
        qs["Series"] = {"projections": [projection(legend)]}
    objects = {}
    if series_colors:
        objects["dataPoint"] = [
            {"selector": {"metadata": f"{v['entity']}.{v['prop']}"},
             "properties": {"fill": {"solid": {"color": lit_s(c)}}}}
            for v, c in zip(values, series_colors)
        ]
    if show_labels:
        objects["labels"] = [{"properties": {"show": lit_b(True)}}]
    return _wrap(name, vtype, qs, x, y, w, h, title, objects or None)


def funnel(name, *, category, value, x, y, w, h, title=None):
    qs = {"Category": {"projections": [projection(category)]},
          "Y": {"projections": [projection(value)]}}
    return _wrap(name, "funnel", qs, x, y, w, h, title)


def table_ex(name, *, fields, x, y, w, h, title=None, sort_by=None, sort_desc=True):
    qs = {"Values": {"projections": [projection(f) for f in fields]}}
    out = _wrap(name, "tableEx", qs, x, y, w, h, title)
    if sort_by:
        ent, prop, kind = sort_by
        field = column_field(prop, ent) if kind == "col" else measure_field(prop, ent)
        out["data"]["visual"]["query"]["sortDefinition"] = {
            "sort": [{"field": field, "direction": "Descending" if sort_desc else "Ascending"}],
            "isDefaultSort": True}
    return out


def matrix(name, *, rows, columns, values, x, y, w, h, title=None):
    qs = {"Rows": {"projections": [projection(f) for f in rows]},
          "Columns": {"projections": [projection(f) for f in columns]},
          "Values": {"projections": [projection(f) for f in values]}}
    return _wrap(name, "pivotTable", qs, x, y, w, h, title)


def slicer(name, field, x, y, w, h, *, title=None):
    qs = {"Values": {"projections": [projection(field)]}}
    return _wrap(name, "slicer", qs, x, y, w, h, title)


def textbox(name, lines, x, y, w, h):
    """Documentation textbox. lines = list of (text, size_pt, bold). Default text color (theme)."""
    paras = []
    for text, size, bold in lines:
        ts = {"fontSize": f"{size}pt"}
        if bold:
            ts["fontWeight"] = "bold"
        paras.append({"textRuns": [{"value": text, "textStyle": ts}], "horizontalTextAlignment": "left"})
    v = {
        "name": name,
        "visual": {
            "visualType": "textbox",
            "query": {"queryState": {}},
            "objects": {"general": [{"properties": {"paragraphs": paras}}]},
            "drillFilterOtherVisuals": True,
        },
        "position": {"x": x, "y": y, "z": 1, "width": w, "height": h, "tabOrder": 0},
        "$schema": SCHEMA_VIS,
    }
    return {"path": f"{name}/visual.json", "data": v}


def year_page_filter(year):
    return {"filters": [{
        "name": f"filter_year_{year}", "type": "Categorical",
        "field": column_field("Year", "dim_calendar"),
        "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "dim_calendar", "Type": 0}],
            "Where": [{"Condition": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Year"}}],
                "Values": [[{"Literal": {"Value": f"{year}L"}}]]}}}]},
        "howCreated": "User"}]}


def write_page(page_dir, page_name, display, w, h, visuals, page_filter=None):
    full = os.path.join(ROOT, page_dir)
    page = {"$schema": SCHEMA_PAGE, "name": page_name, "displayName": display,
            "width": w, "height": h, "displayOption": "FitToWidth"}
    if page_filter:
        page["filterConfig"] = page_filter
    write_json(os.path.join(full, "page.json"), page)
    for v in visuals:
        write_json(os.path.join(full, "visuals", v["path"]), v["data"])


M = lambda p: {"entity": "_Measures", "prop": p, "kind": "measure"}
C = lambda p, e="expected": {"entity": e, "prop": p, "kind": "col"}
STATE_COLORS = ["#2D6948", "#5B9279", "#7FB069", "#B5C99A", "#B46C1A",
                "#C98A3A", "#D9A441", "#A23A2A", "#CE5A4E", "#D8D5CC"]


# ---------- L0 · HEALTH ----------
def page_health():
    L = Layout(PAGE_W, PAGE_H, "L0-Health")
    vis = []
    cw = PAGE_W - 2 * GUTTER
    kpis = [("k-exp", "# Expected", "Expected"), ("k-del", "% Delivered", "% Delivered"),
            ("k-ot", "% On Time", "% On time"), ("k-gold", "% Reached Gold", "% Gold"),
            ("k-over", "# Files Overdue", "Overdue")]
    gap = 8
    kwid = (cw - gap * (len(kpis) - 1)) // len(kpis)
    for i, (n, m, t) in enumerate(kpis):
        vis.append(card(n, m, *L.add(n, GUTTER + i * (kwid + gap), 16, kwid, 110), title=t))

    half = (cw - 16) // 2
    # Stacked bar partitioned by CurrentState (single state per file → sums to Expected)
    vis.append(chart("state-by-month", vtype="columnChart",
        category=C("MonthName", "dim_calendar"), values=[M("# Expected")],
        legend=C("CurrentState"), x=GUTTER, y=140, w=half, h=270,
        title="Delivery state by month"))
    L.add("state-by-month", GUTTER, 140, half, 270)

    rx = GUTTER + half + 16
    vis.append(chart("gold-trend", vtype="lineChart",
        category=C("MonthName", "dim_calendar"), values=[M("% Reached Gold")],
        x=rx, y=140, w=half, h=270, title="% reached gold by month"))
    L.add("gold-trend", rx, 140, half, 270)

    # State breakdown table (whole period)
    vis.append(table_ex("state-table",
        fields=[C("CurrentState"), M("# Expected"), M("% Delivered"), M("% On Time"), M("% Reached Gold")],
        x=GUTTER, y=426, w=cw, h=278, title="By current state",
        sort_by=("expected", "CurrentStateSort", "col"), sort_desc=False))
    L.add("state-table", GUTTER, 426, cw, 278)

    return ("L0-Health", "p0health00000000001", "L0 · Health", PAGE_W, PAGE_H, vis, year_page_filter(2026))


# ---------- L1 · WHERE'S THE PROBLEM ----------
def page_where():
    L = Layout(PAGE_W, PAGE_H, "L1-Where")
    vis = []
    cw = PAGE_W - 2 * GUTTER
    # slicers row
    sl = [("s-year", C("Year", "dim_calendar"), "Year"), ("s-domain", C("domain"), "Domain"),
          ("s-group", C("group"), "Group"), ("s-freq", C("frequency"), "Frequency")]
    sw = (cw - 3 * 12) // 4
    for i, (n, f, t) in enumerate(sl):
        vis.append(slicer(n, f, *L.add(n, GUTTER + i * (sw + 12), 16, sw, 96), title=t))

    # Matrix domain > group > dataset  x  CurrentState
    vis.append(matrix("where-matrix",
        rows=[C("domain"), C("group"), C("dataset_name")],
        columns=[C("CurrentState")],
        values=[M("# Expected")],
        x=GUTTER, y=124, w=cw, h=360, title="Domain ▸ group ▸ dataset by state"))
    L.add("where-matrix", GUTTER, 124, cw, 360)

    # Overdue by group bar
    vis.append(chart("overdue-by-group", vtype="barChart",
        category=C("group"), values=[M("# Files Overdue")],
        x=GUTTER, y=496, w=cw, h=208, title="Overdue by group"))
    L.add("overdue-by-group", GUTTER, 496, cw, 208)

    return ("L1-Where", "p1where000000000001", "L1 · Where", PAGE_W, PAGE_H, vis, None)


# ---------- L2 · PIPELINE FUNNEL ----------
def page_funnel():
    L = Layout(PAGE_W, PAGE_H, "L2-Funnel")
    vis = []
    cw = PAGE_W - 2 * GUTTER
    half = (cw - 16) // 2
    vis.append(funnel("pipe-funnel",
        category=C("Stage", "pipeline_stage"), value=M("# At Stage"),
        x=GUTTER, y=16, w=half, h=540, title="Pipeline funnel (Expected → Gold)"))
    L.add("pipe-funnel", GUTTER, 16, half, 540)

    rx = GUTTER + half + 16
    # Failure / state breakdown bar
    vis.append(chart("state-breakdown", vtype="barChart",
        category=C("CurrentState"), values=[M("# Expected")],
        x=rx, y=16, w=half, h=260, title="Files by current state"))
    L.add("state-breakdown", rx, 16, half, 260)

    # Quarantine/DQ/schema counts table
    vis.append(table_ex("quar-table",
        fields=[M("# Schema Failed - Quarantine"), M("# Quarantine - Scope & Delivery Time"),
                M("# Quarantine - Delivery Time"), M("# Records Found in Inspection - Failed DQ"),
                M("# Business Approved")],
        x=rx, y=292, w=half, h=264, title="Quarantine & DQ breakdown"))
    L.add("quar-table", rx, 292, half, 264)

    # Stage counts strip along the bottom
    vis.append(table_ex("funnel-table",
        fields=[M("# Expected"), M("# Delivered"), M("# On Time"), M("# Reached Gold")],
        x=GUTTER, y=572, w=cw, h=132, title="Stage counts"))
    L.add("funnel-table", GUTTER, 572, cw, 132)

    return ("L2-Funnel", "p2funnel0000000001", "L2 · Funnel", PAGE_W, PAGE_H, vis, None)


# ---------- L2.5 · DAILY OPS ----------
def page_daily():
    L = Layout(PAGE_W, PAGE_H, "L2.5-Daily")
    vis = []
    cw = PAGE_W - 2 * GUTTER
    # KPI cards
    dk = [("d-today", "# Received Today", "Received today"),
          ("d-mtd", "# Received MTD", "Received MTD"),
          ("d-due", "# Expected by Day", "Expected by day")]
    kwid = 240
    for i, (n, m, t) in enumerate(dk):
        vis.append(card(n, m, *L.add(n, GUTTER + i * (kwid + 12), 16, kwid, 96), title=t))
    # Year slicer
    vis.append(slicer("d-year", C("Year", "dim_calendar"),
        *L.add("d-year", GUTTER + 3 * (kwid + 12), 16, cw - 3 * (kwid + 12), 96), title="Year"))

    # MTD vs expected line
    vis.append(chart("d-line", vtype="lineChart",
        category=C("Date", "dim_calendar"),
        values=[M("# Received MTD"), M("# Expected by Day")],
        x=GUTTER, y=124, w=cw, h=240, title="Received MTD vs expected by day"))
    L.add("d-line", GUTTER, 124, cw, 240)

    # Months x days matrix
    vis.append(matrix("d-matrix",
        rows=[C("MonthName", "dim_calendar")], columns=[C("DayOfMonth", "dim_calendar")],
        values=[M("# Received Today")],
        x=GUTTER, y=380, w=cw, h=324, title="Receipts — month × day"))
    L.add("d-matrix", GUTTER, 380, cw, 324)

    return ("L2.5-Daily", "p25daily000000001", "L2.5 · Daily", PAGE_W, PAGE_H, vis, None)


# ---------- L3 · FILE DETAIL ----------
def page_detail():
    L = Layout(PAGE_W, PAGE_H, "L3-Detail")
    vis = []
    cw = PAGE_W - 2 * GUTTER
    # slicers
    sl = [("f-state", C("CurrentState"), "State"), ("f-group", C("group"), "Group"),
          ("f-domain", C("domain"), "Domain")]
    sw = (cw - 2 * 12) // 3
    for i, (n, f, t) in enumerate(sl):
        vis.append(slicer(n, f, *L.add(n, GUTTER + i * (sw + 12), 16, sw, 96), title=t))

    # Hash-grain detail table
    vis.append(table_ex("detail-table",
        fields=[C("hash_id"), C("group"), C("domain"), C("dataset_name"), C("dc_name"),
                C("frequency"), C("deadline_date"), C("CurrentState"), M("# Records Inspected")],
        x=GUTTER, y=124, w=cw, h=580, title="File detail (filter by state / group to investigate)",
        sort_by=("expected", "deadline_date", "col"), sort_desc=False))
    L.add("detail-table", GUTTER, 124, cw, 580)

    return ("L3-Detail", "p3detail00000000001", "L3 · File detail", PAGE_W, PAGE_H, vis, None)


# ---------- MODEL DETAILS (reference tab) ----------
def page_model():
    L = Layout(PAGE_W, PAGE_H, "Model")
    vis = []
    cw = PAGE_W - 2 * GUTTER
    colw = (cw - 16) // 2
    rx = GUTTER + colw + 16

    vis.append(textbox("m-title", [
        ("Model details", 20, True),
        ("gddt delivery tracker · semantic model reference", 9, False),
    ], *L.add("m-title", GUTTER, 16, cw, 56)))

    vis.append(textbox("m-tables", [
        ("TABLES", 11, True),
        ("expected — the plan. 1 row per hash_id × period. Dims: domain, group, dataset_name, dc_name (contract), entity, frequency. period_date → calendar; deadline_date = 15th of the month.", 9, False),
        ("fct_delivery — actuals + pipeline. 1 row per delivery attempt; is_active = latest per hash. status_3..9 flags, insp_record_count, received_date → calendar (inactive).", 9, False),
        ("dim_calendar — time spine, per day (2025–2027). Active on expected[period_date]; inactive on fct_delivery[received_date].", 9, False),
        ("_Measures — semantic layer: counts, rates, daily flow, funnel.", 9, False),
        ("pipeline_stage — disconnected funnel stages.", 9, False),
    ], *L.add("m-tables", GUTTER, 84, colw, 230)))

    vis.append(textbox("m-rels", [
        ("RELATIONSHIPS", 11, True),
        ("fct_delivery[hash_id]  →  expected[hash_id]   (active, many-to-one)", 9, False),
        ("expected[period_date]  →  dim_calendar[Date]   (active)", 9, False),
        ("fct_delivery[received_date]  →  dim_calendar[Date]   (inactive — USERELATIONSHIP)", 9, False),
        ("Files match by relationship + hash; deadline = 15th. Past deadline + not received = Overdue; before deadline + not received = Pending.", 9, False),
    ], *L.add("m-rels", GUTTER, 326, colw, 180)))

    vis.append(textbox("m-state", [
        ("CURRENT STATE — one per file (best-state-wins)", 11, True),
        ("1  Reached Gold", 9, False),
        ("2  Business Approved", 9, False),
        ("3  On Time", 9, False),
        ("4  Delivered (late)", 9, False),
        ("5  DQ Records Found", 9, False),
        ("6  Quarantine – Scope", 9, False),
        ("7  Quarantine – Time", 9, False),
        ("8  Schema Failed", 9, False),
        ("9  Overdue   (past deadline, not received)", 9, False),
        ("10 Pending   (before deadline, not received)", 9, False),
    ], *L.add("m-state", rx, 84, colw, 230)))

    vis.append(textbox("m-measures", [
        ("MEASURES (by folder)", 11, True),
        ("00 Inventory — # Contracts, # Datasets, # Groups", 9, False),
        ("01 Status counts — # Expected, # Delivered, # Missing, # On Time, # Schema Failed, # Quarantine (Scope/Time), # DQ Failed, # Business Approved, # Reached Gold", 9, False),
        ("02 Derived late — # Due By Today, # Files Overdue, # Files Pending", 9, False),
        ("03 Rates — % Delivered, % On Time, % Reached Gold", 9, False),
        ("04 Record volumes — # Records On Time / Reached Gold / Inspected (dynamic #,0 → M → B format)", 9, False),
        ("05 Daily flow — # Received Today, # Received MTD, # Expected by Day", 9, False),
        ("06 Funnel — # At Stage   ·   07 Helpers — State Color", 9, False),
    ], *L.add("m-measures", rx, 326, colw, 230)))

    vis.append(textbox("m-foot", [
        ("All counts use DISTINCTCOUNT(expected[hash_id]). Compatibility level 1601 (dynamic format strings). Source CSVs are local to the project folder.", 8, False),
    ], *L.add("m-foot", GUTTER, 620, cw, 60)))

    return ("Model", "pmodeldetails000001", "Model details", PAGE_W, PAGE_H, vis, None)


def main():
    if os.path.exists(ROOT):
        for item in os.listdir(ROOT):
            full = os.path.join(ROOT, item)
            if os.path.isdir(full):
                shutil.rmtree(full)
            elif item == "pages.json":
                os.remove(full)
    print("wiped existing pages")

    builders = [page_health, page_where, page_funnel, page_daily, page_detail, page_model]
    order = []
    for b in builders:
        pdir, pname, disp, w, h, vis, pf = b()
        write_page(pdir, pname, disp, w, h, vis, pf)
        order.append(pname)
        print(f"  built {disp}: {len(vis)} visuals{' (year-filtered)' if pf else ''}")

    write_json(os.path.join(ROOT, "pages.json"),
               {"$schema": SCHEMA_PAGES, "pageOrder": order, "activePageName": order[0]})
    print(f"wrote pages.json (active = {order[0]})")
    print("done.")


if __name__ == "__main__":
    main()
