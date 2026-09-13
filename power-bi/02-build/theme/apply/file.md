# Apply a custom theme JSON file

Points the report at a custom theme JSON. Theme-first is the rule: appearance belongs in the theme, so reach for this instead of repeating the same formatting override across individual visuals.

## There is no `pbir theme apply`

Checked against pbir-cli 0.9.32: the `theme` group authors the report's *existing* theme
(`colors`, `set-colors`, `fonts`, `set-fonts`, `set-formatting`, `push-visual`, `serialize`, `build`,
`validate`). It has no command that points a report at a new theme file. Applying one is a small
PBIR edit, and it is the same edit Desktop makes on *View > Themes > Browse for themes*:

1. Copy the theme JSON into `<project>.Report/StaticResources/RegisteredResources/<file>.json`.
2. In `definition/report.json`, add the item to the `RegisteredResources` package:
   `{ "name": "<file>.json", "path": "<file>.json", "type": "CustomTheme" }`.
3. Set `themeCollection.customTheme` to
   `{ "name": "<file>.json", "reportVersionAtImport": <copy from baseTheme>, "type": "RegisteredResources" }`.
   Leave `baseTheme` untouched.

Scripted builds do these three steps with `pbirkit.register_theme(theme_path)`
(`02-build/report/tools/pbirkit.py`). It is idempotent, so re-running a build updates the file in place.

## Validate the JSON first

```bash
jq empty path/to/MyTheme.json                         # syntactic
pbir theme validate "<project>.Report"                # after applying - schema
```

Schema detail: `_deep-reference/theme-json-spec.md`.

## Before applying under an existing report

A theme's wildcard (`"*"`) settings reach every visual type. **Padding** is the one that surprises:
it shrinks image visuals (HTML-in-SVG panels, SVG nav rails). Give `image`, `actionButton`, `textbox`
and `shape` explicit zero padding (`report/validate/build-traps.md` trap 18).

## Apply Microsoft-published themes

Microsoft hosts community themes on the [Power BI Theme Gallery](https://community.fabric.microsoft.com/t5/Themes-Gallery/bd-p/ThemesGallery). Download the `.json` and apply it with the steps above.

## After

```bash
pbir validate "<project>.Report"
pbir theme colors "<project>.Report"   # confirm palette took
```

Reopen Power BI Desktop to see the new theme applied.
