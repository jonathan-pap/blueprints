"""Page/visual builder for the Arcane Emporium report. All geometry comes from design-system.yaml.

Structurally the same kit that built telecom-churn - the parts that earned their place there
(headings as textboxes, panels via the theme rather than shape visuals, chrome inside the header
band, everything on the 8px snap) carry over unchanged. What differs is the palette and the
star it is bound to.
"""
import json
import os
import shutil
import subprocess
import sys

import resolve_layout as RL

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(ROOT, "arcane-emporium.Report")
PAGES = os.path.join(REPORT, "definition", "pages")
SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
          "definition/visualContainer/2.10.0/schema.json")
FACT = "FactSales"
M = "_Measures"
Q = chr(39)

# Runeforge Dark v1.0 - keep in step with projects/themes/runeforge/notes.md
INK, INK2, INK3 = "#F2EAE0", "#CDC2B4", "#9E9285"
CANVAS, SURFACE, RULE = "#100E0C", "#1A1714", "#342E28"
BLUE, GOLD, VERD, PLUM = "#B2C6ED", "#C7A726", "#33A095", "#B74BC3"
CRIMSON, FOREST, BRONZE, IRON = "#E9A7B0", "#3BB16C", "#BF7240", "#5F6E7E"

DS = RL.load(os.path.join(ROOT, RL.DS))


def rects(name):
    return RL.layout(name, DS)


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def solid(c):
    return {"solid": {"color": lit("'%s'" % c)}}


def measure(name, entity=M):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": name}}


def col(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def proj_m(name, disp=None):
    p = {"field": measure(name), "queryRef": M + "." + name, "nativeQueryRef": name}
    if disp:
        p["displayName"] = disp
    return p


def proj_c(entity, prop, disp=None):
    p = {"field": col(entity, prop), "queryRef": "%s.%s" % (entity, prop),
         "nativeQueryRef": prop}
    if disp:
        p["displayName"] = disp
    return p


def run(*a):
    p = subprocess.run(a, cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout or "").strip()
    if out:
        print("  " + out[:200])
    if p.returncode:
        print("  ERR:", (p.stderr or "").strip()[:200])
    return p.returncode


def add_page(pid, display, w=1280, h=720):
    before = set(os.listdir(PAGES))
    if run("pbir", "add", "page", "arcane-emporium.Report/%s.Page" % display, "-n", display):
        sys.exit("add page failed: " + display)
    new = sorted(set(os.listdir(PAGES)) - before)
    run("pbir", "pages", "rename", "arcane-emporium.Report/%s.Page" % display, "--to", pid, "-f")
    d = os.path.join(PAGES, pid)
    if not os.path.isdir(d):
        d = os.path.join(PAGES, new[0])
    pj = os.path.join(d, "page.json")
    pg = json.load(open(pj, encoding="utf-8"))
    old = pg["name"]
    pg["name"], pg["displayName"] = pid, display
    pg["width"], pg["height"] = w, h
    pg["displayOption"] = "FitToPage"
    json.dump(pg, open(pj, "w", encoding="utf-8", newline="\n"), indent=2)

    meta_p = os.path.join(PAGES, "pages.json")
    meta = json.load(open(meta_p, encoding="utf-8"))
    meta["pageOrder"] = [pid if x == old else x for x in meta["pageOrder"]]
    if pid not in meta["pageOrder"]:
        meta["pageOrder"].append(pid)
    # drop entries with no folder on disk - a half-deleted page otherwise lingers forever
    live = set(os.listdir(PAGES))
    meta["pageOrder"] = [x for x in meta["pageOrder"] if x in live]
    meta["activePageName"] = meta["pageOrder"][0]
    json.dump(meta, open(meta_p, "w", encoding="utf-8", newline="\n"), indent=2)

    vd = os.path.join(d, "visuals")
    for x in list(os.listdir(vd)) if os.path.isdir(vd) else []:
        v = json.load(open(os.path.join(vd, x, "visual.json"), encoding="utf-8"))
        if v.get("visual", {}).get("visualType") == "textbox":
            shutil.rmtree(os.path.join(vd, x))
    print("  page %s (%dx%d)" % (pid, w, h))
    return d


def write(page_dir, name, obj):
    d = os.path.join(page_dir, "visuals", name)
    os.makedirs(d, exist_ok=True)
    json.dump(obj, open(os.path.join(d, "visual.json"), "w", encoding="utf-8", newline="\n"),
              indent=2)


def vis(name, vtype, rect, z, query=None, objects=None, vco=None, tab=1):
    v = {"visualType": vtype}
    if query is not None:
        v["query"] = {"queryState": query}
    v["objects"] = objects or {}
    v["visualContainerObjects"] = vco if vco is not None else {}
    v["drillFilterOtherVisuals"] = True
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": rect["x"], "y": rect["y"], "z": z,
                         "width": rect["width"], "height": rect["height"], "tabOrder": tab},
            "visual": v}


