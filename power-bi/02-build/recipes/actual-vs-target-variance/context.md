# Recipe — Actual vs Target with variance connectors

> A **native clustered column chart** that reads as an actual-vs-target variance chart:
> outlined target bars, filled actual bars, **directional green/red connectors** drawn with
> repurposed *error bars*, a ▲/▼ % label on top, and a one-sentence narrative subtitle.
> No custom visual, no SVG — all native objects + a handful of measures.

## The idea in one line

Power BI has no native "variance bar". Build it from a **clustered column** (target + actual)
and hijack the visual's **error bars** to draw the gap between them — colored by direction.
The eye sees "did we beat target, and by how much" per period, without reading a number.

## The trick — error bars as a variance connector

Error bars normally show ±uncertainty. Here they're driven by two measures that are blank
unless the variance has the right sign:

```dax
GREEN MAX = IF ( [Delta] > 0, [MAX VALUE] )   -- MAX VALUE = max(actual, target)
RED MAX   = IF ( [Delta] < 0, [MAX VALUE] )
```

- An error bar on the **target** series with `upperBound = GREEN MAX` → when actual **beats**
  target it stretches from target up to actual, painted green.
- An error bar on the **actual** series with `upperBound = RED MAX` → when actual **misses**
  target it stretches from actual up to target, painted red.

Only one fires per period (the other is BLANK), so each bar pair gets exactly one colored
connector pointing the right way. That single idea is the recipe.

## When to use

- Monthly/quarterly **actual vs target / budget / forecast / prior year** with a clear
  beat-or-miss read.
- Performance reviews where "by how much, and which way" matters more than absolute height.
- Anywhere a plain two-series cluster leaves people doing the subtraction in their head.

If you only need the bars side by side with no variance emphasis, a plain clustered column
is enough — this recipe is for the *variance* story.

## The five primitives

1. [Variance measures](primitives/variance-measures.md) — `Delta`, `% Delta`, `MAX VALUE`, `GREEN MAX`, `RED MAX`, `Delta Color`. The measure layer everything else reads. (P1)
2. [Overlay-series scaffold](primitives/overlay-series-scaffold.md) — three Y series: target (outline), actual (fill), **MAX VALUE (transparent)** for the label + headroom; overlapping cluster. (P2)
3. [Error-bar variance connector](primitives/error-bar-variance-connector.md) — the green/red directional connector via `GREEN MAX`/`RED MAX` error-bar bounds. The headline trick. (P3)
4. [Directional variance label](primitives/directional-variance-label.md) — `% Delta` as a ▲/▼ data label on the transparent series, colored by `Delta Color`. (P4)
5. [Narrative takeaway](primitives/narrative-takeaway.md) — a sentence subtitle ("beat target in 7 months, best in March, longest streak 4") from streak/best-month DAX. (P5)

## Variants

| Variant | What changes |
|---|---|
| [vs Prior Year](variants/yoy-variance.md) | swap the target measure for a prior-year measure — same machinery |
| [Tolerance band (RAG)](variants/tolerance-band-rag.md) | three-state color: green / red / **grey within ±tolerance** instead of binary sign |
| [Horizontal by category](variants/horizontal-by-category.md) | flip to `barChart` and put a non-time category on the axis (bullet-style) |
| [Minimal (no narrative)](variants/minimal-no-narrative.md) | drop the takeaway + streak DAX — just the variance bars |

## Build it

- Ordered file map + validation → [workflow.md](workflow.md)
- Token reference → [tokens.md](tokens.md)
- Reusable fragments → [templates/](templates/) (`variance-measures.tmdl`, `actual-vs-target.visual.json`, `dynamic-format-udf.tmdl`)
- Worked end-to-end example → [examples/monthly-sales-vs-target.md](examples/monthly-sales-vs-target.md)

## Provenance

Derived from the community "Chart Bar — Actuel vs Target" PBIP, kept as a runnable
reference at `../../../_examples/pbip/recipes/actual-vs-target-variance/` (do not load unless
asked). Battle-tested live as the **AvT-Variance-Test** page in `projects/test/`.

## Related atomic docs

- `../../report/calculations/error-bar.md` — the native error-bar mechanism this repurposes (P3)
- `../../report/add-visual/clustered-column-chart.md` — the base visual (P2)
- `../../report/format/conditional-fmt-rule.md` — measure-driven color for the label (P4)
- `../../model/update/multi-line-dax.md` — the streak / best-month measures (P5)
- `../disconnected-selection-emphasis/context.md` — pairs well if you add a what-if target slider
