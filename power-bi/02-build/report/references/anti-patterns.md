# Anti-patterns — the dashboard slop catalog

> LLM-generated dashboards gravitate to a set of attractor states — generic, cluttered, or misleading
> designs that *look* complete but fail users. This is the **refusal list**: when you detect these in
> your own output, stop and fix before handing off. **Advisory, never blocking** — surface
> strong-warnings to the user for confirmation. The [validator](../../../04-review/audit/layout-contract-validate.md)
> automates the detection heuristics below.

## Cluster 1 — Visual noise (chartjunk)

| Anti-pattern | Why it fails | Do instead | PBI tell |
|---|---|---|---|
| 3D effects | Perspective distorts; occludes data | Flat 2D | any `3D` visual type |
| Drop shadows on visuals | Decoration; visual weight, no info | Remove; use whitespace | `shadow`/`dropShadow` enabled |
| Saturated background fills | Competes with data ink; kills contrast | White/near-white canvas | `background.color` saturated |

## Cluster 2 — Misleading encoding

| Anti-pattern | Why it fails | Do instead | PBI tell |
|---|---|---|---|
| Truncated bar baseline | Exaggerates diffs 2–10× | Bars start at 0; dot plot if range narrow | `valueAxis.start` ≠ 0 on bar |
| Dual y-axis | Implies correlation by scale; easy to lie | Two charts, shared x, stacked | `secondaryYAxis` enabled |
| Pie/donut >5 slices | Angle encoding imprecise | Sorted horizontal bar | pie/donut >5 points |
| Stacked bar for mid-stack comparison | Only bottom/top share a baseline | Grouped bar / small multiples | stacked >2 segments compared |
| Unshared small-multiple axes | Different scales = impossible comparison | Force identical axis range | auto-scale per tile |
| Gauge / speedometer | Big area, one number, no trend | Card + sparkline or bullet | `gauge` |
| Radar / spider | Area distortion; axis order changes shape | Grouped bar / parallel coords | `radar` |
| Area chart for non-stacked data | Fill implies volume that isn't there | Line for trends; area only stacked | `areaChart` single series |

## Cluster 3 — Cognitive overload

| Anti-pattern | Why it fails | Do instead | PBI tell |
|---|---|---|---|
| KPI carpet-bombing | 8+ cards; nothing stands out | 3–4 KPIs that drive decisions | >6 cards on a page |
| 12+ visuals on a page | Exceeds working memory | 5–7 groups; drill for depth | visual count >12 |
| Alert fatigue | Everything red = nothing red | Reserve red/amber for actionable | >3 CF rules using red |
| Detail matrix on exec page | Execs scan, not read | Summary on exec; matrix on drill | matrix >10 rows with cards |
| Wall of slicers | 5+ slicers paralyze | 2–3 visible; rest in filter pane | >4 slicers on a page |
| Wrong date-slicer grain | `Between` on annual data; control may not render | Year/period dropdown for annual | exec page + yearly data + `between` |
| Multi-page, no navigation | Pages 2+ undiscovered | Page navigator / nav buttons | >3 pages, no navigator |
| Variant default-bias | Every page variant **A** without consulting the data | Walk the per-archetype variant table; rotate ([composition.md](composition.md)) | all pages same `layout_variant` |
| Mono-archetype report | Page-1 archetype copied to all pages | Route each page on its own audience | 3+ pages share one archetype |
| Silent-guess on vague prompt | Ships a templatized guess | Offer 2–3 named options first ([identity-workflow.md](../build-report.md)) | no clarification recorded |
| Mandatory zone-fill | Every wireframe box filled with a redundant card | Drop/repurpose zones without `insight_basis` | callout repeats adjacent measure |

## Cluster 4 — Colour misuse

| Anti-pattern | Why it fails | Do instead | PBI tell |
|---|---|---|---|
| Rainbow on ordered data | No perceptual order | Sequential single-hue ramp | rainbow on a sorted dimension |
| Categorical palette on ordinal | Distinct hues imply no order | Sequential/diverging | categorical on ranked field |
| Red/green sole signal | 8% CVD can't decode | Add icon + label | red+green, no second channel |
| Low-contrast labels | <3:1; unreadable | ≥`#767676` on white | contrast <4.5:1 |
| Semantic colour flip | green=bad confuses everyone | Respect convention | `good` token on a negative |
| Pastel for critical status | Doesn't signal urgency | Saturated red for critical | pastel for "critical" |
| >8 categorical hues | Indistinguishable | Group tail into "Other"; ≤7–8 | >8 hues rendered |

