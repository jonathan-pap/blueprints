# Tables & matrices — build best-practices

> Tables sit at the bottom of the detail gradient ([../layout/detail-gradient.md](../layout/detail-gradient.md)) —
> drill-down detail for readers who need specifics. "Easy to create" ≠ "easy to read." Format a
> table to answer a **specific question**, not to display all available data.

## Decide first

1. What question does this table answer? ("Which products are behind target?")
2. Who reads it, what action follows? ("Sales managers re-allocate.")
3. Which columns are essential? Remove everything else.
4. What should they see first? → sort order + emphasis.

## Table vs matrix

| Scenario | Type |
|---|---|
| flat list, no grouping | `tableEx` |
| hierarchical categories (Region > Country > City) | `pivotTable` (matrix) |
| cross-tab (categories on both axes) | `pivotTable` |

**Rule:** 2+ categorical columns where one is a parent of the other → matrix. A flat table with
repeating parent values is a top anti-pattern. → [../add-visual/table.md](../add-visual/table.md), [../add-visual/matrix.md](../add-visual/matrix.md)

## Column order & sort

Left→right by importance: **row labels/hierarchy → primary measure → secondary measures →
variance/delta**. Sort by the most important measure (often the variance) **descending** —
alphabetical rarely answers a question. Time-based detail tables: sort ascending by date.

## Formatting — subtract, don't add

Default styling (gridlines, banded rows, borders) competes with the data. Remove noise, let
whitespace separate:

| Property | Recommended |
|---|---|
| gridlines | horizontal only, or none (vertical = clutter) |
| banded rows | off, or ≤ 2–3% opacity |
| row padding | 6–10px |
| header font | Segoe UI Semibold 10–12pt |
| value font | Segoe UI 10–12pt |
| borders | minimal/none |

Most of this belongs in the **theme**, not per-visual overrides → [../../theme/modify/visual-type-override.md](../../theme/modify/visual-type-override.md).

**Numbers:** tables are for detail — show the model's full format string, **no display units**
(unlike cards). Numbers right-aligned, text left.

## Conditional formatting — strategically

Offload cognition to perception, but formatting everything = formatting nothing.

| Column type | Formatting | Why |
|---|---|---|
| primary measure | data bars | magnitude at a glance |
| variance / delta | color scale or font color | instant good/bad |
| status (OTD %) | color past a threshold | only when the threshold drives a decision |
| dimensions | none | labels need no emphasis |
| secondary measures | none | restraint |

Drive color from an extension measure returning theme tokens, not hardcoded hex (one place to
change, cascades): `OTD Color = IF([OTD %]>=0.9,"good",IF([OTD %]>=0.8,"neutral","bad"))`. Bind
it to `values.fontColor` via a `dataViewWildcard` selector — see [../schema-patterns/selectors.md](../schema-patterns/selectors.md) and [../format/conditional-fmt-rule.md](../format/conditional-fmt-rule.md).

## Sparklines & inline trends

Native sparkline: bind a measure + date to `Values`. For richer inline visuals (dumbbell,
bullet, progress), use SVG measures → [../../visuals/svg/_index.md](../../visuals/svg/_index.md). Only when the context justifies the upkeep.

## Matrix specifics

- **Row hierarchy:** bind broadest → most granular.
- **Subtotals:** on per level by default (usually wanted); hide intermediates on 4+ level hierarchies to save space.
- **Expand/collapse:** start collapsed to the top level — respects the detail gradient.
- **Column hierarchy:** use column headers for time periods / categorical pivots.

## Sizing — and the horizontal-scrollbar trap

- Min height 180–200px (header + 5–8 rows). Tables usually span full page width.
- **Disable auto-size width when the table shares a row** with another visual: `columnHeaders.autoSizeColumnWidth=false`. Auto-size computes widths from content and overflows a constrained container → horizontal scrollbar (hides columns, breaks scanning). Truncation-with-tooltip beats a scrollbar.
- Full-width table → auto-size is usually fine.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| flat table, repeating parents | matrix with hierarchy |
| > 8 columns | cut non-essential; disable auto-size if constrained |
| alphabetical sort | sort by measure/variance descending |
| CF on every column | data bars on primary, color on variance only |
| heavy gridlines + banding | remove; use whitespace |
| display units in a table | show full precision |
| actual + target + variance all shown | show variance alone if it answers the question |

## Review checklist

- [ ] Question + audience + action defined
- [ ] Type matches structure (flat→table, hierarchy→matrix)
- [ ] Only essential columns; ordered dims-left, variance-right
- [ ] Sorted by primary measure/variance descending
- [ ] Noise removed; data bars on primary; color on variance only
- [ ] Full precision, no display units
- [ ] Subtitle hidden; title differentiates from page title
- [ ] Auto-size width off if sharing a row; height ≥ 5–8 rows
