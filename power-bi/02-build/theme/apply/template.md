# Apply a theme template

Templates are bundled themes the `pbir` CLI installs. New reports already include `sqlbi` — don't re-apply unless changing.

## Available templates

- `sqlbi` — default for new reports. Clean, professional. Muted palette.
- `fluent2` — Microsoft Fluent 2 design system colors and typography.

Run `pbir theme list-templates` to see any additional templates bundled with your CLI version.

## CLI

```bash
pbir theme apply-template "<project>.Report" sqlbi
```

Templates land in `<project>.Report/StaticResources/RegisteredResources/`. Multiple themes can coexist — `definition.pbir` points at the active one.

## Verify

```bash
pbir theme colors "<project>.Report"
pbir theme text-classes "<project>.Report"
```

## Switching themes mid-project

Theme switches preserve visual-level overrides (Level 4). If you've been formatting visuals individually, those overrides will continue to win over the new theme. Run `audit/find-overrides.md` first; consider `promote/from-visuals.md` to bring overrides into the theme proper.

## After

`../../report/validate/validate.md`.
