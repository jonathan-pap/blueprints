# SVG — overlapping bars

Two bars overlaid: prior in light, actual in dark on top. Use when comparing two periods in-row.

## DAX (see `examples/overlapping-bars-measure.dax`)

```dax
Overlapping Bars =
VAR _max   = MAX([Actual], [PY])
VAR _scale = MAX([Actual Max All Rows], [PY Max All Rows])
VAR _w     = 140
VAR _h     = 16
VAR _act_w = ([Actual] / _scale) * _w
VAR _py_w  = ([PY]     / _scale) * _w
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<rect x=""0"" y=""3"" width=""" & _py_w  & """ height=""10"" fill=""#CCCCCC""/>" &
"<rect x=""0"" y=""5"" width=""" & _act_w & """ height=""6""  fill=""#118DFF""/>" &
"</svg>"
```

## When to use

- Need two-period comparison but don't need the variance overlay (use `ibcs-bar.md` if you do).
- Want a cleaner visual than `ibcs-bar.md` for non-financial audiences.

## Variants

- **Stacked**: place actual at x=0 and PY beside it (not overlapping).
- **Mirror**: actual right of center, PY left, creating a butterfly chart.

## See also

- `overlapping-bars-with-variance.md` — same pattern + variance overlay
- `../../examples/overlapping-bars-measure.dax`
