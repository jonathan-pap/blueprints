# PBIP validator — full diagnostic flow

Run when validating a PBIP project, checking rename completeness, or diagnosing "won't open in Desktop" errors. Prefers deterministic tools; falls back to manual walking only for classes of issues the tools don't cover.

## Step 0 — Tool discovery

```bash
which pbir                                                   # confirm pbir-cli on PATH
ls ../scripts/validate_pbip.py                               # locate the project validator
```

If either is missing, note in the report and fall back to Read / Grep for what they'd have covered.

## Step 1 — Project validator (covers cross-cutting structure)

```bash
python ../scripts/validate_pbip.py <project>
```

Accepts a `.pbip` file, `.Report/` / `.SemanticModel/` directory, or a project root. Covers:

- `.pbip` root file and `artifacts[].report.path` resolution.
- `.platform` files: presence, JSON validity, `metadata.type`, GUID `logicalId`.
- `definition.pbir`: `version`, `datasetReference` (`byPath` target resolves, `byConnection` has a `connectionString`).
- `.SemanticModel/` format detection: TMDL vs legacy TMSL, mutually exclusive.
- **Theme resource resolution.** `resourcePackages[]` items must exist on disk. Missing file is a common silent blocker.
- **Page name regex.** Names outside `^[\w-]+$` are silently ignored by Desktop.
- **Orphan page folders.** Folders present on disk but not in `pages.json.pageOrder`.
- **M-expression vs table namespace collision.** ERROR if both share a name.

Exit codes: `0` clean, `1` warnings only, `2` errors, `3` usage error.

## Step 2 — Delegate report validation to `pbir validate`

For each `.Report/` folder:

```bash
pbir validate <Report.Report> --all
```

Covers JSON syntax, Microsoft schema compliance, required fields, PBIR folder structure, visual / page / bookmark name rules, field references against the connected model. **Do not re-walk manually** — use the output verbatim.

Flag reference:

- `--qa` — adds overlap / hidden-visual / filter sanity checks
- `--fields` — validate field refs against connected model
- `--strict` — promote warnings to errors
- `--all` — schema + fields + qa (best default for diagnostics)

## Step 3 — Manual TMDL pass (only what the tools don't cover)

`validate_pbip.py` handles presence checks and namespace collision. You handle:

- `model.tmdl` has `ref table` entries for every file in `tables/`.
- Each `tables/*.tmdl`:
  - Table declaration matches filename (minus `.tmdl`). Spaces allowed.
  - Partition name matches table name for M partitions.
  - Indentation is **tabs only**.
  - `///` description annotations immediately precede their declaration.
  - `formatString` and `summarizeBy` values are valid.
  - DAX in measures / calculated columns has balanced quotes and parentheses.
- `relationships.tmdl`: every referenced table / column exists.
- `cultures/*.tmdl`: `ConceptualEntity` refs match table names.

## Step 4 — Rename-cascade verification (only if asked)

Grep for the old name across every place it could appear:

```bash
PROJ="<project>"; OLD="\[Old Name\]"
grep -rn "$OLD" "$PROJ.Report/" "$PROJ.SemanticModel/"
grep -rn "$OLD" "$PROJ.SemanticModel/DAXQueries/" "$PROJ.Report/DAXQueries/" 2>/dev/null
```

Catches `SparklineData` selector strings, both `DAXQueries/` locations, and embedded references that structured walkers miss.

## Output

Report findings with exact file paths and specific remediation. Apply fixes only when unambiguous and reversible — for everything else, list and let the user choose.

If the user wants the report saved: `../../outputs/$(date +%Y-%m-%d)-<project>-validation.md`.

## Source / see also

- Pattern source: upstream `_examples/pbip/agents/pbip-validator.agent.md`
- The atomic counterparts: `../structure/validate-project.md`, `../structure/post-rename.md`
