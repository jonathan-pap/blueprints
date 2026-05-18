# Add an area chart

Filled time-series. Use for cumulative trends or part-to-whole over time. For pure trend use `line-chart.md`.

## Create

```bash
pbir add visual areaChart "<project>.Report/Overview.Page" --title "Cumulative Revenue" \
  --x 24 --y 300 --width 608 --height 220
```

## Bind fields

```bash
pbir visuals bind "<...>/Cumulative Revenue.Visual" \
  -a "Category:Date.Date" -t Column \
  -a "Y:Sales.Revenue"    -t Measure
```

## Variants

- **Stacked area** — `pbir add visual stackedAreaChart ...` for part-to-whole over time. Add a `Legend` role binding to split.
- **Multiple series** — bind `Legend:Products.Category` for overlaid (not stacked) areas.
- **100% stacked area** — `pbir add visual hundredPercentStackedAreaChart ... --name "stk100Area"`. **Must pass `--name`** — the auto-generated visual name overflows the PBIR schema length limit otherwise.

## Templates

- `../examples/visuals/default/areaChart.json`
- `../examples/visuals/default/stackedAreaChart.json`
- `../examples/visuals/formatted/areaChart-multiple.json` (multi-series with line styles)
- `../examples/visuals/formatted/stackedAreaChart.json`

## After

`../validate/validate.md`.
