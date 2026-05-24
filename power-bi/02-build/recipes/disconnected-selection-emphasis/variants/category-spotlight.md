# Variant — Category spotlight

Let the user pick categories from a disconnected slicer and **emphasise** them — color the
selected, dim the rest — instead of filtering the others away. Keeps the full ranking/context
visible while drawing the eye.

## Deltas from the base recipe

This variant swaps the *band* (P3) for *conditional color*, and uses P4 to drive the colour.

| Primitive | Change |
|---|---|
| P1 source | `VALUES( <dim>[<Category>] )` — the category domain, multi-select. |
| P2 harvest | not MIN/MAX — instead a membership test measure: `Is Selected = INT( <category> IN VALUES( '<SELECTION_TABLE>'[<Category>] ) )` or `ISCROSSFILTERED`-style check against the disconnected selection. |
| P3 band | **omit** — no axis band for categorical emphasis. |
| P4 emphasis | a color measure: `Bar Color = IF( [Is Selected] = 1, "<accent>", "<muted grey>" )`, bound to the visual's `dataPoint.fill` via conditional formatting. |
| P5 slicer | standard list slicer on the disconnected category column; chart keeps its own filters for scope. |

## Color measure

```dax
Spotlight Color =
VAR _sel = VALUES ( '<SELECTION_TABLE>'[<Category>] )
RETURN
    IF (
        SELECTEDVALUE ( <dim>[<Category>] ) IN _sel || NOT ISFILTERED ( '<SELECTION_TABLE>'[<Category>] ),
        "#2D6948",   -- selected (or nothing picked → all normal)
        "#D8D5CC"    -- dimmed
    )
```

Bind it via `pbir visuals cf "<Visual>" --measure "dataPoint.fill <MEASURE_TABLE>.Spotlight Color"`
(see `../../report/format/` conditional-formatting docs).

**Critical — the per-point selector.** A measure-bound `dataPoint.fill` must carry a
`dataViewWildcard` selector or it won't evaluate per bar (every bar renders the same /
default color — looks like nothing highlights). The CLI writes it for you; hand-rolled JSON
must include it:

```json
"dataPoint": [
  {
    "properties": { "fill": { "solid": { "color": { "expr": {
      "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "Spotlight Color" } } } } } },
    "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ] }
  }
]
```

Prefer the CLI (`pbir visuals cf … --measure …`) over hand-writing this — it gets the selector right.

## Use when

- A ranked bar chart where you want to keep all bars but highlight a chosen few.
- Map / scatter emphasis of selected segments.

## Note

This is the most generalised form of the pattern: the disconnected selection drives a
*property* (color) rather than a *band*. Same principle — selection ≠ filtering.
