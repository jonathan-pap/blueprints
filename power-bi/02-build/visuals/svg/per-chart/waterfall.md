# SVG — waterfall (per row)

Stepped bars showing positive/negative contributions to a total. Compact form for in-table use.

## DAX (see `examples/waterfall-measure.dax`)

```dax
Waterfall Step =
VAR _components = { ("Start",0), ("Sales",1), ("Returns",2), ("Discounts",3), ("End",4) }
-- ...build positions and bar heights, color positive green / negative red
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" ...>" &
-- one <rect> per component, stacked from baseline
"</svg>"
```

Full implementation: `../../examples/waterfall-measure.dax`.

## Reads as

Bars step up (green) or down (red) from a baseline, with start/end totals as full-height bars. Each step's height is the magnitude of that component.

## When to use this vs native waterfallChart

- **SVG waterfall**: in-row, paired with a category label per row. Good for many-row comparisons.
- **Native `waterfallChart`**: standalone visual for a single waterfall analysis. Better when the breakdown matters more than the comparison across rows.

## See also

`../../examples/waterfall-measure.dax`.
