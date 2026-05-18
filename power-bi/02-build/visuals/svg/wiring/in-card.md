# SVG inside a card (full-card visual)

Use when the entire visual is the SVG (a custom KPI card, a status display).

## Procedure

1. Author the SVG measure — see `../per-chart/*`.
2. Set `dataCategory = ImageUrl` — see `../image-url-data-category.md`.
3. Add a `cardVisual` or `image` visual:

```bash
pbir add visual cardVisual "<project>.Report/Overview.Page" \
  --x 24 --y 120 --width 300 --height 160
pbir visuals bind "<...>/Card.Visual" -a "Data:_Measures.MySvgKpi" -t Measure
```

4. Configure the card to render as image — in `visual.json` objects, set `dataDesign.displayMode = "image"` (or the visual-type specific equivalent; check `pbir property-catalogue --visual-type cardVisual`).

## Sizing

Card visual: width × height ≥ SVG width × height. Allow padding by giving the card 10–20 px more on each axis than the SVG's intrinsic dimensions.

## When to use this vs Deneb

- **SVG card**: 30 min to author, no custom visual install, no interactivity.
- **Deneb KPI**: 2–4 hours to author, requires Deneb visual install, full interactivity.

Use SVG for fixed-content KPIs; Deneb for anything that needs to respond to selection.

## After

`../../../report/validate/validate.md`. Reopen Desktop.
