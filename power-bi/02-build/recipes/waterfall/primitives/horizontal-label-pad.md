# P5 — Horizontal label pad

**Horizontal variants only.** A transparent right-edge filler that pads every bar out to a
constant total width = `<PREFIX> Axis Max`. Stacked between the bodies and the Anchor, it
gives the Anchor a fixed-position-across-bars for label alignment.

## Why horizontal needs a pad (vertical doesn't)

- **Vertical** has a Y2 role. The anchor line sits on Y2 at a constant height across all
  steps. Labels on the line's data points align top-of-chart for every bar regardless of bar
  height. No pad needed.
- **Horizontal** (`barChart`) has **no Y2 role**. Combo lines don't exist for `barChart`. To
  put labels at a fixed right-edge column across bars of different visible totals, the only
  trick is to fill each bar to the same total width — that's what the pad does.

Without the pad, the Anchor (stacked last in Y) starts at the **end of the visible content**
of each bar, which is different per step. Labels then float at inconsistent positions.

## The DAX

```dax
<PREFIX> Label Pad =
VAR AxisMax = [<PREFIX> Axis Max]
VAR BarTop =
    [<PREFIX> Base]
        + COALESCE ( [<PREFIX> Body · <Step 1>], 0 )
        + COALESCE ( [<PREFIX> Body · <Step 2>], 0 )
        -- ... + COALESCE for every body measure
RETURN
    AxisMax - BarTop
```

`BarTop` is the height of the visible stack at the current step (Base + whatever Body is
non-blank). `AxisMax - BarTop` is the gap to the right edge of the chart — exactly what the
Pad fills.

## Wiring in the visual

**Y projection order matters.** The Pad must come AFTER all bodies and BEFORE the Anchor:

```json
"Y": {
  "projections": [
    { ... <PREFIX> Base ... },
    { ... <PREFIX> Body · Step 1 ... },
    { ... <PREFIX> Body · Step 2 ... },
    /* ... all bodies ... */
    { ... <PREFIX> Label Pad ... },        // <-- HERE
    { ... <PREFIX> Label Anchor ... }      // <-- THEN here
  ]
}
```

**Transparency** — both Pad and Anchor get fully transparent fill:

```json
"dataPoint": [
  /* ... Base, bodies ... */
  { "properties": { "fillTransparency": { "expr": { "Literal": { "Value": "100D" } } } },
    "selector": { "metadata": "_Measures.<PREFIX> Label Pad" } },
  { "properties": { "fillTransparency": { "expr": { "Literal": { "Value": "100D" } } } },
    "selector": { "metadata": "_Measures.<PREFIX> Label Anchor" } }
]
```

**labels** — the Pad gets a placeholder selector with empty `properties: {}` (per the gddt
horizontal pattern), and the Anchor gets the dynamic label binding + position override:

```json
"labels": [
  { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } },
  { "properties": {}, "selector": { "data": [{ "dataViewWildcard": { "matchingOption": 1 } }],
      "metadata": "_Measures.<PREFIX> Label Pad", "highlightMatching": 1 } },
  { "properties": { "dynamicLabelValue": { "expr": { "Measure": {
      ..., "Property": "<PREFIX> Label" /* or "(rich)" */
  } } } },
    "selector": { "data": [{ "dataViewWildcard": { "matchingOption": 1 } }],
      "metadata": "_Measures.<PREFIX> Label Anchor", "highlightMatching": 1 } },
  { "properties": { "color": { ... themed ... },
      "optimizeLabelDisplay": { ... true ... },
      "labelOverflow": { ... true ... },
      "labelPosition": { "expr": { "Literal": { "Value": "'InsideBase'" } } } },
    "selector": { "metadata": "_Measures.<PREFIX> Label Anchor" } },
  /* showSeries: false for Base, every Body, Label Pad — NOT the Anchor */
  { "properties": { "showSeries": { ... false ... } },
    "selector": { "metadata": "_Measures.<PREFIX> Base" } },
  /* ... one per body ... */
  { "properties": { "showSeries": { ... false ... } },
    "selector": { "metadata": "_Measures.<PREFIX> Label Pad" } }
]
```

**Critical** — the Anchor does NOT get `showSeries: false`. See [[pbi-labels-showseries-trap]]
and [P3 — label measures](label-measures.md) for why.

## valueAxis differences (horizontal vs vertical)

In horizontal, the `valueAxis.end` does NOT need to be bound to `<PREFIX> Axis Max` — the Pad
already extends every bar to AxisMax, so the axis auto-scales correctly. Just set
`valueAxis.start: 0` and let the rest auto.

Vertical, by contrast, DOES need `valueAxis.end` bound to Axis Max — there's no pad, so the
auto-axis would only go as far as the tallest bar (no headroom for labels above the bar tops).

## Validation

After creating, run:

```dax
EVALUATE
SUMMARIZECOLUMNS (
    <STEPS_TABLE>[Step], <STEPS_TABLE>[StepSort],
    "BarTop", <stack of Base + Body coalesce>,
    "Pad", [<PREFIX> Label Pad],
    "BarTop + Pad", <BarTop expression> + [<PREFIX> Label Pad]
)
ORDER BY [StepSort]
```

Expected: `BarTop + Pad` is constant across all steps and equals `<PREFIX> Axis Max`. If not,
either the Pad math is wrong or `Axis Max` is changing per step.

## Next

[P6 — stacked sub-segments](stacked-segments.md) if any step splits into composition pieces;
otherwise pick a horizontal [variant](../variants/) (`horizontal-standard.md` or
`horizontal-detailed.md`) and apply the template.
