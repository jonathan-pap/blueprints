# Sub-room — Theme

> Theme JSON sets defaults for **all visuals**. Use this room when a change should apply globally; otherwise stay in `../report/format/`.

## Tool preference

1. `pbir` CLI — `pbir theme colors`, `pbir theme text-classes`, `pbir theme apply-template`, `pbir visuals clear-formatting`.
2. Serialized fragments — `pbir theme serialize` splits a monolith into small editable files (per visual type, per text class). Always operate on fragments, never the monolith.
3. Direct `jq` — last resort. Always validate.

## Workflow router

- **Read the cascade** before any change → `cascade.md`
- **Create a new theme from scratch** → `create/_index.md`
- **Where the theme JSON lives on disk** (storage convention) → `where-themes-live.md`
- **Apply a theme template** to the report → `apply/template.md`
- **Apply a custom theme JSON** → `apply/file.md`
- **Change palette colors** → `modify/colors.md`
- **Change text classes** (callout, title, label sizes) → `modify/text-classes.md`
- **Override every visual** (wildcard) → `modify/wildcard.md`
- **Override one visual type** (e.g., all lineCharts) → `modify/visual-type-override.md`
- **Push visual-level formatting up into the theme** → `promote/from-visuals.md`
- **Find drift** (visuals that bypassed the theme) → `audit/find-overrides.md`
- **Audit compliance** (cascade adherence) → `audit/compliance.md`
- **Split monolith → fragments** for editing → `serialize/split.md`
- **Rebuild fragments → monolith** → `serialize/build.md`
- **Copy a theme from another report** → `apply/copy-from-other.md`
- **Share a theme as a reusable template** (extract, register, distribute) → `apply/share-as-template.md`

## Hard rules

- **Never read the monolithic theme JSON.** Files hit 75 KB / 2000+ lines. Always serialize first or use `jq` to extract specific keys.
- **New reports already ship with sqlbi.** Don't apply a template unless the user explicitly asks for a different one.
- **Push formatting up.** If the same override appears on > 2 visuals of the same type, lift it into the theme via `promote/from-visuals.md`.
- **Validate every theme JSON write** with `jq empty <file>.json`.

## Examples

- `examples/DataGoblins2021.json` — community theme reference
- `examples/Fluent2-CY26SU03.json` — Microsoft Fluent 2

## Deep reference (load only on explicit request)

`_deep-reference/theme-json-spec.md` — full PBIR theme JSON structure. 25 KB. Skip unless answering a specific schema question.
