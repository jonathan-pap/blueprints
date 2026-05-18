# SVG — sparkline (per row in a table)

Mini trend line per row. Showing direction at a glance.

## DAX (from `examples/sparkline-measure.dax`)

Open `../../examples/sparkline-measure.dax` for the full measure. Core pattern:

```dax
Sparkline =
VAR _data = ADDCOLUMNS(
    VALUES('Date'[Month]),
    "@v", [Revenue]
)
VAR _min = MINX(_data, [@v])
VAR _max = MAXX(_data, [@v])
VAR _w = 100
VAR _h = 20
VAR _points =
    CONCATENATEX(
        _data,
        VAR _i = ... -- index of this row
        VAR _x = (_i / (COUNTROWS(_data) - 1)) * _w
        VAR _y = _h - ((([@v] - _min) / (_max - _min)) * _h)
        RETURN _x & "," & _y,
        " "
    )
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<polyline points=""" & _points & """ stroke=""#118DFF"" stroke-width=""1.5"" fill=""none""/>" &
"</svg>"
```

## Wire into a table

See `../wiring/in-table-matrix.md`. Set `imageHeight: 20`, `imageWidth: 100`.

## Variants

- **Filled area**: change `<polyline>` to `<polygon>` and close to baseline.
- **End-dot**: add a `<circle>` at the last point in the same color.
- **Color by direction**: branch on `[Revenue last] vs [Revenue first]` and pick `good` / `bad` colors via `../theme-color-references.md`.

## See also

`../../examples/sparkline-measure.dax` — full working measure.
