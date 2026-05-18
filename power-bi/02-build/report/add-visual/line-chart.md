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

## Templates

- `../examples/visuals/default/lineChart.json`
- `../examples/visuals/formatted/lineChart.json`
- `../examples/visuals/formatted/lineChart-thresholds.json` — threshold reference lines
- `../examples/visuals/formatted/lineChart-visual-calcs.json` — uses visual calculations
- `../examples/visuals/formatted/lineChart-hillvalley.json` — hill / valley shading by direction

## After

`../validate/validate.md`.
