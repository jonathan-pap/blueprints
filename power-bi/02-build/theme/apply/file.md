# Apply a custom theme JSON file

## CLI

```bash
pbir theme apply "<project>.Report" path/to/MyTheme.json
```

The file is copied into `<project>.Report/StaticResources/RegisteredResources/`. `report.json` `themeCollection.customTheme` is updated to point at it.

## Validate the JSON first

```bash
jq empty path/to/MyTheme.json   # syntactic
```

Schema validation: see `_deep-reference/theme-json-spec.md` for the full schema definition.

## Apply Microsoft-published themes

Microsoft hosts community themes on the [Power BI Theme Gallery](https://community.fabric.microsoft.com/t5/Themes-Gallery/bd-p/ThemesGallery). Download the `.json` and pass to `pbir theme apply`.

## After

```bash
pbir validate "<project>.Report"
pbir theme colors "<project>.Report"   # confirm palette took
```

Reopen Power BI Desktop to see the new theme applied.
