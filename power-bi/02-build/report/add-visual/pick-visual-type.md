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
- **"Where geographically?"** → `azureMap` (the default — see [map.md](map.md)). `map`/`filledMap` are **legacy/deprecated**; don't create new ones.
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
| Geographic | `azureMap` (**preferred**). `map` / `filledMap` / `shapeMap` are legacy — `pbir validate` warns `PBIR_VISUAL_TYPE_DEPRECATED`; migrate, don't create. See [map.md](map.md). |

The community / older PBIR reference docs sometimes list `stackedColumnChart` / `stackedBarChart` as valid types — they are not. The stacked variants of column and bar are the **base names** `columnChart` / `barChart` (stacking by default when multiple measures are on Y); the *clustered* variants get the `clustered` prefix.

When in doubt, create the visual in Desktop manually, save, and read the generated `visualType` from disk — that's the only authoritative source.

---

## Choosing the right chart (design judgment)

> Match the chart to the **question**, not the data type. This is the design-time decision; the exact
> `visualType` string for whatever you pick is the table above.
> Sources: Abela's Chart Chooser, FT Visual Vocabulary, Cleveland & McGill.

## Step 1 — name the question
Every visual answers one of these. State it as a sentence first, then pick.

| Question | Primary | When | Alternative | Avoid |
|---|---|---|---|---|
| **Comparison** | Horizontal bar | ≥7 items or long labels | clustered bar, dot plot | pie, donut, 3D |
| **Composition** | 100% stacked bar, treemap | parts of a whole | waterfall (additive) | pie >5 |
| **Distribution** | Histogram, box plot | shape of spread | violin, jitter/strip | single bar showing mean |
| **Relationship** | Scatter | correlation/clusters | bubble (3rd var) | dual-axis line |
| **Trend** | Line | continuous time, ≥7 pts | column (≤6 periods) | smoothed line hiding volatility |
| **Ranking** | Sorted horizontal bar | top-N/bottom-N | lollipop, bump | unsorted bars |
| **Deviation** | Diverging bar | ± from a reference | bullet, waterfall | bar with arbitrary baseline |
| **Flow** | Sankey | redistribution across stages | funnel (monotone shrink) | Sankey for tiny flows |
| **Single KPI** | Compact card + sparkline | exec glance | bullet (vs target) | gauge, oversized bare card |
| **Geospatial** | `azureMap` | location carries the message | sorted bar if pure ranking | legacy `map`/`filledMap` |

> **Power BI lacks native** box plot, violin, jitter, dumbbell, lollipop, bullet, slope, Sankey,
> **candlestick/OHLC**. You **do** have these as recipes — route there instead of settling for the wrong native visual:
> financial OHLC → [`../../recipes/candlestick/context.md`](../../recipes/candlestick/context.md);
> distribution → [`../../visuals/svg/per-chart/boxplot.md`](../../visuals/svg/per-chart/boxplot.md),
> [`jitter-plot.md`](../../visuals/svg/per-chart/jitter-plot.md); deviation/target →
> [`bullet.md`](../../visuals/svg/per-chart/bullet.md),
> [`overlapping-bars-with-variance.md`](../../visuals/svg/per-chart/overlapping-bars-with-variance.md);
> ranking → [`lollipop.md`](../../visuals/svg/per-chart/lollipop.md),
> [`dumbbell.md`](../../visuals/svg/per-chart/dumbbell.md); statistical →
> [`../../visuals/python/`](../../visuals/python/_index.md) / [`r/`](../../visuals/r/_index.md);
> interactive/custom → [`../../visuals/deneb/`](../../visuals/deneb/_index.md).

## Step 2 — refine with secondary filters

| Filter | Rule |
|---|---|
| Precision vs pattern | Exact values → table/matrix. Shape/trend → chart. |
| Cardinality | >15 categories → group/filter or small multiples. Never 40 bars. |
| Part-to-whole | ≤5 → donut · 6–15 → sorted bar · >15 → treemap |
| Magnitude span | >100× → log scale or split. One bar must not dominate. |
| Mixed units | $ vs # → separate visuals. Never dual-axis to merge. |
| Audience | Exec: cards + 1 hero. Analyst: scatter, box plot OK. |
| Comparison mode | Absolute → bar · relative share → 100% stacked · rate of change → line |

