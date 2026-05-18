# Theme authoring checklist

Before considering a theme complete, walk through:

- [ ] **`$schema` is the first key** (versioned GitHub URL, matching Desktop release)
- [ ] **`dataColors` has 6–12 entries**; first color is the "primary" most-used
- [ ] **Semantic colors set** (`good`, `bad`, `neutral`) and distinct from series colors
- [ ] **Background/foreground variants set** (`foreground`, `background`, plus light/dark variants)
- [ ] **`textClasses` covers at minimum**: `title`, `header`, `label`, `callout`, `dataTitle`
- [ ] **textClasses colors are plain hex strings** (NOT wrapped in `{"solid": {...}}`)
- [ ] **Wildcard sets container defaults**: `title`, `background`, `border`, `dropShadow`, `padding`
- [ ] **`dropShadow.show: false` in wildcard**
- [ ] **At minimum `textbox`, `image`, `shape`, `actionButton` have overrides** disabling container chrome
- [ ] **Filter pane** (`outspacePane` + `filterCard`) styled in wildcard
- [ ] **Theme validates** with `pbir theme validate "<project>.Report"` (or `jq empty` as fallback)
- [ ] **Deployed and visually verified** on at least 3 visual types

## Validate the JSON

```bash
pbir theme validate "<project>.Report"
```

Fallback if `pbir` not available:

```bash
THEME_NAME=$(jq -r '.themeCollection.customTheme.name' "<project>.Report/definition/report.json")
THEME="<project>.Report/StaticResources/RegisteredResources/$THEME_NAME"
jq empty "$THEME"
```

## Visually verify

Reopen `<project>.pbip` in Power BI Desktop and check 3 different visual types — at minimum a KPI card, a chart (line or bar), and a slicer. Look for:

- Title font + size matches `textClasses.title`
- Data colors come from `dataColors[]` array (no random hex)
- No drop shadows
- Textboxes have no border / title bar
- Filter pane uses the outspacePane styling

If anything looks wrong, walk back up the cascade per `../cascade.md`.

## Sign-off

If this is a shared / branded theme that other reports will inherit:

- Save the JSON somewhere central (Git, SharePoint, Fabric workspace)
- Document the schema version it targets
- Note the date of the most recent visual verification
- Tag the theme version in `name` field (e.g., `MyCorp Theme v1.2`)

## See also

- `../audit/compliance.md` — ongoing compliance checks after the theme is in use
- `../where-themes-live.md` — file storage convention
