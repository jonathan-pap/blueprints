# Workflow — assemble the recipe

The **base Pareto touches no model files** — it's five visual calculations and some
formatting on a single combo visual. Only the [model-measure variant](variants/model-measure-pareto.md)
edits TMDL. Substitute [tokens](tokens.md) first.

## Ordered file map (base recipe)

| # | Action | File | Primitive · Template |
|---|---|---|---|
| 1 | **Create** the combo visual | `Report/definition/pages/<PAGE_ID>/visuals/<VISUAL_NAME_CHART>/visual.json` | P1 · [pareto-combo.visual.json](templates/pareto-combo.visual.json) |
| 2 | **Confirm** the 5 visual calcs are in the `Y` / `Y2` projections | (same file) | P2·P3·P4 · [visual-calcs.dax](templates/visual-calcs.dax) |
| 3 | **Confirm** the conditional bar fill + axis/format objects | (same file) | P4·P5 |

The whole recipe is one file. The template already contains all three pieces wired
together; steps 2–3 are read-throughs to verify they survived token substitution.

### Or build it incrementally with the CLI

If you'd rather grow it from a plain combo chart than paste the template:

```bash
# 1. add a line + stacked column combo with the category + value
pbir add visual "<project>.Report" --page <PAGE_ID> \
  --type lineStackedColumnComboChart \
  --category "<CATEGORY_TABLE>.<CATEGORY_COLUMN>" \
  --y "<MEASURE_TABLE>.<VALUE_MEASURE>"

# 2. add the visual calculations (order matters — share before cumulative)
pbir visuals visual-calc add "<...>/<VISUAL_NAME_CHART>.Visual" \
  --name "Percent of grand total" --expression "DIVIDE([<VALUE_MEASURE>], COLLAPSEALL([<VALUE_MEASURE>], ROWS))"
pbir visuals visual-calc add "<...>/<VISUAL_NAME_CHART>.Visual" \
  --name "Easy Pareto" --expression "RUNNINGSUM([Percent of grand total], ORDERBY([<VALUE_MEASURE>], DESC))"
pbir visuals visual-calc add "<...>/<VISUAL_NAME_CHART>.Visual" \
  --name "GreenLine" --expression "IF([Easy Pareto]<=<THRESHOLD>,[Easy Pareto])"
pbir visuals visual-calc add "<...>/<VISUAL_NAME_CHART>.Visual" \
  --name "RedLine"   --expression "IF([Easy Pareto] > <THRESHOLD>, [Easy Pareto])"
```

Then hand-apply the secondary axis + conditional fill objects from the template (the CLI
doesn't write those). See P5.

## Why this order

- **Sort first (P1).** Descending sort by `<VALUE_MEASURE>` is what makes the bars a Pareto. Without it the cumulative still computes (P3's `ORDERBY` is robust) but the bars look random.
- **Share before cumulative (P2 → P3).** `Easy Pareto` references `[Percent of grand total]`; a visual calc can only reference calcs already defined on the visual.
- **Cumulative before split (P3 → P4).** `GreenLine`/`RedLine` and the bar fill all read `[Easy Pareto]`.
- **Plumbing last (P5).** Fix the secondary axis to 0–1 and the percent format only once the cumulative series exist on `Y2`.

## Validation

- Bars descend left→right; the cumulative line climbs to 100% at the last bar.
- The line is **green up to the 80% mark, red after** — and the bars under the green run are green, the rest red.
- **Re-sort the axis alphabetically** (temporarily): the line should *stay* a smooth Pareto curve. If it zig-zags, you used the naive `RUNNINGSUM` without `ORDERBY` — fix P3.
- Secondary axis reads 0%–100% (fixed), not auto-scaled.
- `pbir validate "<project>.Report"` is clean.

## Adapt for a variant

- [dynamic-threshold](variants/dynamic-threshold.md) — replace the `0.8` literals with a `[Selected Threshold]` harvester measure (adds a small disconnected table).
- [abc-classification](variants/abc-classification.md) — three line segments + three bar colors instead of two.
- [count-pareto](variants/count-pareto.md) — swap `<VALUE_MEASURE>` for a `COUNT`/count measure; everything else is identical.
- [model-measure-pareto](variants/model-measure-pareto.md) — replace the visual calcs with a `RANKX` column + cumulative measure (touches `model.tmdl`); use when you need the cumulative in cards/tables too.

## Gotchas

- **`ORDERBY` is the recipe.** `RUNNINGSUM([share])` alone is sort-dependent and silently wrong after a re-sort.
- **Conditional bar fill needs the per-point selector.** A measure/SelectRef-driven `dataPoint.fill` must carry `"selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ] }` or every bar renders the same color. The template includes it.
- **Visual-calc names are case-sensitive references.** `[Percent of grand total]`, `[Easy Pareto]` etc. must match exactly across expressions — keep the names as shipped unless you rename every reference in lockstep.
- Every `lineageTag` / `PBI_Id` / visual `name` must be fresh and unique — see [tokens.md](tokens.md).
- Edit with Power BI Desktop **closed**, then reopen to verify (Desktop overwrites on-disk files when it saves).
