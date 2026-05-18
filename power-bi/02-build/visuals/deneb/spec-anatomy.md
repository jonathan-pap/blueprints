# Spec anatomy

Minimal Vega-Lite spec that renders in Deneb.

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "name": "dataset" },
  "mark": "bar",
  "encoding": {
    "x": { "field": "Category", "type": "nominal" },
    "y": { "field": "Value",    "type": "quantitative" }
  }
}
```

## Required pieces

- `$schema` — Vega-Lite v5 or Vega v5. Deneb picks dialect from the schema URL.
- `data.name = "dataset"` — Power BI auto-injects the bound fields as a table called `dataset`. Don't pass `values`.
- `mark` — `bar`, `line`, `point`, `arc`, `area`, `rect`, etc.
- `encoding` — fields per visual channel.

## Field references must match the binding

If the spec encodes `field: "Category"`, the visual's field binding role must be named `Category` (or you must alias in the spec).

## Theme integration

```json
"color": { "value": { "expr": "pbiColor(0)" } }
```

Indexes into the report theme `dataColors[]`. Re-theming the report re-colors the visual.

## Title

Set the visual's title via Power BI (`pbir visuals title`), not the spec. Keeps title formatting consistent with native visuals and respects the theme.
