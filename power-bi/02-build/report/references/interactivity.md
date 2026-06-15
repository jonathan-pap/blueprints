# Interactivity & storytelling

> *Design* the interaction model — what filters, what cross-highlights, what drills, how much. The
> **mechanics** live elsewhere: slicers ([`../add-visual/slicer.md`](../add-visual/slicer.md)), filters
> ([`../filters/`](../filters/_index.md)), bookmarks ([`../bookmarks/`](../bookmarks/_index.md)),
> buttons ([`../add-visual/action-button.md`](../add-visual/action-button.md)). This file decides which,
> and how much, per archetype.

## Core principles

1. **Shneiderman's mantra** — overview first → zoom & filter → details on demand.
2. **Primary insight visible on load** — never behind a click.
3. **Every interaction changes something visible** — if a click does nothing perceptible, remove it.
4. **State must be legible** — the user always sees which filters are active and what scope they're viewing.
5. **Match the interaction budget to the archetype** — execs get 1–2 clicks; analysts get full drill.

## Interaction budget by archetype

| Budget | Max clicks to insight | Allowed | Archetype |
|---|---|---|---|
| **Minimal** | 0–1 | page load shows all; ≤1 slicer | [Executive](archetypes/executive-summary.md) |
| **Guided** | 2–3 | bookmark steps, page navigator, tooltips | [Narrative](archetypes/narrative-story.md) |
| **Moderate** | 3–5 | slicers, cross-filter, drill-through | [Operational](archetypes/operational-monitor.md), [Comparative](archetypes/comparative-benchmark.md) |
| **Rich** | unlimited | full drill, personalize, export, cross-filter matrix | [Analytical](archetypes/analytical-canvas.md) |

## Cross-filter etiquette (Edit Interactions)

The default is cross-filter; **set it deliberately per source→target pair**. In PBIR this is
`page.json → visualInteractions[]` with `type` = `DataFilter` (filter) / `HighlightFilter` (highlight)
/ `NoFilter` (none).

| Mode | Behaviour | Use for | Avoid when |
|---|---|---|---|
| **Highlight** | dims non-selected; keeps context | default for most charts; shows proportion | exact filtered values needed |
| **Filter** | removes non-selected entirely | **cards/KPIs** (must update to the subset); drill source | user needs the whole picture |
| **None** | no cross-interaction | reference/benchmark visuals, independent KPIs | most visuals should respond |

Rules: cards/KPIs → **Filter** · context/benchmark visuals → **None** · charts → **Highlight** (default).
Comparative reports: **sync slicers** across compared visuals/pages ([`../add-visual/slicer.md`](../add-visual/slicer.md) `syncGroup`).

## Descriptive titles & information scent

| Guideline | Example |
|---|---|
| Top inch earns its space (title + 1 sentence or KPI row carries the headline) | "Revenue up 12% QoQ — driven by APAC" |
| Page titles framed as the question answered | "How is revenue trending by region?" |
| Visual titles state the finding, not the chart type | "APAC grew 23% YoY", not "Revenue by Region" |
| Nav labels smell of destination | "Regional Breakdown", not "Page 2" |
| KPI always shows comparison | "12.3M vs 11.0M target (+11.8%)" |

## Navigation patterns (multi-page)

| Feature | Purpose | Key rule |
|---|---|---|
| Drill-through | summary → detail with context | **always a back button**; limit to 1–2 drill fields |
| Tooltip pages | rich hover detail | small (320×240); fast; no critical-only data |
| Page navigator | tab-style switching | descriptive labels; ≤5–7 visible tabs |
| Buttons | nav / bookmark / drill triggers | always show destination |
| Sync slicers | consistent context across pages | sync by field, not visual |
| Personalize visuals | end-user changes measure/axis | **Analytical only** — confusing for casual users |
| Filters pane | persistent filter panel | hide for executive; show for analytical; pre-set defaults |

## Bookmark design rules

| Rule | Detail |
|---|---|
| Name descriptively | "Q4 Revenue by Region", not "Bookmark 1" |
| Capture minimal state | only filters + visibility that change; leave layout |
| Test every transition | each bookmark→bookmark must produce a coherent view |
| Always a Reset bookmark | "Reset to default" |
| Limit count | **5–8 max**; beyond that, use pages |
| Group by purpose | navigation vs filter-state — don't mix |

See [`../bookmarks/bookmark-navigator.md`](../bookmarks/bookmark-navigator.md) for mechanics.

## Anti-patterns (interactivity theatre)

Headline behind a click · invisible slicer state · drill without breadcrumb · bookmark overload (>10) ·
slicer in the top-left focal point · auto-cycling carousel. Full list + detection:
[anti-patterns.md § Cluster 5](anti-patterns.md#cluster-5--interactivity-theatre).

## Related
- [archetypes/_index.md](archetypes/_index.md) — each archetype's interaction design section
- [`../filters/configure-filter-pane.md`](../filters/configure-filter-pane.md) · [`../bookmarks/_index.md`](../bookmarks/_index.md) · [`../add-visual/action-button.md`](../add-visual/action-button.md)
- [composition.md](composition.md) — multi-page navigation choices
