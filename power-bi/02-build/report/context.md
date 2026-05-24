# Sub-room — Report

> Edit `<project>.Report/` files. PBIR JSON via the `pbir` CLI. **Load one atomic step at a time** — do not load this whole folder.

## Tool

`pbir` CLI. Install once: `uv tool install pbir-cli` or `pip install pbir-cli`. Confirm with `pbir --version`.

## Workflow router

Find your intent. Each bullet gives the exact step files to load in order.

- **Add a KPI card bound to a real measure** → `bind/find-canonical-name.md` → `add-visual/kpi-card.md` → `bind/bind-field.md` → `validate/validate.md`
- **Add any other visual (pick chart type)** → `add-visual/_index.md` → matching chart file → `validate/validate.md`
- **Bind / rebind fields** → `bind/_index.md` → matching step
- **Position / size / align visuals** → `layout/_index.md` → matching step
- **Format a single visual (border, title, fonts)** → `format/override-property.md` (or escalate to `../theme/` if it applies to all visuals of a type)
- **Apply a style preset / group visuals** → `format/visual-presets.md` / `layout/visual-groups.md`
- **Conditional formatting** → `format/_index.md` → choose flavour (color-scale, data-bar, rule, svg-icon)
- **Hand-authoring `visual.json` formatting (recipes, build scripts)** → `schema-patterns/_index.md` (selectors, expressions, property catalogue)
- **Design judgment (which/how to format cards, tables, colors, layout)** → `references/_index.md`
- **Add / rename / size a page** → `page/_index.md` → step
- **Add filters / configure filter pane** → `filters/_index.md` → step
- **Bookmarks** → `bookmarks/_index.md`
- **Visual calculation or thin-report measure** → `calculations/_index.md`
- **Rename cascade (table / measure / column)** → `pbip-format/rename-<thing>.md` → `pbip-format/post-rename-checklist.md`
- **PBIP file-format question (extract pbix, encoding)** → `pbip-format/_index.md`
- **Convert legacy report → PBIR** → `validate/convert-legacy.md`
- **Validate after a change** → `validate/validate.md`
- **Read TMDL from the report side (no live connection)** → `semantic-model/_index.md`

## Hard rules

- Run `validate/validate.md` after every mutation.
- Visuals must not overlap.
- New reports already include a default Page 1 with a title textbox at (20, 20). Rename the page, don't add a duplicate. Place new visuals at y ≥ 120.
- Bindings must reference real model fields. Always run `bind/find-canonical-name.md` before guessing.
- Need real DAX validation or live measure values? Stop and load `../../03-bind/`.

## What's here

- `_index.md` — full picker by intent (load when unsure which step)
- Family folders — `add-visual/`, `bind/`, `layout/`, `format/`, `schema-patterns/`, `references/`, `page/`, `filters/`, `bookmarks/`, `calculations/`, `pbip-format/`, `validate/`, `semantic-model/`
- `examples/K201-MonthSlicer.Report/` — structural reference, do not edit
