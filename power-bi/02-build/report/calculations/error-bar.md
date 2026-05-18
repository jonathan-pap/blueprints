# Error bars

Range bars around a chart value. Use for confidence intervals, forecast ranges, min/max bands.

## CLI

```bash
pbir visuals error-bars add "<...>/Visual.Visual" \
  --series "Sales.Revenue" \
  --lower "Sales.Revenue Lower" \
  --upper "Sales.Revenue Upper"
```

## Supported visual types

- `lineChart`
- `clusteredColumnChart`
- `clusteredBarChart`
- `scatterChart`

## Patterns

- **Forecast range** — `--lower` = forecast P10, `--upper` = forecast P90
- **Target band** — `--lower` = target × 0.95, `--upper` = target × 1.05
- **Min/max** — `--lower` and `--upper` from actual measures over the period

## After

`../validate/validate.md`.
