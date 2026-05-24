# P4 — Directional variance label

The number on top: `% Delta` shown as a **▲/▼ percentage** above each period, **colored**
green when up / red when down. It rides the transparent `MAX VALUE` series ([P2](overlay-series-scaffold.md))
so it always sits above the taller bar, and its color comes from the `Delta Color` measure.

## The arrow comes from the format string

`% Delta` carries a **dynamic format string** with three sections — positive ; negative ; zero —
each prefixed with the matching glyph:

```dax
% Delta = DIVIDE ( [Delta], [<TARGET_MEASURE>] )
-- formatStringDefinition = "▲0%;▼0%;0%"
```

So `+0.12 → ▲12%`, `-0.08 → ▼8%`. The arrow is *formatting*, not a separate field — nothing to
concatenate.

## Put the label on the transparent series

In `objects.labels`, turn series labels **on for `MAX VALUE`** and **off for actual/target**
(so only one label per period), then override the displayed value with `% Delta`:

```json
"labels": [
  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "true" } } },
                    "labelPosition": { "expr": { "Literal": { "Value": "'OutsideEnd'" } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.MAX VALUE" } },

  { "properties": { "dynamicLabelValue": { "expr": { "Measure": {
        "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "% Delta" } } } },
    "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ], "highlightMatching": 1 } },

  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.<TARGET_MEASURE>" } },
  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.<ACTUAL_MEASURE>" } }
]
```

`dynamicLabelValue` swaps the label text from MAX VALUE's own number to `% Delta` while keeping
the label *positioned* by the MAX series. (Actual/target keep their own value labels if you
want them — set `showSeries: true` on those instead.)

## Color the label by direction

A measure-driven label color via the wildcard selector:

```json
{ "properties": { "color": { "solid": { "color": { "expr": { "Measure": {
      "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "Delta Color" } } } } } },
  "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ] } }
```

`Delta Color` returns `<POS_COLOR>` / `<NEG_COLOR>` by sign ([P1](variance-measures.md)). The
`dataViewWildcard` selector is required so it evaluates **per period** — without it every label
takes one color. (Same per-point-selector rule as the rest of the recipe; see
`../../report/format/conditional-fmt-rule.md`.)

## Rules

- **One label per period** — labels on `MAX VALUE` only; off for actual/target (or you get
  three stacked numbers).
- **Arrow = format string, color = measure** — keep them separate; don't bake color into the
  format or glyphs into the measure.
- The `% Delta` dynamic format needs **compatibilityLevel ≥ 1601** and block form (see [workflow](../workflow.md)).

## Next

[P5 — narrative takeaway](narrative-takeaway.md) adds the sentence subtitle.