## Cardinality limits

| Visual | Max categories | Max series | When exceeded |
|---|---|---|---|
| Horizontal bar | 15–20 | 1 (best), 2–3 clustered | scroll or "Other" bucket |
| Clustered bar | 10 | 2–3 | >3 series → small multiples |
| Line | n/a (continuous) | 5 lines | >5 → spaghetti; highlight one |
| Pie / donut | 5 | 1 | >5 → unreadable; use bar |
| Scatter | hundreds | 3–5 colour groups | >5 groups → facets |
| Treemap | 20–30 tiles | 1–2 levels | deep nesting → unreadable |
| Small multiples | 4–16 panels | 1/panel | >16 → overload |
| Table / matrix | unlimited rows | 5–8 visible cols | scroll; hide low-value cols |
| Card | 1 | 1 | one value per card |
| `azureMap` | 200–500 points | 1 measure | >500 → aggregate to regions |

## Encoding-accuracy hierarchy (Cleveland & McGill)
Ranked most→least accurate. **Precision matters → use position/length (bars, dots).** Pattern matters
→ heatmaps/area acceptable.

| Rank | Encoding | Best for |
|---|---|---|
| 1 | Position on common scale | bar, dot, scatter |
| 2 | Position on non-aligned scale | small multiples (shared axis) |
| 3 | Length | bar |
| 4 | Direction / slope | line (trend) |
| 5 | Angle | pie — *why pies are imprecise* |
| 6 | Area | bubble, treemap |
| 7 | Volume | 3D — never |
| 8 | Colour saturation/hue | heatmap (pattern, not precision) |

## Series-count decision tree

```text
How many series?
├── 1  → single value: Card · over time: Line · across categories: sorted Bar
├── 2–3 → same unit: clustered bar / multi-line · different units: SEPARATE charts (not dual axis)
├── 4–5 → comparison: small multiples · composition: 100% stacked
└── 6+  → "Top 5 + Other", or small-multiples grid
```

## Edge cases & exceptions

| Scenario | Default | Exception |
|---|---|---|
| Bar baseline | always 0 | non-zero only on line/dot where relative change matters |
| Pie | avoid | ≤5 slices, exact % labelled, composition is the question |
| Area | avoid (implies volume) | stacked area for composition over time, ≤3 series |
| Dual axis | never | only if both series share the same unit ($ vs $) |
| 3D | never | no exceptions |
| Sorted bars | sort by value | alphabetical only when order is inherent (months, stages) |
| Smoothed lines | avoid | moving-average overlay, labelled, alongside raw |

## Archetype applicability

| Archetype | Preferred | Avoid |
|---|---|---|
| [Executive](../references/archetypes/executive-summary.md) | card, KPI, single hero line/bar, bullet | scatter, box plot, histogram, matrix |
| [Operational](../references/archetypes/operational-monitor.md) | card+sparkline, table, RAG indicators | scatter, Sankey, violin |
| [Analytical](../references/archetypes/analytical-canvas.md) | scatter, histogram, box plot, small multiples, matrix | gauge, 3D, pie |
| [Narrative](../references/archetypes/narrative-story.md) | annotated line, waterfall, before/after bar, slope | cluttered multi-series |
| [Comparative](../references/archetypes/comparative-benchmark.md) | small multiples, grouped bar, slope, dumbbell | stacked bar for comparison |

## Decision checklist
1. What question does this chart answer? (one sentence)
2. Is the type the most direct encoding for that answer?
3. Does cardinality fit? (bars ≤15, pie ≤5, lines ≤5 series)
4. Is the baseline honest? (bars at 0)
5. Would a card suffice — and if so, is it kept compact (not a hero)?
6. Does the archetype allow it?
7. Decodable in <5 seconds?

Used at [build step A3](../build-report.md); misleading-encoding cluster → [`../references/anti-patterns.md`](../references/anti-patterns.md).
