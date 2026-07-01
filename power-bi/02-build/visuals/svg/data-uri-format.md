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
- **A coordinate system — set a `viewBox` (preferred) _or_ both `width` and `height`.** Without one,
  the SVG has no intrinsic size: a _narrow_ cell happens to act as the viewport (looks fine), but a
  _wide_ cell leaves absolute coords (`x='20'`, `width='100'`) stranded top-left and any **percentage
  dimension** (`height='80%'`) resolves against nothing → the cell renders as a flat grey box.
  Chart-in-cell measures get reused at different column widths, so **always set a `viewBox`** sized to
  the drawing (e.g. `viewBox='0 0 125 24'`).
- If you use `%` for any `width`/`height`, a `viewBox` is **mandatory** (it defines what the `%` is of).
  Safer still: convert `%` to absolute units inside the viewBox.
- `preserveAspectRatio='xMinYMid meet'` keeps a bar/sparkline left-anchored and vertically centred when
  the cell's aspect differs from the drawing's.

## Pitfalls

- Forgot the data URI prefix → Power BI shows the raw text.
- Missing `xmlns` → Power BI shows broken image icon.
- **Renders as a featureless grey box (esp. in a wide column)** → no `viewBox`/`width`/`height` (no
  coordinate system) and/or `%` dimensions with no viewport. Add a `viewBox`. See "Required SVG attributes".
- Used hardcoded hex in DAX → re-theming the report doesn't propagate. See `theme-color-references.md`.