def ts(size, colour=INK, face="Segoe UI"):
    return {"fontFamily": face, "fontSize": size, "color": colour}


def noframe():
    off = [{"properties": {"show": lit("false")}}]
    return {"title": off, "background": off, "border": off}


def textbox(name, rect, runs, z=900):
    paras = [{"textRuns": [{"value": v, "textStyle": s}]} for v, s in runs]
    return vis(name, "textbox", rect, z, query={},
               objects={"general": [{"properties": {"paragraphs": paras}}]}, vco=noframe())


def head_tb(name, rect, title, sub=None):
    """Heading as a textbox, never the container title: setting title.text on a chart makes
    Power BI render the custom title AND its auto-generated name, stacked."""
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    return textbox(name, rect, runs, z=900)


def stack(rect, sub=False, gap=8):
    """Split a region into a heading strip on the canvas and a content rect below it.

    Heading heights and the gap are multiples of the 8px snap so the derived content rect
    stays on-grid.
    """
    h = 40 if sub else 24
    head = {"x": rect["x"], "y": rect["y"], "width": rect["width"], "height": h}
    body = {"x": rect["x"], "y": rect["y"] + h + gap,
            "width": rect["width"], "height": rect["height"] - h - gap}
    return head, body


def axis(show=True, colour=INK3, extra=None):
    p = {"show": lit("true" if show else "false"), "showAxisTitle": lit("false"),
         "labelColor": solid(colour), "fontSize": lit("9D"), "gridlineShow": lit("false")}
    if extra:
        p.update(extra)
    return [{"properties": p}]


