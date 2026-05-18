# Measure name construction order

Canonical order for the full name of a measure:

```
[Aggregation] [Base Name] [Period] ([Unit])
```

## Examples

| Combination | Result |
|---|---|
| Base only | `Turnover` |
| Base + unit | `Turnover (Quantity)` |
| Base + period | `Turnover 1YP` |
| Base + period + unit | `Turnover 1YP (Quantity)` |
| Aggregation + base + period | `MTD Turnover 1YP` |
| Base + comparison + unit | `Turnover vs 1YP (%)` |
| Aggregation + base + comparison + unit | `MTD Turnover vs 1YP (%)` |

## Why the order matters

Consistent left-to-right reading lets users scan a long measure list and instantly understand each measure's shape:

- **Aggregation prefix** (MTD/QTD/YTD) — most readers look here first when scanning a "Time Intelligence" folder.
- **Base name** — the metric itself (Turnover, Net Sales, Profit).
- **Period suffix** (1YP/2YP) — comparison anchor, scanned to distinguish current vs prior.
- **Unit in parens** — disambiguates (%) from absolute.

## Column name rules (simpler)

Columns don't need the same construction order. They just need:

1. Full, human-readable names with spaces.
2. Standard casing (not snake_case or CamelCase).
3. No abbreviations.
4. Hidden key columns: `[Table Name] Key` pattern.
5. Display folder grouping by purpose (Hierarchy, Attributes, Keys, Facts).

## See also

- `naming-rules.md` — all 11 default rule categories
- `audit-workflow.md` — phased workflow to apply
