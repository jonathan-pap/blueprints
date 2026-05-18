# Add a waterfall chart

Step bars showing positive / negative contributions to a total. Use for "Q1 → Q4 variance" or "Last Year → This Year breakdown".

## Create

```bash
pbir add visual waterfallChart "<project>.Report/Overview.Page" --title "Revenue Bridge YoY" \
  --x 24 --y 300 --width 800 --height 400
```

## Bind fields

```bash
pbir visuals bind "<...>/Revenue Bridge YoY.Visual" \
  -a "Category:Date.Quarter"     -t Column \
  -a "Breakdown:Products.Category" -t Column \
  -a "Y:Sales.Revenue Variance"  -t Measure
```

## Field roles

- `Category` (Column) — primary x-axis steps (e.g. quarters)
- `Breakdown` (Column, optional) — secondary breakdown within each step
- `Y` (Measure) — the magnitude (typically a variance measure)

## Color rule

Positive contributions auto-color green; negative auto-color red. Override via theme `visualStyles["waterfallChart"]["*"]` if you need different sentiment colors (see `../../theme/modify/visual-type-override.md`).

## Templates

- `../examples/visuals/default/waterfallChart.json`
- `../examples/visuals/formatted/waterfallChart.json`
- `../examples/visuals/formatted/waterfallChart-flash.json`

## After

`../validate/validate.md`.
