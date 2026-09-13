"""model_tweaks - idempotent model settings the native visuals need, re-applied on every build.

Why a build step and not a one-off edit: synthetic-data's handoff_to_pbi.py rewrites the Dim table
TMDL whenever the data is re-spliced, which would silently drop anything added by hand.

- sortByColumn on every ordinal label, so native visuals sort Copper < Bronze < Silver < Gold instead
  of alphabetically. The order columns are LITERAL member columns, never derived from the column they
  sort - the circular-dependency trap in 02-build/report/validate/build-traps.md #3.
- MonthYear ("Jan 2023") sorted by YearMonth (202301): a categorical month axis in time order. The
  numeric YearMonth alone reads as a continuous axis with a hole between 202312 and 202401.
- the order columns hidden, so nobody drags RankOrder into a visual by mistake.

Run with Power BI Desktop CLOSED (it rewrites TMDL on save).
TMDL: column properties at depth 2 (two tabs); line endings preserved as found.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.normpath(os.path.join(HERE, "..", "realm-chronicle.SemanticModel", "definition", "tables"))

# table -> [(label column, order column)]
SORTS = {
    "DimAdventurer": [("Rank", "RankOrder")],
    "DimQuest":      [("Danger", "DangerOrder"), ("RankRequired", "RankRequiredOrder")],
    "DimItem":       [("Rarity", "RarityOrder")],
    "DimMonster":    [("Kind", "KindOrder")],
    "DimDate":       [("MonthYear", "YearMonth")],
}
HIDE = {"RankOrder", "DangerOrder", "RankRequiredOrder", "RarityOrder", "KindOrder"}


def _blocks(lines):
    """Yield (start, end) line spans of each `column X` block (end exclusive)."""
    starts = [i for i, l in enumerate(lines) if re.match(r"^\t(column|measure|partition|hierarchy) ", l)]
    starts.append(len(lines))
    for a, b in zip(starts, starts[1:]):
        if lines[a].startswith("\tcolumn "):
            yield a, b


def apply():
    changes = []
    for table, pairs in SORTS.items():
        path = os.path.join(TABLES, table + ".tmdl")
        raw = io.open(path, encoding="utf-8", newline="").read()
        eol = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(eol)
        sort_for = dict(pairs)
        edits = []                                   # (insert_after_index, text)
        for a, b in _blocks(lines):
            name = lines[a][len("\tcolumn "):].strip().strip("'")
            body = lines[a + 1:b]
            last_prop = max((i for i in range(a + 1, b) if lines[i].startswith("\t\t")), default=a)
            if name in sort_for and not any(l.strip().startswith("sortByColumn:") for l in body):
                edits.append((last_prop, "\t\tsortByColumn: " + sort_for[name]))
                changes.append("%s[%s] sortByColumn %s" % (table, name, sort_for[name]))
            if name in HIDE and not any(l.strip() == "isHidden" for l in body):
                edits.append((a, "\t\tisHidden"))
                changes.append("%s[%s] hidden" % (table, name))
        for idx, text in sorted(edits, key=lambda e: e[0], reverse=True):
            lines.insert(idx + 1, text)
        if edits:
            io.open(path, "w", encoding="utf-8", newline="").write(eol.join(lines))
    return changes


if __name__ == "__main__":
    for c in apply() or ["no changes - already applied"]:
        print("  " + c)
