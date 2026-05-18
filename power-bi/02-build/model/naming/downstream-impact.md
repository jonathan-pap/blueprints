# Downstream report impact (warning)

**Renaming model objects breaks downstream report visuals that reference those fields.**

## Before you rename

Always warn the user. If downstream reports exist:

1. **Make a backup** of the model before changes (`cp -r <project>.SemanticModel <project>.SemanticModel.backup`).
2. **Plan a rebinding session** for the report side.
3. **Consider batching with a Tabular Editor C# script** that renames + rebinds atomically (avoids the visual-by-visual fix).

## Find downstream reports first

For per-project reports (in this workspace's `projects/`):

```bash
# Every visual that references the renamed measure
pbir fields find "<project>.Report" -f "<Table>.Old Name"
```

For cross-workspace impact (Fabric):

- Run `../../../04-review/lineage/downstream-reports.md` to list every report bound to the model across the tenant.

## After renaming model objects

The report side must also be updated. Use the rename-cascade files in the report room:

- `../../report/pbip-format/rename-measure.md`
- `../../report/pbip-format/rename-column.md`
- `../../report/pbip-format/rename-table.md`
- `../../report/pbip-format/post-rename-checklist.md`

These cover every file location: TMDL, visual JSON, report extensions, cultures, DAX queries, and embedded SparklineData selectors that grep can miss.

## What breaks if you forget

- Visuals show "broken field" indicators in Power BI Desktop.
- Bookmarks targeting the old field stop working.
- Conditional formatting expressions error out.
- DAX queries saved in `DAXQueries/` fail at runtime.
- Report extension measures (thin-report measures) referencing the old name fail.

## After both sides updated

Validate everything:

```bash
pbir validate "<project>.Report" --all
python ../../../04-review/scripts/validate_pbip.py "<project>"
```

Then reopen in Power BI Desktop to confirm no broken-visual badges remain.
