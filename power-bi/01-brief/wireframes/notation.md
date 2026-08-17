# Wireframe notation — text sketches that map to the canvas

A wireframe here is **ASCII zones + placeholder visuals** — reproducible by an AI, diff-able in git, and
mappable one-to-one onto the real Power BI canvas. Low-fi on purpose: boxes and labels, no colours, no
real data.

## The canvas

- Default **1280 × 720** (16:9), **24px margins**, **16px gaps**, 8px snap — the same **12×12 grid** the
  build uses ([layout-guidelines](../../02-build/report/layout/layout-guidelines.md#grid-12x12)).
- A page is a stack of **zones**; each zone holds one or more **placeholder visuals**. A zone is a low-fi
  sketching device — it resolves to one or more **grid regions** at build (see "Map to the build" below).
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

Each wireframe zone becomes a **grid region + band** on the 12×12 grid, then a real visual. A sketch zone
is a loose sketching device; the build speaks grid regions `[col_start,row_start,col_end,row_end]`
(1-indexed, end-exclusive) and per-type spans from `design-system.yaml`:

| Wireframe | → grid band | → region / token | → build |
|---|---|---|---|
| `header` band | `summary` (row 1) | `[1,1,13,2]` | textbox / page title |
| `KPI row` × 4 | `summary` (rows 2–3) | `layouts.kpi_row_4` | `pbir add visual card` × 4 |
| `★ main` | `analysis` (rows 4–9) | largest region, e.g. `[1,4,7,10]` | the hero chart (cookbook picks the type) |
| `detail` table | `detail` (rows 10–12) | `[1,10,13,13]` / `defaults.table` | `tableEx` / `pivotTable` |
| `filter rail` | crosses all bands | `defaults.rail` `[1,1,3,13]` | slicers |

So the wireframe's zones resolve to grid regions in
[`design-system.yaml`](../../02-build/report/layout/design-system.md) (cell math in
[layout-guidelines](../../02-build/report/layout/layout-guidelines.md#grid-12x12)), and each
`[Type ▸ label]` becomes a real visual via
[`visual-cookbook.md`](../../02-build/report/references/visual-cookbook.md). Save the finished sketch to
`projects/<name>/wireframe.md`. When you emit the portable spec ([`handoff.md`](handoff.md)) it carries
these same regions + bands, so it drops straight into a [design contract](../../02-build/report/layout/design-contract.md) `layout_contract`.

## If you need a picture

The ASCII is the working artifact. For stakeholder sign-off, render the **same zones** as an HTML/SVG
mock (an Artifact) — greyscale boxes + labels, no real data. Don't over-invest: the point of a wireframe
is that it's cheap to throw away.
