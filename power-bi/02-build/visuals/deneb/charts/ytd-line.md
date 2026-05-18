# Deneb — YTD line chart

Two lines: current year YTD vs prior year YTD. Cleaner for trend comparison than overlaid bars when the period is long.

## Bindings

```bash
pbir visuals bind "<...>/YtdLine.Visual" \
  -a "Category:Date.Calendar Month (ie Jan)" -t Column \
  -a "CY:Sales.Revenue YTD"                   -t Measure \
  -a "PY:Sales.Revenue YTD PY"                -t Measure
```

## Spec

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "name": "dataset" },
  "transform": [
    {
      "fold": ["CY", "PY"],
      "as": ["Series", "Value"]
    }
  ],
  "mark": { "type": "line", "point": true, "tooltip": true },
  "encoding": {
    "x": { "field": "Category", "type": "nominal" },
    "y": { "field": "Value",    "type": "quantitative" },
    "color": {
      "field": "Series",
      "type":  "nominal",
      "scale": { "domain": ["CY","PY"], "range": [{ "expr": "pbiColor(0)" }, "#CCCCCC"] }
    },
    "strokeDash": {
      "condition": { "test": "datum.Series === 'PY'", "value": [4, 4] },
      "value": [1, 0]
    }
  }
}
```

PY shown as dashed gray line; CY as solid theme color. Single legend entry per series.

## Reference

`../examples/visual/ytd-line-chart.json` — full PBIR visual.
