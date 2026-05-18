# Add a simple card

Use for a headline number without a target. If a target exists, use `kpi-card.md` instead.

## Create

```bash
pbir add visual cardVisual "<project>.Report/Overview.Page" --title "Revenue" \
  -d "Data:Sales.Revenue" \
  --x 24 --y 120 --width 290 --height 140
```

## Field roles

- `Data` (Measure, required)

## Sizing

Minimum height **130 px** so the value + label don't clip. Width 200–300 px for KPI rows.

## Hide redundant chrome

Cards show the metric name twice by default (visual title + category label). Pick one:

```bash
# Keep category label only (preferred — value reads as "3.8M Revenue")
pbir visuals title "<...>/Revenue.Visual" --no-show
```

## Templates

- `../examples/visuals/default/cardVisual.json` — new card (preferred)
- `../examples/visuals/default/card.json` — legacy card
- `../examples/visuals/formatted/cardVisual.json` — theme colors + SVG image + visual filter
- `../examples/visuals/formatted/card-with-filter.json` — gradient fill rule with visual-level filter

## After

`../validate/validate.md`.
