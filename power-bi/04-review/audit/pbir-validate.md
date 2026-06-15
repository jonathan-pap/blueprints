# `pbir validate` — interpreting its output

> `pbir validate <project>.Report` is the standard schema check after any `report/` mutation. It produces a structured findings table. **Not every error is a real error** — the CLI's bundled schemas lag behind Desktop's current versions, so some flags are cosmetic.

## Run

```bash
pbir validate "<project>.Report"
```

Encoding flags for Windows (the CLI's `--help` and validation output crash on cp1252):

```bash
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 COLUMNS=400 pbir validate "<project>.Report"
```

## Telling real errors from CLI lag

`pbir` (v0.9.19 **through at least 0.9.21** — upgrading does **not** fix it) ships bundled JSON schemas that are one version behind Desktop. Desktop currently writes:

- `report/3.3.0` (report.json)
- `pagesMetadata/1.1.0` (pages.json)
- `visualContainer/2.9.0` (visual.json)

`pbir`'s bundled validator expects `3.2.0` / `1.0.0` and has no local `2.9.0`. Consequences:

| Symptom | Reality |
| --- | --- |
| `Report > report.json` → `SCHEMA_ERROR` ($schema "was expected") | Cosmetic — appears on every Desktop-authored report including pristine backups |
| `Report > pages.json` → `SCHEMA_ERROR` | Same — cosmetic |
| Any 2.9.0 visual → `SCHEMA_DEGRADED` (validated against bundled fallback) | Cosmetic — visual is fine |
| `queryState.sortDefinition` → "Additional properties not allowed / 'projections' is required" | **False positive** — Desktop accepts this; omit only if you want a clean pbir run |
| `visualContainerObjects` at root → `SCHEMA_ERROR` cascade | **Real** — Desktop also rejects this. See `../../02-build/report/schema-patterns/visual-json-structure.md` |

## ⚠️ The lag can FATALLY BLOCK writes — not just colour `validate` output

The same version mismatch that is *cosmetic* for `validate` is **fatal** for write operations. When
Desktop has bumped `pages.json` to `pagesMetadata/1.1.0`, **`pbir add page` / `add visual` refuse to
run** because they re-validate `pages.json` against the bundled `1.0.0` schema before writing:

```text
Error: Schema validation failed for 'pagesMetadata': $schema: Declared schema 'pagesMetadata'
version '1.1.0' is not available locally; ... '.../pagesMetadata/1.0.0/schema.json' was expected
```

There is **no `--force` / `--no-validate` flag**, and **upgrading pbir does not help** (0.9.21 still
bundles 1.0.0). `add page` is also **not atomic** — it can create the page folder before failing on the
`pages.json` write, leaving an orphan.

**Workaround — pin the declared schema down to the bundled version, build, let Desktop re-bump:**

```bash
# 1. pin pages.json $schema to what pbir bundles (1.1.0 -> 1.0.0)
#    (1.0.0 is a strict subset; Desktop re-bumps it to 1.1.0 on next open/save)
# edit <project>.Report/definition/pages/pages.json: pagesMetadata/1.1.0  ->  /1.0.0
# 2. run your pbir add page / add visual commands (they now write)
# 3. optional: leave it at 1.0.0 (stays pbir-editable) OR restore 1.1.0 for fidelity
```

`report.json` (`report/3.3.0`) and `visual.json` (`visualContainer/2.9.0`) lag too, but those are only
*read* during `add visual`, so they don't block — only `pages.json`, which every `add page` rewrites,
does. Revert the pin any time with `git checkout -- <...>/pages.json`.

## Validate against a backup to discriminate

Take a known-good Desktop-saved backup, run `pbir validate` on it, capture the baseline:

```bash
pbir validate "<project>.Report.bak" 2>&1 | tee baseline.txt
pbir validate "<project>.Report"     2>&1 | tee current.txt
diff baseline.txt current.txt
```

Anything that ALSO appears in `baseline.txt` is pbir-version lag, not your defect. Only errors that are NEW in `current.txt` are real.

A clean baseline still shows the standard 2 `SCHEMA_ERROR` + 2 `SCHEMA_DEGRADED` floor — that's the expected steady state for a 2026-vintage Desktop-authored report.

## Real errors that DO matter

These warrant a fix:

- `Additional property 'visualContainerObjects' was included in the root property` — structural placement bug. See `../../02-build/report/schema-patterns/visual-json-structure.md`.
- `Column 'X' in table 'Y' cannot be found` — binding to a non-existent field. Run canonical-name check (`pbir model -d`).
- `Visual name 'X' does not match required pattern` — `name` field has invalid chars (must be word-chars + hyphens only).
- `Page name 'X' contains spaces` — page folder must be kebab-case.

## See also

- `quick-checks.md` — fast pre-audit sanity tests
- `full-report.md` — structured audit findings (separate run, not the same as `validate`)
- `../hooks/validate-pbir.sh` — PostToolUse hook that runs validate after each `report/` edit
- `../../02-build/report/schema-patterns/visual-json-structure.md` — root JSON layout (where `visualContainerObjects` actually goes)
