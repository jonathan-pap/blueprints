# Archetype — Analytical Canvas

> **Audience:** analyst. **Question:** "Why did X happen?" Hypothesis testing, drilldowns, comparisons.
> The most flexible archetype — **the default when the signal is ambiguous**, because it degrades
> gracefully. Built for someone who will spend real time in the report.

## Intent

- **Exploration over headline** — rich filtering, multiple linked visuals, cross-filtering that lets
  the analyst pivot a hypothesis quickly.
- Higher visual count tolerated (still mind the [perf budget](../../layout/layout-guidelines.md#visual-count-vs-performance) — 6–8 optimal).
- A persistent filter surface (rail or inline) plus drillable detail.
- Predictable cross-filter behavior — decide Filter vs Highlight per visual and keep it consistent.

## Zone allocation (3-30-300)

| Zone | Fills with | Notes |
|---|---|---|
| Header band / rail | title + the filter set (inline band for ≤3, side rail for more) | rail variant moves filters to a left column |
| Zone 1 Summary | a compact context strip (current selection's key measures) | optional; keep it thin |
| Zone 2 Analysis | the working area — 2–4 linked charts (trend, breakdown, scatter, distribution) | the heart of the page |
| Zone 3 Detail | drillable table/matrix with the row-level evidence | full-width |

## Layout variants

| Variant | When (data signal) | Shape |
|---|---|---|
| **A — Filter rail** | many filterable dimensions; deep exploration | left filter rail; content (charts + detail) to its right |
| **B — Inline slicers** | one focused question, 2–3 filters | top slicer band; balanced chart grid + detail below |
| **C — Small-multiples grid** | comparing the same metric across many entities | a grid of small repeated charts (one per entity) + a detail table |

Walk this table **per page** in a multi-page report — rotate variants rather than repeating one
([composition.md](../composition.md)).

## Chart mix
Line/area (trend), clustered bar/column (breakdown), scatter (correlation), matrix (cross-tab),
distribution (box/histogram via SVG if needed — [`../../visuals/svg/`](../../../visuals/svg/_index.md)).
One analytical question per visual; split a visual that answers two.

## Density & tone
Medium-high density (ratio 1.25–1.333). Tones: **Industrial Dense**, **Corporate Cool**,
**Monospace Terminal**. Signature: [S12 modular grid](../signatures.md#s12-modular-grid-with-consistent-gutter), [S1 tabular numerals](../signatures.md#s1-tabular-numerals-throughout).

## Common failure
A wall of 12+ visuals with no filter discipline and overlapping questions — looks busy, answers nothing.
Fewer visuals, each with a clear question, plus strong filtering.

## Job to be done
Primary user: analyst / data scientist. Trigger: a live question ("Why did EMEA dip in Q3?"). Workflow:
hypothesis → slice → drill outlier → pivot measure → bookmark finding. Success: questions answered per
session + every cut reproducible. Failure: analyst exports to Excel to "really look at it". Implication:
density is a feature; 10–12 visuals acceptable; interactivity is primary.

## Charts — use / don't-use
| Use | Don't use |
|---|---|
| slicer rail, `scatterChart`, small multiples (shared Y), decomposition tree, `pivotTable`, field parameters | dominating KPI cards, `gauge`, `donutChart`, 3D, infographic icons |

## Decision checklist
- [ ] filter rail shows 3–6 slicers with visible state · [ ] reset button clears all · [ ] active filters in a breadcrumb/pills
- [ ] hero supports drill or field-parameter swap · [ ] small multiples share Y axis · [ ] cross-filter behaviour tuned (edit interactions)
- [ ] bookmarks capture reproducible cuts · [ ] ≤12 visuals · [ ] personalize-visuals enabled

## Related
- [executive-summary.md](executive-summary.md) (the landing it drills from) · [comparative-benchmark.md](comparative-benchmark.md) (ranking)
- [`../../layout/layout-guidelines.md`](../../layout/layout-guidelines.md) · [`../../filters/_index.md`](../../filters/_index.md) · [`../../add-visual/pick-visual-type.md`](../../add-visual/pick-visual-type.md)
