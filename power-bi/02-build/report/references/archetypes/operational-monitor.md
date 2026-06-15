# Archetype — Operational Monitor

> **Audience:** shift operator, NOC, on-call, wallboard viewer. **Question:** "Is it broken? What needs
> action now?" A status board read at a glance, often on a large always-on screen. Status-coded, dense
> enough to cover the estate, with an exception/action queue.

## Intent

- **Status first** — the board reads as traffic lights. Color = state, not decoration ([S8 status-coded cards](../signatures.md#s8-status-coded-kpi-cards), [S15 status icons in tables](../signatures.md#s15-status-icons-in-tables)).
- Show **what's wrong and what to do**, not historical analysis. Exceptions surface to the top.
- Near-real-time framing: "as of" timestamp, current-period focus.
- Wallboard context → 1920×1080, larger type, no slicers (no one interacts with a wallboard).

## Zone allocation (3-30-300)

| Zone | Fills with | Notes |
|---|---|---|
| Header band | title + "as of" timestamp; slicers only if interactive (not wallboard) | |
| Zone 1 Summary | status KPI tiles (green/amber/red), counts of open/breached | accent bar carries the signal |
| Zone 2 Analysis | live trend / throughput + a status-by-segment breakdown | quadrant layout works well here |
| Zone 3 Detail | exception/action queue table with status-icon column | the "do something" list |

## Layout variants

| Variant | When (data signal) | Shape |
|---|---|---|
| **A — Status strip + quadrant** | several subsystems, each with a few metrics | status tiles → 2×2 quadrant of breakdowns → exception table |
| **B — Single-system deep monitor** | one system, many metrics over time | status tiles → wide live trend + gauge → detailed event table |
| **C — Wallboard** | always-on big screen, no interaction | oversized status tiles + one big trend; no slicers, no detail table; everything legible at distance |

## Chart mix
Status cards (accent-bar driven by measure), gauges/KPI-with-target, line trend, a status-by-category
bar, and a table with conditional-formatting status icons. Reserve **red strictly for genuine alerts**.

## Density & tone
Higher density (ratio 1.25–1.333). Tones: **Industrial Cockpit** (dark) or **Industrial Dense** (light).
Dark mode triggers every formatting trap at once — carry the dark-mode discipline into authoring
([`../../../theme/modify/wildcard.md`](../../../theme/modify/wildcard.md), [`../../format/_index.md`](../../format/_index.md)).

## Common failure
Pretty historical charts with no status encoding — an operator can't tell at a glance what's broken.
Lead with state; defer trends.

## Job to be done
Primary user: shift operator / on-call / supervisor. Mode: continuous peripheral surveillance, burst
attention on anomaly. Core question: "Is it me or is it broken?" Success: deviation detected <5s,
before the downstream alert fires. Implication: passive consumption — minimize required clicks to zero.

## Charts — use / don't-use
| Use | Don't use |
|---|---|
| status tiles (`cardVisual`+shape+CF), bullet (bar+referenceLine), sparkline `lineChart`, exception `tableEx` (CF icons+data bars), `azureMap` | `pieChart`/`donutChart`, `scatterChart`, `treemap`, analytical slicers, decomposition tree |

## Decision checklist
- [ ] last-updated timestamp visible + prominent · [ ] staleness flag fires past expected cadence · [ ] every metric has good/warn/bad thresholds
- [ ] state = colour + shape + icon (never colour alone) · [ ] exception list sorted severity desc · [ ] fonts sized for actual viewing distance
- [ ] zero clicks for normal-state assessment · [ ] drillthrough from a red tile to detail + runbook

## Related
- [executive-summary.md](executive-summary.md) (the rollup) · [narrative-story.md](narrative-story.md) (post-incident review)
- [S8](../signatures.md#s8-status-coded-kpi-cards) · [S15](../signatures.md#s15-status-icons-in-tables) · [`../../format/conditional-fmt-rule.md`](../../format/conditional-fmt-rule.md)
