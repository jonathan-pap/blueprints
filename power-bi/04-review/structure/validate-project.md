# Validate the full PBIP project

Run before opening in Power BI Desktop. Catches issues that would break the load.

## Script

```bash
python ../scripts/validate_pbip.py "<project>"
```

## What it checks

- TMDL syntax across `<project>.SemanticModel/`
- PBIR JSON syntax across `<project>.Report/`
- Required schema fields present
- M expression vs table namespace collision
- `definition.pbir` byPath vs byConnection consistency
- UTF-8 BOM check across all text files
- Folder name issues (spaces, special chars)
- Referential integrity (TMDL ↔ PBIR cross-references)
- Lineage tag uniqueness

## Run as a Git pre-commit

In `.git/hooks/pre-commit`:

```bash
#!/bin/bash
for proj in projects/*/; do
  python power-bi/04-review/scripts/validate_pbip.py "$proj" || exit 1
done
```

## Output

Pass / Fail with one line per failed check. Severity: ERROR (blocks load), WARNING (loads but suboptimal), INFO (hygiene suggestion).

## Compared to `hooks/`

- `hooks/` validate ONE file per Write — fast, narrow.
- `validate_pbip.py` validates the WHOLE project — slower, comprehensive.

Use hooks for the inner loop, `validate_pbip.py` before commit / before opening Desktop.
