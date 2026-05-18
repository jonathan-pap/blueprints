# Color system design (4 layers)

The color system in a theme has four layers. **Design them in this order** — each layer feeds the next.

## Layer 1 — Data colors (`dataColors`)

The primary series palette. Ordered by expected usage frequency — most-used color first.

### Rules

- **6–12 colors** recommended. Fewer is more cohesive.
- **Visually distinguishable** including for color-blind users. Favor blue/orange/teal over red/green for series.
- **Test by listing the palette and imagining a 4-series bar chart** — the first 4 colors carry the most meaning.
- **Muted, desaturated tones** preferable to saturated "screaming" colors.

```json
"dataColors": ["#1971c2", "#f08c00", "#2f9e44", "#ae3ec9", "#e03131", "#0c8599"]
```

## Layer 2 — Semantic colors

Flat top-level hex string keys used by conditional formatting measures that return color name strings (`"good"`, `"bad"`, `"neutral"`).

> **NOT nested under a `sentimentColors` object** — they are individual keys at the root level of the theme JSON.

```json
"good": "#2f9e44",
"bad": "#e03131",
"neutral": "#868e96",
"maximum": "#1971c2",
"center": "#f8f9fa",
"minimum": "#e03131"
```

CF measures that return `"good"` will use whatever hex is set here. **This centralizes CF color control in one place** — change once, propagates everywhere.

## Layer 3 — Background/foreground variants

Extended palette for container surfaces, canvas backgrounds, foreground text. Feeds into `visualContainerObjects` backgrounds and the filter pane.

```json
"foreground": "#343a40",
"foregroundLight": "#868e96",
"foregroundDark": "#212529",
"foregroundNeutralSecondary": "#adb5bd",
"background": "#ffffff",
"backgroundLight": "#f8f9fa",
"backgroundNeutral": "#e9ecef",
"backgroundDark": "#dee2e6"
```

## Layer 4 — Additional accent colors

```json
"tableAccent": "#1971c2",
"hyperlink": "#1971c2",
"shapeStroke": "#dee2e6",
"accent": "#1971c2"
```

## Color principles

- **WCAG contrast** — text on background must clear 4.5:1 (normal) or 3:1 (large 18pt+). See `../../report/format/_index.md` for visual-level CF; for theme-level, just pick safe defaults.
- **Use `ThemeDataColor` references in visual JSON** (`{"ThemeDataColor": {"ColorId": 1, "Percent": 0}}`) rather than hardcoded hex. Re-coloring the theme then propagates everywhere.
- **`dataColors[0]` is the "primary" color** — appears most frequently across the report.

## After

Set typography next → `typography-roles.md`. Color decisions cascade into title color, label color, etc. — those should align to the foreground variants in Layer 3.

## See also

- `../modify/colors.md` — CLI to set palette after theme exists
- `../modify/sentiment-colors.md` — CLI to set `good`/`bad`/`neutral`
- `../modify/visual-type-override.md` — per-visual-type color overrides
- `../audit/find-hardcoded-hex.md` — find visuals still using hex instead of theme refs
