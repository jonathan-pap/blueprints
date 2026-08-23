"""Page/visual builder for the churn report. All geometry comes from design-system.yaml."""
import json
import os
import shutil
import subprocess
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
FACT = "telecom_customer_churn"

# Spectrum (Light) - keep in step with build_theme.py, which is the audited source of truth
INK, INK2, INK3 = "#0B1020", "#4A5578", "#6E7A9C"
CHURNED, STAYED, JOINED = "#9D174D", "#0E7490", "#9575F5"
SURFACE, RULE, CANVAS = "#FFFFFF", "#DEE4F2", "#F1F4FB"

# ---- shared PBIR core lives in the room (one copy for every project) ------------------
WS = os.path.normpath(os.path.join(ROOT, "..", "..", "02-build", "report"))
sys.path[:0] = [os.path.join(WS, "tools"), os.path.join(WS, "layout")]
import pbirkit as K  # noqa: E402
DS = K.configure(root=ROOT, report="telecom-churn.Report", fact="telecom_customer_churn", palette=dict(INK=INK, INK2=INK2, INK3=INK3, CHURNED=CHURNED, STAYED=STAYED, JOINED=JOINED, SURFACE=SURFACE, RULE=RULE, CANVAS=CANVAS))
from pbirkit import *  # noqa: E402,F401,F403  (after configure: DS/PAGES/palette are bound)


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
