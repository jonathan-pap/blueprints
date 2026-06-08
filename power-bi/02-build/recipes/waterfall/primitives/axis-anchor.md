# P4 — Axis max + label anchor

Two small but essential measures that make the waterfall render correctly. Without them the
axis cuts off labels and labels have nowhere to attach.

## `<PREFIX> Axis Max` — dynamic value-axis end

The maximum y-value the chart should display, with headroom for labels:

```dax
<PREFIX> Axis Max =
    CEILING ( [<FIRST_TOTAL_MEASURE>] * <AXIS_MAX_HEADROOM>, <AXIS_MAX_ROUND> )
```

Where:
- `<FIRST_TOTAL_MEASURE>` is the source of the first TOTAL step (e.g. `[Trade Quantity]`).
  That's the bar that defines the maximum height the chart needs to display.
- `<AXIS_MAX_HEADROOM>` defaults to `1.15` (15% above the first total — enough space for labels
  at the top).
- `<AXIS_MAX_ROUND>` defaults to a sensible round-up unit based on scale (`10`, `1000`,
  `1000000` etc.). Round-up makes the axis tick marks land on clean numbers.

Bound in `visual.json` at `objects.valueAxis[0].properties.end`:

```json
"valueAxis": [{ "properties": {
  "end": { "expr": { "Measure": {
      "Expression": { "SourceRef": { "Entity": "_Measures" } },
      "Property": "<PREFIX> Axis Max"
  } } }
} }]
```

**Why dynamic** — when filters change context (e.g. a date slicer narrowing the data), the
headline total changes too. A dynamic axis max scales with the data so the chart stays
proportionate. A hardcoded axis end would either crop on large data or leave huge empty space
on small data.

## `<PREFIX> Label Anchor` — the carrier

A single constant value used to position the label-rendering series. For vertical waterfalls,
this is a Y2 line; for horizontal, it's stacked LAST in Y.

```dax
<PREFIX> Label Anchor = [<FIRST_TOTAL_MEASURE>]
```

That's it. The anchor's value equals the first-total source — meaning the line (vertical) or
stack segment (horizontal) sits at the same height as the chart's headline total. Its label
binding (`dynamicLabelValue → <PREFIX> Label`) puts the label at that fixed position per step.

### Vertical — Y2 line

In the visual.json the anchor is on Y2:

```json
"Y2": {
  "projections": [
    { "field": { "Measure": { ..., "Property": "<PREFIX> Label Anchor" } } }
  ]
}
```

Combined with `lineStyles.showMarker: false` and `lineStyles.strokeTransparency: 100D` the
line itself is invisible — only its data labels render, at the configured `labelPosition`.

### Horizontal — stacked last in Y

For `barChart` (no Y2 role), the anchor goes in Y as the LAST stacked series, after a
transparent Pad ([P5](horizontal-label-pad.md)) that fills each bar out to AxisMax. The
anchor's segment then sits at the same fixed right edge across all bars, and
`labelPosition: 'InsideBase'` places the label at the start of that segment = right-aligned
across every bar.

```json
"Y": {
  "projections": [
    /* ... Funnel Base, body measures ... */
    { "field": { "Measure": { ..., "Property": "<PREFIX> Label Pad" } } },
    { "field": { "Measure": { ..., "Property": "<PREFIX> Label Anchor" } } }
  ]
}
```

Both Pad and Anchor have `fillTransparency: 100D` so they're invisible.

## Anchor color (horizontal only)

When the anchor is in the Y stack (horizontal), its label color defaults to the series color.
Override with the theme's text color:

```json
{ "properties": { "color": { "solid": { "color": { "expr": {
    "ThemeDataColor": { "ColorId": 1, "Percent": 0 } } } } },
    "optimizeLabelDisplay": { "expr": { "Literal": { "Value": "true" } } },
    "labelOverflow": { "expr": { "Literal": { "Value": "true" } } },
    "labelPosition": { "expr": { "Literal": { "Value": "'InsideBase'" } } } },
  "selector": { "metadata": "_Measures.<PREFIX> Label Anchor" } }
```

`optimizeLabelDisplay: true` + `labelOverflow: true` together let the label extend beyond
the (invisible) anchor segment's bounds when the text doesn't fit.

## Sanity check

After creating both measures, validate via DAX query:

```dax
EVALUATE
ROW (
    "AxisMax", [<PREFIX> Axis Max],
    "Anchor", [<PREFIX> Label Anchor]
)
```

Expected: `AxisMax` ≈ `Anchor × 1.15` rounded up. If `AxisMax` is BLANK, `<FIRST_TOTAL_MEASURE>`
is wrong or BLANK in the current filter context.

## Next

- For **horizontal** variants: [P5 — horizontal label pad](horizontal-label-pad.md).
- For **stacked composition**: [P6 — stacked sub-segments](stacked-segments.md).
- Otherwise: pick a [variant](../variants/) and apply the template.
