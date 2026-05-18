# Deneb — bar chart (Vega-Lite)

Use Deneb bar only when native bar can't express it (custom mark, layered annotations, advanced interaction). Otherwise use `../../report/add-visual/bar-chart.md`.

## Bindings

```bash
pbir visuals bind "<...>/MyBar.Visual" \
  -a "Category:Geography.Region" -t Column \
  -a "Y:Sales.Revenue"           -t Measure
```

## Spec

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "name": "dataset" },
  "mark": { "type": "bar", "tooltip": true },
  "encoding": {
    "y": { "field": "Category", "type": "nominal", "sort": "-x" },
    "x": { "field": "Y",        "type": "quantitative" },
    "color": { "value": { "expr": "pbiColor(0)" } }
  }
}
```

`sort: "-x"` orders bars descending by value (best practice for category comparisons).

## Variants

- **Horizontal** (above): `y = Category`, `x = Y`. Good for long category labels.
- **Vertical**: swap — `x = Category`, `y = Y`. Good for short labels.

## See also

- `../examples/spec/vega/bar-chart.json` (Vega version)
- `selection-signals.md` for cross-filter integration
