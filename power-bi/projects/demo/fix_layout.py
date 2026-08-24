#!/usr/bin/env python3
"""Repair the layout defects across all three demo pages.

Three root causes, all mine, all visible in renders I posted without acting on them:

1. TITLES SCROLL. `pbir add title` writes a 24pt text run and sizes the box to 65px to suit
   it. I forced every title to a 40px grid rect and left the font at 24pt, so the text
   overflows its own box and Power BI adds a scrollbar. Fix: 16pt in a 48px band. The font
   has to come down with the box - resizing one without the other is what caused this.

2. SLICERS UNREACHABLE. A `slicer` defaults to LIST mode, which needs ~160px to show a header
   plus rows. At the 40px I gave them you get a header and a sliver. Fix: Dropdown mode
   (`objects.data[].mode`), which is what the room doc says to default to anyway, at 48px.

3. SCATTER UNREADABLE. Eight bubbles clustered in the lower-left with 12pt labels on top of
   each other. Fix: taller plot, 9pt labels, and drop the size-by-Quests encoding - every
   adventurer completes roughly the same number of quests, so the bubble areas were nearly
   identical and the encoding bought nothing while making the overlap worse.

Vertical rhythm, rebuilt so bands do not collide (1280x720, margin 24, gutter 16):

    title band   y=24   h=48    -> 72
    body 1       y=88          (page-specific height)
    body 2       ...           -> 696
    bottom margin                 720
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "demo.Report", "definition", "pages")

TITLE_PT = 16          # fits a 48px box; 24pt did not fit 40px
TITLE_H = 48


# ---------------------------------------------------------------------------------------
# DO NOT RE-RUN BLIND. Page 1 and the Quest Board scatter were adjusted by hand in Desktop
# after this script last ran (KPI cards 152 -> 104, trend y=256 -> 208 and taller, scatter
# gridlines restored at 84% transparency on both axes). The table below has been synced to
# what is on disk so a re-run is a no-op rather than a rollback.
# ---------------------------------------------------------------------------------------

# page -> visual -> (x, y, width, height)
RECTS = {
    "Guild_Overview": {
        "Title":           (24, 24, 1232, 48),
        "dangerBar":       (648, 488, 608, 208),
        "kpiAdventurers":  (1064, 88, 192, 104),
        "kpiAvgBounty":    (648, 88, 192, 104),
        "kpiAvgDays":      (856, 88, 192, 104),
        "kpiBounty":       (24, 88, 400, 104),
        "kpiQuests":       (440, 88, 192, 104),
        "realmBar":        (24, 488, 608, 208),
        "trendLine":       (24, 208, 1232, 264),
    },
    "Quest_Board": {
        "Title_1":         (24, 24, 920, 48),
        "fltYear":         (960, 24, 296, 56),
        "questPareto":     (24, 88, 1232, 232),
        "questScatter":    (24, 336, 616, 360),
        "realmDanger":     (656, 336, 600, 240),
    },
    "Adventurer_Roster": {
        "Title_1":         (24, 24, 616, 48),
        "fltRank":         (960, 24, 296, 56),
        "fltRealm":        (656, 24, 288, 56),
        "rankBar":         (24, 88, 608, 360),
        "rosterTable":     (24, 464, 1232, 232),
        "topAdventurers":  (648, 88, 608, 360),
    },
}

TITLES = {("Guild_Overview", "Title"), ("Quest_Board", "Title_1"),
          ("Adventurer_Roster", "Title_1")}
SLICERS = {("Quest_Board", "fltYear"), ("Adventurer_Roster", "fltRealm"),
           ("Adventurer_Roster", "fltRank")}


def path(page, visual):
    return os.path.join(PAGES, page, "visuals", visual, "visual.json")


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def main():
    changed = []
    for page, visuals in RECTS.items():
        for visual, rect in visuals.items():
            p = path(page, visual)
            if not os.path.exists(p):
                print("  MISSING %s/%s" % (page, visual))
                continue
            d = json.load(io.open(p, encoding="utf-8"))
            d["position"].update(dict(zip(("x", "y", "width", "height"), rect)))

            if (page, visual) in TITLES:
                for para in d["visual"]["objects"]["general"][0]["properties"]["paragraphs"]:
                    for run in para.get("textRuns", []):
                        run.setdefault("textStyle", {})["fontSize"] = "%dpt" % TITLE_PT
                changed.append("%s/%s title -> %dpt in %dpx" % (page, visual, TITLE_PT, rect[3]))

            if (page, visual) in SLICERS:
                objs = d["visual"].setdefault("objects", {})
                objs["data"] = [{"properties": {"mode": lit("'Dropdown'")}}]
                changed.append("%s/%s -> Dropdown" % (page, visual))

            # The questScatter block that used to live here forced categoryLabels back on at
            # 9pt. That is now WRONG: the scatter identifies its points by legend, and the
            # gridlines were restored by hand at 84% transparency. Re-applying the old
            # formatting would undo both, so it is gone rather than commented out - a
            # commented-out clobber is still a clobber the next time someone uncomments it.

            io.open(p, "w", encoding="utf-8", newline="\n").write(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n")

    for c in changed:
        print("  " + c)
    print("%d adjustments" % len(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
