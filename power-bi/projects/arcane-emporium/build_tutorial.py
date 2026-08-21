"""A guided tutorial: ten steps that put one graph on stage and explain it.

HOW IT WORKS

Each step is a bookmark that captures DISPLAY state only (`suppressData: true`, so the reader's
slicers are never touched). It hides every other data visual on the page and reveals a caption
textbox that explains the one left standing. The captions live in the page with `isHidden: true`
at the root of visual.json, so the page's normal state is unchanged - they exist only inside
their step.

WHY HIDE RATHER THAN DIM

Dimming the others needs an overlay ABOVE them and the focused visual ABOVE the overlay, and
z-order is static in PBIR - it cannot change per bookmark. The usual workaround is to duplicate
every focusable visual at a high z and reveal the duplicate, which doubles the visual count and
the query load. Hiding needs one mechanism (`display.mode`), no z-order reasoning, no duplicates,
and it hands the freed space to the explanation, which dimming does not. A shape-based scrim was
never on the table: a shape visual would not render its fill in this workspace before (see
churnkit's panel note).

WHAT COULD NOT BE VERIFIED

The Desktop Bridge reloads and screenshots but cannot click, so the bookmarks' RESTORE behaviour
is unproven. What is proven: every caption renders where it should, and the page's default state
is untouched - checked by flipping `isHidden` off, screenshotting, and flipping it back.
"""
import io
import json
import os

from emporiumkit import (GOLD, INK, INK2, INK3, PAGES, REPORT, rects, textbox, ts, write)

BM_DIR = os.path.join(REPORT, "definition", "bookmarks")
SCHEMA_BM = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
             "definition/bookmark/1.4.0/schema.json")
SCHEMA_IDX = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
              "definition/bookmarksMetadata/1.0.0/schema.json")

# Never hidden. `tutorBar` is the load-bearing one: leave it out and the step hides the
# very navigator you would use to reach the next step or to press Show all, and the
# reader is stranded - the page tour cannot rescue them either, because those bookmarks
# carry suppressDisplay and will not un-hide anything.
CHROME = {"pageTitle", "selCaption", "fltRealm", "fltCategory", "fltYear",
          "tourBar", "tutorBar"}


def region(page, layout, idx=0):
    return rects(layout)[idx]


def block(top, bottom, x=24, width=1232, pad=16):
    """A caption rect inside a freed band."""
    return {"x": x + pad, "y": top + pad, "width": width - 2 * pad,
            "height": bottom - top - 2 * pad}


ov_kpi = region("Overview", "kpi_hero_plus_4")
ov_trend = region("Overview", "overview_trend")
ov_split = region("Overview", "overview_split")
rl = rects("realms_body")
it_hero = region("Items", "items_hero")
it_strip = region("Items", "items_strip")
pt = rects("patrons_two")
pt_body = region("Patrons", "patrons_body")

