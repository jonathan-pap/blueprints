# SVG — status pill

Colored rounded-rect with a text label. Best for status indicators ("Active", "Late", "On Track").

## DAX (see `examples/status-pill-measure.dax`)

```dax
Status Pill =
VAR _status =
    SWITCH(
        TRUE(),
        [Variance] < 0,                "Behind",
        [Variance] < [Target] * 0.1,   "On Track",
                                       "Ahead"
    )
VAR _color =
    SWITCH(
        TRUE(),
        _status = "Behind",   "#D4602E",
        _status = "On Track", "#999999",
                              "#2B7A78"
    )
VAR _w = 80
VAR _h = 20
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""" & _w & """ height=""" & _h & """>" &
"<rect width=""" & _w & """ height=""" & _h & """ rx=""10"" fill=""" & _color & """/>" &
"<text x=""" & (_w/2) & """ y=""14"" text-anchor=""middle"" font-size=""11"" fill=""white"" font-family=""Segoe UI"">" & _status & "</text>" &
"</svg>"
```

## Wire

See `../wiring/in-table-matrix.md`. `imageHeight: 20`, `imageWidth: 80`.

## Theming

Replace the hardcoded colors with a sentiment color measure (`../theme-color-references.md`). Re-theming propagates.

## Common variants

- **Icon-only** (no text): drop the `<text>` element.
- **Compact** (just a dot): `<circle cx="10" cy="10" r="6" fill="..."/>`.
- **Two-tone** (pill with separator): two `<rect>` halves with different colors.

## See also

`../../examples/status-pill-measure.dax`.
