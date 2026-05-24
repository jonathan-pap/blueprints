# Variant — Horizontal by category

Flip the chart on its side and put a **non-time category** (product, region, rep, store) on
the axis — a bullet-style "actual vs target by thing" ranking. Same measures, same error-bar
connectors; just a horizontal bar visual and a category axis.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| `visualType` | `clusteredColumnChart` → `barChart` (horizontal) |
| `<AXIS_COLUMN>` | a category column instead of a month label |
| Error bars | now horizontal — `upperBound` extends left/right; config is otherwise identical |
| Sort | sort the axis by `<ACTUAL_MEASURE>` or `Delta` DESC so the ranking reads top-down |
| P1 / P4 | unchanged |
| P5 narrative | usually drop or reword — "best month / streak" doesn't apply to a category axis |

## What stays the same

`Delta`, `% Delta`, `MAX VALUE`, `GREEN MAX`, `RED MAX`, `Delta Color` ([P1](../primitives/variance-measures.md))
are axis-agnostic — they compare two measures in the current row context, whether that row is a
month or a product. The [error-bar connector](../primitives/error-bar-variance-connector.md)
logic is unchanged; Power BI orients the bars to match the visual.

## Sort for ranking

```json
"sortDefinition": { "sort": [ { "field": { "Measure": {
  "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<ACTUAL_MEASURE>" } },
  "direction": "Descending" } ], "isDefaultSort": true }
```

Sort by `Delta` instead if you want biggest over/under-performers at the top rather than
biggest absolute.

## Use when

- "Which products/regions beat target, by how much" — a leaderboard with variance.
- Many categories (horizontal bars label better than rotated column ticks).

## Note

For a single category and a richer in-row treatment (target line + qualitative bands), the SVG
[bullet chart](../../../visuals/svg/per-chart/bullet.md) or [target bar](../../../visuals/svg/per-chart/target-bar.md)
may read better — this variant shines when you want *many* categories natively with the
directional connector.
