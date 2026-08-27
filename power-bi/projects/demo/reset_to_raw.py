#!/usr/bin/env python3
"""Reset the demo to a RAW state: star schema + data, nothing built on top of it.

Run with Power BI Desktop CLOSED - this edits TMDL on disk, and an open Desktop
overwrites on-disk files when it saves.

WHAT GETS REMOVED
  report   every page and every visual -> one blank Page_1 (1280x720)
  model    all 10 measures out of _Measures (the table itself stays as the home)
           DangerOrder (DimQuestType) + RankOrder (DimAdventurer) calculated columns,
           and the sortByColumn bindings on Danger / Rank that point at them

WHAT STAYS - and why
  the five tables, their M partitions and the CSV SourceFolder expression, so the
    model still loads real data on first refresh
  relationships + DimDate marked as a date table - that is the star, not the build
  DimDate's sortByColumn bindings (MonthName->Month, DayName->DayNum,
    MonthYear->YearMonth). These point at REAL source columns from the generator,
    not at anything the build added, so they are part of the raw star.
  the registered theme, so a blank page still renders on the intended surface

The previous build is kept whole under _reference/built-2026-08-26/ (report definition,
model definition, design-system.yaml and the build scripts).
"""
import io
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "demo.SemanticModel", "definition")
PAGES = os.path.join(HERE, "demo.Report", "definition", "pages")

PAGE_SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
               "definition/page/2.3.0/schema.json")
PAGES_SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
                "definition/pagesMetadata/1.1.0/schema.json")

# table file -> (calculated column to drop, column whose sortByColumn points at it)
CALC_COLUMNS = {
    "DimQuestType.tmdl": ("DangerOrder", "Danger"),
    "DimAdventurer.tmdl": ("RankOrder", "Rank"),
}


def read(p):
    # newline="" on BOTH read and write. Without it Python rewrites every line
    # ending in the file and the diff becomes unreadable.
    return io.open(p, encoding="utf-8", newline="").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="").write(s)


def strip_measures(path):
    """Drop every `measure ...` block, keeping the table header, column and partition.

    TMDL is indentation-scoped: a measure block runs from its `measure` line until
    the next line at the same indent or shallower. Docstring `///` lines directly
    above a measure belong to it and go too.
    """
    src = read(path)
    nl = "\r\n" if "\r\n" in src else "\n"
    lines = src.split(nl)
    out, i, removed = [], 0, 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)measure\s", line)
        if not m:
            out.append(line)
            i += 1
            continue
        indent = len(m.group(1))
        # Drop the docstring lines already emitted for this measure.
        while out and out[-1].strip().startswith("///"):
            out.pop()
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if nxt.strip() == "":
                # A blank line ends the block only if what follows is not deeper.
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j >= len(lines) or (len(lines[j]) - len(lines[j].lstrip())) <= indent:
                    break
            elif (len(nxt) - len(nxt.lstrip())) <= indent:
                break
            i += 1
        removed += 1
        # Collapse the blank line the block left behind.
        while i < len(lines) and lines[i].strip() == "" and out and out[-1].strip() == "":
            i += 1
    write(path, nl.join(out))
    return removed


def strip_calc_column(path, col, sorted_col):
    """Remove a calculated column block and the sortByColumn line pointing at it."""
    src = read(path)
    nl = "\r\n" if "\r\n" in src else "\n"
    lines = src.split(nl)
    out, i, dropped_col, dropped_sort = [], 0, False, False
    while i < len(lines):
        line = lines[i]
        if re.match(r"^\s*sortByColumn:\s*%s\s*$" % re.escape(col), line):
            dropped_sort = True
            i += 1
            continue
        m = re.match(r"^(\s*)column\s+%s\s*=" % re.escape(col), line)
        if not m:
            out.append(line)
            i += 1
            continue
        indent = len(m.group(1))
        while out and out[-1].strip().startswith("///"):
            out.pop()
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if nxt.strip() == "":
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j >= len(lines) or (len(lines[j]) - len(lines[j].lstrip())) <= indent:
                    break
            elif (len(nxt) - len(nxt.lstrip())) <= indent:
                break
            i += 1
        dropped_col = True
        while i < len(lines) and lines[i].strip() == "" and out and out[-1].strip() == "":
            i += 1
    write(path, nl.join(out))
    return dropped_col, dropped_sort


def reset_pages():
    removed = []
    for name in sorted(os.listdir(PAGES)):
        p = os.path.join(PAGES, name)
        if os.path.isdir(p):
            removed.append(name)
            shutil.rmtree(p)
    blank = os.path.join(PAGES, "Page_1")
    os.makedirs(os.path.join(blank, "visuals"), exist_ok=True)
    write(os.path.join(blank, "page.json"), json.dumps(
        {"$schema": PAGE_SCHEMA, "name": "Page_1", "displayName": "Page 1",
         "displayOption": "FitToPage", "height": 720, "width": 1280},
        indent=2, ensure_ascii=False) + "\n")
    write(os.path.join(PAGES, "pages.json"), json.dumps(
        {"$schema": PAGES_SCHEMA, "pageOrder": ["Page_1"], "activePageName": "Page_1"},
        indent=2, ensure_ascii=False) + "\n")
    return removed


def main():
    print("report")
    for name in reset_pages():
        print("  removed page %s" % name)
    print("  -> one blank Page_1 (1280x720, 0 visuals)")

    print("model")
    n = strip_measures(os.path.join(MODEL, "tables", "_Measures.tmdl"))
    print("  removed %d measures from _Measures (table kept as the home)" % n)
    for fname, (col, sorted_col) in CALC_COLUMNS.items():
        got_col, got_sort = strip_calc_column(
            os.path.join(MODEL, "tables", fname), col, sorted_col)
        print("  %-20s column %s: %s | %s.sortByColumn: %s"
              % (fname, col, "removed" if got_col else "NOT FOUND",
                 sorted_col, "removed" if got_sort else "NOT FOUND"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
