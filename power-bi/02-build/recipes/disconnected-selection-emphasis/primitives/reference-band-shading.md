# P3 — Reference-band + shading

Two axis reference lines placed at the [boundary measures](boundary-measures.md), each
with shading, so the area between them reads as a highlighted band. Lives in the
chart's `objects.xAxisReferenceLine` (or `yAxisReferenceLine` for value bands).

## Pattern (two lines, shade-between via overlap)

The trick: both lines shade `'before'` (toward the axis origin). The **end** line shades
everything before it at high transparency; the **start** line shades everything before
*it* opaque in the page colour — visually erasing the pre-window area and leaving only
the window tinted.

```json
"xAxisReferenceLine": [
  {
    "properties": {
      "show":   { "expr": { "Literal": { "Value": "true" } } },
      "displayName": { "expr": { "Literal": { "Value": "'window end'" } } },
      "value": { "expr": { "Aggregation": {
        "Expression": { "Column": {
          "Expression": { "SourceRef": { "Entity": "<SELECTION_TABLE_NAME>" } },
          "Property": "<SOURCE_COLUMN>" } },
        "Function": 4 } } },                       // 4 = Max  → window end
      "shadeShow":   { "expr": { "Literal": { "Value": "true" } } },
      "shadeRegion": { "expr": { "Literal": { "Value": "'before'" } } },
      "position":    { "expr": { "Literal": { "Value": "'back'" } } },
      "shadeTransparency": { "expr": { "Literal": { "Value": "85D" } } },
      "width": { "expr": { "Literal": { "Value": "1D" } } }
    },
    "selector": { "id": "1" }
  },
  {
    "properties": {
      "show":   { "expr": { "Literal": { "Value": "true" } } },
      "displayName": { "expr": { "Literal": { "Value": "'window start'" } } },
      "value": { "expr": { "Aggregation": {
        "Expression": { "Column": {
          "Expression": { "SourceRef": { "Entity": "<SELECTION_TABLE_NAME>" } },
          "Property": "<SOURCE_COLUMN>" } },
        "Function": 3 } } },                       // 3 = Min  → window start
      "shadeShow":   { "expr": { "Literal": { "Value": "true" } } },
      "shadeRegion": { "expr": { "Literal": { "Value": "'before'" } } },
      "position":    { "expr": { "Literal": { "Value": "'back'" } } },
      "shadeColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } },
      "shadeTransparency": { "expr": { "Literal": { "Value": "0D" } } },
      "width": { "expr": { "Literal": { "Value": "1D" } } }
    },
    "selector": { "id": "2" }
  }
]
```

## Aggregation function codes

| `Function` | Meaning |
|---|---|
| 3 | Min |
| 4 | Max |
| 0 | Sum · 1 Avg · 2 Count (others, rarely used here) |

So the reference line `value` aggregates the disconnected column directly — you don't
even strictly need the P2 measures for the *lines* (they aggregate the column), but you
do need P2 for tooltips and for [P4](conditional-series-visual-calc.md).

## Rules

- `position: 'back'` keeps the band behind the data.
- The start line's `shadeColor` should match the page background (here `ColorId 0`) so the pre-window region looks blank, not tinted.
- For a **value** band (numeric Y axis) use the same shape under `yAxisReferenceLine`.
- Two unique `selector.id`s ("1","2") are required — they're distinct reference-line instances.

## Next

[P4 — conditional series](conditional-series-visual-calc.md) adds in-window data labels/markers.
