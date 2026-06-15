# Archetypes — per-page router

> Route **each page independently** on its audience + purpose. Even a single "cover everything" request
> decomposes into pages of different archetypes. Pick the archetype here, then walk that file's **variant
> selection table** using the page's data shape ([identity-workflow Step 0](../../build-report.md#a0--data-first-investigation-mandatory)).

## Router

| Signal | Archetype |
|---|---|
| C-suite / board / GM; ≤10s scan; "is it on track?" | [Executive Summary](executive-summary.md) |
| Shift operator / NOC / wallboard; "is it broken?" | [Operational Monitor](operational-monitor.md) |
| Analyst; hypothesis testing; "why did X happen?" | [Analytical Canvas](analytical-canvas.md) |
| Author-driven argument; "here's what happened" | [Narrative Story](narrative-story.md) |
| Ranking / benchmarking / variance; "relative to what?" | [Comparative Benchmark](comparative-benchmark.md) |

When the signal is ambiguous, **default to Analytical Canvas** — the most flexible, degrades gracefully.

## Vague prompts: ASK before routing

A prompt is vague if audience, purpose, page count, or filter depth is missing. When vague, **stop and
offer 2–3 concrete named options** in user-facing terms (never expose archetype names). Each option =
a specific archetype+variant tailored to what's in the model. If the user picks, proceed; else ask one
narrowing follow-up; after two rounds, pick the best, record the assumption in `variant_rationale`, and
proceed. See [`../../../../01-brief/references/vague-prompts.md`](../../../../01-brief/references/vague-prompts.md).

## Variants are advisory, not a checklist

Each archetype ships 2–3 layout variants (A/B/C) with a selection table keyed on data signals. **Don't
default to variant A.** A variant is a starting point, not a required-component list — every card,
callout, and tile must earn its space by answering a distinct question. If the model lacks the derived
insight a zone wants (delta, variance %, rank shift, exception threshold, baseline, narrative text),
**drop or repurpose that zone** rather than fill it with a duplicate absolute measure.

## How archetypes map to the blueprint

These files describe **intent + zone allocation**, not pixels. They map onto the existing layout model:

- **Zones** = the 3-30-300 detail gradient ([`../../layout/detail-gradient.md`](../../layout/detail-gradient.md)):
  Zone 1 Summary (cards/KPIs/slicers) → Zone 2 Analysis (charts) → Zone 3 Detail (tables).
- **Dimensions** come from [`../../layout/design-system.md`](../../layout/design-system.md) (`design-system.yaml`)
  and the equal-gap math in [`../../layout/layout-guidelines.md`](../../layout/layout-guidelines.md).
- **Default canvas** is 1280×720 ([page-dimensions](../../layout/page-dimensions.md)) — *not* assumed FHD.
  Use 1920×1080 only for presentation/wallboard contexts where noted.

The archetype decides *which zones exist and what fills them*; the layout room decides *the numbers*.

## Multi-page
For 2+ pages, see [`../composition.md`](../composition.md) — composition patterns, variant rotation, and
the rule that all pages share one tone + signature.
