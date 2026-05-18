# 02-build/theme — atomic file index

- `cascade.md` — the 4-level formatting cascade (read once, apply always)
- `where-themes-live.md` — file storage convention (`StaticResources/RegisteredResources/`, naming, `.Theme/` folder)

## create/

- `_index.md` — author from scratch (7-step workflow)
- `starting-point.md` — never author from `{}`; valid bases (SQLBI, community, exported)
- `from-scratch.md` — full 4-phase serialize → design → build → validate workflow
- `schema-integration.md` — `$schema` first key, versioned GitHub URLs
- `color-system.md` — 4 layers (`dataColors`, semantic, bg/fg, accents)
- `typography-roles.md` — `textClasses` catalog + plain-hex-string gotcha
- `wildcard-defaults.md` — minimum viable `visualStyles["*"]["*"]`
- `visual-type-priorities.md` — must-override types (textbox, image, shape, actionButton)
- `checklist.md` — 12-point completion checklist

## apply/

- `template.md` — bundled template (`sqlbi`, `fluent2`, `datagoblins2021`)
- `file.md` — your own theme JSON
- `copy-from-other.md` — lift a theme from another report
- `share-as-template.md` — extract a theme as a reusable template; download from Service / Fabric / community; diff themes

## modify/

- `colors.md` — palette colors via CLI
- `text-classes.md` — title / callout / label sizes
- `wildcard.md` — `visualStyles["*"]["*"]` overrides
- `visual-type-override.md` — `visualStyles["lineChart"]["*"]` overrides
- `sentiment-colors.md` — set `good`/`bad`/`neutral` for semantic measures

## promote/

- `from-visuals.md` — lift visual-level overrides into the theme
- `clear-visual-overrides.md` — remove redundant per-visual fmt after promoting

## audit/

- `compliance.md` — does each visual inherit cleanly from the theme?
- `find-overrides.md` — list visuals with `objects` / `visualContainerObjects`
- `find-hardcoded-hex.md` — find hex colors that should reference theme colors

## serialize/

- `split.md` — monolith → fragments
- `build.md` — fragments → monolith
- `fragment-layout.md` — what each fragment file contains

## _deep-reference/

- `theme-json-spec.md` — full schema (25 KB, load only on explicit ask)
