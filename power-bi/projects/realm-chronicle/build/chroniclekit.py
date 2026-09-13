"""chroniclekit - Realm Chronicle project specifics, on top of the room core (pbirkit).

Only what belongs to THIS project lives here: where the report is, which model table holds the
HTML measures, and the dark canvas those components are designed for. Everything reusable is in
../../../02-build/report/tools/pbirkit.py - import it, don't fork it.

Naming: the file-map convention says build/<name>kit.py, but a hyphenated module name
(realm-chroniclekit) cannot be imported, so the kit takes a short word - as churnkit and
emporiumkit did before it.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
TOOLS = os.path.normpath(os.path.join(ROOT, "..", "..", "02-build", "report", "tools"))
sys.path.insert(0, TOOLS)

import pbirkit as K  # noqa: E402

K.configure(
    root=ROOT,
    report="realm-chronicle.Report",
    # HTML measures live in their own table: the synthetic-data hand-off rewrites
    # _Measures.tmdl on every run and would delete anything added there.
    measures_table="_HTML",
    ds_path=os.path.join(ROOT, "design-system.yaml"),
)

CANVAS = "#070B14"     # the page
OUTSPACE = "#04070D"   # the area around the page


def dark_canvas(page_dir):
    """Paint a page dark. The HTML-in-SVG components carry their own dark surfaces; on Power BI's
    default light page they'd sit in white margins - the 'white-on-white' gotcha, inverted."""
    pj = os.path.join(page_dir, "page.json")
    pg = json.load(open(pj, encoding="utf-8"))
    pg["objects"] = {
        "background": [{"properties": {"color": K.solid(CANVAS), "transparency": K.lit("0D")}}],
        "outspace": [{"properties": {"color": K.solid(OUTSPACE), "transparency": K.lit("0D")}}],
    }
    json.dump(pg, open(pj, "w", encoding="utf-8", newline="\n"), indent=2)


# ---- pages + the navigation rail (design A, "Gilded Rail", approved 2026-09-13) -------------
# The report's pages in rail order. Flip `built` when a page gets content. An unbuilt page still
# appears on the rail - dimmed, with no button - so the rail tells the whole story from the first
# page onward without a single dead link.
PAGES = [
    {"id": "intro",    "display": "Intro",        "label": "INTRO",    "icon": "intro", "built": True},
    {"id": "hunt",     "display": "The Hunt",     "label": "THE HUNT", "icon": "hunt",  "built": True},
    {"id": "quests",   "display": "Quest Board",  "label": "QUESTS",   "icon": "quest", "built": False},
    {"id": "exchange", "display": "The Exchange", "label": "EXCHANGE", "icon": "trade", "built": False},
    {"id": "realms",   "display": "Realm Map",    "label": "REALMS",   "icon": "map",   "built": False},
]

RAIL_W, RAIL_H = 88, 1080            # fixed chrome, outside the content grid (recorded in overrides:)
ITEM_TOP, ITEM_STEP, ITEM_H = 104, 88, 72   # every edge a multiple of the 8px snap
GOLD, MUTED, DIM = "#e8c349", "#8aa0c0", "#3a4a66"

# 24-unit line icons - the same set as the approved mockup.
ICONS = {
    "crest": ["M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z", "M8.5 12.5l2.5 2.5 4.5-5"],
    "intro": ["M3 18h18", "M4 18L3 8l5 4 4-6 4 6 5-4-1 10"],
    "hunt":  ["M5 3l12 12", "M19 3L7 15", "M4 16l4 4", "M16 20l4-4"],
    "quest": ["M7 4h11a2 2 0 010 4H9", "M7 4a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V8", "M9 12h6M9 15.5h6"],
    "trade": ["M12 4v16M8 20h8M5 7h14", "M5 7l-3 6a3 3 0 006 0z", "M19 7l-3 6a3 3 0 006 0z"],
    "map":   ["M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z", "M9 4v14M15 6v14"],
}


def _icon(name, x, y, size, colour):
    s = size / 24.0
    paths = "".join("<path d='%s'/>" % d for d in ICONS[name])
    return ("<g transform='translate(%d,%d) scale(%.4f)' fill='none' stroke='%s' stroke-width='%.3f' "
            "stroke-linecap='round' stroke-linejoin='round'>%s</g>" % (x, y, s, colour, 1.6 / s, paths))