See [color-palettes.md](color-palettes.md) + [accessibility.md](accessibility.md#colour-vision-deficiency-cvd).

## Cluster 5 — Interactivity theatre

| Anti-pattern | Why it fails | Do instead | PBI tell |
|---|---|---|---|
| Headline behind a click | Primary insight invisible on load | Show insight on load; interaction = depth | key metric only via drill/bookmark |
| Invisible slicer state | User can't tell what's filtered | Show slicer headers / filter indicators | slicers with hidden headers |
| Drill without breadcrumb | User gets lost | Back button; show drill path | drillthrough page, no back button |
| Bookmark overload | >10 unmanageable | 5–8 max, descriptive names | >10 bookmarks |
| Slicer in prime real estate | Top-left wasted on controls | Slicers right/rail/panel | slicer at x<200, y<100 |
| Auto-cycling carousel | Users can't control pace; a11y fail | Static + manual next/prev | timer-driven bookmark cycling |

See [interactivity.md](interactivity.md).

## Cluster 6 — Archetype mismatch

| Anti-pattern | Do instead | PBI tell |
|---|---|---|
| Executive page with 30 visuals | 4–6 groups; cards + 1 hero | archetype=exec + visuals >10 |
| Operational without timestamp | "Last refreshed: {time}" in footer | no timestamp on ops page |
| Analytical without drill/export | Enable drill-through, personalize | analytical + no drill pages |
| Narrative without thesis | Lead every page with a finding | narrative page, no insight textbox |
| Default "All" on large model | Pre-filter to recent / top-N | no default slicer + large dataset |
| Comparative with unsynced slicers | Sync slicers across compared visuals | comparative + independent slicer state (see [`../add-visual/slicer.md`](../add-visual/slicer.md) syncGroup) |

## LLM-specific failure modes

| Failure | Fix |
|---|---|
| Clustered bar for everything | Consult [chart-selection.md](../add-visual/pick-visual-type.md) |
| Ignoring small multiples | Use them when comparing >3 entities |
| One line chart per measure | Combine related; cards for single values |
| Missing sort | Descending by value ([`../add-visual/bar-chart.md`](../add-visual/bar-chart.md)) |
| Skipping alt text | Insight-driven per visual ([accessibility.md](accessibility.md)) |
| Hardcoding hex | Theme `dataColors`/sentiment ([`../../theme/audit/find-hardcoded-hex.md`](../../theme/audit/find-hardcoded-hex.md)) |
| Six font sizes | 4-tier ramp ([`../../theme/create/typography-roles.md`](../../theme/create/typography-roles.md)) |
| Off-grid drift | Snap to 8px (`audit-layout-consistency.sh`) |
| Title as chart type | Title states the insight |

## Detection heuristics + severity

| # | Check | Trigger | Severity |
|---|---|---|---|
| 1 | Hue count | >8 rendered `dataColors` | warn |
| 2 | Dual axis | `secondaryYAxis` on any visual | strong-warn |
| 3 | Card count | >6 cards on a page | warn |
| 4 | Bar baseline | `valueAxis.start` ≠ 0 on bar/column | strong-warn |
| 5 | Pie slices | pie/donut >5 points | warn |
| 6 | Visual density | >12 visuals on a page | warn |
| 7 | Pixel grid | x/y/w/h not ÷8 | info |
| 8 | Contrast | any text/bg <4.5:1 | strong-warn |
| 9 | Alt text | empty on non-decorative visual | warn |
| 10 | Inline hex | hardcoded hex not in theme | info |
| 11 | Freshness | ops page, no timestamp | warn |
| 12 | Ramp bloat | >4 distinct title/label sizes | info |

**Severity model:** `info` = log only · `warn` = surface + suggest fix · `strong-warn` = recommend
explicit user confirmation. Never blocks output.

## Remediation quick-reference

| Detected | Fix | Time |
|---|---|---|
| 3D | Flat 2D | 1m |
| Truncated baseline | `valueAxis.start: 0` | 30s |
| Dual axis | Split, stack vertically | 5m |
| Pie >5 | Sorted bar | 3m |
| >12 visuals | Move detail to drill page | 10m |
| >8 colours | Group tail to "Other" | 5m |
| Missing alt text | Insight template per visual | 2m/visual |
| Pixel drift | Snap to ÷8 | 1m/visual |
| Rainbow on sequential | Single-hue ramp | 3m |
| Missing timestamp | Footer "Last refreshed" | 2m |
| Hardcoded hex | Move to theme | 5m |
| Unsorted bars | Descending by value | 30s |
| Gauge | Card + sparkline | 3m |
| Slicer top-left | Move to rail/strip | 2m |
| Semantic flip | green=good/red=bad | 2m |

## Pre-publish review (run in order)

1. **Layout** — ≤7 groups; on-grid; consistent gutters; margins ≥24px; reserved title/slicer band
2. **Colour** — ≤8 hues; no rainbow-on-ordered; WCAG pass; no red/green-alone; CVD pass; theme not inline
3. **Typography** — ≤4 sizes; numbers right-aligned; consistent number formats; nothing <8pt
4. **Charts** — every chart answers a stated question; bars at 0; no dual axes; no pie>5; sorted
5. **Interactivity** — primary insight on load; slicer state visible; drill back button; ≤8 bookmarks
6. **Accessibility** — alt text; tab order; keyboard end-to-end; targets ≥24px; high-contrast tested
7. **Archetype** — density / interaction budget / type ramp / palette match the archetype

## Related
- [`../../../04-review/audit/layout-contract-validate.md`](../../../04-review/audit/layout-contract-validate.md) — automates the heuristics · [`../../../04-review/audit/visual-design.md`](../../../04-review/audit/visual-design.md) — generic quality
- [chart-selection.md](../add-visual/pick-visual-type.md) · [accessibility.md](accessibility.md) · [interactivity.md](interactivity.md) · [color-palettes.md](color-palettes.md)
