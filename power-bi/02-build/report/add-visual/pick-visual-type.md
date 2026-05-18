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
