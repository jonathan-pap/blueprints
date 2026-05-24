# SVG inside an image visual (standalone canvas graphic)

Use when the SVG is its **own visual** on the canvas — a KPI header, a dashboard tile, a
wide gauge — rather than an inline micro-chart in a table row. The `image` visual gives it a
free-standing container that can be any size.

## Critical: `sourceType` must be `'imageData'`

For a `data:image/svg+xml;utf8,...` data URI the image visual **must** use
`sourceType = 'imageData'`. Using `'imageUrl'` (which is for real HTTP URLs) throws
`VisualDataProxyExecutionUnknownError` and renders a **black box**. This is the #1 reason an
SVG measure "works in a table but not in an image visual".

## Binding

1. Author the SVG measure with `dataCategory = ImageUrl` (see `../image-url-data-category.md`).
2. Add an `image` visual and bind the measure via `objects.image` — there is **no `query`
   block** (the measure is read directly through `sourceField`):

```json
{
  "objects": {
    "image": [{
      "properties": {
        "sourceType": { "expr": { "Literal": { "Value": "'imageData'" } } },
        "transparency": { "expr": { "Literal": { "Value": "0D" } } },
        "effects": { "expr": { "Literal": { "Value": "false" } } },
        "sourceField": {
          "expr": {
            "Measure": {
              "Expression": { "SourceRef": { "Schema": "extension", "Entity": "<TABLE>" } },
              "Property": "<SVG MEASURE>"
            }
          }
        }
      }
    }]
  }
}
```

(`Schema: "extension"` because SVG measures are usually thin-report extension measures — drop
it if the measure lives in the model. See `../../../report/pbip-format/` for the file shape.)

## Differences from a table/matrix SVG

| | Table/matrix cell | Image visual |
|---|---|---|
| Binding | `Values` projection | `objects.image.sourceField` (no query) |
| Size | `grid.imageHeight/Width` (~25×100) | the visual container — make `viewBox` match |
| viewBox | small (`0 0 100 25`) | wide (`0 0 300 60`, `0 0 200 80`, …) |
| Font sizes | 8–12 px | can go large (22–28 px values) |
| Labels | often in adjacent columns | put **all** text inside the SVG |

Recommended viewBoxes: KPI card `0 0 300 60` · dashboard tile `0 0 200 80` · banner `0 0 600 40`.

## Gotchas

- **`'imageData'`, not `'imageUrl'`** — see above.
- **Hex `#`, never `%23`** — `%23` breaks image visuals specifically (see `../svg-elements.md`).
- **No `query` block** — adding one can double-evaluate the measure.
- Turn `effects` off and `transparency` to `0D` so Power BI's default image styling doesn't
  tint or shadow the graphic.

## Worked example — KPI header

A value + label + PY-trend arrow, sized for a wide image visual:

```dax
KPI Header SVG =
VAR _Value = [Total Revenue]
VAR _Change = DIVIDE ( _Value - [Total Revenue PY], [Total Revenue PY] )
VAR _Color = IF ( _Change >= 0, "#2D6A2E", "#982F2F" )
VAR _Arrow =
    IF ( _Change >= 0,
        "<polygon points='170,28 175,20 180,28' fill='" & _Color & "'/>",
        "<polygon points='170,20 175,28 180,20' fill='" & _Color & "'/>" )
RETURN
"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 60'>" &
"<text x='10' y='20' font-family='Segoe UI' font-size='11' fill='#666' font-weight='600'>TOTAL REVENUE</text>" &
"<text x='10' y='48' font-family='Segoe UI' font-size='28' fill='#333' font-weight='700'>" & FORMAT ( _Value, "$#,##0,, M" ) & "</text>" &
_Arrow &
"<text x='185' y='28' font-family='Segoe UI' font-size='12' fill='" & _Color & "' font-weight='600'>" & FORMAT ( _Change, "+#,##0.0%;-#,##0.0%" ) & " vs PY</text>" &
"</svg>"
```

Any `per-chart/*` measure also renders here — just widen its `viewBox`. The
[target bar](../per-chart/target-bar.md) is a natural fit for an image visual.

## After

`../../../report/validate/validate.md`. Reopen Desktop.
