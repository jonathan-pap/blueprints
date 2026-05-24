# Variant — Minimal (no narrative)

Just the variance bars. Drop the narrative subtitle and its three streak/best-month measures —
keep the overlay scaffold, the directional connectors, and the ▲/▼ label. Fewer measures, no
`<MONTH_KEY_COLUMN>` / `<YEAR_COLUMN>` dependency, faster to stand up.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| P5 measures | **omit** `TAKEAWAY`, `Number Successful Months`, `Best Month`, `Longest Winning Streak` |
| Subtitle | omit the `subTitle` binding (or set a plain literal) |
| P1 / P2 / P3 / P4 | unchanged |

## What you keep

The required core is just [P1](../primitives/variance-measures.md)'s six measures —
`Delta`, `% Delta`, `MAX VALUE`, `GREEN MAX`, `RED MAX`, `Delta Color` — plus the visual
([P2](../primitives/overlay-series-scaffold.md) + [P3](../primitives/error-bar-variance-connector.md) +
[P4](../primitives/directional-variance-label.md)). That's the whole "did we beat target, by
how much" read with **no axis-key requirement**.

## Workflow

Follow [workflow.md](../workflow.md) **steps 1 and 4 only** — append the six measures, create
the visual. Skip steps 2–3 (narrative measures, format UDF) unless you want the dynamic K/M/B
number format.

## Use when

- Small multiples / a tile in a grid where there's no room for a sentence.
- The axis isn't time (the streak/best-month framing is month-specific anyway — see
  [horizontal-by-category](horizontal-by-category.md)).
- You just want the technique without the analytical prose.

## Note

This is the cleanest starting point — add the [narrative](../primitives/narrative-takeaway.md)
back later if the chart earns a headline.
