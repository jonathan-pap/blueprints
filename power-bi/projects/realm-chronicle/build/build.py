"""Realm Chronicle - build entry point. Re-runnable: running it twice gives the same report.

Run with Power BI Desktop CLOSED - Desktop overwrites files that change on disk while it's open.

    python power-bi/projects/realm-chronicle/build/build.py

Pages
  intro  THE REALM CHRONICLE cover - four HTML-in-SVG components on the `intro` grid layout
         (design-system.yaml): hero, the four ledgers, hall of legends, the boss roll.
         Doctrine: ../../../02-build/visuals/svg/html-in-svg.md. Measures: model table _HTML.
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chroniclekit import K, dark_canvas, svg_panel  # noqa: E402


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


def build_intro():
    clear_page("intro")
    d = K.add_page("intro", "Intro", w=1920, h=1080)
    dark_canvas(d)

    hero, ledgers, legends, bosses = K.rects("intro")
    panels = [
        ("introHero",    hero,    "Intro Hero HTML",
         "The Realm Chronicle: guilds, monsters, quests and gold across four years"),
        ("introLedgers", ledgers, "Intro Ledgers HTML",
         "The four ledgers: monsters slain, gold in bounties, loot drops, gold traded, each with growth vs the prior year"),
        ("introLegends", legends, "Intro Legends HTML",
         "Hall of Legends: the five adventurers with the most monster kills"),
        ("introBosses",  bosses,  "Intro Bosses HTML",
         "The Boss Roll: the four raid bosses by kills and party wipes per thousand kills"),
    ]
    for tab, (name, rect, measure_name, alt) in enumerate(panels, start=1):
        K.write(d, name, svg_panel(name, rect, measure_name, alt, z=100 * tab, tab=tab))
        print("  %-13s %4dx%-4d at (%d,%d)  <- %s"
              % (name, rect["width"], rect["height"], rect["x"], rect["y"], measure_name))
    return d


if __name__ == "__main__":
    print("building realm-chronicle")
    build_intro()
    print("done - validate: pbir validate + 04-review/hooks/lint-report-traps.sh --page Intro")
