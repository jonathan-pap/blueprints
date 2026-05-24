# Recipe — Disconnected Selection Emphasis

> A disconnected slicer whose selection is **harvested** into boundary measures
> that drive **visual emphasis** (reference-band shading + a gated series) —
> *without filtering the data*. "Time-window highlight" is one application of this.

## The idea in one line

Selection ≠ filtering. A table with **no relationships** can't filter anything, so
its slicer becomes a pure *input*. Measures read the selection back; visual objects
react to it. The rest of the report is untouched.

## When to use

- Highlight a **band** on a chart (a date window, a value range, a target zone) while keeping all data visible.
- **Spotlight** selected items (color them, dim the rest) instead of filtering them out.
- Mark a **comparison period** (selected quarter, prior year) on a trend.
- Any "show me X but emphasise Y" where filtering would hide context.

If you actually want to *remove* non-selected data, use a normal related slicer instead — not this recipe.

## The five primitives

Each is atomic and reusable on its own. Compose them.

1. [Disconnected selection table](primitives/disconnected-selection-table.md) — `VALUES(source[col])`, deliberately unrelated. (P1)
2. [Boundary / harvester measures](primitives/boundary-measures.md) — `MIN`/`MAX` (range) or `SELECTEDVALUE` (single) over the disconnected column. (P2)
3. [Reference-band + shading](primitives/reference-band-shading.md) — axis reference lines at the boundaries with fill between. (P3)
4. [Conditional series (visual calc)](primitives/conditional-series-visual-calc.md) — a `NativeVisualCalculation` that returns the value only inside the selection → drives "labels/markers only in window". (P4)
5. [Self-filter wiring](primitives/self-filter-wiring.md) — slicer self-filter + chart axis/value filters, because the disconnected table can't propagate. (P5)

## Variants (swap the source type + aggregation)

| Variant | Source column | Harvest | Emphasis |
|---|---|---|---|
| [Time-window highlight](variants/time-window-highlight.md) | date | MIN / MAX | shade between two dates (the original skill) |
| [Numeric threshold band](variants/numeric-threshold-band.md) | number | MIN / MAX | shade a value range on the axis |
| [Comparison-period shading](variants/comparison-period-shading.md) | date/period | SELECTEDVALUE | shade one selected period |
| [Category spotlight](variants/category-spotlight.md) | category | selection set | color selected, dim the rest (P3→conditional color) |

## Build it

- Ordered file map + validation → [workflow.md](workflow.md)
- Token reference → [tokens.md](tokens.md)
- Generalized fragments → [templates/](templates/)
- Worked end-to-end example → [examples/sales-monthly-window.md](examples/sales-monthly-window.md)

## Related atomic docs

- `../../report/calculations/visual-calculation.md` — the `NativeVisualCalculation` mechanism (P4)
- `../../report/calculations/reference-line.md` — reference lines (P3)
- `../../model/add/table.md` / `../../model/add/measure.md` — table + measure creation (P1, P2)
- `../../report/add-visual/slicer.md` — slicer visual (P5)
