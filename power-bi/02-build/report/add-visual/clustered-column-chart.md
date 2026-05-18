# Add a clustered column chart

Same as `column-chart.md` but with a `Legend` field that splits each category into grouped bars.

## Create

```bash
pbir add visual clusteredColumnChart "<project>.Report/Overview.Page" --title "Revenue by Quarter & Product" \
  --x 24 --y 300 --width 608 --height 280
```

## Bind fields

```bash
pbir visuals bind "<...>/Revenue by Quarter & Product.Visual" \
  -a "Category:Date.Calendar Quarter" -t Column \
  -a "Y:Sales.Revenue" -t Measure \
  -a "Legend:Products.Category" -t Column
```

## Limit the legend

More than ~5 legend values → switch to small multiples or a different visual:

```bash
pbir visuals bind "<...>" -a "SmallMultiples:Products.Category" -t Column
```

## Templates

- `../examples/visuals/formatted/clusteredBarChart-variance.json` — variance analysis with custom data-point colors

## After

`../validate/validate.md`.
