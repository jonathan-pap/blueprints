# Deneb — trend with target line

Line chart with a horizontal target line and shaded area above/below target.

## Bindings

```bash
pbir visuals bind "<...>/MyTrend.Visual" \
  -a "Category:Date.Month"          -t Column \
  -a "Y:Sales.Revenue"              -t Measure \
  -a "Target:Sales.Revenue Target"  -t Measure
```

## Layers

```json
"layer": [
  {
    "mark": "area",
    "transform": [{ "calculate": "datum.Y - datum.Target", "as": "Variance" }],
    "encoding": {
      "x": { "field": "Category", "type": "temporal" },
      "y": { "field": "Y",        "type": "quantitative" },
      "y2":{ "field": "Target",   "type": "quantitative" },
      "color": {
        "condition": { "test": "datum.Variance >= 0", "value": "#2B7A78" },
        "value": "#D4602E"
      },
      "opacity": { "value": 0.2 }
    }
  },
  { "mark": { "type": "line", "color": { "expr": "pbiColor(0)" } } },
  {
    "mark": { "type": "rule", "color": "#999", "strokeDash": [4, 4] },
    "encoding": { "y": { "field": "Target", "aggregate": "average", "type": "quantitative" } }
  }
]
```

Shows the gap visually: green-shaded area = ahead of target, orange-shaded = behind.

## Reference

- `../examples/visual/trend-line.json` — full PBIR visual
- `../examples/visual/ytd-comparison.json` — variant with YTD target
