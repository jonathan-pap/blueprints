# Sub-room — Model (TMDL)

> Edit `<project>.SemanticModel/definition/` TMDL files directly on disk. **No live connection.** For live edits prefer `../../03-bind/via-mcp/` (preferred) or `../../03-bind/via-powershell/` (alternative).

## When to edit TMDL directly

- Working in a Git branch without PBI Desktop open.
- No Power BI MCP available and no PowerShell to TOM.
- Quick text fixes: descriptions, format strings, display folders, `summarizeBy`.
- Rename cascades (cross-cutting — see `../report/pbip-format/rename-table.md` for the file list).

## Workflow router

- **Add a measure** → `add/measure.md`
- **Add a column** (DataColumn or calculated) → `add/column.md` or `add/calculated-column.md`
- **Add a table** (M-sourced or calculated) → `add/table-m.md` or `add/table-calculated.md`
- **Add a relationship** → `add/relationship.md`
- **Add a hierarchy** → `add/hierarchy.md`
- **Add a role / RLS filter** → `add/role.md`
- **Update a property** (formatString, summarizeBy, displayFolder, description) → `update/property.md`
- **Fix a common bug pattern** → `fix-pattern/_index.md` then specific pattern
- **Look up valid property values for any object** → `object-types/_index.md`
- **Rename anything** (table / measure / column) → leave this room and use `../report/pbip-format/rename-<thing>.md` — cascade touches both `.SemanticModel/` AND `.Report/`
- **Standardize naming conventions** (audit + apply consistent names) → `naming/_index.md`
- **Write / fix / optimize Power Query M** (partition expressions, query folding, validation) → `power-query/_index.md`
- **Optimize DAX performance** (slow measures, trace diagnostics, pattern catalog) → `dax/_index.md`

## Critical TMDL rules (apply always)

- `///` sets `Description` on the **next** declaration. No blank line between. `//` is a plain comment.
- **Tabs only.** Indentation = nesting depth. Multi-line DAX is **2 levels deeper than its enclosing declaration**.
- Single-quote names that contain spaces, dots, `=`, `:`, parens, currency, or start with a digit. Otherwise unquoted.
- **`lineageTag` is a GUID — never edit existing values.** Generate new ones only for new objects.
- **`PBI_FormatHint` is auto-managed by Power BI.** Leave it alone; it returns after deletion.
- **Named expressions and tables share a namespace.** `expression Sales` and `table Sales` collide. Suffix M expressions with `" Query"` (e.g. `Sales Query`).

## Validation

After every TMDL edit:

```bash
bash ../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"
```

If you don't have the hook installed, run the Python validator:

```bash
python ../../04-review/scripts/validate_pbip.py "<project>"
```

## Examples

`examples/SpaceParts.SemanticModel/` — full real-world model (40 tables, 152 measures, 8 calculation groups, 8 RLS roles). Use as a structural reference; do not edit in place.
