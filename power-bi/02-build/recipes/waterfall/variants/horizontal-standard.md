# Variant — Horizontal Standard

`barChart` (horizontal stacked bars) + Pad + Anchor stacked in Y + `<PREFIX> Label` for labels.
The horizontal-version equivalent of vertical-standard.

## Visual

Template: [../templates/horizontal.visual.json](../templates/horizontal.visual.json).

## Required measures

- P1: [steps disconnected table](../primitives/steps-table.md)
- P2: `<PREFIX> Base` + body measures
- P3: `<PREFIX> Label`
- P4: `<PREFIX> Axis Max` + `<PREFIX> Label Anchor`
- **P5: [`<PREFIX> Label Pad`](../primitives/horizontal-label-pad.md) — REQUIRED for horizontal**

Skip P6.

## Why horizontal needs P5

`barChart` has no Y2 role — combo lines are vertical-only. The Pad fills each bar out to a
constant total width = `<PREFIX> Axis Max`, so the Anchor (stacked last in Y) sits at the same
right-edge position across all bars. `labelPosition: 'InsideBase'` then puts the label at the
start of the Anchor segment = right-aligned across the entire chart.

Without Pad, labels would float at inconsistent positions per bar's visible width.

## Label binding

```json
"labels": [
  { "properties": { "show": true } },
  { "properties": {}, "selector": { ... "metadata": "<PREFIX> Label Pad" ... } },
  { "properties": { "dynamicLabelValue": "<PREFIX> Label" },
    "selector": { ... "metadata": "<PREFIX> Label Anchor" ... } },
  { "properties": { "color": themed, "labelPosition": "'InsideBase'", "optimizeLabelDisplay": true, "labelOverflow": true },
    "selector": { "metadata": "<PREFIX> Label Anchor" } },
  // showSeries: false for Base, every Body, Label Pad — NOT the Anchor (showSeries trap)
]
```

See [../primitives/horizontal-label-pad.md](../primitives/horizontal-label-pad.md) for the
full pattern and [[pbi-labels-showseries-trap]] for the gotcha.

## When to choose this

- Long step names (vertical clips them; horizontal gives them their own row).
- 6+ steps (vertical gets cramped).
- Mobile/portrait layouts where vertical space is more abundant than horizontal.

## Sample read

The chart visually reads:
```
  Total Volume        ████████████████████████ 526,274
  NPC Mediated                            ███ -100,329
  Player Volume       ████████████████████ 425,945
  Common+Uncommon                       ████ -357,701
  Rare+ Player        ████ 68,244
```

All labels right-aligned to the same column thanks to the Pad+Anchor trick.
