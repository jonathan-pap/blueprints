# SVG — lollipop chart

A line + dot pattern, often used as a less heavy alternative to bar charts.

## DAX (see `examples/lollipop-conditional-measure.dax`)

```dax
Lollipop =
VAR _val   = [Revenue]
VAR _max   = [Revenue Max All Rows]
VAR _w     = 120
VAR _h     = 16
VAR _x     = (_val / _max) * (_w - 8)
VAR _color = IF(_val >= [Target], "#2B7A78", "#D4602E")
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<line x1=""4"" y1=""8"" x2=""" & _x & """ y2=""8"" stroke=""" & _color & """ stroke-width=""1""/>" &
"<circle cx=""" & _x & """ cy=""8"" r=""4"" fill=""" & _color & """/>" &
"</svg>"
```

## Reads as

A stick from the baseline to a dot whose horizontal position encodes the value. Conditional color (good/bad) makes the row's status pop without needing a separate status column.

## Why lollipop over bar

- Less "ink" than a bar — easier to scan many rows.
- The dot draws the eye to the precise endpoint.
- Pairs well with conditional color.

## Wire

See `../wiring/in-table-matrix.md`. `imageHeight: 16`, `imageWidth: 120`.

## See also

`../../examples/lollipop-conditional-measure.dax`.
