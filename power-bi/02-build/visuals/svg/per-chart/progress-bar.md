# SVG — progress bar

Percent-of-goal as a horizontal bar.

## DAX (see `examples/progress-bar-measure.dax`)

```dax
Progress Bar =
VAR _pct  = MIN(DIVIDE([Actual], [Target]), 1)
VAR _w    = 100
VAR _h    = 16
VAR _fill = _pct * _w
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<rect width=""" & _w & """ height=""" & _h & """ fill=""#EEEEEE"" rx=""8""/>" &
"<rect width=""" & _fill & """ height=""" & _h & """ fill=""#2B7A78"" rx=""8""/>" &
"</svg>"
```

## Wire into a table

See `../wiring/in-table-matrix.md`. `imageHeight: 16`, `imageWidth: 100`.

## Variants

- **Cap percentage at 100%**: `MIN(..., 1)` (default). Or allow over-target: remove `MIN` and let the inner rect exceed the outer.
- **Color by performance**: branch the fill color on `_pct`:
  - `< 0.6` → bad
  - `0.6–0.9` → neutral
  - `≥ 0.9` → good
- **Add label**: `<text>` element with `[Actual] / [Target]` value, positioned at right.

## See also

`../../examples/progress-bar-measure.dax` — full measure.
