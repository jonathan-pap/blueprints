# Variant — Numeric threshold band

Highlight a **value range** the user picks (e.g. "show deals between £10k and £50k") on a
chart, without filtering the rest out. Same recipe, numeric source.

## Deltas from the base recipe

| Primitive | Change |
|---|---|
| P1 source | `GENERATESERIES( <MIN>, <MAX>, <STEP> )` (synthetic scale) **or** `VALUES( <fact>[<amount>] )`. Drop `formatString: Short Date`; use `#,0` or none. |
| P2 harvest | `MIN`/`MAX` of the numeric column → `Threshold Low` / `Threshold High`. |
| P3 band | If banding the **value (Y) axis**, move the reference lines to `yAxisReferenceLine`; Function 3/4 on the numeric column. If banding the X axis (X is the numeric scale), keep `xAxisReferenceLine`. |
| P4 series | visual calc: `IF( [<AXIS_VALUE>] >= [Threshold Low] && [<AXIS_VALUE>] <= [Threshold High], [<VALUE_MEASURE>] )`. |
| P5 slicer | numeric range slicer — the slicer `objects.data` uses numeric bounds, not `startDate/endDate`. Set the slicer to **Between** numeric mode in Desktop and copy the resulting `data`/`general.filter` shape; literals are plain numbers (`10000`, not `datetime'...'`). |

## When this beats filtering

- A scatter/column chart where you want to *see the whole distribution* but call out a band.
- "Within tolerance" highlighting on a quality/measurement chart.

## Caveat

`GENERATESERIES` with a fine step makes a large disconnected table — keep the step coarse
enough for a usable slider (hundreds–thousands of rows, not millions).
