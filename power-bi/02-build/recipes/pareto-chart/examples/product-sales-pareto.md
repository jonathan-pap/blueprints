# Worked example — Product sales Pareto

The recipe applied end-to-end, exactly as the source "Easy Pareto Formatted" page builds it:
`Sold $` by `Product`, descending, with a cumulative line that splits teal/red at 80%. **No
model changes** — the whole thing is one combo visual with five visual calculations.

## Token values

| Token | Value |
|---|---|
| `<CATEGORY_TABLE>` | `02: Product` |
| `<CATEGORY_COLUMN>` | `Product` |
| `<MEASURE_TABLE>` | `00: Calculations` |
| `<VALUE_MEASURE>` | `Sold $` |
| `<THRESHOLD>` | `0.8` (→ `0.8D` in JSON) |
| `<VITAL_COLOR>` | `#1E9790` (teal) |
| `<TRIVIAL_COLOR>` | `#ED4D55` (red) |
| `<VITAL_LABEL_COLOR>` | `#C1DEC1` |
| `<TRIVIAL_LABEL_COLOR>` | `#efb5b9` |
| `<VISUAL_NAME_CHART>` | `722800342dc94d0680d8` |
| `<PAGE_ID>` | `aed1cfde31680b38cb65` (an existing page folder) |
| chart pos | x 0 · y 0 · z 1000 · h 719.62 · w 1280 · tab 1000 |

## Steps 1–3 — one file

Copy [templates/pareto-combo.visual.json](../templates/pareto-combo.visual.json) to
`Report/definition/pages/aed1cfde31680b38cb65/visuals/722800342dc94d0680d8/visual.json` and
apply the token values above. That single file carries P1 (sorted combo), P2–P4 (the five
visual calcs), and P4–P5 (conditional fill + secondary axis). No TMDL is touched.

The five visual calcs resolve to:

```dax
Percent of grand total = DIVIDE ( [Sold $], COLLAPSEALL ( [Sold $], ROWS ) )
Pareto                 = RUNNINGSUM ( [Percent of grand total] )                                  -- hidden, the "before"
Easy Pareto            = RUNNINGSUM ( [Percent of grand total], ORDERBY ( [Sold $], DESC ) )      -- the trick
GreenLine              = IF ( [Easy Pareto] <= 0.8, [Easy Pareto] )                               -- vital few (teal)
RedLine                = IF ( [Easy Pareto] >  0.8, [Easy Pareto] )                               -- trivial many (red)
```

## Result

- Bars descend by `Sold $` left→right; the secondary axis is fixed 0%–100%.
- The cumulative line climbs teal to the 80% mark, then turns red — and the bars under the
  teal run are teal, the rest red. The "vital few" products are unmistakable.
- Re-sorting the axis (alphabetical, by another column) keeps the line a smooth Pareto curve,
  because `Easy Pareto` accumulates by `ORDERBY([Sold $], DESC)`, not by display order.

## Try the variants on this same chart

- **Dynamic threshold** — add a `Threshold Slicer` and let reviewers drag the cutoff. → [dynamic-threshold](../variants/dynamic-threshold.md)
- **ABC** — split products into A/B/C at 80%/95%. → [abc-classification](../variants/abc-classification.md)
- **"How many products = 80%?"** in a card — needs the model-measure approach. → [model-measure-pareto](../variants/model-measure-pareto.md)
