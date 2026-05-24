# Add a simple card

Use for a headline number without a target. If a target exists, use `kpi-card.md` instead.

> Design guidance (the three elements, display-unit rule, title-vs-label, anti-patterns):
> [../references/cards-and-kpis.md](../references/cards-and-kpis.md).

## Create

```bash
pbir add visual card "<project>.Report/Overview.Page" --title "Revenue" \
  -d "Values:Sales.Revenue" \
  --x 24 --y 120 --width 290 --height 140
```

For the newer `cardVisual` (different visualType), the role names also differ — use `pbir add visual cardVisual --list` or check `examples/visuals/default/cardVisual.json`.

## Field roles

- `Values` (Measure, required) — the headline number

> Confirmed against pbir 0.9.19 on 2026-05-19. Earlier this doc said `Data`, which the CLI rejects: `Role 'Data' not valid for card. Available: Values`.

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
