# `visual.json` — the root structure

> Every hand-authored visual must follow this skeleton. Misplacing a top-level key (especially `visualContainerObjects`) makes Desktop reject the visual with a cascade of schema errors.

## The skeleton

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
  "name": "20-char-hex-id",
  "position": { "x": 24, "y": 64, "z": 0, "height": 320, "width": 600, "tabOrder": 0 },
  "visual": {
    "visualType": "lineChart",
    "query": { "queryState": { ... } },
    "objects": { ... },
    "visualContainerObjects": { ... },
    "drillFilterOtherVisuals": true
  },
  "filterConfig": { ... }
}
```

Five root keys: `$schema`, `name`, `position`, `visual`, optionally `filterConfig`. Everything chart-shaped lives inside `visual`.

## `objects` vs `visualContainerObjects` — two distinct blocks, BOTH inside `visual`

A common bug: hand-authored visuals place `visualContainerObjects` at the root next to `visual`. Desktop rejects this with *"An additional property 'visualContainerObjects' was included in the root property"* — cascading into multiple SCHEMA_ERROR entries from `pbir validate`. The CLI's bundled-fallback schema flags it too.

| Block | Lives inside | Holds |
| --- | --- | --- |
| `objects` | `visual` | **in-chart formatting**: `labels`, `legend`, `valueAxis`, `categoryAxis`, `dataPoint`, `lineStyles`, `markers`, `error`, `xAxisReferenceLine`, `yAxisReferenceLine`, etc. |
| `visualContainerObjects` | `visual` | **container chrome**: `title`, `subTitle`, `border`, `dropShadow`, `divider`, `padding`, `spacing`, `background`, `visualHeader` |

Right:

```json
"visual": {
  "visualType": "lineChart",
  "query": {...},
  "objects": { "labels": [...], "valueAxis": [...] },
  "visualContainerObjects": { "title": [...], "border": [...] },
  "drillFilterOtherVisuals": true
}
```

Wrong (Desktop rejects, `pbir validate` flags 26+ errors at once when a build batch pastes the same broken template):

```json
"visual": { ... },
"visualContainerObjects": { "title": [...] }   ← at the root, sibling of "visual" — broken
```

Confirmed 2026-06-04 against a 26-visual hand-authored batch — every single one errored on Desktop open with the same root-placement message until the block was nested inside `visual`.

## Anchoring the two blocks in your head

- "`objects` are inside the chart" → in-chart formatting.
- "`visualContainerObjects` wrap the chart" → frame/title chrome.
- Both are inside the `visual` object alongside `visualType`, `query`, and `drillFilterOtherVisuals`.

## See also

- `property-catalogue.md` — the universal containers list (which live in `visualContainerObjects`) + per-type containers (which live in `objects`)
- `selectors.md` — scoping properties inside either block
- `expressions.md` — `expr` value forms used in both blocks
