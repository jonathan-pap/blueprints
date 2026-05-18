# Conditional formatting — SVG icon

Inline icon (arrow, status pill, traffic light) per row, driven by a DAX measure that returns SVG.

## How it works

1. Write a DAX measure that returns a `data:image/svg+xml;utf8,...` string. See `../../visuals/svg/context.md` for the SVG engine details and ready-made example measures.
2. Set the measure's **`dataCategory = ImageUrl`** in TMDL (see `../../model/references/object-properties.md`).
3. Bind the measure to a table/matrix `Values` role or a card `Image URL` role.

## Minimal example (status pill)

```dax
Status Pill =
VAR _c = SWITCH(TRUE(), [Variance] < 0, "#D4602E", [Variance] >= 0, "#2B7A78", "#999999")
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""60"" height=""20"">" &
"<rect width=""60"" height=""20"" rx=""10"" fill=""" & _c & """/>" &
"</svg>"
```

Bind as a column in your `tableEx` Values role.

## After

`../validate/validate.md`. The icon column won't render in `pbir tree`, but it will in Desktop.
