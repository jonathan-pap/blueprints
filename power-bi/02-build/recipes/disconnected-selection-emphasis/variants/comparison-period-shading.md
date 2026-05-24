# Variant — Comparison-period shading

Let the user pick **one** period (a quarter, a month, a year) from a disconnected slicer
and shade just that period on a trend — to anchor "vs. this period" reading while every
period stays visible.

## Deltas from the base recipe

| Primitive | Change |
|---|---|
| P1 source | `VALUES( dimDate[YearQuarter] )` (or YearMonth / Year) — a period label, single-select. |
| P2 harvest | `SELECTEDVALUE( '<SELECTION_TABLE>'[YearQuarter] )` → `Selected Period`. Add `Period Start`/`Period End` measures that map the picked label to its first/last date for the band. |
| P3 band | Two `xAxisReferenceLine`s at `Period Start` / `Period End` (measure-driven `value`), shade between — same shape as the base. |
| P4 series | visual calc: value when the axis date falls in the selected period; labels only there. |
| P5 slicer | single-select dropdown/list slicer on the period column; default to the latest period. |

## Deriving Period Start / Period End from a picked label

```dax
Period Start =
VAR _p = [Selected Period]
RETURN CALCULATE ( MIN ( dimDate[Date] ), REMOVEFILTERS ( dimDate ), dimDate[YearQuarter] = _p )

Period End =
VAR _p = [Selected Period]
RETURN CALCULATE ( MAX ( dimDate[Date] ), REMOVEFILTERS ( dimDate ), dimDate[YearQuarter] = _p )
```

These run on the *related* `dimDate` (so they can resolve the label to dates) while the
slicer itself stays on the disconnected table — selection still doesn't filter the trend.

**Two requirements (both cost a build cycle if missed):**
1. **Materialise the picked label into a `VAR` first.** Referencing the harvester measure
   directly inside the CALCULATE boolean filter (`dimDate[YearQuarter] = [Selected Period]`)
   throws *"A function 'PLACEHOLDER' has been used in a True/False expression used as a table
   filter expression"*. The `VAR _p = ...` makes it a plain scalar predicate.
2. **`REMOVEFILTERS`** so the period resolves independently of the chart's current axis date —
   otherwise the axis context narrows the MIN/MAX and the band collapses.

## Use when

- "Highlight the quarter we're reviewing" on an always-full trend.
- Pairs well with a comparison measure (vs. selected period) shown alongside.
