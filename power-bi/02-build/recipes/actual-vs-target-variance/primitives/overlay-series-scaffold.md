# P2 — Overlay-series scaffold

The chart base: a **clustered column** with three Y series sharing the category axis —
**target** (outlined, hollow), **actual** (filled), and **MAX VALUE** (fully transparent).
The first two are the visible comparison; the third is an invisible scaffold that carries the
variance label and reserves headroom.

## The three series — `Y.projections`

```json
"Y": { "projections": [
  { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<TARGET_MEASURE>" } },
    "queryRef": "<MEASURE_TABLE>.<TARGET_MEASURE>", "nativeQueryRef": "Target", "displayName": "Target" },
  { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<ACTUAL_MEASURE>" } },
    "queryRef": "<MEASURE_TABLE>.<ACTUAL_MEASURE>", "nativeQueryRef": "Net", "displayName": "Net" },
  { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "MAX VALUE" } },
    "queryRef": "<MEASURE_TABLE>.MAX VALUE", "nativeQueryRef": " ", "displayName": " " }
] }
```

(The MAX series uses a blank `displayName`/`nativeQueryRef` `" "` so it doesn't clutter the legend.)

## Styling each series — `objects.dataPoint`

```json
"dataPoint": [
  { "properties": { "fill": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0.2 } } } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.<ACTUAL_MEASURE>" } },
  { "properties": { "fill": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } },
                    "borderShow": { "expr": { "Literal": { "Value": "true" } } },
                    "borderColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0.2 } } } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.<TARGET_MEASURE>" } },
  { "properties": { "fillTransparency": { "expr": { "Literal": { "Value": "100D" } } },
                    "fill": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.MAX VALUE" } }
]
```

- **Actual** — solid fill (theme accent).
- **Target** — white fill + colored border → a *hollow outline* bar, the "benchmark ghost".
- **MAX VALUE** — `fillTransparency: 100` → invisible.

## Make the cluster overlap

```json
"layout": [ { "properties": {
  "clusteredGapSize": { "expr": { "Literal": { "Value": "25D" } } },
  "clusteredGapOverlaps": { "expr": { "Literal": { "Value": "true" } } }
} } ]
```

`clusteredGapOverlaps: true` slides the three series **on top of each other** instead of
side by side — so actual sits inside the target outline, and the transparent MAX sits over
both. That overlap is what makes the variance connector ([P3](error-bar-variance-connector.md))
read as one stacked pair rather than separate bars.

## Why the invisible MAX series

It does two jobs no visible series can:
1. **Label anchor** — its top is always at `max(actual, target)`, so the ▲/▼ % label
   ([P4](directional-variance-label.md)) sits above *whichever* bar is taller.
2. **Headroom** — being the tallest series, it sets the axis max, so labels/connectors above
   the actual/target bars don't clip.

Remove it and the label jumps around / clips. Keep it transparent, never hidden.

## Next

[P3 — error-bar variance connector](error-bar-variance-connector.md) draws the gap.
