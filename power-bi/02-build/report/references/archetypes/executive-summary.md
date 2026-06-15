# Archetype — Executive Summary

> **Audience:** C-suite, board, GM. **Question:** "Is it on track?" **Scan budget:** ≤10 seconds.
> A landing page that states the answer before any chart. Few visuals, high signal, zero exploration
> burden. Pairs with drillthrough/Analytical pages for the "why".

## Intent

- Lead with the **insight as a title** ("Revenue Fell 8% YoY in EMEA"), not a label ("Overview").
- Primary metric + its context first; the eye lands on it instantly ([S9 composite KPI focus](../signatures.md#s9-composite-kpi-focus)).
- Trend + one driver/comparison to prove the headline. Detail table optional, at the bottom.
- Slicers minimal — a Year dropdown, maybe one segment. No full-date range slicer by default.

## Zone allocation (3-30-300)

| Zone | Fills with | Notes |
|---|---|---|
| Header band | page title (insight) + 1–2 dropdown slicers right-aligned | reserved; content starts below |
| Zone 1 Summary | KPI strip, 3–5 cards with Δ/reference context | 2 rows tall so cards show value + context |
| Zone 2 Analysis | the hero — trend line + one driver (bar/variance/map) | this is the largest region, **not** a card |
| Zone 3 Detail | optional compact table or "needs attention" list | omit if it doesn't earn space |

**Never** let a bare single-value card be the dominant region — see [contract space rules](../../layout/design-contract.md#space-rules).

## Layout variants

| Variant | When (data signal) | Shape |
|---|---|---|
| **A — KPI strip + dual hero** | 3–5 headline KPIs + a clear trend and one driver | cards row → trend (left) + driver (right) → optional detail |
| **B — Composite hero** | one dominant metric, everything else context | large composite KPI tile (value + spark + Δ) + supporting cards + one explanatory chart |
| **C — KPI strip + single trend** | the story is one metric over time | cards row → full-width trend → optional table |

Pick on the data, not habit. One headline metric → B. A few co-equal KPIs → A. Pure trend → C.

## Chart mix
Cards (with context), one line/area trend, one bar/variance for the driver, optional table. Avoid pie;
avoid dense scatter. Keep total visuals ≤6 (executive scan).

## Density & tone
Lower density (ratio 1.5–1.618). Tones that fit: **Minimal Restrained**, **Editorial Newsroom**,
**Corporate Cool**. Signature: [S9](../signatures.md#s9-composite-kpi-focus), [S5 single-accent](../signatures.md#s5-single-accent-discipline), [S10 hairline](../signatures.md#s10-hairline-rules-instead-of-borders).

## Common failure
A page of four giant number-cards and nothing else — high prominence, low information. Give the hero
region to the trend/driver; cards belong in the KPI strip.

## Job to be done
Primary user: CEO/GM/VP — time-poor decision-maker. Trigger: Monday skim before standup. Core question:
"Is the business on/off track, and why?" Success: comprehension in ≤10s. Failure: they open a second
artifact to understand status. Implication: everything beyond headline + KPIs goes behind drillthrough.

## Charts — use / don't-use
| Use | Don't use |
|---|---|
| `cardVisual` (value+Δ+label), sparkline `lineChart`, one hero bar/line, bullet, `actionButton` (drill) | `scatterChart`, `treemap`, histogram, `pivotTable`/matrix, `gauge`, `donutChart` |

## Decision checklist
- [ ] Title is a thesis sentence, not a label · [ ] KPI count ≤6 · [ ] every KPI shows absolute + Δ + direction
- [ ] one hero chart supports the headline · [ ] palette = 3 semantic + grey · [ ] all detail behind drillthrough
- [ ] scans in ≤10s (test with a colleague) · [ ] ≤1 slicer visible · [ ] visual headers hidden on cards · [ ] footer shows source + refresh

## Related
- [comparative-benchmark.md](comparative-benchmark.md) (the ranking drill) · [analytical-canvas.md](analytical-canvas.md) (the why drill)
- [`../../references/cards-and-kpis.md`](../../references/cards-and-kpis.md) · [`../../layout/detail-gradient.md`](../../layout/detail-gradient.md)
