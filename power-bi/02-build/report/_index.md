# 02-build/report — atomic file index

> Pick by intent. Load only the file(s) you need. Folder map below.

## build-report.md` — the build SEQUENCE (one line per step; read every build) · `build-report-detail.md — the one path for a full report (greenfield/redesign)
- `build-report.md` — **read first when building a whole report** — the end-to-end pipeline:
  design (tone → archetype → charts → contract) → build (design-system.yaml → theme → pages → visuals → gate)
- the design vocabulary it uses lives in `references/` (below); the contract spec is `layout/design-contract.md`

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
- `layout-guidelines.md` — sizes, equal-gap math, column alignment, z-order, perf limits
- `visual-groups.md` — bind visuals to move/scale together (`pbir visuals group`)
- `copy-move-delete.md`

## format/ — appearance
- `override-property.md` — single-visual override (when not theme-worthy)
- `conditional-fmt-color-scale.md`
- `conditional-fmt-data-bar.md`
- `conditional-fmt-rule.md`
- `conditional-fmt-svg-icon.md`
- `visual-presets.md` — one-shot style bundles (`pbir visuals preset`)
- `apply-theme-to-report.md`

## schema-patterns/ — PBIR formatting internals (hand-authoring)
- `selectors.md` — when/what a property applies to (dataViewWildcard, metadata:"select", scopeId)
- `expressions.md` — what goes inside `expr` (literals, Measure, FillRule, Conditional)
- `property-catalogue.md` — `pbir schema` discovery + per-type container index (49 types)

## references/ — design judgment + vocabulary (build-time)
- `design-identity.md` — the tone + signature + per-page archetype model (read for greenfield)
- `tones.md` · `signatures.md` — the design-identity catalogs (12 tones, 15 signatures)
- `references/archetypes/_index.md` — per-page router → 5 archetypes (+ variants)
- `composition.md` — multi-page composition + variant rotation
- `color-palettes.md` — CVD-safe palettes + colour-assignment strategy
- `accessibility.md` · `anti-patterns.md` — pre-ship checks (WCAG, the slop catalog)
- `interactivity.md` — cross-filter etiquette, interaction budget per archetype
- `brownfield.md` — redesign / restyle / theme-swap workflow
- `cards-and-kpis.md` — three elements, display units, title-vs-label, anti-patterns
- `tables-and-matrices.md` — table vs matrix, subtract-don't-add, strategic CF
- `visual-colors.md` — theme tokens, semantic sentiment, contrast, colorblind-safe

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
- `tools/` — room-level Python for scripted builds: `pbirkit.py` (the shared PBIR authoring core every project kit imports) — see `tools/_index.md`
