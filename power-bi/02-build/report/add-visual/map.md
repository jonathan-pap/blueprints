# Add a map (azureMap)

Use when **location or spatial distribution carries the message**. If geography is only a ranked
category ("top 10 countries by sales"), a sorted [bar chart](bar-chart.md) is clearer — see
[pick-visual-type.md](pick-visual-type.md).

> **Always `azureMap`.** `map` and `filledMap` are legacy Bing visuals — deprecated; `pbir validate`
> warns `PBIR_VISUAL_TYPE_DEPRECATED`. Do **not** create them; migrate existing ones to `azureMap`.
> `shapeMap` is not a substitute either.

## Create

```bash
pbir add visual azureMap "<project>.Report/Overview.Page" --title "Sales by region" \
  --x 24 --y 120 --width 600 --height 400
```

## Bind fields

```bash
pbir visuals bind "<...>/Sales by region.Visual" \
  -a "Category:Geography.Country" -t Column \
  -a "Size:Sales.Revenue" -t Measure
```

## Field roles

- `Category` (Column) — the **location**; required. A geographic column (country/state/city) auto-geocodes.
- `Size` (Measure, max 1) — bubble size.
- `Series` (Column, max 1) — legend grouping.
- `Y` (Latitude) / `X` (Longitude) — use only when you have explicit coordinate columns instead of named places.
- `Tooltips` (Measure).

## Design rules

- Bind a clean geographic column to `Category`; Azure Maps geocodes it — no lat/lon needed unless you
  have coordinates (then bind `Y`/`X`).
- Give `Size` a measure so bubbles encode magnitude; add a size legend so the reader can decode it.
- Symbol (bubble) map for point magnitude; choropleth when a region fill is the message.
- Keep ≤200–500 points; beyond that, aggregate to a coarser region ([chart-selection cardinality](pick-visual-type.md#cardinality-limits)).

## When it won't render

Geocoding/format failures (ambiguous place names, missing coords, unsupported region):

1. Debug the field — check values, try an alternative geographic column, or coarser aggregation level.
2. If you have lat/lon, bind `Y`/`X` instead of `Category`.
3. **Azure Maps disabled by tenant policy / unsupported region** → fall back to a **non-map** encoding:
   a `tableEx` of locations with conditional formatting, or a clustered bar by region — and tell the
   user *why*. Never fall back to the legacy `map`/`filledMap`/`shapeMap`.
4. Don't silently swap a map for a non-map on a *resolvable* data issue — fix the data or ask the user first.

## Theme

Map appearance (base style, controls) is theme-level → [`../../theme/examples/visual-types/azureMap.md`](../../theme/examples/visual-types/azureMap.md).
For dark mode, the base-map style is an **enum** (`mapControls.defaultStyle`: `night`/`grayscale_dark`
for dark), not a hex — a hex sweep won't touch it ([`../../theme/modify/dark-mode-checklist.md`](../../theme/modify/dark-mode-checklist.md)).

## After

`../validate/validate.md`.
