"""A five-stop bookmark tour, plus the navigator bar that drives it.

DESIGN NOTE — why these bookmarks navigate but do not stage filters.

A bookmark can capture three things: the active page, the data state (filters and slicer
selections) and the display state (visibility). These capture the PAGE only:

    options = {suppressData: true, suppressDisplay: true}

Two reasons, in order of weight.

1. A tour that yanks the slicers fights the person giving the demo. The moment they set
   Realm = Grimmwald to answer a question and then press Next, their selection vanishes. The
   presenter should own the filters; the tour should own the running order.
2. Staged-filter bookmarks cannot be verified from here. The Desktop Bridge can reload and
   screenshot, but it cannot click - so a bookmark whose slicer state is wrong would look
   perfect in every screenshot and fail live in front of an audience. Shipping the part that
   can be proven, and writing the staged moments into tour.md as live clicks instead, trades
   a little polish for something that cannot embarrass anyone.

`pbir bookmarks new` does NOT exist in pbir 0.9.25 (the room's create-bookmark.md documents
it, but the CLI has only list/rename/data/display/current-page/visuals/json). Hence the
hand-authored JSON - the option vocabulary below is copied from the shipped K201 example.
"""
import io
import json
import os

from emporiumkit import (INK, INK2, INK3, RULE, SURFACE, GOLD, PAGES, REPORT, Q, lit,
                         noframe, solid, vis, write)

BM_DIR = os.path.join(REPORT, "definition", "bookmarks")
SCHEMA_BM = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
             "definition/bookmark/1.4.0/schema.json")
SCHEMA_IDX = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
              "definition/bookmarksMetadata/1.0.0/schema.json")

# name, displayName, page. Order IS the tour.
# tile labels are short because a navigator tile is ~120px wide and truncates with no
# ellipsis budget to spare; the narrative lives in tour.md
STOPS = [
    ("tourStop1", "1 · Chain", "Overview"),
    ("tourStop2", "2 · Realms", "Realms"),
    ("tourStop3", "3 · Wares", "Items"),
    ("tourStop4", "4 · Patrons", "Patrons"),
    ("tourStop5", "5 · Home", "Overview"),
]

os.makedirs(BM_DIR, exist_ok=True)
for f in os.listdir(BM_DIR):
    os.remove(os.path.join(BM_DIR, f))

for name, display, page in STOPS:
    bm = {
        "$schema": SCHEMA_BM,
        "displayName": display,
        "name": name,
        # targetVisualNames [] = the whole page; the two suppress flags then narrow it to
        # navigation alone, so nothing about the reader's filters or visibility is touched
        "options": {"targetVisualNames": [], "suppressData": True, "suppressDisplay": True},
        # `sections` is required by the schema even when nothing about the section is
        # being restored - an empty visualContainers map satisfies it, and the two
        # suppress flags above mean it is never read
        "explorationState": {"version": "1.3", "activeSection": page,
                             "sections": {page: {"visualContainers": {}}}},
    }
    with io.open(os.path.join(BM_DIR, "%s.bookmark.json" % name), "w",
                 encoding="utf-8", newline="\n") as f:
        json.dump(bm, f, indent=2)
        f.write("\n")

# build_tutorial.py rewrites this file with both groups; this keeps build_tour.py runnable
# on its own.
with io.open(os.path.join(BM_DIR, "bookmarks.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({"$schema": SCHEMA_IDX,
               "items": [{"name": "grpTour", "displayName": "Tour",
                          "children": [n for n, _, _ in STOPS]}]}, f, indent=2)
    f.write("\n")
print("  %d bookmarks written" % len(STOPS))

# ---------------------------------------------------------------- the navigator bar
# 48px is the smallest height at which the navigator's tile labels are not clipped - at 32px
# the tiles draw but the text is cut through the middle. So the tour gets its own grid row
# (row 12, y 656..704) and every content band on every page now stops at row 12.
# the row splits: page tour on the left, that page's tutorial on the right
TOUR = {"x": 24, "y": 656, "width": 608, "height": 48}
TUTOR = {"x": 648, "y": 656, "width": 608, "height": 48}


def navigator(name, rect, group):
    """A bookmarkNavigator is fussy, in two ways that both fail SILENTLY.

    1. `query={}` is required. Omit it and the visual writes, validates and reloads cleanly,
       then draws nothing - no error, no placeholder.
    2. Its `objects` block is picky. A version carrying layout / text / fill / outline / shape
       also drew nothing, at every height tried. A single `bookmarks.bookmarkGroup` property is
       fine, so that is all it carries; styling comes from the theme, which is the workspace's
       theme-first rule anyway.

    Without a group a navigator lists EVERY bookmark in the report - grouping them in
    bookmarks.json is not enough on its own, the navigator has to be pointed at one.
    """
    return vis(name, "bookmarkNavigator", rect, 950, query={},
               objects={"bookmarks": [{"properties": {
                   "bookmarkGroup": lit(Q + group + Q)}}]},
               vco=noframe(), tab=99)


for page in ("Overview", "Realms", "Items", "Patrons"):
    write(os.path.join(PAGES, page), "tourBar", navigator("tourBar", TOUR, "grpTour"))
    write(os.path.join(PAGES, page), "tutorBar",
          navigator("tutorBar", TUTOR, "grpTut" + page))
print("  tour + tutorial navigators on 4 pages")
print("tour built")
