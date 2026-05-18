# Add a column chart (vertical)

Use for category comparisons with short labels. For long labels use `bar-chart.md`. For time use `line-chart.md`.

## Create

```bash
pbir add visual clusteredColumnChart "<project>.Report/Overview.Page" --title "by Quarter" \
  --x 24 --y 300 --width 608 --height 220
```

## Bind fields

```bash
pbir visuals bind "<...>/by Quarter.Visual" \
  -a "Category:Date.Calendar Quarter" -t Column \
  -a "Y:Sales.Revenue" -t Measure
```

## Field roles

- `Category` (Column)
- `Y` (Measure)
- `Legend` (Column, optional)

## Sort

Descending by measure unless category is ordinal (then ascending by category).

## 100% stacked variant

For a `hundredPercentStackedColumnChart` (each category sums to 100%), pass `--name "stk100Col"` — the auto-generated name overflows the PBIR schema length limit otherwise.

## Templates

- `../examples/visuals/default/columnChart.json`
- `../examples/visuals/formatted/columnChart.json` — custom data-point colors + label formatting

## After

`../validate/validate.md`.
