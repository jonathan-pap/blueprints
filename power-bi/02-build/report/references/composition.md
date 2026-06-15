# Archetype composition & variant rotation

> Use this when a report has **more than one page**. Per-page routing (archetype + variant) lives in
> [`archetypes/_index.md`](archetypes/_index.md); this file covers report-level composition and the
> rule against mono-archetype reports.

## Common multi-archetype compositions

| Report shape | Page 1 | Page 2 | Page 3+ | Notes |
|---|---|---|---|---|
| **Executive + Drill** | Executive Summary | Analytical Canvas | Comparative Benchmark for rankings | Most common: KPI landing → exploration → ranking |
| **Ops + Detail** | Operational Monitor | Analytical Canvas | Narrative Story for post-incident | NOC board → incident drill → write-up |
| **Story + Evidence** | Narrative Story | Comparative Benchmark | Analytical Canvas appendix | Quarterly reviews, board decks |
| **Multi-domain** ("cover everything") | Executive Summary landing | Comparative Benchmark for entity rankings | Analytical Canvas for exploration; Narrative for history | Default decomposition when one request spans entities + events + locations + actors |

## Avoid mono-archetype reports

A 4-page report that is 4× Analytical Canvas (or 4× Executive Summary) usually means each page wasn't
routed independently — page 1's archetype was copied to pages 2–4 by inertia. **Route every page on its
own data shape and audience**, not the report's overall shape.

When the same archetype is genuinely right for multiple pages, those pages **must rotate layout
variants** (below). When even variant rotation can't differentiate two pages, that's a signal to merge
or split them — not to ship two identical layouts.

## Cross-page variant rotation

When a report has 2+ pages of the **same archetype**, actively pick **different variants** where the
data supports it. A 4-page Analytical report should not be 4× Filter-Rail — pick Filter-Rail for the
dense exploration page, Inline-Slicers for the focused-question page, Small-Multiples for the
cross-entity comparison.

| Same-archetype page count | Variant-rotation expectation |
|---|---|
| 1 | Pick the variant the data calls for; no rotation |
| 2 | ≥1 page differs from the other |
| 3 | ≥2 distinct variants; prefer all 3 if data supports |
| 4+ | All variants for that archetype appear unless every page has identical data signals |

The per-archetype selection tables are the mechanism — walk them per page using **that page's** data
shape. Only repeat a variant when two pages genuinely share data signals AND serve distinct purposes.

## Composition is independent of tone

The composition pattern (which archetypes the pages occupy) is independent of the design identity
(`tone` + `signature`). An Executive + Drill report can be Editorial Newsroom OR Industrial Cockpit OR
Minimal Restrained — the tone propagates **uniformly** across every page; the composition just decides
which archetypes those pages are.

**Pages within one report MUST share a tone and signature.** A report where page 1 is Editorial and
page 2 is Industrial reads as two reports stitched together. If the user genuinely needs different
tones for different audiences ("an exec page and an ops page"), that's a signal to produce **two
reports**, not one with two identities.

## Navigation across pages

Multi-page reports need a wayfinding pattern decided here, built in [`../`](../context.md):
- **Drillthrough** (detail/profile pages) → [`../filters/`](../filters/_index.md) + page `type`
- **Bookmark navigator / buttons** → [`../bookmarks/bookmark-navigator.md`](../bookmarks/bookmark-navigator.md), [`../add-visual/action-button.md`](../add-visual/action-button.md)
- Keep interactions **predictable and consistent** across pages (same cross-filter behavior, same slicer placement).

## Related
- [archetypes/_index.md](archetypes/_index.md) — the per-page router + variant selection tables
- [identity-workflow.md](../build-report.md) — Step 2 routes archetypes; Step 3 sets the page plan
- [`../layout/design-contract.md`](../layout/design-contract.md) — one `pages[]` entry per page, each with its archetype + variant
