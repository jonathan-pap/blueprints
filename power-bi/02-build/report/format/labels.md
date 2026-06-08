# Data labels (`objects.labels`)

The `labels` formatting object on a visual controls per-series data-label rendering — show/hide, position, font, color, and the `dynamicLabelValue` binding that swaps a measure's printed value for a label-text measure.

## Anatomy

Each entry in the `labels` array has `properties` (what to set) and optionally `selector` (which series the entry applies to). Without a selector, properties apply to every series.

```json
"labels": [
  { "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "labelPosition": { "expr": { "Literal": { "Value": "'OutsideEnd'" } } },
      "fontSize": { "expr": { "Literal": { "Value": "10D" } } }
  } },
  { "properties": {
      "dynamicLabelValue": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Label Text" } } }
  },
    "selector": { "data": [{ "dataViewWildcard": { "matchingOption": 1 } }], "metadata": "_Measures.Label Anchor", "highlightMatching": 1 }
  }
]
```

Common properties: `show`, `showSeries`, `labelPosition` (`'OutsideEnd'`, `'InsideEnd'`, `'InsideBase'`, `'Above'`), `fontSize`, `color`, `backgroundColor`, `enableValueDataLabel`, `enableBackground`, `dynamicLabelValue`.

## Pitfall — the `showSeries: false` trap on label carriers

`showSeries: false` does TWO things — it hides the series from the legend AND removes the series from the label rendering pipeline. If you apply it to the series that ALSO carries the `dynamicLabelValue` binding, the dynamic label silently never renders. No error, no warning — labels just don't appear, and the math looks right because the binding is technically wired.

**The rule:** apply `showSeries: false` to every OTHER series in the visual, never to the series carrying `dynamicLabelValue`.

A bare carrier (carrier series with no `showSeries` entry) renders the dynamic label correctly. Two examples:

### Vertical combo (Y2 anchor pattern)

The Y2 measure (e.g. waterfall `Item Flow Label Anchor` or variance `MAX VALUE`) carries the label.

```json
"labels": [
  { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } },
  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
    "selector": { "metadata": "_Measures.Item Flow Base" } },
  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
    "selector": { "metadata": "_Measures.Item Flow Body · Items Placed" } },
  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
    "selector": { "metadata": "_Measures.Item Flow Body · Item Rarity" } },
  { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
    "selector": { "metadata": "_Measures.Item Flow Body · Items Sold" } },

  // NO entry for "_Measures.Item Flow Label Anchor" with showSeries: false — it's the carrier.

  { "properties": { "enableValueDataLabel": { "expr": { "Literal": { "Value": "true" } } } },
    "selector": { "metadata": "_Measures.Item Flow Label Anchor" } },
  { "properties": { "dynamicLabelValue": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Item Flow Label" } } } },
    "selector": { "data": [{ "dataViewWildcard": { "matchingOption": 1 } }], "metadata": "_Measures.Item Flow Label Anchor", "highlightMatching": 1 } }
]
```

### Horizontal bar (stacked Pad + Anchor)

The Anchor measure stacked last in Y carries the label; `labelPosition: 'InsideBase'` lands the label at the Anchor segment's start (= right edge of the visible bar).

```json
{ "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
  "selector": { "metadata": "_Measures.Item Flow Label Pad" } },
// NO entry on "_Measures.Item Flow Label Anchor"
```

## Spotting the trap

If labels mysteriously don't render but the math is correct and the visual loads without error, audit your `labels[]` for any entry whose `selector.metadata` matches the carrier measure name AND has `showSeries: false`. Delete that entry.

Confirmed against grand-exchange Item Flow waterfall and variance recipe builds — bit twice in one session 2026-06-04 before the pattern was caught.

## See also

- `../calculations/visual-calculation.md` — `NativeVisualCalculation` carriers
- `../../recipes/waterfall/context.md` — recipe-specific callout under "Critical gotcha — the showSeries trap"
- `../../recipes/actual-vs-target-variance/context.md` — the variance recipe's `% Delta` label carrier (`MAX VALUE`)