def bars(name, rect, entity, column, meas, colour=BLUE, z=200, horizontal=True,
         sort_field=None, sort_dir="Descending", labels=True, fill_measure=None):
    dp = [{"properties": {"fill": solid(colour)}}]
    if fill_measure:
        dp.append({"properties": {"fill": {"solid": {"color": {"expr": measure(fill_measure)}}}},
                   "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}})
    v = vis(name, "barChart" if horizontal else "columnChart", rect, z,
            query={"Category": {"projections": [proj_c(entity, column)]},
                   "Y": {"projections": [proj_m(meas)]}},
            objects={"dataPoint": dp,
                     "categoryAxis": axis(True),
                     "valueAxis": axis(False),
                     "legend": [{"properties": {"show": lit("false")}}],
                     "labels": [{"properties": {
                         "show": lit("true" if labels else "false"),
                         "color": solid(INK2), "fontSize": lit("9D"),
                         # Auto flips labels INSIDE a long bar where they fail on the fill
                         "labelPosition": lit("'OutsideEnd'")}}]},
            vco=noframe())
    if sort_field is not None:
        v["visual"]["query"]["sortDefinition"] = {
            "sort": [{"field": sort_field, "direction": sort_dir}]}
    return v


GRID = {"gridVertical": lit("false"), "gridHorizontal": lit("true"),
        "gridHorizontalColor": solid(RULE), "outlineWeight": lit("0D"), "rowPadding": lit("1D")}
HDRS = [{"properties": {"fontColor": solid(INK3), "fontSize": lit("9D"),
                        "backColor": solid(SURFACE)}}]
VALS = [{"properties": {"fontColor": solid(INK), "fontSize": lit("9D"),
                        "backColorPrimary": solid(SURFACE),
                        "backColorSecondary": solid(SURFACE)}}]
NOTOT = [{"properties": {"totals": lit("false")}}]


def table(name, rect, projections, grid_extra=None, z=200, values_extra=None):
    g = dict(GRID)
    if grid_extra:
        g.update(grid_extra)
    vals = VALS
    if values_extra:
        p = dict(VALS[0]["properties"])
        p.update(values_extra)
        vals = [{"properties": p}]
    return vis(name, "tableEx", rect, z,
               query={"Values": {"projections": projections}},
               objects={"grid": [{"properties": g}], "columnHeaders": HDRS,
                        "values": vals, "total": NOTOT})


def sort_by(v, field, direction="Descending"):
    """sortDefinition is a SIBLING of queryState, not inside it."""
    v["visual"]["query"]["sortDefinition"] = {"sort": [{"field": field, "direction": direction}]}
    return v


def kpi(d, name, rect, meas, title, colour=INK, size="30D", units=None, prec=None, note=None):
    head, body = stack(rect)
    if note:
        body = dict(body, height=body["height"] - 40)
    write(d, name + "H", head_tb(name + "H", head, title))
    props = {"color": solid(colour), "fontSize": lit(size),
             "fontFamily": lit("'Segoe UI Semibold'")}
    if units:
        props["labelDisplayUnits"] = lit(units)
    if prec is not None:
        props["labelPrecision"] = lit(prec)
    write(d, name, vis(name, "card", body, 200,
                       query={"Values": {"projections": [proj_m(meas)]}},
                       objects={"labels": [{"properties": props}],
                                "categoryLabels": [{"properties": {"show": lit("false")}}]}))
    if note:
        write(d, name + "N", textbox(name + "N",
                                     {"x": rect["x"], "y": body["y"] + body["height"] + 8,
                                      "width": rect["width"], "height": 32},
                                     [(note, ts("9pt", INK2))]))


# ---- global chrome -------------------------------------------------------------------
# Three synced dropdowns, the cap the room sets. All three are ATTRIBUTES of the sale, not
# measures of it, so filtering any of them leaves every visual on the page still meaningful.
FILTERS = [
    ("fltRealm", "DimShop", "Realm", "flt_realm"),
    ("fltCategory", "DimItem", "Category", "flt_category"),
    ("fltYear", "DimDate", "Year", "flt_year"),
]


def slicer(name, rect, entity, prop, group, tab=1):
    proj = proj_c(entity, prop)
    proj["active"] = True
    v = vis(name, "slicer", rect, 800,
            query={"Values": {"projections": [proj]}},
            objects={"data": [{"properties": {"mode": lit(Q + "Dropdown" + Q)}}]},
            vco={"title": [{"properties": {"show": lit("false")}}]}, tab=tab)
    # syncGroup is a SIBLING of visualType. Without it each page keeps its own selection and
    # a cross-page comparison silently lies.
    v["visual"]["syncGroup"] = {"groupName": group, "fieldChanges": True, "filterChanges": True}
    return v


def chrome_rects():
    """Caption + slicer rects inside header_filters. Shared with the auditor so the builder
    and the layout check cannot drift."""
    f = rects("header_filters")[0]
    cap = {"x": f["x"], "y": f["y"], "width": f["width"], "height": 24}
    sw, sh = DS["defaults"]["slicer"]["size"]
    gap = (f["width"] - sw * len(FILTERS)) // (len(FILTERS) - 1)
    slicers = [{"x": f["x"] + i * (sw + gap), "y": f["y"] + 32, "width": sw, "height": sh}
               for i in range(len(FILTERS))]
    return cap, slicers


def page_chrome(d, title, sub):
    """Wordmark + selection caption + the three synced slicers. Identical on every page.

    All of it sits INSIDE the header band, so adding the chrome costs no content height.
    """
    t = rects("header_title")[0]
    write(d, "pageTitle", textbox("pageTitle", t, [
        (title, ts("20pt", INK, "Segoe UI Semibold")), (sub, ts("10pt", INK2))]))

    cap, slicers = chrome_rects()
    # a card, not a textbox: the caption has to name whatever is currently selected, and a
    # textbox cannot read filter context
    write(d, "selCaption", vis("selCaption", "card", cap, 850,
                               query={"Values": {"projections": [proj_m("Selection Caption")]}},
                               objects={"labels": [{"properties": {
                                   "color": solid(INK3), "fontSize": lit("10D"),
                                   "fontFamily": lit("'Segoe UI'"),
                                   "horizontalAlignment": lit("'right'"),
                                   "wordWrap": lit("false")}}],
                                   "categoryLabels": [{"properties": {"show": lit("false")}}]},
                               vco=noframe()))
    for i, (nm, ent, prop, grp) in enumerate(FILTERS):
        write(d, nm, slicer(nm, slicers[i], ent, prop, grp, tab=i + 1))
