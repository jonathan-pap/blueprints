# Variant — ABC classification

Three bands instead of two. Inventory and spend analysis classically split a Pareto into
**A** (the vital few, 0–80% cumulative), **B** (the next tranche, 80–95%), and **C** (the
long tail, 95–100%). Same machinery as the base — just two cut-points and three colors.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| P3 cumulative | unchanged — `Easy Pareto`. |
| P4 split | **three** line series at two cut-points instead of one. |
| P4 bar fill | three conditional cases instead of two. |
| P5 | unchanged. |

## Two cut-points

```dax
ALine = IF ( [Easy Pareto] <= 0.8, [Easy Pareto] )                          -- A: vital few
BLine = IF ( [Easy Pareto] >  0.8 && [Easy Pareto] <= 0.95, [Easy Pareto] ) -- B: middle
CLine = IF ( [Easy Pareto] >  0.95, [Easy Pareto] )                         -- C: tail
```

Three `Y2` projections (`select3`/`select4`/`select5`), colored e.g. teal `#1E9790` (A),
amber `#E8A33D` (B), red `#ED4D55` (C).

> **Overlap each segment by one point or the line breaks at every cut-point.** As in
> [P4](../primitives/threshold-split-emphasis.md), comparing to the literal cut-point
> (`>= 0.8`) does *not* connect the segments — real cumulative values never land exactly on
> it. Instead extend each *lower* band to include the first bar that crosses, using the
> "cumulative before this bar" trick (`[Easy Pareto] - [Percent of grand total]`):
>
> ```dax
> ALine = IF ( [Easy Pareto] - [Percent of grand total] < 0.8,  [Easy Pareto] )   -- A + first B-crosser
> BLine = IF ( [Easy Pareto] > 0.8 || [Easy Pareto] - [Percent of grand total] < 0.95,
>              IF ( [Easy Pareto] - [Percent of grand total] < 0.95, [Easy Pareto] ) )  -- B + first C-crosser
> CLine = IF ( [Easy Pareto] > 0.95, [Easy Pareto] )                                -- C
> ```
>
> Each band now shares its boundary bar with the next, so the colored strokes join into one
> continuous line. (`BLine` simplifies in practice — the point is: gate on the *previous*
> cumulative, not the literal cut-point.)

## Three-case bar fill

Extend the P4 `Conditional.Cases` to three (evaluated top-down, first match wins):

```text
Case 1: select2 >  0.95            -> '#ED4D55'   (C)
Case 2: select2 >  0.8  (<= 0.95)  -> '#E8A33D'   (B)
Case 3: select2 >= 0    (<= 0.8)   -> '#1E9790'   (A)
```

Order matters — put the highest band first so a 0.97 bar matches C, not B. Keep the
`dataViewWildcard` per-point selector (see [P4](../primitives/threshold-split-emphasis.md)).

## Optional — a class label

Add an `ABC Class` visual calc for tooltips / a table:

```dax
ABC Class = SWITCH ( TRUE (), [Easy Pareto] <= 0.8, "A", [Easy Pareto] <= 0.95, "B", "C" )
```

## Use when

- Inventory / spend / SKU rationalization — the A/B/C convention is expected.
- You want three actions ("manage tightly / monitor / review for cut") rather than a binary keep/drop.

## Note

Generalises to *n* bands — it's just more `SWITCH`/`IF` cut-points and colors. Beyond three
the chart gets noisy; prefer a class column in a table at that point.
