"""Page/visual builder for the churn report. All geometry comes from design-system.yaml."""
import json
import os
import shutil
import subprocess
import sys

import resolve_layout as RL

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(ROOT, "telecom-churn.Report")
PAGES = os.path.join(REPORT, "definition", "pages")
SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
          "definition/visualContainer/2.10.0/schema.json")
FACT = "telecom_customer_churn"
Q = chr(39)

# Spectrum (Light) - keep in step with build_theme.py, which is the audited source of truth
INK, INK2, INK3 = "#0B1020", "#4A5578", "#6E7A9C"
CHURNED, STAYED, JOINED = "#9D174D", "#0E7490", "#9575F5"
SURFACE, RULE, CANVAS = "#FFFFFF", "#DEE4F2", "#F1F4FB"

DS = RL.load(os.path.join(ROOT, RL.DS))


def rects(layout_name):
    return RL.layout(layout_name, DS)


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def solid(c):
    return {"solid": {"color": lit("'%s'" % c)}}


def measure(name):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": name}}


def col(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def proj_m(name, disp=None):
    p = {"field": measure(name), "queryRef": "_Measures." + name, "nativeQueryRef": name}
    if disp:
        p["displayName"] = disp
    return p


def proj_c(entity, prop, disp=None):
    p = {"field": col(entity, prop), "queryRef": "%s.%s" % (entity, prop), "nativeQueryRef": prop}
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
    if run("pbir", "add", "page", "telecom-churn.Report/%s.Page" % display, "-n", display):
        sys.exit("add page failed: " + display)
    new = sorted(set(os.listdir(PAGES)) - before)
    run("pbir", "pages", "rename", "telecom-churn.Report/%s.Page" % display, "--to", pid, "-f")
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
    # drop entries with no folder on disk - a half-deleted page otherwise lingers in
    # pageOrder forever and Desktop shows a phantom tab
    live = set(os.listdir(PAGES))
    meta["pageOrder"] = [x for x in meta["pageOrder"] if x in live]
    meta["activePageName"] = meta["pageOrder"][0]
    json.dump(meta, open(meta_p, "w", encoding="utf-8", newline="\n"), indent=2)
    # remove the auto Title textbox
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


def textbox(name, rect, runs, z=900):
    paras = [{"textRuns": [{"value": v, "textStyle": s}]} for v, s in runs]
    return vis(name, "textbox", rect, z,
               query={}, objects={"general": [{"properties": {"paragraphs": paras}}]},
               vco=noframe())


def ts(size, colour=INK, face="Segoe UI"):
    return {"fontFamily": face, "fontSize": size, "color": colour}


def noframe():
    off = [{"properties": {"show": lit("false")}}]
    return {"title": off, "background": off, "border": off}


def panel():
    """Card chrome. The container TITLE is always off: setting title.text on a chart makes
    Power BI render the custom title AND its auto-generated name ("Churned Customers by
    Churn Category") stacked. Every heading is a textbox instead - deterministic, and it is
    the pattern the rest of the workspace already uses."""
    return {"title": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("true"), "color": solid(SURFACE),
                                           "transparency": lit("0D")}}],
            "border": [{"properties": {"show": lit("true"), "color": solid(RULE),
                                       "radius": lit("6D")}}]}


def heading(name, rect, title, sub=None, pad=14, z=950):
    """Heading textbox pinned inside a panel's top edge."""
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    h = 44 if sub else 26
    return textbox(name, {"x": rect["x"] + pad, "y": rect["y"] + 8,
                          "width": rect["width"] - 2 * pad, "height": h}, runs, z=z)


def inset(rect, top=38, pad=8, bottom=8):
    """Content rect inside a panel, below its heading."""
    return {"x": rect["x"] + pad, "y": rect["y"] + top,
            "width": rect["width"] - 2 * pad, "height": rect["height"] - top - bottom}


def image_svg(name, rect, measure_name, z=100):
    return vis(name, "image", rect, z,
               objects={"image": [{"properties": {
                   "sourceType": lit("'imageData'"), "transparency": lit("0D"),
                   "effects": lit("false"), "fit": lit("'Fit'"),
                   "sourceField": {"expr": measure(measure_name)}}}]},
               vco=noframe())

def stack(rect, sub=False, gap=8):
    """Split a region into a heading strip (on the canvas) and a content rect below it.

    Panels-as-shapes were abandoned: a shape visual would not render its fill even with
    objects.fill set explicitly. Every content visual instead carries its OWN themed white
    card (theme `*` sets background + border), and the heading sits above it on the canvas.
    Fewer visuals, nothing to keep in sync, and no z-order to reason about.
    """
    # heading heights and the gap are all multiples of the 8px snap, so the derived content
    # rect stays on-grid - the audit caught 44 off-snap coordinates when gap was 6
    h = 40 if sub else 24
    head = {"x": rect["x"], "y": rect["y"], "width": rect["width"], "height": h}
    body = {"x": rect["x"], "y": rect["y"] + h + gap,
            "width": rect["width"], "height": rect["height"] - h - gap}
    return head, body


