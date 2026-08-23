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


ROOT = os.path.dirname(os.path.abspath(__file__))
FACT = "FactSales"
M = "_Measures"

# Runeforge Dark v1.0 - keep in step with projects/themes/runeforge/notes.md
INK, INK2, INK3 = "#F2EAE0", "#CDC2B4", "#9E9285"
CANVAS, SURFACE, RULE = "#100E0C", "#1A1714", "#342E28"
BLUE, GOLD, VERD, PLUM = "#B2C6ED", "#C7A726", "#33A095", "#B74BC3"
CRIMSON, FOREST, BRONZE, IRON = "#E9A7B0", "#3BB16C", "#BF7240", "#5F6E7E"

# ---- shared PBIR core lives in the room (one copy for every project) ------------------
WS = os.path.normpath(os.path.join(ROOT, "..", "..", "02-build", "report"))
sys.path[:0] = [os.path.join(WS, "tools"), os.path.join(WS, "layout")]
import pbirkit as K  # noqa: E402
DS = K.configure(root=ROOT, report="arcane-emporium.Report", fact="FactSales", palette=dict(INK=INK, INK2=INK2, INK3=INK3, CANVAS=CANVAS, SURFACE=SURFACE, RULE=RULE, BLUE=BLUE, GOLD=GOLD, VERD=VERD, PLUM=PLUM, CRIMSON=CRIMSON, FOREST=FOREST, BRONZE=BRONZE, IRON=IRON))
from pbirkit import *  # noqa: E402,F401,F403  (after configure: DS/PAGES/palette are bound)


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
