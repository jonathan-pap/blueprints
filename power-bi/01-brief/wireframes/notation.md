# Wireframe notation — text sketches that map to the canvas

A wireframe here is **ASCII zones + placeholder visuals** — reproducible by an AI, diff-able in git, and
mappable one-to-one onto the real Power BI canvas. Low-fi on purpose: boxes and labels, no colours, no
real data.

## The canvas

- Default **1280 × 720** (16:9), **24px margins**, **16px gaps**, 8-grid snap.
- A page is a stack of **zones**; each zone holds one or more **placeholder visuals**.
- Standard zones (use the ones the page needs):

| Zone | Typical y-band | Holds |
|---|---|---|
| `header` | top ~40–56px | title, last-refresh, logo, page nav |
| `filter rail` | left or right ~240px | global slicers |
| `KPI row` | under header | 3–6 cards / KPIs |
| `main` | centre, largest | the hero chart(s) |
| `detail` | lower / right | table, breakdown, small multiples |

## Placeholder visuals

`[Type ▸ label]` — **intent**, not the final chart type (that's chosen at build via the visual-cookbook).

```
[KPI: Total Sales]        [Card ▸ vs Target]      [Slicer: Date]
[Bar ▸ Sales by Region]   [Line ▸ Sales trend]    [Table ▸ Top accounts]
[Donut ▸ Mix]             [Map ▸ Sales by state]  [Text ▸ takeaway]
```

Mark the **hero** with `★` and note reading order with small numbers if useful.

## A page, wireframed

```
Page 1 — Executive Summary   (Q: are we up or down vs plan, and where's the gap?)
┌────────────────────────────────────────────────────────────────────────────┐
│ Sales Performance — FY26            [logo]        Updated: 12 Aug  · [tabs]  │  header
├───────────┬────────────────────────────────────────────────────────────────┤
│ FILTERS   │  [KPI: Total Sales] [KPI: Margin %] [KPI: vs Target] [KPI: YoY%] │  KPI row
│ [Slicer:  │────────────────────────────────────────────────────────────────│
│  Date]    │                                                                  │
│ [Slicer:  │   ★ [Bar ▸ Sales vs Target by Region]        [Line ▸ Sales trend]│  main
│  Region]  │      (the hero — answers "where's the gap")   (context: trend)   │
│           │                                                                  │
│           │────────────────────────────────────────────────────────────────│
│           │   [Table ▸ Region · Sales · Target · Δ · YoY]                    │  detail
└───────────┴────────────────────────────────────────────────────────────────┘
Reading order: KPIs (1) → hero bar (2) → trend (3) → table (4).  Hero = Sales vs Target by Region.
```

Keep boxes roughly proportional to real size — a hero is visibly bigger than a card. Exact pixels come later.

## Map to the build

Each zone/placeholder becomes a real position + visual:

| Wireframe | → design-system.yaml zone | → build |
|---|---|---|
| `header` band | `zones.header` (y 24, h 40) | textbox / page title |
| `KPI row` × 4 | `zones.kpiRow`, per-type card size | `pbir add visual card` × 4 |
| `★ main` | `zones.main` (largest slot) | the hero chart (cookbook picks the type) |
| `detail` table | `zones.detail` | `tableEx` / `pivotTable` |
| `filter rail` | `zones.filterRail` (left 240) | slicers |

So the wireframe's zones drive [`design-system.yaml`](../../02-build/report/layout/design-system.md) sizes,
and each `[Type ▸ label]` becomes a real visual via
[`visual-cookbook.md`](../../02-build/report/references/visual-cookbook.md). Save the finished sketch to
`projects/<name>/wireframe.md`.

## If you need a picture

The ASCII is the working artifact. For stakeholder sign-off, render the **same zones** as an HTML/SVG
mock (an Artifact) — greyscale boxes + labels, no real data. Don't over-invest: the point of a wireframe
is that it's cheap to throw away.
