# SVG — jitter plot (per row)

Dots placed along a horizontal axis with vertical jitter to show distribution density per row.

## DAX (see `examples/jitter-plot-measure.dax`)

```dax
Jitter =
VAR _w = 140
VAR _h = 20
VAR _min = MINX(ALLSELECTED('Sales'[OrderID]), [Revenue])
VAR _max = MAXX(ALLSELECTED('Sales'[OrderID]), [Revenue])
VAR _circles =
    CONCATENATEX(
        ALLSELECTED('Sales'[OrderID]),
        VAR _x = (([Revenue] - _min) / (_max - _min)) * _w
        VAR _y = 4 + RAND() * 12      -- deterministic jitter would be better
        RETURN "<circle cx=""" & _x & """ cy=""" & _y & """ r=""1.5"" fill=""#118DFF"" opacity=""0.4""/>",
        ""
    )
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
_circles &
"</svg>"
```

Full implementation: `../../examples/jitter-plot-measure.dax`.

## Reads as

A horizontal scatter of dots per row. Density along the axis shows where values cluster; vertical jitter spreads dots so overlapping values are visible.

## Cap dot count

With 1000+ dots per row, the SVG string gets long enough that Power BI's data-URI limit may trip. Cap at ~200 dots per row (sample if needed).

## See also

- `boxplot.md` — pre-aggregated summary instead of raw points
- `../../examples/jitter-plot-measure.dax`
