# Chart Selection — pick the visual from the question, not the data

> Adapted from skills-for-fabric (MIT) — see [../../../ATTRIBUTIONS.md](../../../ATTRIBUTIONS.md).
> This is the **selection** layer: *which* visual answers the question. Once chosen, configure it
> with [visual-cookbook.md](visual-cookbook.md), get canonical PBIR `visualType` names from
> [`../add-visual/_index.md`](../add-visual/_index.md), and confirm archetype fit in
> [archetypes/_index.md](archetypes/_index.md). The "avoid" column expands in [anti-patterns.md](anti-patterns.md).

## Core principle

Match the chart to the **question**, not the data type. Every chart answers one of a small set of
analytical questions: **comparison, composition, distribution, relationship, trend, ranking,
deviation, flow, status**. Name the question as a sentence first, then pick the most direct encoding.

*Sources: Abela's Chart Chooser, FT Visual Vocabulary, Schwabish taxonomy, Cleveland & McGill.*

## Primary decision matrix

| Purpose | Primary choice | Use when | Alternative | Avoid |
|---|---|---|---|---|
| **Comparison** | Horizontal bar | ≥7 items or long labels | Clustered bar, dot plot | Pie, donut, 3D bars |
| **Composition** | 100% stacked bar, treemap | Parts of a whole | Waterfall (additive breakdown) | Pie >5 slices |
| **Distribution** | Histogram, box plot | Shape of spread matters | Violin, strip/jitter | Single bar showing mean |
| **Relationship** | Scatter | Correlation / clusters | Bubble (3rd variable) | Dual-axis line |
| **Trend** | Line | Continuous time, ≥7 points | Column (≤6 periods) | Smoothed line hiding volatility |
| **Ranking** | Sorted horizontal bar | Top-N / bottom-N | Lollipop, bump | Unsorted bars |
| **Deviation** | Diverging bar | +/− variance vs a reference | Bullet graph, waterfall | Bar with arbitrary baseline |
| **Flow** | Sankey | Redistribution across stages | Funnel (monotone shrink) | Sankey for tiny flows |
| **Single KPI** | Compact card + sparkline/context | Executive glance metric | Bullet graph (vs target) | Gauge or oversized bare-card hero |
| **Geospatial** | `azureMap` symbol/choropleth | Location/spatial carries the message | Sorted bar if the question is pure ranking | Legacy `map`/`filledMap`, bubble maps w/o size legend |

## Secondary selection filters (apply after the primary pick to refine/override)

