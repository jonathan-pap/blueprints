"""Realm Chronicle - build entry point. Re-runnable: running it twice gives the same report.

Run with Power BI Desktop CLOSED. A bridge `reload` refreshes the report pages but does NOT pick up
changed measure DAX (observed 2026-09-13) - after a build that touches _HTML.tmdl, reopen Desktop.

    python power-bi/projects/realm-chronicle/build/build.py

Pages (rail order lives in chroniclekit.PAGES)
  intro     THE REALM CHRONICLE cover - hero, the four ledgers, hall of legends, the boss roll.
  bestiary  THE BESTIARY - a field guide: header with kills by kind, every creature as a card grouped
            Boss > Elite > Field, and the families they add up to (with the deadliest creature).
All panels are HTML-in-SVG (../../../02-build/visuals/svg/html-in-svg.md); their measures live in the
model table _HTML, generated to the resolved region sizes by html_measures.py. Every page carries the
navigation rail (design A); the grid lays out to its right via meta.chrome.left. Canvas: 1280x720.
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chroniclekit import K, PAGES, dark_canvas, nav_rail, svg_panel  # noqa: E402
import html_measures  # noqa: E402
import model_tweaks  # noqa: E402
import theme  # noqa: E402

PAGE_W = int(K.DS["meta"]["page"]["width"])
PAGE_H = int(K.DS["meta"]["page"]["height"])
HTML_TMDL = os.path.join(K.ROOT, "realm-chronicle.SemanticModel", "definition", "tables", "_HTML.tmdl")

# Pages that once existed and have been replaced. Their folders and rail images are removed on build,
# so a rename never leaves a stray page or a dead registered resource shipping with the report.
RETIRED = ["hunt"]            # The Hunt -> The Bestiary, 2026-09-13


def _pages_meta():
    return os.path.join(K.PAGES, "pages.json")


def _has_visuals(page_dir):
    vd = os.path.join(page_dir, "visuals")
    return os.path.isdir(vd) and bool(os.listdir(vd))


def clear_page(pid, placeholder_names=("Page 1",)):
    """Remove the page we are about to rebuild, plus any EMPTY Desktop placeholder page.
    A placeholder that has visuals is left alone - that's someone's work, not a placeholder."""
    for entry in os.listdir(K.PAGES):
        d = os.path.join(K.PAGES, entry)
        pj = os.path.join(d, "page.json")
        if not os.path.isfile(pj):
            continue
        pg = json.load(open(pj, encoding="utf-8"))
        rebuild = pg.get("name") == pid
        placeholder = pg.get("displayName") in placeholder_names and not _has_visuals(d)
        if rebuild or placeholder:
            shutil.rmtree(d)
            print("  cleared %s (%s)" % (entry, "rebuild" if rebuild else "empty placeholder"))
    # keep pages.json honest before pbir runs, so it never sees a page with no folder
    meta = json.load(open(_pages_meta(), encoding="utf-8"))
    live = {e for e in os.listdir(K.PAGES) if os.path.isdir(os.path.join(K.PAGES, e))}
    meta["pageOrder"] = [p for p in meta.get("pageOrder", []) if p in live]
    if meta["pageOrder"]:
        meta["activePageName"] = meta["pageOrder"][0]
    json.dump(meta, open(_pages_meta(), "w", encoding="utf-8", newline="\n"), indent=2)


def retire_pages():
    for pid in RETIRED:
        if os.path.isdir(os.path.join(K.PAGES, pid)):
            clear_page(pid)
        K.unregister_image("navRail-%s.svg" % pid)


def write_measures():
    groups = [html_measures.intro_group(K.rects("intro")),
              html_measures.bestiary_group(K.rects("bestiary")),
              html_measures.quests_group(K.rects("quests")),
              html_measures.exchange_group(K.rects("exchange")),
              html_measures.realms_group(K.rects("realms")),
              html_measures.live_group(K.rects("live"))]
    for folder, name in html_measures.write_measures(HTML_TMDL, groups):
        print("  measure %-9s %s" % (folder, name))


def place(d, panels):
    for tab, (name, rect, measure_name, alt) in enumerate(panels, start=1):
        K.write(d, name, svg_panel(name, rect, measure_name, alt, z=100 * tab, tab=tab))
        print("  %-18s %4dx%-4d at (%d,%d)" % (name, rect["width"], rect["height"], rect["x"], rect["y"]))


def build_intro():
    clear_page("intro")
    d = K.add_page("intro", "Intro", w=PAGE_W, h=PAGE_H)
    dark_canvas(d)
    nav_rail(d, "intro")
    hero, ledgers, legends, bosses = K.rects("intro")
    place(d, [
        ("introHero",    hero,    "Intro Hero HTML",
         "The Realm Chronicle: guilds, monsters, quests and gold across four years"),
        ("introLedgers", ledgers, "Intro Ledgers HTML",
         "The four ledgers: monsters slain, gold in bounties, loot drops, gold traded, each with growth vs the prior year"),
        ("introLegends", legends, "Intro Legends HTML",
         "Hall of Legends: the five adventurers with the most monster kills"),
        ("introBosses",  bosses,  "Intro Bosses HTML",
         "The Boss Roll: the four raid bosses by kills and party wipes per thousand kills"),
    ])
    return d


def build_bestiary():
    clear_page("bestiary")
    d = K.add_page("bestiary", "The Bestiary", w=PAGE_W, h=PAGE_H)
    dark_canvas(d)
    nav_rail(d, "bestiary")
    header, creatures, families = K.rects("bestiary")
    place(d, [
        ("bestiaryHeader",    header,    "Bestiary Header HTML",
         "The Bestiary: monster kills by kind - field, elite and boss - and the number of creatures catalogued"),
        ("bestiaryCreatures", creatures, "Bestiary Creatures HTML",
         "Every creature as a card, grouped boss, elite and field, with family, habitat, tier, kills and party wipes per thousand kills"),
        ("bestiaryFamilies",  families,  "Bestiary Families HTML",
         "Kills by monster family with share and party wipes per thousand kills, and the single deadliest creature"),
    ])
    return d


def build_page(pid, display, layout, panels):
    """One inner page: clear, create, dark canvas, rail, then each panel onto its region in order.
    panels: [(visual name, measure name, alt text), ...] matching the layout's regions."""
    clear_page(pid)
    d = K.add_page(pid, display, w=PAGE_W, h=PAGE_H)
    dark_canvas(d)
    nav_rail(d, pid)
    rects = K.rects(layout)
    assert len(rects) == len(panels), "%s: %d regions, %d panels" % (layout, len(rects), len(panels))
    place(d, [(n, r, m, a) for (n, m, a), r in zip(panels, rects)])
    return d


