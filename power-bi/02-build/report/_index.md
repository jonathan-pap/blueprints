# 02-build/report — atomic file index

> Pick by intent. Load only the file(s) you need. Folder map below.

## add-visual/ — create a new visual
- `kpi-card.md`, `card.md` — single-value visuals
- `line-chart.md`, `bar-chart.md`, `column-chart.md`, `clustered-column-chart.md`
- `table.md`, `matrix.md`
- `slicer.md`
- `textbox.md`, `image.md`
- `pick-visual-type.md` — decision tree by reader question

## bind/ — wire fields to visuals
- `find-canonical-name.md` — discover the real table/field name (no live conn)
- `bind-field.md` — add a field to a visual role
- `column-vs-measure.md` — set the correct field kind
- `swap-field.md`, `clear-binding.md`
- `inspect-bindings.md`

## layout/ — position and align
- `page-dimensions.md` — query and pick page size
- `position-visual.md`, `size-visual.md`
- `align-visuals-row.md`, `align-visuals-grid.md`
- `detail-gradient.md` — 3-30-300 layout pattern
- `copy-move-delete.md`

## format/ — appearance
- `override-property.md` — single-visual override (when not theme-worthy)
- `conditional-fmt-color-scale.md`
- `conditional-fmt-data-bar.md`
- `conditional-fmt-rule.md`
- `conditional-fmt-svg-icon.md`
- `apply-theme-to-report.md`

## page/ — page-level edits
- `add-page.md`, `rename-page.md`, `delete-page.md`
- `set-page-size.md`
- `set-page-wallpaper.md`
- `add-page-title.md`

## filters/
- `add-page-filter.md`, `add-visual-filter.md`
- `configure-filter-pane.md`

## bookmarks/
- `create-bookmark.md`
- `bookmark-navigator.md`

## calculations/
- `visual-calculation.md` — DAX scoped to one visual
- `thin-report-measure.md` — DAX scoped to the report
- `reference-line.md`, `error-bar.md`

## pbip-format/ — file format & cascade renames
- `_index.md` — full picker
- `what-is-pbip.md`, `thick-vs-thin.md`, `extract-pbix.md`, `pbix-encoding-table.md`
- `rename-table.md`, `rename-measure.md`, `rename-column.md`, `post-rename-checklist.md`

## validate/
- `validate.md` — `pbir validate` after every mutation
- `convert-legacy.md` — old `report.json` → PBIR
- `fix-broken-field-reference.md`

## semantic-model/ — read TMDL from the report side (no live conn)
- `find-field-from-tmdl.md`
- `read-measure-definition.md`
- `infer-dax-from-visual.md`
- `rebind-to-different-field.md`
