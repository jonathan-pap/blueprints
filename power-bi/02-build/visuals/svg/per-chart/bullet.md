# SVG — bullet chart (per row)

Actual vs target with banded ranges. Compact form of the classic Stephen Few bullet.

## DAX (see `examples/bullet-chart-measure.dax`)

Layered rects: 3 background bands, 1 actual bar, 1 target tick.

```dax
Bullet =
VAR _max  = [Range 100pct]
VAR _w    = 120
VAR _h    = 14
VAR _r1   = ([Range 50pct]  / _max) * _w
VAR _r2   = ([Range 80pct]  / _max) * _w
VAR _act  = ([Actual]       / _max) * _w
VAR _tgt  = ([Target]       / _max) * _w
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<rect x=""0""        width=""" & _w   & """ height=""" & _h & """ fill=""#E5E5E5""/>" &
"<rect x=""0""        width=""" & _r2  & """ height=""" & _h & """ fill=""#CCCCCC""/>" &
"<rect x=""0""        width=""" & _r1  & """ height=""" & _h & """ fill=""#999999""/>" &
"<rect x=""0"" y=""4"" width=""" & _act & """ height=""6""           fill=""#118DFF""/>" &
"<line x1=""" & _tgt & """ y1=""2"" x2=""" & _tgt & """ y2=""12"" stroke=""#000"" stroke-width=""2""/>" &
"</svg>"
```

## Wire

See `../wiring/in-table-matrix.md`. `imageHeight: 14`, `imageWidth: 120`.

## Reading

- Pale gray bar: max range.
- Mid gray: 80% range.
- Dark gray: 50% range.
- Blue bar: actual.
- Black tick: target.

Reader sees instantly whether actual is poor (within dark gray), satisfactory (mid gray), or good (pale gray), and whether it crossed the target tick.

## See also

`../../examples/bullet-chart-measure.dax` — full measure.
