# Where themes live (storage convention)

A PBIP report stores its custom theme as a JSON file inside the `.Report/` folder and references it by name from `report.json`.

## File layout

```text
<project>.Report/
├── definition/
│   └── report.json              # references the active theme by name
└── StaticResources/
    └── RegisteredResources/
        └── <ThemeName>.json     # the actual theme JSON
```

The theme JSON itself lives **only** in `StaticResources/RegisteredResources/`. It is registered (made active) via `definition/report.json`.

## How `report.json` references the theme

```json
{
  "themeCollection": {
    "customTheme": {
      "name": "MyCorpTheme-v1.2.json",
      "type": "RegisteredResources"
    }
  }
}
```

The `name` field is the **filename** in `RegisteredResources/`, not the theme's display name. The `name:` field inside the theme JSON is separate (used by Power BI Desktop UI only).

## Naming convention

- **Use a descriptive, versioned filename**: `MyCorpTheme-v1.2.json`, not `theme.json`
- **Match `name:` inside the JSON to the filename** (without `.json`) so they stay in sync
- **Use `pbir theme rename "<project>.Report"`** to keep filename + `name:` field aligned after edits

## Where serialized fragments live

When using `serialize/` workflow, the `.Theme/` folder lives **outside** `.Report/`:

```text
/tmp/MyTheme.Theme/        # OK outside .Report/, safe to edit
<project>.Report/
└── ...                    # do NOT serialize here — PBIR hooks reject fragments
```

PBIR validation hooks monitor `.Report/` for valid PBIR JSON. Serialized fragments are NOT valid PBIR — they will be flagged as invalid and block further edits.

After `pbir theme build /tmp/MyTheme.Theme -o "<project>.Report" -f --clean`, the built monolith lands back in `StaticResources/RegisteredResources/`.

## Central / shared themes

For themes shared across reports (corporate brand, design system):

- **In this workspace**: store under `projects/themes/<slug>/<slug>-vX.Y.json`. See `projects/themes/README.md`.
- **External source of truth**: Git repo (versioned, peer-reviewed), SharePoint, or a Fabric workspace
- **Distribution**: apply via `pbir theme apply-template "<project>.Report" --from-file <theme>.json`
- **Template library**: `pbir theme create-template --new-template <theme>.json --name "<slug>"` registers it in `~/.pbir/templates/themes/` for reuse

See `apply/copy-from-other.md` for copying a theme out of an existing report.

## See also

- `create/_index.md` — author a theme from scratch
- `apply/file.md` — apply an existing theme JSON file
- `apply/copy-from-other.md` — lift a theme from another report
- `serialize/split.md` — split monolith into fragments for editing
