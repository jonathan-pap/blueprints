# Set sentiment colors (`good` / `bad` / `neutral`)

Theme-level sentiment colors are referenced by extension measures (e.g. `IF(... , "good", "bad")`) and by conditional formatting. Setting them once means re-theming propagates everywhere.

## Default palette (sqlbi-style)

- `good` — `#2B7A78` (muted teal)
- `bad` — `#D4602E` (muted orange — accessible alternative to red)
- `neutral` — `#999999` (gray)
- `minColor` — gradient minimum
- `maxColor` — gradient maximum

## Apply via CLI

```bash
pbir theme set-sentiment "<project>.Report" \
  --good "#2B7A78" \
  --bad  "#D4602E" \
  --neutral "#999999"
```

## How they get used in DAX

Extension measures return the literal string:

```dax
Variance Status = IF([Variance] >= 0, "good", "bad")
```

In visual conditional formatting, bind this measure as the color source. Power BI resolves the string against the theme's sentiment colors.

## Accessibility

Blue / orange beats red / green for color blindness. Pair color with arrows or icons via SVG measures (`../../report/format/conditional-fmt-svg-icon.md`).

## After

`../../report/validate/validate.md`.
