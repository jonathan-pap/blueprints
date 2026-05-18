# SVG — boxplot (per row)

Quartiles + median + whiskers per row. Use for distribution comparison.

## DAX (see `examples/boxplot-measure.dax`)

```dax
Boxplot =
VAR _min  = MINX(ALLSELECTED('Sales'[OrderID]), [Revenue])
VAR _q1   = PERCENTILEX.INC(ALLSELECTED('Sales'[OrderID]), [Revenue], 0.25)
VAR _med  = PERCENTILEX.INC(ALLSELECTED('Sales'[OrderID]), [Revenue], 0.5)
VAR _q3   = PERCENTILEX.INC(ALLSELECTED('Sales'[OrderID]), [Revenue], 0.75)
VAR _max  = MAXX(ALLSELECTED('Sales'[OrderID]), [Revenue])
-- map to pixel positions, build SVG
RETURN ...
```

Full implementation: `../../examples/boxplot-measure.dax`.

## Reads as

A small box (Q1 to Q3) with a vertical line at the median, plus whiskers extending to min and max. Width encodes the spread; placement shows where the median sits within the spread.

## When to use

- "Are sales per order more consistent in Region A or B?" — boxplot per row makes it visually obvious.
- Anywhere distribution matters more than the average alone.

## Common pitfall

DAX percentile functions can be slow on large detail tables. Pre-aggregate where possible.

## See also

`../../examples/boxplot-measure.dax`.