def build_quests():
    return build_page("quests", "Quest Board", "quests", [
        ("questsHeader", "Quests Header HTML",
         "The Quest Board: bounty gold, quests completed, gold per quest and days per quest"),
        ("questsChains", "Quests Chains HTML",
         "The quest chains, each a row of its quests in prerequisite order with danger, type and bounty"),
        ("questsDanger", "Quests Danger HTML", "Bounty gold by quest danger, Low to Extreme"),
        ("questsRank",   "Quests Rank HTML",   "Bounty gold by adventurer rank, Gold to Copper"),
    ])


def build_exchange():
    return build_page("exchange", "The Exchange", "exchange", [
        ("exchangeHeader",   "Exchange Header HTML",
         "The Exchange: gold traded, units traded, gold per unit and legendary loot drops"),
        ("exchangeBoard",    "Exchange Board HTML",    "Market board: the twelve items with the most gold traded"),
        ("exchangeCategory", "Exchange Category HTML", "Gold traded by item category"),
        ("exchangeRarity",   "Exchange Rarity HTML",   "Loot drops by rarity, Common to Legendary, with gold value"),
    ])


def build_realms():
    return build_page("realms", "Realm Map", "realms", [
        ("realmsHeader", "Realms Header HTML",
         "The Realm Map: realms, regions, the busiest trading post and realms at Extreme threat"),
        ("realmsMap",    "Realms Map HTML",
         "Map of the eight realms plotted by latitude and longitude, bubbles sized by gold traded and coloured by threat"),
        ("realmsLedger", "Realms Ledger HTML",
         "Realm ledger: each realm's region, terrain, threat, gold traded and monsters slain there"),
    ])


# ---- LIVE pages - native visuals start every interaction --------------------------------------

M_TABLE = "_Measures"


def _units(k=True):
    """Data labels + value axis in thousands (372K, not 0.37M)."""
    return {"labels": [{"properties": {"show": K.lit("true"), "labelDisplayUnits": K.lit("1000D"),
                                       "labelPrecision": K.lit("0L")}}],
            "valueAxis": [{"properties": {"labelDisplayUnits": K.lit("1000D")}}]} if k else \
           {"labels": [{"properties": {"show": K.lit("true")}}]}


def _year_drill(name, rect, measure, label, tab, thousands=True):
    """Year > Month on a column chart: four readable columns, drill-down opens a year into months.
    Sorted on the axis column ascending - never the CLI's measure-descending default (build trap 1)."""
    v = K.vis(name, "clusteredColumnChart", rect, 300,
              query={"Category": {"projections": [K.proj_c("DimDate", "Year", "Year"),
                                                  K.proj_c("DimDate", "MonthYear", "Month")]},
                     "Y": {"projections": [K.proj_m(measure, label, M_TABLE)]}},
              objects=_units(thousands), tab=tab)
    return K.sort_by(v, K.col("DimDate", "Year"), "Ascending")


