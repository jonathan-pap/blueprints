# Recipe — Pareto chart (cumulative contribution)

> Sorted bars + a cumulative-% line that splits at the 80% mark — the "vital few vs.
> trivial many" reading. Built **entirely from visual calculations**: no rank column,
> no cumulative measure, no model changes. "Easy Pareto" is the name of the trick.

## The idea in one line

A Pareto is just three derived values stacked on a sorted bar chart: each category's
**share of total**, the **running sum** of that share, and a **threshold split** that
colors the cumulative line (and the bars) green up to 80% and red beyond. Visual
calculations compute all three *inside the visual*, so the model stays untouched.

## The trick — why it's "easy"

The naive cumulative `RUNNINGSUM([share])` works *only while the visual stays sorted by
value*. Re-sort the axis (alphabetical, by another column) and the line zig-zags. The fix:

```dax
Easy Pareto = RUNNINGSUM ( [Percent of grand total], ORDERBY ( [<VALUE_MEASURE>], DESC ) )
```

`ORDERBY([value], DESC)` pins the running order to the value itself, so the cumulative is
correct no matter how the bars are sorted. That one argument is the whole recipe. The
traditional approach needs a `RANKX` column **and** a cumulative `CALCULATE` measure in the
model — see the [model-measure variant](variants/model-measure-pareto.md) for that contrast.

## When to use

- "What few categories drive most of the total?" — sales by product, revenue by customer, cost by vendor.
- Quality / root-cause analysis — 80% of defects from 20% of causes (the [count variant](variants/count-pareto.md)).
- Any ranked contribution where you want the cutoff to *pop* without filtering anything out.

If you don't need the cumulative line — just sorted bars — this is overkill; use a plain
column chart.

## The five primitives

Each is atomic and reusable on its own. Compose them inside one combo visual.

1. [Sorted combo base](primitives/sorted-combo-base.md) — `lineStackedColumnComboChart`, category × value, **descending sort**. The sort order *is* the Pareto order. (P1)
2. [Share of total](primitives/share-of-total.md) — `DIVIDE([value], COLLAPSEALL([value], ROWS))` visual calc → each bar's fraction of the grand total. (P2)
3. [Sort-independent cumulative](primitives/sort-independent-cumulative.md) — `RUNNINGSUM([share], ORDERBY([value], DESC))` → the Pareto line. The headline trick. (P3)
4. [Threshold split + emphasis](primitives/threshold-split-emphasis.md) — split the line green/red at 0.8 and color the bars to match. The "vital few" cutoff. (P4)
5. [Dual-axis plumbing](primitives/dual-axis-plumbing.md) — secondary axis fixed 0–100%, percent format, the `dataViewWildcard` per-bar selector, label styling. (P5)

## Variants

| Variant | What changes |
|---|---|
| [Dynamic threshold](variants/dynamic-threshold.md) | the 80% cutoff becomes a slicer/parameter — composes with [disconnected-selection-emphasis](../disconnected-selection-emphasis/context.md) |
| [ABC classification](variants/abc-classification.md) | two bands → three (A 0–80%, B 80–95%, C 95–100%) |
| [Count Pareto](variants/count-pareto.md) | value = a **count** of defects/events — the quality-control framing |
| [Model-measure Pareto](variants/model-measure-pareto.md) | visual calcs → model `RANKX` column + cumulative measure (reusable in cards/tables; pre-visual-calc Power BI) |

## Build it

- Ordered file map + validation → [workflow.md](workflow.md)
- Token reference → [tokens.md](tokens.md)
- Reusable fragments → [templates/](templates/) (`pareto-combo.visual.json`, `visual-calcs.dax`, `model-measures.tmdl`)
- Worked end-to-end example → [examples/product-sales-pareto.md](examples/product-sales-pareto.md)

## Related atomic docs

- `../../report/calculations/visual-calculation.md` — the `NativeVisualCalculation` mechanism + the `pbir visuals visual-calc add` CLI (P2–P4)
- `../../report/add-visual/combo-chart.md` — the line + stacked column combo visual (P1)
- `../../report/format/conditional-fmt-rule.md` — rule-based conditional color for the bars (P4)
- `../../report/calculations/reference-line.md` — an alternative way to draw the 80% marker (P4)
