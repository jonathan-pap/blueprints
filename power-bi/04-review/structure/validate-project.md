# Validate the full PBIP project

Run before opening in Power BI Desktop. Catches issues that would break the load.

## Script

```bash
python ../scripts/validate_pbip.py "<project>"
```

**Point it at the `.pbip` file, not the folder, when a project holds more than one.** Given a
directory it picks the first `.pbip` alphabetically and warns `multiple_pbip` — so a folder
holding `demo.pbip` alongside a `demo-v1.pbip` backup silently validates the backup, and its
errors look like they belong to the live project:

```bash
python ../scripts/validate_pbip.py "projects/demo/demo.pbip"      # unambiguous
```

The same applies to `--fix-schema`: aimed at the folder it repairs the wrong project's
`definition.pbir` / `definition.pbism`. It does not accept a path to the `.pbism` itself.

## Two bugs fixed 2026-08-26 — if you see them again, this is why

Both made a **clean** report come back as `ERR [pbir_cli_reported_errors]`, and they stacked, so
the first hid the second.

1. **`pbir validate --quiet` does not exist** (0.9.25). pbir exited 2 on every single run, and
   any exit code outside `(0, 1)` is reported as errors. The flag is gone from the call.
2. **Windows console encoding.** `subprocess.run(..., text=True)` with no `encoding` decodes with
   the console codepage — cp1252 by default — and dies on the `✓` pbir prints. The reader thread
   raises `UnicodeDecodeError`, `subprocess` still returns, but with **empty output**, so the
   error message explaining bug 1 was invisible. Printing the report then failed the same way in
   reverse (`UnicodeEncodeError`) *after* every check had run. Fixed with an explicit
   `encoding="utf-8", errors="replace"` on the call and `sys.stdout.reconfigure(...)` in `main()`.

Lesson worth keeping: a wrapper that turns a subprocess's exit code into an error **must** show
that subprocess's output, and must decode it explicitly. Silent capture plus a non-zero exit is
indistinguishable from a genuine failure.

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
