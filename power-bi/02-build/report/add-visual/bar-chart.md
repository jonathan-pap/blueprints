# Add a bar chart (horizontal)

Use for category comparisons with long labels. Horizontal bars handle long category names better than vertical columns.

## Create

```bash
pbir add visual clusteredBarChart "<project>.Report/Overview.Page" --title "by Region" \
  --x 648 --y 300 --width 608 --height 220
```

## Bind fields

```bash
pbir visuals bind "<...>/by Region.Visual" \
  -a "Category:Geography.Region" -t Column \
  -a "Y:Sales.Revenue" -t Measure
```

## Field roles

- `Category` (Column) — the bars
- `Y` (Measure) — bar length
- `Legend` (Column, optional) — stack/cluster

## Sort

Bar charts → descending by primary measure:

```bash
pbir visuals sort "<...>/by Region.Visual" -f "Sales.Revenue" -d Descending
```

## 100% stacked variant

For a `hundredPercentStackedBarChart` (each category sums to 100%), pass `--name "stk100Bar"` — the auto-generated name overflows the PBIR schema length limit otherwise.

## Templates

- `../examples/visuals/default/barChart.json`
- `../examples/visuals/formatted/barChart-bullet.json` — bullet-chart pattern (banded ranges + actual + target)
- `../examples/visuals/formatted/barChart-divergent.json` — diverging positive / negative
- `../examples/visuals/formatted/barChart-lollipop.json` — lollipop variant
- `../examples/visuals/formatted/barChart-progress.json` — progress-bar pattern
- `../examples/visuals/formatted/clusteredBarChart-variance.json` — variance overlay

## After

`../validate/validate.md`.
