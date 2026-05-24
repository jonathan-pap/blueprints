# Add a line chart

Use for time series. Avoid bar/column charts for time.

## Create

```bash
pbir add visual lineChart "<project>.Report/Overview.Page" --title "Monthly Trend" \
  --x 24 --y 300 --width 608 --height 220
```

## Bind fields

```bash
pbir visuals bind "<...>/Monthly Trend.Visual" \
  -a "Category:Date.Calendar Month (ie Jan)" -t Column \
  -a "Y:Sales.Revenue" -t Measure
```

## Field roles

- `Category` (Column) — time axis
- `Y` (Measure) — value
- `Legend` (Column, optional) — split into multiple lines
- `SmallMultiples` (Column, optional) — panel by category

## Sort

Time series → ascending by date:

```bash
pbir visuals sort "<...>/Monthly Trend.Visual" -f "Date.Date" -d Ascending
```

## Design rules

Propagate formatting to the theme where possible; these are the per-visual exceptions.

- **Markers:** off for dense series (daily-over-a-year), on for sparse (4 quarters). `lineStyles.showMarker`.
- **Data labels off** — lines show trend; precise values belong in tables/tooltips.
- **≤ 3–4 series.** Differentiate by stroke weight + color (primary thick/blue, secondary thin/grey/dashed); beyond that use SmallMultiples.
- **Series labels over a legend** for 2–3 series (`seriesLabels.show` + leader lines) so the reader doesn't cross-reference.
- **Area shading** optional at 85–90% transparency to hint magnitude without overpowering the line.
- **Spotlight the latest point:** add a blank-gated extension measure as a second Y series, show marker+label only on it via the `metadata:"select"` / per-series selector → [../schema-patterns/selectors.md](../schema-patterns/selectors.md).

## Templates

- `../examples/visuals/default/lineChart.json`
- `../examples/visuals/formatted/lineChart.json`
- `../examples/visuals/formatted/lineChart-thresholds.json` — threshold reference lines
- `../examples/visuals/formatted/lineChart-visual-calcs.json` — uses visual calculations
- `../examples/visuals/formatted/lineChart-hillvalley.json` — hill / valley shading by direction

## After

`../validate/validate.md`.
