#!/usr/bin/env python3
"""Finish the demo build: header band, titles, slicer mode, corner radius.

Everything `pbir add visual` cannot do, in one deterministic pass. Re-running is safe -
it sets absolute values rather than nudging.

WHY THE HEADER BAND IS 56px AND NOT THE GRID'S 40px
    One 12x12 grid row resolves to 40px at 1280x720. That is enough for a text run but
    NOT for a labelled slicer: a slicer draws its own header plus the dropdown control,
    and at 40px you get the header and a sliver - the exact defect from the v1 build.
    So the header band takes 56px on every page and content starts at 96. Page 1 has no
    slicers but keeps the same band, because a title that changes height page to page is
    the kind of drift nobody notices and everybody feels.

Traps this file exists to avoid (02-build/report/validate/build-traps.md):
  #5  `pbir add title` writes 24pt into a 65px box -> scrollbar. 16pt in 56px fits.
  #6  slicers default to LIST mode and need ~160px. Dropdown, and hide the container
      title so the field name does not render twice.
  #11 theme corner radius does not reach visuals. Set `border.radius` per visual.
"""
import io
import json
import os
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "demo.Report", "definition", "pages")

TITLE_PT = 16
RADIUS = 6
VC_SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
             "definition/visualContainer/2.9.0/schema.json")

# page -> visual -> (x, y, width, height).  Header band 24..80, content from 96.
RECTS = {
    "Guild_Overview": {
        "pageTitle":       (24, 24, 1232, 56),
        "kpiBounty":       (24, 96, 400, 104),
        "kpiQuests":       (440, 96, 192, 104),
        "kpiAvgBounty":    (648, 96, 192, 104),
        "kpiAvgDays":      (856, 96, 192, 104),
        "kpiAdventurers":  (1064, 96, 192, 104),
        "trendLine":       (24, 216, 1232, 248),
        "realmBar":        (24, 480, 608, 216),
        "dangerBar":       (648, 480, 608, 216),
    },
    "Quest_Board": {
        "pageTitle":       (24, 24, 920, 56),
        "fltYear":         (960, 24, 296, 56),
        "questPareto":     (24, 96, 1232, 256),
        "questScatter":    (24, 368, 608, 328),
        "realmDanger":     (648, 368, 608, 328),
    },
    "Adventurer_Roster": {
        "pageTitle":       (24, 24, 608, 56),
        "fltRealm":        (648, 24, 296, 56),
        "fltRank":         (960, 24, 296, 56),
        "rankBar":         (24, 96, 608, 256),
        "topAdventurers":  (648, 96, 608, 256),
        "rosterTable":     (24, 368, 1232, 328),
    },
}

# Insight titles, not page labels. Every number here was verified with a DAX query
# against the live model before it was written down - see the build log.
TITLES = {
    "Guild_Overview":
        "6.0M in bounty across three realms — Eldoria's halls carry two-fifths of it",
    "Quest_Board":
        "Five of eight quest types carry 80% of the bounty",
    "Adventurer_Roster":
        "Gold rank takes 40% of the bounty — the roster shows who actually earns it",
}

SLICERS = {("Quest_Board", "fltYear"),
           ("Adventurer_Roster", "fltRealm"),
           ("Adventurer_Roster", "fltRank")}


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def vpath(page, visual):
    return os.path.join(PAGES, page, "visuals", visual, "visual.json")


def write(path, d):
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def make_title(page, rect, text):
    """Textbox title. 16pt in a 56px box - the pairing that does not scroll."""
    d = {
        "$schema": VC_SCHEMA,
        "name": uuid.uuid4().hex[:16],
        "position": {"x": rect[0], "y": rect[1], "width": rect[2], "height": rect[3], "z": 0},
        "visual": {
            "visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [
                {"textRuns": [{"value": text,
                               "textStyle": {"fontSize": "%dpt" % TITLE_PT}}]}]}}]},
            # visualContainerObjects nests INSIDE `visual`. At the root it cascades
            # into a schema error across the whole page.
            "visualContainerObjects": {
                "title": [{"properties": {"show": lit("false")}}],
                "background": [{"properties": {"show": lit("false")}}],
            },
            "drillFilterOtherVisuals": True,
        },
    }
    return d


def main():
    made, moved, styled = [], 0, 0
    for page, visuals in RECTS.items():
        for visual, rect in visuals.items():
            p = vpath(page, visual)

            if visual == "pageTitle":
                if not os.path.exists(p):
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    write(p, make_title(page, rect, TITLES[page]))
                    made.append("%s/pageTitle" % page)
                    continue

            if not os.path.exists(p):
                print("  MISSING %s/%s" % (page, visual))
                continue

            d = json.load(io.open(p, encoding="utf-8"))
            d["position"].update(dict(zip(("x", "y", "width", "height"), rect)))
            moved += 1

            vis = d["visual"]
            if (page, visual) in SLICERS:
                objs = vis.setdefault("objects", {})
                objs["data"] = [{"properties": {"mode": lit("'Dropdown'")}}]
                # The slicer draws its own header; the container title would repeat it.
                vco = vis.setdefault("visualContainerObjects", {})
                vco["title"] = [{"properties": {"show": lit("false")}}]

            # Trap 11: the theme's radius does not reach visuals. Set it here.
            vco = vis.setdefault("visualContainerObjects", {})
            vco["border"] = [{"properties": {"show": lit("true"),
                                             "radius": lit("%dD" % RADIUS)}}]
            styled += 1
            write(p, d)

    for m in made:
        print("  created %s" % m)
    print("%d titles created, %d visuals repositioned, %d given radius %dpx"
          % (len(made), moved, styled, RADIUS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