# id, page, title, focus visuals, caption rect, caption body
STEPS = [
    ("tut01", "Overview", "The headline numbers",
     ["kpiGold", "kpiGoldH", "kpiYoY", "kpiYoYH", "kpiUnits", "kpiUnitsH",
      "kpiTxn", "kpiTxnH", "kpiAvg", "kpiAvgH"],
     block(ov_trend["y"], ov_split["y"] + ov_split["height"]),
     "Five numbers, and only the first is a headline. 25.00M is the four-year take — the "
     "generator was told to hit exactly 25,000,000 and landed on 25,000,000.76.\n\n"
     "Growth reads +12.0%, and that number is fussier than it looks. The obvious measure "
     "compares the whole selection with the same span a year earlier, which across all four "
     "years means comparing 2023–2026 against 2023–2025 — arithmetic, not growth, and it "
     "reports +41.6%. This card uses a measure that always answers 'how did the most recent "
     "year do', whatever is selected."),

    ("tut02", "Overview", "Four years, month by month",
     ["trendH", "trendCombo"],
     block(ov_split["y"], ov_split["y"] + ov_split["height"]),
     "Columns are each month's take; the gold line is a trailing three-month mean. The line is "
     "there so the spikes read as spikes rather than as the trend moving — every November and "
     "December is the Frostfall festival.\n\n"
     "Filter the Year slicer to one year and the same shape appears at a smaller scale: the "
     "festival is a property of the month, not of the year."),

    ("tut03", "Overview", "Two ways to cut the same Gold",
     ["realmH", "realmBar", "catH", "catBar"],
     block(ov_trend["y"], ov_trend["y"] + ov_trend["height"]),
     "Realm on the left, category of ware on the right. Both splits are pinned by the "
     "generator — realms at 45 / 30 / 25, wares at 30 / 25 / 20 / 15 / 10 — and the model "
     "reproduces them to eight decimal places.\n\n"
     "The category chart is vertical and the realm chart horizontal for a dull reason worth "
     "knowing: five horizontal bars did not fit the band, and Power BI drops the fifth rather "
     "than crowd them. A silently missing category is worse than a rotated label."),

    ("tut04", "Realms", "Every shop, ranked",
     ["shopH", "shopBar"],
     block(rl[1]["y"], rl[1]["y"] + rl[1]["height"], x=rl[1]["x"], width=rl[1]["width"]),
     "Eight shops, bar colour by realm — Eldoria blue, Grimmwald plum, Sunspire gold.\n\n"
     "Read the realms, not the shops. Within a realm the shops are near-identical "
     "(3,750,001 / 3,750,000 / 3,749,999) because the generator splits each realm's Gold "
     "evenly across its shops. The realm split means something; the shop split does not."),

    ("tut05", "Realms", "The shop ledger",
     ["leagueH", "leagueTable"],
     block(rl[0]["y"], rl[0]["y"] + rl[0]["height"], x=rl[0]["x"], width=rl[0]["width"]),
     "Share re-bases to whatever the header slicers have selected. Pick one realm and each of "
     "its shops jumps from 15% to 33% — it is always a share of what you are looking at, never "
     "a share of the whole four years.\n\n"
     "YoY here is per shop, and it is the latest-year measure rather than the naive one, for "
     "the same reason the headline card is."),

    ("tut06", "Items", "The vital few",
     ["paretoH", "itemPareto"],
     block(it_strip["y"], it_strip["y"] + it_strip["height"]),
     "Bars are Gold, the line is the running share. Gold up to the 80% mark, iron beyond it: "
     "four wares carry over half the takings and eleven carry eighty percent.\n\n"
     "The cumulative line is a VISUAL calculation — no rank column, no cumulative measure, "
     "nothing added to the model. The trick is ORDERBY: accumulation is pinned to "
     "value-descending, so the line stays correct even if you re-sort the axis. The naive "
     "version zig-zags the moment you do.\n\n"
     "Filter to one category and the Pareto rebuilds — the vital few are relative to what you "
     "are looking at."),

    ("tut07", "Items", "Every ware, with its place in the tail",
     ["wareH", "wareTable"],
     block(it_hero["y"], it_hero["y"] + it_hero["height"]),
     "The same twenty-four wares as numbers. Elixir of Vitality alone is 20.2% of everything; "
     "the bottom thirteen together are under twenty.\n\n"
     "Avg price is Gold per unit, so it reads as a blended price across whatever is in filter "
     "context rather than a list price — there is no price column in the model."),

    ("tut08", "Patrons", "Gold by kind of patron",
     ["typeH", "typeBar"],
     block(pt_body["y"], pt_body["y"] + pt_body["height"]),
     "Four kinds, pinned at 40 / 25 / 20 / 15. Adventurers are the biggest block of Gold and "
     "nobles the smallest — which is the opposite of the cliché, and it is deliberate: the "
     "generator was told these shares and the model reproduces them exactly."),

    ("tut09", "Patrons", "Average purse — the counter-intuitive one",
     ["purseH", "purseBar"],
     block(pt_body["y"], pt_body["y"] + pt_body["height"]),
     "Gold per sale line. Adventurers have the BIGGEST average purse (284) and nobles the "
     "smallest (190).\n\n"
     "That surprises people, so it is worth being able to explain: every patron visits about "
     "as often as every other — roughly five thousand times across four years — so average "
     "purse has nothing left to track except the pinned Gold share. It is an artefact of how "
     "the data was generated, not a finding about nobles."),

    ("tut10", "Patrons", "The big spenders",
     ["bigH", "bigTable"],
     block(pt[0]["y"], pt[0]["y"] + pt[0]["height"]),
     "All twenty patrons. Kaelen Swiftblade alone is 24.1% of everything — more than the whole "
     "Noble kind put together.\n\n"
     "The generator ranks big spenders first WITHIN each kind, so the pareto runs inside the "
     "type rather than across it. That is why the top of this list is not simply four "
     "adventurers."),
]