def rail_svg(active_id):
    """The rail artwork for one page, active item baked in. Pure SVG, no foreignObject: nav chrome
    must survive PDF/PowerPoint export, which blanks foreignObject content."""
    p = ["<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 %d %d'>" % (RAIL_W, RAIL_H, RAIL_W, RAIL_H),
         "<defs>",
         "<linearGradient id='bg' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#121b2d'/><stop offset='1' stop-color='#090e19'/></linearGradient>",
         "<radialGradient id='wash' cx='0' cy='0.5' r='0.9'><stop offset='0' stop-color='#e8c349' stop-opacity='0.18'/><stop offset='1' stop-color='#e8c349' stop-opacity='0'/></radialGradient>",
         "</defs>",
         "<rect width='%d' height='%d' fill='url(#bg)'/>" % (RAIL_W, RAIL_H),
         "<rect x='%d' y='0' width='1' height='%d' fill='#2a3953'/>" % (RAIL_W - 1, RAIL_H),
         _icon("crest", 30, 30, 28, GOLD),
         "<rect x='26' y='80' width='36' height='1' fill='#2a3953'/>"]
    for i, pg in enumerate(PAGES):
        y = ITEM_TOP + i * ITEM_STEP
        active = pg["id"] == active_id
        colour = GOLD if active else (MUTED if pg["built"] else DIM)
        if active:
            p += ["<rect x='0' y='%d' width='%d' height='%d' fill='url(#wash)'/>" % (y, RAIL_W, ITEM_H),
                  "<rect x='0' y='%d' width='8' height='%d' fill='#e8c349' opacity='0.16'/>" % (y + 6, ITEM_H - 12),
                  "<rect x='0' y='%d' width='3' height='%d' rx='1.5' fill='#e8c349'/>" % (y + 10, ITEM_H - 20)]
        p.append(_icon(pg["icon"], 33, y + 13, 22, colour))
        p.append("<text x='44' y='%d' text-anchor='middle' font-family='Segoe UI,Arial,sans-serif' font-size='9.5' "
                 "font-weight='600' letter-spacing='1' fill='%s'>%s</text>" % (y + 57, colour, pg["label"]))
    # the chronicle's span, set like a date on a manuscript spine
    p.append("<text transform='translate(48,1048) rotate(-90)' font-family='Georgia,serif' font-size='10' "
             "letter-spacing='3' fill='#9a7a1c'>MMXXIII &#8211; MMXXVI</text>")
    p.append("</svg>")
    return "".join(p)


def nav_rail(page_dir, active_id):
    """Stamp the rail onto a page: its artwork (a registered SVG, one per page so the active item
    is baked in), plus a button over every OTHER built page."""
    current = next(pg["display"] for pg in PAGES if pg["id"] == active_id)
    alt = "Page navigation. You are on %s. Pages: %s." % (current, ", ".join(pg["display"] for pg in PAGES))
    item = "navRail-%s.svg" % active_id
    K.register_image(item, rail_svg(active_id))
    K.write(page_dir, "navRail",
            K.image_resource("navRail", {"x": 0, "y": 0, "width": RAIL_W, "height": RAIL_H},
                             item, alt, z=50, tab=0))
    tab = 1
    for i, pg in enumerate(PAGES):
        if not pg["built"] or pg["id"] == active_id:
            continue
        name = "nav" + pg["id"].capitalize()
        rect = {"x": 0, "y": ITEM_TOP + i * ITEM_STEP, "width": RAIL_W, "height": ITEM_H}
        K.write(page_dir, name, K.nav_button(name, rect, pg["id"], "Go to " + pg["display"],
                                             z=60 + i, tab=tab, hover=GOLD, hover_transparency=86))
        tab += 1


def svg_panel(name, rect, measure_name, alt, z, tab):
    """An HTML-in-SVG component: the room's image_svg() plus alt text and a real tab order,
    which image_svg() leaves at its defaults. Alt text matters here - the component is an image,
    so without it a screen reader announces nothing."""
    v = K.image_svg(name, rect, measure_name, z=z)
    v["visual"]["objects"]["image"][0]["properties"]["altText"] = K.lit("'%s'" % alt.replace("'", "''"))
    v["position"]["tabOrder"] = tab
    return v
