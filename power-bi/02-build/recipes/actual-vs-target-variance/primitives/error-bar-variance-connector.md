# P3 — Error-bar variance connector (the trick)

The headline move: Power BI's native **error bars** — meant for ±uncertainty whiskers — are
repurposed to draw the **gap between actual and target**, colored by direction. No custom
visual, no extra series shapes; just two error-bar configs bound to the gated bounds from
[P1](variance-measures.md).

## How it works

An error bar extends from a series' value to an explicit bound. Point that bound at
`GREEN MAX` / `RED MAX` (each BLANK unless the variance has its sign) and the error bar
becomes a one-directional connector that only appears on the right side:

- **On the target series**, `upperBound = GREEN MAX`. When actual **beats** target,
  `GREEN MAX = actual`, so the bar runs **target → actual**, painted `<POS_COLOR>` (green).
- **On the actual series**, `upperBound = RED MAX`. When actual **misses**, `RED MAX = target`,
  so the bar runs **actual → target**, painted `<NEG_COLOR>` (red).

Exactly one fires per period (the other bound is BLANK → no bar). The result looks like a
hand-drawn variance bracket, but it's 100% native.

## The config — `objects.error`

Two pieces per direction: a **style** block (color, width) keyed by series `metadata`, and a
**range** block (the measure bound) keyed by a per-point `dataViewWildcard` selector.

```json
"error": [
  { "properties": { "enabled": { "expr": { "Literal": { "Value": "true" } } },
                    "markerShow": { "expr": { "Literal": { "Value": "false" } } },
                    "barColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'<NEG_COLOR>'" } } } } },
                    "barWidth": { "expr": { "Literal": { "Value": "3D" } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.<ACTUAL_MEASURE>" } },

  { "properties": { "errorRange": { "kind": "ErrorRange", "explicit": {
        "isRelative": { "expr": { "Literal": { "Value": "false" } } },
        "upperBound": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "RED MAX" } } } } } },
    "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 0 } } ],
                  "metadata": "<MEASURE_TABLE>.<ACTUAL_MEASURE>", "highlightMatching": 1 } },

  { "properties": { "errorRange": { "kind": "ErrorRange", "explicit": {
        "isRelative": { "expr": { "Literal": { "Value": "false" } } },
        "upperBound": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "GREEN MAX" } } } } } },
    "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 0 } } ],
                  "metadata": "<MEASURE_TABLE>.<TARGET_MEASURE>", "highlightMatching": 1 } },

  { "properties": { "enabled": { "expr": { "Literal": { "Value": "true" } } },
                    "markerShow": { "expr": { "Literal": { "Value": "false" } } },
                    "barColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'<POS_COLOR>'" } } } } },
                    "barWidth": { "expr": { "Literal": { "Value": "3D" } } } },
    "selector": { "metadata": "<MEASURE_TABLE>.<TARGET_MEASURE>" } }
]
```

## Rules / gotchas

- **`isRelative: false`** — the bound is an absolute value (the other bar's height), not a ±delta.
- **Bind the range with the `dataViewWildcard` selector** (`"data":[{"dataViewWildcard":{"matchingOption":0}}]`)
  so each category evaluates its own `GREEN MAX`/`RED MAX`. Without it the error bar uses one
  value for the whole series and the connectors vanish or stick.
- **Style vs range are separate `error` entries** — color/width keyed by `metadata` (the
  series); the measure bound keyed by the wildcard. Keep both for each direction.
- **Green rides the target series, red rides the actual series** — that's deliberate, so each
  connector starts at the *lower* bar and points up to the *higher* one. Swap them and the
  brackets point the wrong way.
- Error bars are a native object — see `../../report/calculations/error-bar.md` for the
  general feature.

## Generalises to

- Any "distance between two series" mark — last-year vs this-year, plan vs forecast, min vs max.
- Pair with a tolerance gate ([tolerance variant](../variants/tolerance-band-rag.md)) to suppress connectors inside a dead-band.

## Next

[P4 — directional variance label](directional-variance-label.md) adds the ▲/▼ % on top.
