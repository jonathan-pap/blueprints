# Worked example — Monthly sales vs target

The recipe applied as the source "Actual vs Target" report builds it: `NET SALES` vs
`TARGET SALES` by month, with green/red error-bar connectors, a ▲/▼ % label, and a narrative
subtitle.

## Token values

| Token | Value |
|---|---|
| `<MEASURE_TABLE>` | `Mesures` |
| `<ACTUAL_MEASURE>` | `NET SALES` |
| `<TARGET_MEASURE>` | `TARGET SALES` |
| `<AXIS_TABLE>` | `Dim_Date` |
| `<AXIS_COLUMN>` | `MoisCourt_2_en` (short month label) |
| `<MONTH_KEY_COLUMN>` | `MoisAnnéeNo` (sortable `"MMYYYY"`) |
| `<YEAR_COLUMN>` | `Année` |
| `<POS_COLOR>` | `#1B7F4A` (green) |
| `<NEG_COLOR>` | `#B00020` (red) |
| `<VISUAL_NAME_CHART>` | `e2c1052a212642eea438` |
| `<PAGE_ID>` | `7d79b06727af40cc8ca1` (an existing page folder) |
| chart pos | x 24 · y 130 · z 1000 · h 402 · w 840 · tab 0 |

## Step 1 — append the measures

Copy [templates/variance-measures.tmdl](../templates/variance-measures.tmdl) into `Mesures.tmdl`
(before its `partition`) and substitute. The core six resolve to:

```dax
Delta       = [NET SALES] - [TARGET SALES]
% Delta     = DIVIDE ( [Delta], [TARGET SALES] )                                   -- "▲0%;▼0%;0%"
MAX VALUE   = IF ( [NET SALES] > [TARGET SALES], [NET SALES], [TARGET SALES] )
GREEN MAX   = IF ( [Delta] > 0, [MAX VALUE] )
RED MAX     = IF ( [Delta] < 0, [MAX VALUE] )
Delta Color = SWITCH ( TRUE (), [Delta] > 0, "#1B7F4A", [Delta] < 0, "#B00020", BLANK () )
```

Plus the four narrative measures (`Number Successful Months`, `Best Month`,
`Longest Winning Streak`, `TAKEAWAY`).

## Steps 2–3 — (optional) format UDF + compat level

For the `€ #,0,,.0"M"` dynamic value format, add [templates/dynamic-format-udf.tmdl](../templates/dynamic-format-udf.tmdl)
to `functions.tmdl` and set `formatStringDefinition = DYNAMIC_FORMATING_INDICATORS()` on
`NET SALES` / `TARGET SALES`. Ensure `database.tmdl` is **compatibilityLevel: 1601**.

## Step 4 — the chart

Copy [templates/actual-vs-target.visual.json](../templates/actual-vs-target.visual.json) to
`Report/definition/pages/7d79b06727af40cc8ca1/visuals/e2c1052a212642eea438/visual.json` and
apply the tokens. It carries the three-series overlay (P2), the green/red error-bar connectors
(P3), the ▲/▼ `% Delta` label colored by `Delta Color` (P4), and the `TAKEAWAY` subtitle (P5).

## Result

- Outlined **target** bars, filled **net** bars, overlapping.
- A **green** bracket on months that beat target, **red** on months that missed — one per month.
- A ▲/▼ **% variance** above each pair, green/red.
- Subtitle: *"In 2024, we beat the target in 7 months, with the strongest overperformance in
  March and the longest winning streak of 4 months."*

## Try the variants

- **vs prior year** instead of target → [yoy-variance](../variants/yoy-variance.md)
- **±2% neutral zone** → [tolerance-band-rag](../variants/tolerance-band-rag.md)
- **by product/region** horizontally → [horizontal-by-category](../variants/horizontal-by-category.md)
- **just the bars** → [minimal-no-narrative](../variants/minimal-no-narrative.md)
