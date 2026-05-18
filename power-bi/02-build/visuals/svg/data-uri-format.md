# SVG data URI format

The returned string MUST start with `data:image/svg+xml;utf8,` followed by valid SVG.

## Minimum viable example

```dax
Hello SVG =
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""100"" height=""20"">" &
"<rect width=""100"" height=""20"" fill=""#118DFF""/>" &
"</svg>"
```

## Escape rules

Inside DAX strings, double-quote characters are escaped by doubling:

- HTML `"` → DAX `""`
- HTML `'` → DAX `'` (no escape needed)
- DAX strings use `""` to escape quotes; SVG attributes use `"..."` for values.

Result: every `"..."` in HTML becomes `""..""` in DAX.

## Required SVG attributes

- `xmlns="http://www.w3.org/2000/svg"` — required, or Power BI won't recognize it as SVG.
- `width` and `height` — must be set; Power BI sizes the rendered image to fit the cell.
- `viewBox` — optional but recommended for crisp scaling.

## Pitfalls

- Forgot the data URI prefix → Power BI shows the raw text.
- Missing `xmlns` → Power BI shows broken image icon.
- Used hardcoded hex in DAX → re-theming the report doesn't propagate. See `theme-color-references.md`.
