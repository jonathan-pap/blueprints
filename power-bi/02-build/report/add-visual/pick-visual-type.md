# Pick a visual type

Drive selection from the reader's question, not the data shape. Ask: **"What comparison or pattern should the reader perceive?"**

## Decision

- **"What is the current value?"** → `cardVisual` (no target) or `kpi-card` (with target)
- **"How does this trend over time?"** → `line-chart` — never use bars for time
- **"How do categories compare?"** → `bar-chart` (long labels) or `column-chart` (short labels)
- **"Two measures related?"** → scatter (`scatterChart`)
- **"Part-to-whole, single split?"** → donut (`donutChart`) — max 5 slices
- **"Part-to-whole, multi-category?"** → stacked bar/column
- **"Individual records, flat?"** → `table`
- **"Individual records, hierarchy?"** → `matrix`
- **"What to filter by?"** → `slicer` (max 3 per page)
- **"Where geographically?"** → `map` / `filledMap`
- **"Cumulative contribution to a total?"** → `waterfallChart`

## When native falls short

- Interactive custom (lollipop, dumbbell, cross-filter selection) → `../../visuals/deneb/`
- Inline graphics in tables (sparkline, status pill) → `../../visuals/svg/`
- Statistical (distribution, regression) → `../../visuals/python/` or `../../visuals/r/`

Custom visuals cost iteration time and are harder to maintain. Discuss trade-off with the user before committing.

## Native `visualType` strings — the exact spellings Desktop accepts

These are the `visualType` strings to write in `visual.json`. Get one wrong and Desktop treats it as a missing custom visual ("Can't display this visual — add it to this report first: …").

| Reader's question | `visualType` |
| --- | --- |
| Stacked vertical bars | `columnChart` (NOT `stackedColumnChart`) |
| Clustered vertical bars | `clusteredColumnChart` |
| Stacked horizontal bars | `barChart` (NOT `stackedBarChart`) |
| Clustered horizontal bars | `clusteredBarChart` |
| Line + bars on two axes | `lineStackedColumnComboChart` / `lineClusteredColumnComboChart` |
| Time-series line | `lineChart` |
| Area / stacked area | `areaChart` / `stackedAreaChart` |
| Donut / pie | `donutChart` / `pieChart` |
| Scatter | `scatterChart` |
| Native waterfall | `waterfallChart` |
| Flat row list | `tableEx` (NOT `table`) |
| Hierarchical rows + columns | `pivotTable` |
| Single value | `card` / `kpi` |
| Filter input | `slicer` |
| Geographic | `map` / `filledMap` / `shapeMap` / `azureMap` |

The community / older PBIR reference docs sometimes list `stackedColumnChart` / `stackedBarChart` as valid types — they are not. The stacked variants of column and bar are the **base names** `columnChart` / `barChart` (stacking by default when multiple measures are on Y); the *clustered* variants get the `clustered` prefix.

When in doubt, create the visual in Desktop manually, save, and read the generated `visualType` from disk — that's the only authoritative source.
