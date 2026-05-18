# Deneb — line chart (Vega-Lite)

## Bindings

```bash
pbir visuals bind "<...>/MyLine.Visual" \
  -a "Category:Date.Date" -t Column \
  -a "Y:Sales.Revenue"    -t Measure
```

## Spec

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "name": "dataset" },
  "mark": { "type": "line", "tooltip": true, "point": true },
  "encoding": {
    "x": { "field": "Category", "type": "temporal" },
    "y": { "field": "Y",        "type": "quantitative" },
    "color": { "value": { "expr": "pbiColor(0)" } }
  }
}
```

## Multi-series

Add a Legend role binding (`Products.Category` for example), then:

```json
"color": { "field": "Legend", "type": "nominal", "scale": { "range": { "expr": "pbiColorRange()" } } }
```

`pbiColorRange()` returns the theme's full palette as an array — series get distinct colors automatically.

## Latest-point label

Common request. Add a layered mark:

```json
"layer": [
  { "mark": "line" },
  {
    "mark": { "type": "text", "align": "left", "dx": 6 },
    "encoding": {
      "x": { "aggregate": "max", "field": "Category", "type": "temporal" },
      "y": { "aggregate": { "argmax": "Category" }, "field": "Y", "type": "quantitative" },
      "text": { "aggregate": { "argmax": "Category" }, "field": "Y", "format": ",.0f" }
    }
  }
]
```

## See also

- `../examples/spec/vega/line-chart.json`
- `charts/trend-with-target.md` for adding a target line
