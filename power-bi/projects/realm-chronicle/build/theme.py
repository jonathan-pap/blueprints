"""theme - Realm Chronicle Dark: the theme the interactive pages' native visuals inherit.

Approved 2026-09-13 (the blueprint rule is never to create a theme unless asked - this was asked).
Derived from the validated library theme Gilded Arcanum (../../themes/gilded-arcanum/), per
02-build/theme/create/starting-point.md - never authored from an empty {}. Changes are the minimum
to match the report: its own accent palette, light body text for readability, subtle borders like
the HTML panels, dark table/slicer surfaces, and chrome suppressed on textbox/image/shape/actionButton
(the create/checklist.md requirement Gilded Arcanum lacks).

The HTML pages stay as designed ONLY because image/actionButton/textbox/shape get zero padding here -
their visuals set title/background/border off themselves, but padding cascades from the wildcard.
Output: projects/themes/realm-chronicle-dark/realm-chronicle-dark-v1.0.json (the library copy).
"""
import copy
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = os.path.normpath(os.path.join(HERE, "..", "..", "themes"))
BASE = os.path.join(THEMES, "gilded-arcanum", "gilded-arcanum-v1.0.json")
OUT_DIR = os.path.join(THEMES, "realm-chronicle-dark")
NAME = "Realm Chronicle Dark v1.0"
FILE = "realm-chronicle-dark-v1.0.json"

CANVAS, SURFACE, SURFACE_2, LINE, LINE_SOFT = "#070B14", "#0D1524", "#16243C", "#2A3953", "#1B243A"
TEXT, MUTED, FAINT = "#E8EDF5", "#8AA0C0", "#56688A"
GOLD, GOLD_BRIGHT = "#E8C349", "#F0CF5E"


def solid(c):
    return {"solid": {"color": c}}


def build():
    t = copy.deepcopy(json.load(io.open(BASE, encoding="utf-8")))
    t["name"] = NAME
    # the report's own accents - same order the HTML panels use, gold first as the primary series
    t["dataColors"] = ["#E8C349", "#7CC8FF", "#6FD49B", "#FF7B7B", "#C89BFF", "#F97316", "#5CC8D6", "#D08A4C"]
    t.update({"good": "#6FD49B", "bad": "#FF7B7B", "neutral": "#F2C037",
              "foreground": TEXT, "foregroundNeutralSecondary": MUTED, "foregroundNeutralTertiary": FAINT,
              "foregroundDark": CANVAS, "background": SURFACE, "backgroundLight": CANVAS,
              "backgroundNeutral": SURFACE_2, "backgroundDark": "#050810",
              "tableAccent": GOLD, "accent": GOLD, "hyperlink": "#7CC8FF", "shapeStroke": LINE})

    tc = t.setdefault("textClasses", {})
    tc["title"] = {"fontFace": "Georgia", "fontSize": 13, "color": GOLD}
    tc["header"] = {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": TEXT}
    tc["label"] = {"fontFace": "Segoe UI", "fontSize": 10, "color": MUTED}
    tc["callout"] = {"fontFace": "Segoe UI Semibold", "fontSize": 26, "color": GOLD_BRIGHT}
    tc["dataTitle"] = {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": TEXT}

    vs = t.setdefault("visualStyles", {})
    w = vs.setdefault("*", {}).setdefault("*", {})
    w["background"] = [{"show": True, "color": solid(SURFACE), "transparency": 0}]
    w["border"] = [{"show": True, "color": solid(LINE), "radius": 12}]
    w["dropShadow"] = [{"show": False}]
    w["title"] = [{"show": True, "fontColor": solid(GOLD), "fontFamily": "Georgia", "fontSize": 13}]
    w["subTitle"] = [{"show": False}]
    w["padding"] = [{"top": 10, "bottom": 10, "left": 12, "right": 12}]
    w["categoryAxis"] = [{"labelColor": solid(MUTED), "titleColor": solid(MUTED), "gridlineColor": solid(LINE_SOFT)}]
    w["valueAxis"] = [{"labelColor": solid(MUTED), "titleColor": solid(MUTED), "gridlineColor": solid(LINE_SOFT)}]
    w["legend"] = [{"labelColor": solid(MUTED)}]
    w["labels"] = [{"color": solid(TEXT)}]

    # container chrome off where it never belongs (create/checklist.md) - and padding ZERO. Without it the
    # wildcard padding reaches every image visual: an HTML-in-SVG panel or the nav rail then scales down
    # to fit inside the padding and renders shrunken with uneven gaps (seen on Intro, 2026-09-13).
    off = {"title": [{"show": False}], "background": [{"show": False}], "border": [{"show": False}],
           "padding": [{"top": 0, "bottom": 0, "left": 0, "right": 0}]}
    for vt in ("textbox", "image", "shape", "actionButton"):
        vs.setdefault(vt, {})["*"] = copy.deepcopy(off)

    vs.setdefault("slicer", {})["*"] = {
        "background": [{"show": True, "color": solid(SURFACE), "transparency": 0}],
        "header": [{"fontColor": solid(MUTED)}],
        "items": [{"fontColor": solid(TEXT), "background": solid(SURFACE)}]}
    table = {
        "columnHeaders": [{"fontColor": solid(GOLD), "backColor": solid(SURFACE_2)}],
        "values": [{"fontColorPrimary": solid(TEXT), "backColorPrimary": solid(SURFACE),
                    "fontColorSecondary": solid(TEXT), "backColorSecondary": solid(CANVAS)}],
        "grid": [{"gridHorizontalColor": solid(LINE_SOFT), "gridVerticalColor": solid(LINE_SOFT),
                  "outlineColor": solid(LINE)}],
        "total": [{"fontColor": solid(GOLD_BRIGHT), "backColor": solid(SURFACE_2)}]}
    vs.setdefault("tableEx", {})["*"] = copy.deepcopy(table)
    pivot = copy.deepcopy(table)
    pivot["rowHeaders"] = [{"fontColor": solid(TEXT), "backColor": solid(SURFACE)}]
    vs.setdefault("pivotTable", {})["*"] = pivot

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, FILE)
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(t, indent=2) + "\n")
    return path


if __name__ == "__main__":
    print(build())