# tile label per step - a navigator tile is ~150px here and truncates. The full title is on
# the caption, which has the room for it.
TILES = {
    "tut01": "Numbers", "tut02": "Trend", "tut03": "Splits",
    "tut04": "Shops", "tut05": "Ledger",
    "tut06": "Pareto", "tut07": "Ware list",
    "tut08": "By kind", "tut09": "Avg purse", "tut10": "Spenders",
}


def page_visuals(page):
    d = os.path.join(PAGES, page, "visuals")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


# ---------------------------------------------------------------- captions
all_caps = {s[0] for s in STEPS}
for page in ("Overview", "Realms", "Items", "Patrons"):
    for v in page_visuals(page):
        if v.startswith("cap"):
            import shutil
            shutil.rmtree(os.path.join(PAGES, page, "visuals", v))

for sid, page, title, focus, rect, body in STEPS:
    tb = textbox("cap" + sid, rect,
                 [(title, ts("14pt", GOLD, "Segoe UI Semibold")),
                  (body, ts("10pt", INK2))], z=980)
    # hidden in the page's normal state; the step's bookmark is what reveals it
    tb["isHidden"] = True
    write(os.path.join(PAGES, page), "cap" + sid, tb)
print("  %d captions written (hidden by default)" % len(STEPS))

# ---------------------------------------------------------------- bookmarks
for f in os.listdir(BM_DIR):
    if f.startswith("tut") or f.startswith("rst"):
        os.remove(os.path.join(BM_DIR, f))

for sid, page, title, focus, rect, body in STEPS:
    keep = set(focus) | CHROME | {"cap" + sid}
    # `display.mode` accepts ONLY "hidden" - "visible", "shown", "show", "default", "normal",
    # "active" and "expanded" are all rejected by the schema. Visibility is therefore expressed
    # by OMISSION: a bookmark lists what to hide, and everything it does not mention is shown.
    # That is also the shape the shipped K201 bookmarks use.
    containers = {v: {"singleVisual": {"display": {"mode": "hidden"}}}
                  for v in page_visuals(page) if v not in keep}
    bm = {
        "$schema": SCHEMA_BM,
        "displayName": TILES[sid],
        "name": sid,
        # display only - suppressData keeps the reader's slicer selections intact
        "options": {"targetVisualNames": [], "suppressData": True},
        "explorationState": {"version": "1.3", "activeSection": page,
                             "sections": {page: {"visualContainers": containers}}},
    }
    with io.open(os.path.join(BM_DIR, "%s.bookmark.json" % sid), "w",
                 encoding="utf-8", newline="\n") as f:
        json.dump(bm, f, indent=2)
        f.write("\n")
print("  %d tutorial bookmarks written" % len(STEPS))

# a way OUT of every step. The page tour cannot do it - those bookmarks carry
# suppressDisplay, so they restore the page and deliberately leave visibility alone. This
# one hides every caption and, by omitting them, brings every data visual back.
for pg in ("Overview", "Realms", "Items", "Patrons"):
    caps = {v: {"singleVisual": {"display": {"mode": "hidden"}}}
            for v in page_visuals(pg) if v.startswith("cap")}
    bm = {"$schema": SCHEMA_BM, "displayName": "Show all", "name": "rst" + pg,
          "options": {"targetVisualNames": [], "suppressData": True},
          "explorationState": {"version": "1.3", "activeSection": pg,
                               "sections": {pg: {"visualContainers": caps}}}}
    with io.open(os.path.join(BM_DIR, "rst%s.bookmark.json" % pg), "w",
                 encoding="utf-8", newline="\n") as f:
        json.dump(bm, f, indent=2)
        f.write("\n")
print("  4 reset bookmarks written")

# ---------------------------------------------------------------- index
# One group per page. A navigator lists EVERY bookmark unless it is pointed at a group, so
# without this the bottom bar showed all fifteen tiles, every label truncated to four
# characters. Each page's tutorial navigator gets its own group; the page tour keeps grpTour.
PAGE_LIST = ("Overview", "Realms", "Items", "Patrons")
idx = {"$schema": SCHEMA_IDX,
       "items": [{"name": "grpTour", "displayName": "Tour",
                  "children": ["tourStop%d" % i for i in range(1, 6)]}]
       + [{"name": "grpTut" + pg, "displayName": pg + " tutorial",
           "children": ["rst" + pg] + [s[0] for s in STEPS if s[1] == pg]}
          for pg in PAGE_LIST]}
with io.open(os.path.join(BM_DIR, "bookmarks.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(idx, f, indent=2)
    f.write("\n")
print("tutorial built")