def _live_scaffold(pid, display, header_measure, header_alt, slicers):
    """Every LIVE page: page, canvas, rail, the reacting HTML header, four synced dropdown slicers.
    Returns the page dir and the three content rects. Chart titles come from theme + projection
    displayNames - never a container title.text on a chart (build trap 15)."""
    clear_page(pid)
    d = K.add_page(pid, display, w=PAGE_W, h=PAGE_H)
    dark_canvas(d)
    nav_rail(d, pid)
    header, s1, s2, s3, s4, main, top, bottom = K.rects("live")
    K.write(d, pid + "Header", svg_panel(pid + "Header", header, header_measure, header_alt, z=100, tab=1))
    for tab, ((entity, prop, group), rect) in enumerate(zip(slicers, (s1, s2, s3, s4)), start=2):
        name = "sl" + prop
        K.write(d, name, K.slicer(name, rect, prop, group, tab=tab, entity=entity))
    return d, main, top, bottom


def _report(*named):
    for n, r in named:
        print("  %-18s %4dx%-4d at (%d,%d)" % (n, r["width"], r["height"], r["x"], r["y"]))


def build_huntlive():
    """Hunt Command - the bar, the year chart and the table cross-filter each other and the header."""
    d, bar, trend, table = _live_scaffold(
        "huntlive", "Hunt Command", "Hunt Live Header HTML",
        "Hunt Command totals - monsters slain, bosses slain, party wipes and gold earned - for the current filters",
        [("DimDate", "Year", "year"), ("DimAdventurer", "Guild", "guild"),
         ("DimMonster", "Habitat", "habitat"), ("DimMonster", "Kind", "kind")])
    guild = K.vis("killsByGuild", "clusteredBarChart", bar, 300,
                  query={"Category": {"projections": [K.proj_c("DimAdventurer", "Guild", "Guild")]},
                         "Y": {"projections": [K.proj_m("Total MonstersSlain", "Monsters slain", M_TABLE)]}},
                  objects=_units(), tab=6)
    K.write(d, "killsByGuild", K.sort_by(guild, K.measure("Total MonstersSlain", M_TABLE), "Descending"))
    K.write(d, "killsByYear", _year_drill("killsByYear", trend, "Total MonstersSlain", "Monsters slain", 7))
    board = K.vis("leaderboard", "tableEx", table, 300,
                  query={"Values": {"projections": [
                      K.proj_c("DimAdventurer", "Adventurer", "Adventurer"),
                      K.proj_c("DimAdventurer", "Guild", "Guild"),
                      K.proj_c("DimAdventurer", "Rank", "Rank"),
                      K.proj_m("Total MonstersSlain", "Slain", M_TABLE),
                      K.proj_m("Kill Bar SVG", "Kills", "_HTML")]}},
                  objects={"grid": [{"properties": {"imageHeight": K.lit("12D"), "imageWidth": K.lit("120D")}}],
                           "total": [{"properties": {"totals": K.lit("false")}}]},
                  vco={"title": [{"properties": {"show": K.lit("true"), "text": K.lit("'Top slayers'")}}]}, tab=8)
    K.write(d, "leaderboard", K.sort_by(board, K.measure("Total MonstersSlain", M_TABLE), "Descending"))
    _report(("killsByGuild", bar), ("killsByYear", trend), ("leaderboard", table))
    return d