| Filter | Rule |
|---|---|
| Precision vs pattern | Exact values → table/matrix. Shape/trend → chart. |
| Cardinality | >15 categories → group/filter or small multiples. Never 40 bars. |
| Part-to-whole cardinality | ≤5 → donut; 6–15 → sorted bar; >15 → treemap |
| Magnitude span | >100× range → log scale or separate charts. Don't let one bar dominate. |
| Mixed units | Revenue ($) vs count (#) → separate visuals. Never dual-axis to merge. |
| Audience tolerance | Exec: cards + 1 hero chart. Analyst: scatter, box plot OK. |
| Data density | Sparse → dot/strip. Dense → histogram, hex-bin scatter. |
| Comparison mode | Absolute → bar. Relative share → 100% stacked. Rate of change → line. |

## Power BI native-visual crosswalk

> Confirm exact `visualType` strings in [`../add-visual/_index.md`](../add-visual/_index.md) before binding
> (e.g. `columnChart`, **not** `stackedColumnChart`).

| Purpose | Native PBI visual | Notes |
|---|---|---|
| Comparison | `barChart` (horizontal) | `orientation: horizontal` |
| Comparison (clustered) | `clusteredBarChart` | 2–3 series max |
| Composition | `hundredPercentStackedBarChart`, `treemap` | Treemap for hierarchical |
| Distribution | `histogram` (binning on column) | No native box plot — custom visual |
| Relationship | `scatterChart` | `play axis` for time animation |
| Trend | `lineChart` | Line (not area) for precision |
| Trend (few periods) | `columnChart` | ≤6 discrete periods only |
| Ranking | `barChart` sorted desc | Top-N filter or `sortBy` |
| Deviation | `waterfallChart`, `barChart` + reference line | Diverging bar needs conditional formatting |
| Flow | `decompositionTreeVisual` | Native Sankey limited — custom |
| Single KPI | `cardVisual` | Pair with `lineChart` sparkline |
| Geospatial | `azureMap` | Sorted `barChart` when geography is only a ranked category |
| Table / detail | `tableEx`, `pivotTable` | When precision > pattern |

## Archetype applicability

Cross-check the pick against the page archetype ([archetypes/_index.md](archetypes/_index.md)):

| Archetype | Preferred | Acceptable | Avoid |
|---|---|---|---|
| **Executive** | Card, KPI, single hero line/bar, bullet | Waterfall, treemap | Scatter, box plot, histogram, matrix |
| **Operational** | Card + trend sparkline, table, RAG indicators | Bar, funnel | Scatter, Sankey, violin |
| **Analytical** | Scatter, histogram, box plot, small multiples, matrix | Any chart with clear purpose | Gauge, 3D, pie |
| **Narrative** | Annotated line, waterfall, before/after bar | Slope chart | Cluttered multi-series |
| **Comparative** | Small multiples, grouped bar, slope chart | Scatter (group color) | Stacked bar for comparison |

## Cardinality limits by visual

| Visual | Max categories | Max series | When exceeded |
|---|---|---|---|
| Horizontal bar | 15–20 | 1 best, 2–3 clustered | Scroll or "Other" bucket |
| Clustered bar | 10 | 2–3 | Beyond 3 → small multiples |
| Line | n/a (continuous) | 5 lines | Beyond 5 → spaghetti |
| Pie / donut | 5 | 1 | Beyond 5 → unreadable |
| Scatter | n/a (hundreds OK) | 3–5 color groups | Beyond 5 → facets |
| Treemap | 20–30 tiles | 1–2 levels | Deep nesting → unreadable |
| Small multiples | 4–16 panels | 1 per panel | Beyond 16 → overload |
| Table / matrix | Unlimited rows | 5–8 visible cols | Scroll; hide low-value cols |
| Card | 1 | 1 | One value per card by design |
| Map | 200–500 points | 1 measure | Beyond 500 → aggregate to regions |

## Encoding-accuracy hierarchy (Cleveland & McGill — the *why*)

Most → least accurate: **1** position on common scale (bar, dot, scatter) → **2** position on
non-aligned scale (small multiples) → **3** length (bar) → **4** direction/slope (line) → **5** angle
(pie — why pies are imprecise) → **6** area (bubble, treemap) → **7** volume (3D — never) → **8**
colour saturation/hue (heatmap — pattern, not precision).

**Implication:** precision → bars & dots (position); pattern/shape → heatmaps & area are acceptable.

## Series-count decision tree

```text
How many data series?
├── 1 series
│   ├── Single value → Card
│   ├── Over time → Line
│   └── Across categories → Sorted bar
├── 2–3 series
│   ├── Same unit → Clustered bar or multi-line
│   └── Different units → Separate charts (NOT dual axis)
├── 4–5 series
│   ├── Comparison focus → Small multiples
│   └── Composition focus → 100% stacked bar
└── 6+ series → "Top 5 + Other", or a small-multiples grid
```

## Edge cases & exceptions

| Scenario | Default | Exception (condition) |
|---|---|---|
| Bar baseline | Always 0 | Non-zero only for line/dot where relative change matters |
| Pie | Avoid | ≤5 slices, exact % labelled, composition is the question |
| Area | Avoid (implies volume) | Stacked area for composition over time, ≤3 series |
| Dual axis | Never | Only if both series share the same unit ($ vs $) |
| 3D | Never | No exceptions |
| Sorted bars | Sort by value | Alphabetical only when category order is inherent (months, stages) |
| Smoothed lines | Avoid | Moving-average overlay, labelled, alongside raw data |

## Decision checklist (verify before committing to a type)

1. **What question does this answer?** — state it as a sentence.
2. **Is this the most direct encoding for that answer?** — check the matrix.
3. **Does cardinality fit?** — bars ≤15, pie ≤5, lines ≤5 series, scatter up to hundreds.
4. **Is the baseline honest?** — bars start at 0; break a line axis only if clearly marked.
5. **Would a simpler chart work?** — if a card answers it, keep it compact (never a bare-card hero).
6. **Does the archetype allow it?** — exec pages reject scatter; analytical pages reject gauges.
7. **Decodable in <5 seconds?** — if not, simplify or split.
