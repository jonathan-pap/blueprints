# Share a theme as a reusable template

Once a theme is good, register it so other reports can pull it in with one command.

## Extract the theme JSON from a report

```bash
pbir cat "<project>.Report/theme" > /tmp/<theme>.json
```

This pulls the active theme out of `StaticResources/RegisteredResources/` as a standalone file.

## Register as a CLI template

```bash
pbir theme create-template --new-template /tmp/<theme>.json \
  --name "<slug>" \
  --description "<short description>" \
  --author "<team or person>" \
  --recommended check
```

The template lands in `~/.pbir/templates/themes/` and is then available to every report via:

```bash
pbir theme apply-template "<target>.Report" <slug>
```

### Recommendation status

- `check` — recommended for general use
- `warning` — usable with caveats
- `none` — no recommendation

## Update an existing template

```bash
pbir cat "<project>.Report/theme" > /tmp/updated.json
pbir theme create-template /tmp/updated.json --update-template <slug>
```

## Download themes from external sources

### From a Fabric workspace

```bash
pbir download "<workspace>.Workspace/<report>.Report" -o ./downloaded
pbir cat "downloaded/<report>.Report/theme" > theme.json
```

### From the Power BI service UI

`View → Themes → Save current theme` exports the active theme as JSON. Save locally, then apply it with the round-trip below.

### From the community

[deldersveld/PowerBI-ThemeTemplates](https://github.com/deldersveld/PowerBI-ThemeTemplates) — download a JSON, then:

```bash
pbir theme serialize <downloaded>.json -o /tmp/<slug>.Theme
pbir theme build /tmp/<slug>.Theme -o "<target>.Report" -f --clean
```

> **`apply-template` takes a registered template NAME, not a path.** There is no `--from-file` flag
> (verified against pbir 0.9.25). To apply a standalone JSON, either round-trip it through
> `serialize` → `build` as above, or register it once and then apply it by name:
>
> ```bash
> pbir theme create-template --new-template <downloaded>.json --name <slug>
> pbir theme apply-template "<target>.Report" <slug>
> ```

Or serialize it first for customization → `../serialize/split.md`.

## Compare themes before adopting

```bash
pbir theme diff "<report-A>.Report" "<report-B>.Report"
pbir theme diff "<report>.Report" "<standalone>.json"
pbir theme diff "<BrandA>.Theme" "<BrandB>.Theme"
```

Flags: `--colors`, `--text-classes` to scope the diff.

## See also

- `template.md` — apply a bundled template
- `file.md` — apply a standalone JSON file
- `copy-from-other.md` — copy a theme directly between two reports
- `../where-themes-live.md` — storage convention (central source-of-truth: Git, SharePoint, Fabric workspace)
