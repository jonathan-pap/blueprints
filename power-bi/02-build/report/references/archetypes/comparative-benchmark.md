# Archetype — Comparative Benchmark

> **Audience:** anyone asking "relative to what?" **Question:** ranking, benchmarking, variance against a
> baseline. The page exists to compare — entities against each other, actuals against a target, this
> period against last. The comparison *is* the content.

## Intent

- **Always show the baseline.** A bare value with no reference answers nothing — every comparison needs
  prior period, plan/target, peer median, or a selected entity to compare against.
- **Rank and highlight.** Sort by the comparison measure; grey everything except what matters
  ([S6 highlight-and-grey](../signatures.md#s6-highlight-and-grey)).
- Variance is the headline measure — Δ, variance %, gap-to-benchmark, rank shift. Not the absolute.
- IBCS-style discipline fits well (actual vs target, variance bars) — see the
  [actual-vs-target-variance recipe](../../../recipes/actual-vs-target-variance/context.md).

## Zone allocation (3-30-300)

| Zone | Fills with | Notes |
|---|---|---|
| Header band | title (the comparison framing) + baseline selector (period/target/peer) | |
| Zone 1 Summary | the headline gap — variance cards (Δ vs baseline), not bare totals | |
| Zone 2 Analysis | the ranked comparison — sorted bars with variance, or a benchmark scatter | the hero |
| Zone 3 Detail | ranked table with variance columns + status icons | full-width |

## Layout variants

| Variant | When (data signal) | Shape |
|---|---|---|
| **A — Ranked variance bars** | comparing many entities on one measure | variance cards → sorted bar chart (highlight top/bottom) → ranked table |
| **B — Actual vs target** | every entity has a plan/target | variance cards → actual-vs-target overlay (bullet/overlapping bars) → table with RAG |
| **C — Benchmark scatter** | two measures, position vs peers | quadrant scatter (e.g. growth × margin) with reference lines → entity detail table |

## Chart mix
Sorted bar/column (the workhorse), bullet / overlapping-bars for actual-vs-target (SVG if needed —
[`../../visuals/svg/per-chart/bullet.md`](../../../visuals/svg/per-chart/bullet.md),
[`overlapping-bars-with-variance.md`](../../../visuals/svg/per-chart/overlapping-bars-with-variance.md)),
scatter with reference lines, ranked table with variance + [status icons](../signatures.md#s15-status-icons-in-tables).
**Sort by the comparison measure**, descending, by default.

## Density & tone
Medium density (ratio 1.25–1.333). Tones: **Industrial Dense** (IBCS), **Corporate Cool**,
**FT Pink Financial**. Signature: [S6 highlight-and-grey](../signatures.md#s6-highlight-and-grey), [S1 tabular numerals](../signatures.md#s1-tabular-numerals-throughout).

## Common failure
Unsorted bars of absolute values with no baseline — looks like a comparison, answers none. Add the
baseline, compute variance, sort, and highlight.

## Job to be done
Primary user: FP&A analyst / regional manager / product owner. Core question: "Relative to what?" — rank,
pair, or benchmark 2+ entities. Success: differences immediately visible (Δ, %, rank shift,
gap-to-benchmark). Failure: the viewer does arithmetic in their head. Implication: pre-compute every
comparison; show absolute AND relative variance. Adopt **IBCS** wholesale where the finance audience is
trained; cherry-pick (variance columns + Δ/Δ% notation) for mixed audiences.

## Charts — use / don't-use
| Use | Don't use |
|---|---|
| paired/clustered bar (AC vs PY), dumbbell, variance column (diverging at 0), small multiples (shared Y), ranked bar, tornado, `waterfallChart`, slope/`ribbonChart` | stacked bar (obscures comparison), `pieChart`/`donutChart`, `gauge`, radar |

## Decision checklist
- [ ] small multiples share one Y axis · [ ] variance axis includes zero (not truncated) · [ ] both Δ and Δ% shown where scales differ
- [ ] sorted by variance/value, not alphabetical · [ ] diverging palette centred at zero · [ ] baseline drawn (reference/constant line)
- [ ] AC vs PY visually distinct (fill vs outline) · [ ] tabular numerals on all variance values · [ ] viewer never does arithmetic — all comparisons pre-computed

## Related
- [executive-summary.md](executive-summary.md) (the rollup it drills from) · [analytical-canvas.md](analytical-canvas.md)
- [`../../../recipes/actual-vs-target-variance/context.md`](../../../recipes/actual-vs-target-variance/context.md) · [`../../../recipes/pareto-chart/context.md`](../../../recipes/pareto-chart/context.md)
