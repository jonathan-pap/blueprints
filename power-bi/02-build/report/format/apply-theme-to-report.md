# Apply a theme to the report

Point the report at a theme JSON. The theme file goes into `<project>.Report/StaticResources/RegisteredResources/`.

## Apply a bundled template

```bash
pbir theme apply-template "<project>.Report" sqlbi
```

Templates available: `sqlbi`, `fluent2`, `datagoblins2021` (see `../../theme/examples/`).

## Apply your own theme file

```bash
pbir theme apply "<project>.Report" path/to/MyTheme.json
```

## Verify

```bash
pbir theme colors "<project>.Report"       # current palette
pbir theme text-classes "<project>.Report" # current text style defaults
```

## Don't re-apply on new reports

New reports already ship with the sqlbi theme. Skip this step unless the user explicitly wants a different one.

## To author or modify the theme itself

Escalate to `../../theme/context.md`.

## After

`../validate/validate.md`.
