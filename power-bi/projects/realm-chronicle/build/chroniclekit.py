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


def svg_panel(name, rect, measure_name, alt, z, tab):
    """An HTML-in-SVG component: the room's image_svg() plus alt text and a real tab order,
    which image_svg() leaves at its defaults. Alt text matters here - the component is an image,
    so without it a screen reader announces nothing."""
    v = K.image_svg(name, rect, measure_name, z=z)
    v["visual"]["objects"]["image"][0]["properties"]["altText"] = K.lit("'%s'" % alt.replace("'", "''"))
    v["position"]["tabOrder"] = tab
    return v
