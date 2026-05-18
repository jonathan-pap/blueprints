# Add a scatter chart

Two continuous axes. Use for correlation between two measures (margin vs revenue, days-to-deliver vs order size).

## Create

```bash
pbir add visual scatterChart "<project>.Report/Overview.Page" --title "Margin vs Volume" \
  --x 24 --y 300 --width 600 --height 400
```

## Bind fields

```bash
pbir visuals bind "<...>/Margin vs Volume.Visual" \
  -a "Category:Products.Product Name"  -t Column \
  -a "X:Sales.Order Count"             -t Measure \
  -a "Y:Sales.Margin %"                -t Measure \
  -a "Size:Sales.Revenue"              -t Measure
```

## Field roles

- `Category` (Column) — what each point represents (one point per category value)
- `X` (Measure) — horizontal axis
- `Y` (Measure) — vertical axis
- `Size` (Measure, optional) — point size (creates a bubble chart)
- `Legend` (Column, optional) — color points by group

## Templates

- `../examples/visuals/default/scatterChart.json`
- `../examples/visuals/formatted/scatterChart.json`
- `../examples/visuals/formatted/scatterChart-flash.json`

## Cap point count

> 500 points becomes visual noise. Use a filter or pre-aggregate.

## After

`../validate/validate.md`.
