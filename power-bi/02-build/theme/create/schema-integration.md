# Schema integration

Add a `$schema` property as the **first key** in the theme JSON to enable IDE autocomplete + Desktop validation on import. Without it, you author blind.

## Two schema URLs in practice

```json
// Generic Power BI schema reference (used in exported themes)
{ "$schema": "https://powerbi.com/product/schema#reportTheme" }

// Versioned GitHub schema (recommended for authoring — enables full validation)
{ "$schema": "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json" }
```

## When to use which

- **Versioned GitHub URL** — when authoring or editing. Full validation + autocomplete in VS Code.
- **Generic `powerbi.com` URL** — if it was already present in an exported theme and you're not changing it. Don't add it new — prefer the versioned form.

## Schema versioning

Versioned monthly alongside Power BI Desktop releases. Pattern: `reportThemeSchema-2.{version}.json`.

As of March 2026, latest is `2.152` (exploration version 5.71). **Target the version matching the Desktop release your report consumers use.**

Schema index (check for newer): https://github.com/microsoft/powerbi-desktop-samples/tree/main/Report%20Theme%20JSON%20Schema

## What the schema gives you

- **Draft 7 compliant** — used verbatim by Desktop to validate themes on import. Invalid themes are rejected.
- **VS Code autocomplete** — Ctrl+Space inside theme JSON shows valid property names and enum values matching the Format pane.
- **The `visualStyles` section documents every property available for each visual type** — most reliable reference for which properties exist and what their valid values are.

## Pattern

In `_config.json` (after `serialize`) or the monolithic theme:

```json
{
  "$schema": "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json",
  "name": "MyTheme",
  "dataColors": [...],
  ...
}
```

`$schema` must be the FIRST property — JSON Schema discovery by editors looks at the top of the file.
