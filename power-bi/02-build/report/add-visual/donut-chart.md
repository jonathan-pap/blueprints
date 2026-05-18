# Add a donut chart

Part-to-whole, single split. Max 5 slices for legibility; above that use a bar chart instead.

## Create

```bash
pbir add visual donutChart "<project>.Report/Overview.Page" --title "Revenue by Category" \
  --x 24 --y 300 --width 400 --height 300
```

## Bind fields

```bash
pbir visuals bind "<...>/Revenue by Category.Visual" \
  -a "Category:Products.Category" -t Column \
  -a "Y:Sales.Revenue"            -t Measure
```

## When NOT to use donut

- More than 5 slices → use a horizontal `bar-chart.md` sorted descending.
- Comparing series across categories → use a `stackedBarChart` or `clusteredBarChart`.
- Showing change over time → never use donuts for time.

## Templates

- `../examples/visuals/default/donutChart.json`
- `../examples/visuals/formatted/donutChart.json`

## After

`../validate/validate.md`.
