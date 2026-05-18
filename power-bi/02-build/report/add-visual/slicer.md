# Add a slicer

Use for page-level filtering exposed as a visual. Limit to **3 slicers per page** — extras belong in the filter pane (`../filters/configure-filter-pane.md`).

## Create

```bash
pbir add visual slicer "<project>.Report/Overview.Page" --title "Year" \
  --x 24 --y 120 --width 200 --height 80
```

## Bind field

```bash
pbir visuals bind "<...>/Year.Visual" \
  -a "Values:Date.Calendar Year" -t Column
```

## Variants

- `slicer` — classic dropdown / list
- `advancedSlicerVisual` — newer button-style with multi-select

## Position consistently

All slicers on a page should sit in a single row at the top **or** a single column on the left. Pick one and stick to it across pages.

## Templates

- `../examples/visuals/default/slicer-list.json` — classic list slicer
- `../examples/visuals/default/slicer-dropdown.json` — dropdown mode
- `../examples/visuals/default/advancedSlicer.json` — newer button-style
- `../examples/visuals/formatted/slicer.json` — formatted list slicer
- `../examples/visuals/formatted/slicer-flash.json` — highlighted-selection variant
- `../examples/visuals/formatted/advancedSlicer-buttons.json` — button slicer with custom selection colors

## After

`../validate/validate.md`.
