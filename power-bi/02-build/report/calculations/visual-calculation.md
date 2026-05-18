# Visual calculation

DAX scoped to one visual, evaluated AFTER the visual's normal aggregation. Use for running totals, moving averages, % of total within the visual.

## CLI

```bash
pbir visuals visual-calc add "<...>/Visual.Visual" \
  --name "Running Total" \
  --expression "RUNNINGSUM([Revenue])"
```

## Common patterns

```dax
RUNNINGSUM([Revenue])                       // cumulative
MOVINGAVERAGE([Revenue], 3)                 // 3-period moving avg
DIVIDE([Revenue], COLLAPSEALL([Revenue]))   // % of grand total
PREVIOUS([Revenue])                         // value from prior row/category
```

## When to use vs thin-report-measure

- **Visual calc** — needs the post-aggregation context (running total across visual rows)
- **Thin-report measure** — same logic needed across multiple visuals; or wants standard DAX context

## After

`../validate/validate.md`.