def head_tb(name, rect, title, sub=None):
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    return textbox(name, rect, runs, z=900)


# ---- global chrome -------------------------------------------------------------------
# Three synced dropdowns - the cap the room sets ("Limit to 3 slicers per page - extras
# belong in the filter pane", 02-build/report/add-visual/slicer.md).
#
# Customer Status is deliberately NOT one of them. It is the comparison axis the whole
# report is built on: filtering it would blank two of the three columns in the profile
# matrix, collapse the waffle, and make the tornado compare a segment against a baseline
# that no longer exists. Status is communicated by the LEGEND instead. The three slicers
# are attributes - things you would want to hold constant while comparing statuses.
FILTERS = [
    ("fltContract", "Contract", "flt_contract"),
    ("fltInternet", "Internet", "flt_internet"),
    ("fltTenure", "Tenure Band", "flt_tenure"),
]


def slicer(name, rect, prop, group, tab=1):
    proj = proj_c(FACT, prop)
    proj["active"] = True
    v = vis(name, "slicer", rect, 800,
            query={"Values": {"projections": [proj]}},
            objects={"data": [{"properties": {"mode": lit(Q + "Dropdown" + Q)}}]},
            vco={"title": [{"properties": {"show": lit("false")}}]}, tab=tab)
    # syncGroup is a SIBLING of visualType, not an object. Without it every page keeps its
    # own selection and a cross-page comparison silently lies
    # (02-build/report/references/anti-patterns.md, cluster 6).
    v["visual"]["syncGroup"] = {"groupName": group, "fieldChanges": True,
                                "filterChanges": True}
    return v


def in_filter(entity, prop, values, fname):
    """Categorical In-filter over several values of one column."""
    src = {"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": prop}}
    return {"name": fname,
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}},
                                 "Property": prop}},
            "type": "Categorical",
            "filter": {"Version": 2,
                       "From": [{"Name": "f", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"In": {
                           "Expressions": [src],
                           "Values": [[{"Literal": {"Value": Q + v + Q}}] for v in values]}}}]},
            "howCreated": "User"}


def chrome_rects():
    """Legend + slicer rects inside the header_filters region.

    Shared with audit_report.py: three slicers tile inside ONE region, so their inner
    origins are not region edges. The auditor derives them from here rather than from a
    hardcoded allow-list, so the two can never drift.
    """
    f = rects("header_filters")[0]
    lw, lh = DS["defaults"]["legend"]["size"]
    # right-aligned; the SVG viewBox is authored at exactly lw x lh so the image visual
    # maps 1:1 instead of letterboxing
    legend = {"x": f["x"] + f["width"] - lw, "y": f["y"], "width": lw, "height": lh}
    sw, sh = DS["defaults"]["slicer"]["size"]
    gap = (f["width"] - sw * len(FILTERS)) // (len(FILTERS) - 1)
    slicers = [{"x": f["x"] + i * (sw + gap), "y": f["y"] + 32, "width": sw, "height": sh}
               for i in range(len(FILTERS))]
    return legend, slicers


def page_chrome(d, title, sub):
    """Wordmark + global legend + the three synced slicers. Identical on every page.

    All of it lives INSIDE the header band (design-system.yaml header_title /
    header_filters), so adding the chrome cost no content height on any page.
    """
    t = rects("header_title")[0]
    write(d, "pageTitle", textbox("pageTitle", t, [
        (title, ts("20pt", INK, "Segoe UI Semibold")), (sub, ts("10pt", INK2))]))

    legend, slicers = chrome_rects()
    write(d, "statusLegend", image_svg("statusLegend", legend, "Status Legend", z=850))
    for i, (nm, prop, grp) in enumerate(FILTERS):
        write(d, nm, slicer(nm, slicers[i], prop, grp, tab=i + 1))


# ---- tooltip pages -------------------------------------------------------------------
# Every visual that carries an SVG measure showed its raw data: URI in the default tooltip.
# A report-page tooltip REPLACES the default one outright, which fixes that and buys room
# for context the cell could never hold. Four pages, one per hover context - a tooltip built
# for the wrong context is worse than none: a churn RATE inside a churn-reason row is 100%
# by construction, and inside a Customer Status row it is circular.
TOOLTIP_MAP = {
    "categoryBar": "ttReason", "reasonTable": "ttReason",
    "divTableA": "ttAttr", "divTableB": "ttAttr", "tornado": "ttAttr",
    "dContract": "ttSegment", "dTenure": "ttSegment", "dInternet": "ttSegment",
    "dPayment": "ttSegment", "dSecurity": "ttSegment", "dSupport": "ttSegment",
    "revQ": "ttSegment", "chgQ": "ttSegment", "cityTable": "ttSegment",
    "shortTable": "ttCustomer",
}

