# Deneb — YTD comparison

Compare current year YTD vs prior year YTD as overlaid bars (or grouped lines).

## Bindings

```bash
pbir visuals bind "<...>/YtdComp.Visual" \
  -a "Category:Date.Calendar Month (ie Jan)" -t Column \
  -a "CY:Sales.Revenue YTD"                   -t Measure \
  -a "PY:Sales.Revenue YTD PY"                -t Measure
```

## Spec pattern (overlaid bars)

```json
"layer": [
  {
    "mark": { "type": "bar", "color": "#CCCCCC", "opacity": 0.6 },
    "encoding": {
      "x": { "field": "Category", "type": "nominal" },
      "y": { "field": "PY",       "type": "quantitative" }
    }
  },
  {
    "mark": { "type": "bar", "color": { "expr": "pbiColor(0)" } },
    "encoding": {
      "x": { "field": "Category", "type": "nominal" },
      "y": { "field": "CY",       "type": "quantitative" }
    }
  }
]
```

Light gray PY behind, theme-colored CY in front. Reader sees both the trajectory and where this year diverges.

## Variance label

Add a third layer with a text mark showing `(CY - PY) / PY` as a percentage above each pair.

## Reference

- `../examples/visual/ytd-comparison.json`
- `../examples/visual/ytd-line-chart.json` — line-chart variant
