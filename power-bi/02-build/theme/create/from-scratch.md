# Create a theme from scratch (full workflow)

End-to-end. Use after `starting-point.md` has set your base.

## Phase 1 — Serialize

Split the base theme into editable fragments:

```bash
pbir theme serialize "<project>.Report" -o /tmp/MyTheme.Theme
```

**IMPORTANT:** Serialize to a temporary folder OUTSIDE `.Report/`. The PBIR validation hooks monitor `.Report/` for JSON changes and will flag serialized fragments as invalid PBIR files. Use `/tmp/`, a sibling folder, or the `-o` flag elsewhere.

Produces:

- `_config.json` — colors, text classes, named colors
- `_wildcards.json` — wildcard visual styles
- One file per visual-type override (`slicer.json`, `page.json`, etc.)

## Phase 2 — Design (in order)

These decisions cascade. Do them in sequence:

1. **Add `$schema` reference** → `schema-integration.md`
2. **Design color system** (4 layers) → `color-system.md`
   - `dataColors` (primary palette)
   - Semantic colors (`good`, `bad`, `neutral`)
   - Background/foreground variants
   - Accent colors
3. **Set typography** → `typography-roles.md`
   - At minimum: `title`, `header`, `label`, `callout`
   - Segoe UI / Segoe UI Semibold only
4. **Set wildcard container defaults** → `wildcard-defaults.md`
   - `title.show: true`, `dropShadow.show: false`, padding
   - Border, background, filter pane
5. **Override critical visual types** → `visual-type-priorities.md`
   - At minimum: `textbox`, `image`, `shape`, `actionButton`

## Phase 3 — Build and apply

```bash
# Build only (produces a merged theme.json without applying)
pbir theme build /tmp/MyTheme.Theme

# Build and apply directly to the report
pbir theme build /tmp/MyTheme.Theme -o "<project>.Report" -f --clean
```

`--clean` removes the `.Theme` folder after building.

## Phase 4 — Validate

```bash
pbir theme validate "<project>.Report"
```

Or fallback:

```bash
jq empty "<project>.Report/StaticResources/RegisteredResources/<theme>.json"
```

Walk through `checklist.md` to confirm you didn't miss anything. Deploy and visually verify on at least 3 visual types.

## Quick modifications (no serialize needed)

For small changes after the theme exists, use CLI directly:

```bash
pbir theme set-colors "<project>.Report" --good "#00B050" --bad "#FF0000"
pbir theme set-text-classes "<project>.Report" title --font-size 14 --font-face "Segoe UI Semibold"
pbir theme set-formatting "<project>.Report" "*.*.dropShadow.show" --value false
```

See `../modify/` for atomic files per modification type.

## After creation

The theme JSON lands in `<project>.Report/StaticResources/RegisteredResources/<theme>.json` and is referenced from `report.json`'s `themeCollection.customTheme`. See `../where-themes-live.md` for the full storage convention.
