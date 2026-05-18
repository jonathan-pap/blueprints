# Audit workflow (5 phases)

End-to-end procedure for standardizing names in a TMDL-based semantic model.

## Phase 1 — Discover the model

Locate the TMDL files. Ask the user for the path to `.SemanticModel/definition/` if not obvious.

```bash
ls "<project>.SemanticModel/definition/tables/"*.tmdl
```

Read all table TMDL files to build a complete picture. Look at:

- Table names (technical prefixes? `DIM_`, `FACT_`, `STG_`?)
- Measure names (abbreviations? CamelCase? snake_case? inconsistent unit/period syntax?)
- Column names (programming conventions?)
- Display folder structure (organized? numbered?)
- Presence of `///` descriptions

## Phase 2 — Understand business context (CRITICAL)

**Do not rename anything without business context.** Use `AskUserQuestion` per `core-principle.md`.

## Phase 3 — Audit and report

Produce a markdown table BEFORE making changes:

```markdown
| Object Type | Current Name   | Proposed Name | Issues Found              |
|-------------|----------------|---------------|---------------------------|
| Table       | FACT_Invoices  | Invoices      | Technical prefix          |
| Measure     | NetSls         | Net Sales     | CamelCase, abbreviation   |
| Column      | shp_dt         | Ship Date     | snake_case, abbreviation  |
```

Group findings by issue type. Ask the user to confirm or adjust before proceeding.

## Phase 4 — Apply changes

For each table file:

1. Rename the table (if needed).
2. Rename measures — and update ALL internal DAX references in `[Old Name]` → `[New Name]` across every table file in the model.
3. Rename columns — update `'Table'[Old Column]` → `'Table'[New Column]` everywhere.
4. Reorganize `displayFolder:` properties.
5. Add `///` descriptions to measures and columns that lack them.
6. Update `relationships.tmdl` for renamed tables/columns.

**Cross-file updates are critical.** Grep before sed:

```bash
grep -rn "OldName" "<project>.SemanticModel/definition/"
```

## Phase 5 — Validate

After applying changes:

1. All TMDL files parse correctly (`pbir validate "<project>.Report"`).
2. No orphaned references to old names anywhere in `definition/`.
3. Display folders consistent across tables.
4. Descriptions present on all visible measures and columns.

Final grep to catch any miss:

```bash
grep -rn "old_pattern" "<project>.SemanticModel/definition/"
```

## Downstream

After model-side renames complete, follow `../../report/pbip-format/rename-measure.md` / `rename-column.md` / `rename-table.md` for the report-side cascade. See `downstream-impact.md` for the full warning.