TT_W, TT_H = 320, 240


def add_tooltip_page(pid, display):
    """A hidden, ActualSize page marked type=Tooltip. Built by hand rather than via
    `pbir add page` because the CLI has no flag for the type/visibility pair."""
    d = os.path.join(PAGES, pid)
    os.makedirs(os.path.join(d, "visuals"), exist_ok=True)
    page = {
        "$schema": ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
                    "definition/page/2.3.1/schema.json"),
        "name": pid, "displayName": display,
        "width": TT_W, "height": TT_H,
        # tooltip pages do not scale - FitToPage would letterbox them
        "displayOption": "ActualSize",
        "type": "Tooltip",
        "visibility": "HiddenInViewMode",
        "objects": {"background": [{"properties": {"color": solid(SURFACE),
                                                   "transparency": lit("0D")}}]},
    }
    with open(os.path.join(d, "page.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(page, f, indent=2)
        f.write("\n")
    meta_p = os.path.join(PAGES, "pages.json")
    meta = json.load(open(meta_p, encoding="utf-8"))
    if pid not in meta["pageOrder"]:
        meta["pageOrder"].append(pid)
    json.dump(meta, open(meta_p, "w", encoding="utf-8", newline="\n"), indent=2)
    print("  tooltip page %s (%dx%d)" % (pid, TT_W, TT_H))
    return d


def tt_card(name, rect, meas, label, colour=INK, size="15D", units=None, prec=None,
            show_label=True):
    """A card that labels itself. On a tooltip the measure's displayName IS the caption, so
    no separate heading textbox is needed - half the visuals, half the geometry."""
    props = {"color": solid(colour), "fontSize": lit(size),
             "fontFamily": lit("'Segoe UI Semibold'"), "wordWrap": lit("true")}
    if units:
        props["labelDisplayUnits"] = lit(units)
    if prec is not None:
        props["labelPrecision"] = lit(prec)
    return vis(name, "card", rect, 200,
               query={"Values": {"projections": [proj_m(meas, label)]}},
               objects={"labels": [{"properties": props}],
                        "categoryLabels": [{"properties": {
                            "show": lit("true" if show_label else "false"),
                            "color": solid(INK3), "fontSize": lit("9D")}}]},
               vco=panel())


def tt_title(name, meas, colour=INK):
    return vis(name, "card", {"x": 8, "y": 8, "width": 304, "height": 32}, 300,
               query={"Values": {"projections": [proj_m(meas)]}},
               objects={"labels": [{"properties": {
                   "color": solid(colour), "fontSize": lit("13D"),
                   "fontFamily": lit("'Segoe UI Semibold'"),
                   "horizontalAlignment": lit("'left'"), "wordWrap": lit("false")}}],
                        "categoryLabels": [{"properties": {"show": lit("false")}}]},
               vco=noframe())


def tt_grid():
    """Four card rects in a 2x2 under the title, plus the footer strip."""
    # Every number here is a multiple of the 8px snap, same as the report pages - a
    # 320x240 popup is not on the 12x12 grid, but there is no reason for it to sit off
    # the pixel snap. Title 8..40, cards 48..112 and 120..184, footer 192..232.
    # The footer needs the full 40: at 24 it clipped its second line and drew a scroll
    # indicator - the same "there is more below" lie the page-2 and page-4 tables told.
    cells = [{"x": x, "y": y, "width": 144, "height": 64}
             for y in (48, 120) for x in (8, 168)]
    foot = {"x": 8, "y": 192, "width": 304, "height": 40}
    return cells, foot


def apply_tooltips():
    """Point every mapped visual at its tooltip page. Run AFTER the pages are built.

    visualTooltip lives in visualContainerObjects; `section` is the tooltip page's `name`,
    NOT its displayName.
    """
    n = 0
    for page in sorted(os.listdir(PAGES)):
        vdir = os.path.join(PAGES, page, "visuals")
        if not os.path.isdir(vdir):
            continue
        for nm in sorted(os.listdir(vdir)):
            tt = TOOLTIP_MAP.get(nm)
            if not tt:
                continue
            p = os.path.join(vdir, nm, "visual.json")
            v = json.load(open(p, encoding="utf-8"))
            v["visual"].setdefault("visualContainerObjects", {})["visualTooltip"] = [
                {"properties": {"show": lit("true"),
                                "type": lit(Q + "ReportPage" + Q),
                                "section": lit(Q + tt + Q)}}]
            json.dump(v, open(p, "w", encoding="utf-8", newline="\n"), indent=2)
            n += 1
    print("  tooltips wired: %d visuals" % n)
