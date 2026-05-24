# P4 — Conditional series (visual calculation)

A second Y series defined as a **visual calculation** (`NativeVisualCalculation`) that
returns the base value *only* when the axis point falls inside the harvested boundaries.
It renders on top of the main series, carrying the markers/data-labels — so labels appear
**only inside the selection**, while the main line stays clean across the full range.

## The series projection (in `query.queryState.Y.projections`)

```json
{
  "field": {
    "NativeVisualCalculation": {
      "Language": "dax",
      "Expression": "\r\nIF (\r\n    [<AXIS_COLUMN>] >= [<WINDOW_START_MEASURE>]\r\n        && [<AXIS_COLUMN>] <= [<WINDOW_END_MEASURE>],\r\n    [<VALUE_MEASURE>]\r\n)",
      "Name": "<WINDOW_CALC_NAME>"
    }
  },
  "queryRef": "select",
  "nativeQueryRef": "<WINDOW_CALC_NAME>"
}
```

Readable form of the expression:

```dax
IF (
    [<AXIS_COLUMN>] >= [<WINDOW_START_MEASURE>]
        && [<AXIS_COLUMN>] <= [<WINDOW_END_MEASURE>],
    [<VALUE_MEASURE>]
)
```

`BLANK` outside the window → that point isn't drawn → no marker/label there.

## Pairing with formatting

The two series are styled oppositely (in `objects.lineStyles` / `objects.labels`,
selected by `metadata`):

- **`select`** (the visual calc) — markers ON, data labels ON, stroke OFF → it's just dots+labels inside the window.
- **`<MEASURE_TABLE>.<VALUE_MEASURE>`** (the main line) — markers OFF, `showSeries` label OFF → clean continuous line.

```json
"lineStyles": [
  { "properties": { "strokeShow": {"expr":{"Literal":{"Value":"false"}}},
                    "markerColor": {"solid":{"color":{"expr":{"ThemeDataColor":{"ColorId":2,"Percent":0.2}}}}},
                    "markerSize": {"expr":{"Literal":{"Value":"4D"}}} },
    "selector": { "metadata": "select" } },
  { "properties": { "showMarker": {"expr":{"Literal":{"Value":"false"}}} },
    "selector": { "metadata": "<MEASURE_TABLE>.<VALUE_MEASURE>" } }
],
"labels": [
  { "properties": { "show": {"expr":{"Literal":{"Value":"true"}}}, "fontSize": {"expr":{"Literal":{"Value":"8D"}}} } },
  { "properties": { "showSeries": {"expr":{"Literal":{"Value":"false"}}} },
    "selector": { "metadata": "<MEASURE_TABLE>.<VALUE_MEASURE>" } }
]
```

## Requirement — referenced measures must be ON the visual

A visual calculation can only reference fields that are **present in the same visual**.
`[<WINDOW_START_MEASURE>]` / `[<WINDOW_END_MEASURE>]` (and any harvester it uses) must be
added to the chart — put them in the **Tooltips** projection (`query.queryState.Tooltips`).
Omit them and Analysis Services throws *"Column 'NAME' cannot be found or may not be
used in this expression"* at the visual-calc line. The axis column (`[<AXIS_COLUMN>]`) is
already present as the Category, so it needs no extra projection.

```json
"Tooltips": {
  "projections": [
    { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<WINDOW_START_MEASURE>" } },
      "queryRef": "<MEASURE_TABLE>.<WINDOW_START_MEASURE>", "nativeQueryRef": "<WINDOW_START_MEASURE>" },
    { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<WINDOW_END_MEASURE>" } },
      "queryRef": "<MEASURE_TABLE>.<WINDOW_END_MEASURE>", "nativeQueryRef": "<WINDOW_END_MEASURE>" }
  ]
}
```

(Tooltips doubles as the place users read the active selection — two birds.)

## Why a visual calculation (not a model measure)

The condition compares the **axis value of the current point** (`[<AXIS_COLUMN>]`) to the
boundaries. That per-point axis context only exists *in the visual* — a model measure
can't see "the current category on the axis" the same way. Visual calculations evaluate
along the visual's own row/axis, which is exactly what gating-by-position needs.

See `../../report/calculations/visual-calculation.md` for the general mechanism.

## Generalises to

- Markers/labels only inside any band (value, date, rank).
- Conditional **color** instead of a separate series (return a colour string and bind it) → the [category spotlight](../variants/category-spotlight.md) variant.

## Next

[P5 — self-filter wiring](self-filter-wiring.md) makes the slicer and chart filter themselves.
