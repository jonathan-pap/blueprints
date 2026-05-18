# Deneb — bullet chart

Bullet charts show actual vs target on a banded range (poor / satisfactory / good). Native PBI can fake this with a bar + error bar; Deneb does it cleanly.

## Bindings

```bash
pbir visuals bind "<...>/MyBullet.Visual" \
  -a "Category:Geography.Region"      -t Column \
  -a "Actual:Sales.Revenue"           -t Measure \
  -a "Target:Sales.Revenue Target"    -t Measure \
  -a "Range1:Sales.Revenue 50pct"     -t Measure \
  -a "Range2:Sales.Revenue 80pct"     -t Measure \
  -a "Range3:Sales.Revenue 100pct"    -t Measure
```

## Reference example

`../examples/visual/bullet-chart.json` — full working PBIR visual block.
`../examples/spec/vega-lite/bullet-chart.json` — spec-only.

## Layers

1. Three background bands (`mark: bar`, light to dark gray)
2. Actual bar (`mark: bar`, dark color)
3. Target tick (`mark: tick`, contrasting color, on top)

Stacked vertically per category. Repeat across `Category` via Vega-Lite faceting.

## Why bullet over bar+error

- Cleaner visual hierarchy.
- Easier to label each band.
- Standard in dashboarding (Stephen Few popularized the form).
