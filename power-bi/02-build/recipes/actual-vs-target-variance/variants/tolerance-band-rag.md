# Variant — Tolerance band (RAG)

Three states instead of two. A small miss or beat inside **±tolerance** (say ±2%) is "on
target" — shown **grey/neutral**, no connector — so the eye only catches *material* variances.
Turns the binary beat/miss into a Red-Amber-Green read.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| `Delta Color` | three-way `SWITCH` on `% Delta` against ±tolerance |
| `GREEN MAX` / `RED MAX` | gate on the **tolerance**, not on `Delta`'s raw sign — so no connector inside the dead-band |
| P2 / P5 | unchanged |

## Tolerance-aware measures

```dax
Tolerance = 0.02   -- ±2%; or a what-if parameter (see disconnected-selection-emphasis)

Delta Color =
SWITCH ( TRUE (),
    [% Delta] >  [Tolerance], "<POS_COLOR>",
    [% Delta] < -[Tolerance], "<NEG_COLOR>",
    "<NEUTRAL_COLOR>" )

GREEN MAX = IF ( [% Delta] >  [Tolerance], [MAX VALUE] )   -- connector only on a material beat
RED MAX   = IF ( [% Delta] < -[Tolerance], [MAX VALUE] )   -- connector only on a material miss
```

Inside the band both bounds are BLANK → **no connector**, and `Delta Color` is neutral → the
▲/▼ label renders grey. Beyond the band it behaves exactly like the base recipe.

## Optional — neutral glyph in the band

Extend the `% Delta` format to mark the on-target zone with a dash instead of an arrow by
swapping the measure for a tiny SWITCH that prefixes `■`/`▲`/`▼`, or keep the numeric `0%`
section (the base format's third section already covers exact zero).

## Make the tolerance interactive

Promote `Tolerance` to a what-if slider by harvesting it from a disconnected table — that's
the [disconnected-selection-emphasis](../../disconnected-selection-emphasis/context.md) pattern.
Reviewers then drag the dead-band and watch connectors appear/disappear.

## Use when

- Operational dashboards where only out-of-tolerance periods deserve attention.
- SLAs / KPIs with an explicit acceptable range.

## Note

Pick the tolerance as a **percentage** (`% Delta`) not an absolute, so it scales across
periods of different magnitude.
