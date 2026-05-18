# SVG — IBCS-styled bar

International Business Communication Standards bar pattern: actual vs prior, with variance bar overlay.

## DAX (see `examples/ibcs-bar-measure.dax`)

Three layered rects:
1. Prior period bar (light gray, full or partial width)
2. Actual bar (black, on top, slightly shorter height)
3. Variance overlay (red or green) only on the difference region

```dax
IBCS Bar =
VAR _max   = [Revenue Max All Rows]
VAR _w     = 140
VAR _h     = 18
VAR _act_w = ([Actual] / _max) * _w
VAR _py_w  = ([PY]     / _max) * _w
VAR _diff  = _act_w - _py_w
VAR _var_color = IF([Actual] >= [PY], "#2B7A78", "#D4602E")
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<rect x=""0""               y=""3"" width=""" & _py_w  & """ height=""12"" fill=""#CCCCCC""/>" &
"<rect x=""0""               y=""5"" width=""" & _act_w & """ height=""8""  fill=""#000000""/>" &
"<rect x=""" & MIN(_act_w,_py_w) & """ y=""3"" width=""" & ABS(_diff) & """ height=""12"" fill=""" & _var_color & """ opacity=""0.5""/>" &
"</svg>"
```

## Reads as

Two bars (PY in light gray, Actual in black on top); the variance is shaded between them — green if Actual > PY, red if behind.

## When to use

- IBCS-compliant reports for financial / managerial audiences.
- Comparing two periods on the same row.
- When you want the variance visually attached to the comparison rather than in a separate column.

## See also

`../../examples/ibcs-bar-measure.dax`.
