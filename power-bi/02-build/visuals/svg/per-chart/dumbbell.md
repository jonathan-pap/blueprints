# SVG — dumbbell chart

Two dots connected by a line. Used for two-point comparisons (CY vs PY, before vs after, target vs actual).

## DAX (see `examples/dumbbell-chart-measure.dax`)

```dax
Dumbbell =
VAR _max   = [Max All Rows]
VAR _w     = 140
VAR _h     = 14
VAR _x_py  = ([PY]     / _max) * (_w - 12) + 6
VAR _x_cy  = ([Actual] / _max) * (_w - 12) + 6
VAR _color = IF([Actual] >= [PY], "#2B7A78", "#D4602E")
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<line x1=""" & _x_py & """ y1=""7"" x2=""" & _x_cy & """ y2=""7"" stroke=""" & _color & """ stroke-width=""2""/>" &
"<circle cx=""" & _x_py & """ cy=""7"" r=""4"" fill=""#999999""/>" &
"<circle cx=""" & _x_cy & """ cy=""7"" r=""4"" fill=""" & _color & """/>" &
"</svg>"
```

## Reads as

Gray dot = PY, colored dot = CY, line between shows direction and magnitude of change. Color encodes good/bad direction.

## When to use

- Two-point comparison per row.
- "Before / after" tables.
- Anywhere a bar chart would feel heavy for what's essentially showing change.

## See also

`../../examples/dumbbell-chart-measure.dax`.