def build_questlive():
    """Quest Command - the chain matrix expands chain > quest; danger and year charts cross-filter it."""
    d, main, top, bottom = _live_scaffold(
        "questlive", "Quest Command", "Quest Live Header HTML",
        "Quest Command totals - bounty gold, quests completed, gold per quest and days per quest - for the current filters",
        [("DimDate", "Year", "year"), ("DimQuest", "Danger", "danger"),
         ("DimQuest", "QuestType", "questtype"), ("DimAdventurer", "Rank", "rank")])
    chains = K.vis("chainMatrix", "pivotTable", main, 300,
                   query={"Rows": {"projections": [K.proj_c("DimQuest", "ChainName", "Chain"),
                                                   K.proj_c("DimQuest", "Quest", "Quest")]},
                          "Values": {"projections": [K.proj_m("Total BountyGold", "Bounty gold", M_TABLE),
                                                     K.proj_m("Total QuestsCompleted", "Quests done", M_TABLE),
                                                     K.proj_m("Total DaysOnQuest", "Days", M_TABLE)]}},
                   vco={"title": [{"properties": {"show": K.lit("true"), "text": K.lit("'Quest chains - expand a chain'")}}]},
                   tab=6)
    K.write(d, "chainMatrix", K.sort_by(chains, K.measure("Total BountyGold", M_TABLE), "Descending"))
    danger = K.vis("bountyByDanger", "clusteredColumnChart", top, 300,
                   query={"Category": {"projections": [K.proj_c("DimQuest", "Danger", "Danger")]},
                          "Y": {"projections": [K.proj_m("Total BountyGold", "Bounty gold", M_TABLE)]}},
                   objects=_units(False), tab=7)
    # Danger has sortByColumn DangerOrder in the model: sorting on the column gives Low..Extreme
    K.write(d, "bountyByDanger", K.sort_by(danger, K.col("DimQuest", "Danger"), "Ascending"))
    K.write(d, "bountyByYear", _year_drill("bountyByYear", bottom, "Total BountyGold", "Bounty gold", 8, False))
    _report(("chainMatrix", main), ("bountyByDanger", top), ("bountyByYear", bottom))
    return d


def build_marketlive():
    """Market Command - the item table, category bars and year chart cross-filter each other."""
    d, main, top, bottom = _live_scaffold(
        "marketlive", "Market Command", "Market Live Header HTML",
        "Market Command totals - gold traded, units traded, gold per unit and legendary drops - for the current filters",
        [("DimDate", "Year", "year"), ("DimRealm", "Realm", "realm"),
         ("DimItem", "Category", "category"), ("DimItem", "Rarity", "rarity")])
    items = K.vis("itemBoard", "tableEx", main, 300,
                  query={"Values": {"projections": [
                      K.proj_c("DimItem", "Item", "Item"),
                      K.proj_c("DimItem", "Category", "Category"),
                      K.proj_c("DimItem", "Rarity", "Rarity"),
                      K.proj_m("Total GoldVolume", "Gold traded", M_TABLE),
                      K.proj_m("Total QuantityTraded", "Units", M_TABLE),
                      K.proj_m("Gold Bar SVG", "Share", "_HTML")]}},
                  objects={"grid": [{"properties": {"imageHeight": K.lit("12D"), "imageWidth": K.lit("120D")}}],
                           "total": [{"properties": {"totals": K.lit("false")}}]},
                  vco={"title": [{"properties": {"show": K.lit("true"), "text": K.lit("'Items on the exchange'")}}]}, tab=6)
    K.write(d, "itemBoard", K.sort_by(items, K.measure("Total GoldVolume", M_TABLE), "Descending"))
    cat = K.vis("goldByCategory", "clusteredBarChart", top, 300,
                query={"Category": {"projections": [K.proj_c("DimItem", "Category", "Category")]},
                       "Y": {"projections": [K.proj_m("Total GoldVolume", "Gold traded", M_TABLE)]}},
                objects=_units(False), tab=7)
    K.write(d, "goldByCategory", K.sort_by(cat, K.measure("Total GoldVolume", M_TABLE), "Descending"))
    K.write(d, "goldByYear", _year_drill("goldByYear", bottom, "Total GoldVolume", "Gold traded", 8, False))
    _report(("itemBoard", main), ("goldByCategory", top), ("goldByYear", bottom))
    return d


def finalize_order():
    """Rebuilding a page re-appends it, so order drifts on every re-run unless it's set last.
    Report pages follow chroniclekit.PAGES; any page not in the registry keeps its place after them."""
    meta = json.load(open(_pages_meta(), encoding="utf-8"))
    live = {e for e in os.listdir(K.PAGES) if os.path.isdir(os.path.join(K.PAGES, e))}
    known = [p["id"] for p in PAGES if p["id"] in live]
    meta["pageOrder"] = known + [x for x in meta["pageOrder"] if x in live and x not in known]
    meta["activePageName"] = meta["pageOrder"][0]
    json.dump(meta, open(_pages_meta(), "w", encoding="utf-8", newline="\n"), indent=2)
    print("  page order: %s" % " > ".join(meta["pageOrder"]))


if __name__ == "__main__":
    print("building realm-chronicle")
    retire_pages()
    K.register_theme(theme.build())
    print("  theme: Realm Chronicle Dark v1.0")
    for c in model_tweaks.apply():
        print("  model: " + c)
    write_measures()
    build_intro()
    build_bestiary()
    build_quests()
    build_exchange()
    build_realms()
    build_huntlive()
    build_questlive()
    build_marketlive()
    finalize_order()
    print("done - validate: pbir validate + 04-review/hooks/lint-report-traps.sh per page")
