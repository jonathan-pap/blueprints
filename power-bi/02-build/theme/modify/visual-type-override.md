# Override per visual type

Apply formatting only to visuals of one type. `visualStyles["lineChart"]["*"]` overrides all line charts; wildcards (Level 2) below it still apply for properties this override doesn't set.

## Serialize first

```bash
pbir theme serialize "<project>.Report"
```

Find or create the visual-type fragment — typically `<theme>/visual-types/lineChart.json`.

## Example: all line charts in muted gray

```json
{
  "lineStyles": [{ "lineColor": { "solid": { "color": "#999999" } } }],
  "dataPoint": [{ "defaultColor": { "solid": { "color": "#999999" } } }],
  "title": [{ "show": true, "fontSize": 12, "bold": true }]
}
```

## Common targets

- `lineChart`, `clusteredColumnChart`, `clusteredBarChart`, `cardVisual`, `kpi`, `tableEx`, `pivotTable`, `slicer`, `donutChart`, `scatterChart`.

Full visual-type list: see `../examples/visual-types/` (49 per-visual-type override examples) or `../_deep-reference/theme-json-spec.md` for the schema.

## Rebuild + validate

```bash
pbir theme build "<project>.Report"
jq empty "<project>.Report/StaticResources/RegisteredResources/<theme>.json"
pbir validate "<project>.Report"
```

## See also

- `wildcard.md` — applies to every visual
- `../audit/find-overrides.md` — find what visual-level overrides currently exist
- `../promote/from-visuals.md` — lift those into a visual-type override here
