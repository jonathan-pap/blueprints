# calculations/ — atomic files

- `visual-calculation.md` — DAX scoped to one visual (post-aggregation)
- `thin-report-measure.md` — DAX scoped to the whole report (`reportExtensions.json`)
- `reference-line.md` — constant or measure-driven line on a chart
- `error-bar.md` — error / range bars on a chart

## Where DAX lives

| Scope | File | Use when |
|---|---|---|
| Whole model | `<project>.SemanticModel/definition/tables/<table>.tmdl` | Reusable across reports |
| One report | `<project>.Report/definition/reportExtensions.json` | Report-specific only |
| One visual | `visual.json` `visualCalculations` block | Post-aggregation transform, single visual |
