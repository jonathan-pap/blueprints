# Reference theme colors inside SVG DAX

Hardcoded hex doesn't follow theme changes. Use a sibling measure that returns a sentiment color, or use the theme's known palette.

## Pattern — sentiment via sibling measure

```dax
Status Color =
SWITCH(
    TRUE(),
    [Variance] < 0,    "#D4602E",   -- bad
    [Variance] = 0,    "#999999",   -- neutral
                       "#2B7A78"    -- good
)
```

Then reference inside the SVG:

```dax
Status Pill =
VAR _color = [Status Color]
RETURN
"data:image/svg+xml;utf8," &
"<svg xmlns=""http://www.w3.org/2000/svg"" width=""60"" height=""20"">" &
"<rect width=""60"" height=""20"" rx=""10"" fill=""" & _color & """/>" &
"</svg>"
```

Re-theming the report → update `Status Color` → every SVG visual using it updates.

## Pattern — theme palette by index

Reference theme's `dataColors[i]` by hardcoding the hex the theme currently uses. Less flexible than a sentiment measure, but works for non-semantic visuals (e.g., a sparkline matching theme primary).

For full theme integration, use Deneb (`../deneb/charts/*.md`) — Vega exposes the live theme palette via `pbiColor(N)`.

## See also

- `../../theme/modify/sentiment-colors.md` — set `good` / `bad` / `neutral` at theme level
- `data-uri-format.md` — escape rules for embedding the color into DAX
