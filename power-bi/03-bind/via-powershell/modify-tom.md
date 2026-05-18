# Modify the model via TOM

Mutations buffer until `SaveChanges()`. Prefer `../via-mcp/add-measure.md` etc. when MCP is available — this is the fallback / leverage path.

## Golden rules

1. **Buffer, then save.** Without `$model.SaveChanges()`, every change is silently discarded.
2. **Save once per batch.** Don't loop with `SaveChanges()` inside.
3. **Disconnect after saving.** `$server.Disconnect()` — otherwise orphan processes.
4. **No undo.** Power BI Desktop can't `Ctrl+Z` an external TOM change. Test on a backup.
5. **Never modify metadata without explicit user direction.**

## Anatomy

```powershell
# 1. Connect (see quickstart.md)
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("Data Source=localhost:<PORT>")
$model  = $server.Databases[0].Model

# 2. Mutate
$measure = New-Object Microsoft.AnalysisServices.Tabular.Measure
$measure.Name         = "Total Revenue"
$measure.Expression   = "SUM('Sales'[Amount])"
$measure.FormatString = "#,##0"
$model.Tables["Sales"].Measures.Add($measure)

# 3. Commit
$model.SaveChanges()

# 4. Disconnect
$server.Disconnect()
```

## Per-object CRUD

Every object type has its own pattern (collection name, constructor, properties). See `tom-object-types/_index.md`.

## Leverage operations

- **Field parameter** → `field-parameter.md` (calculated table + sort column + metadata in one shot)
- **Load a TMDL fragment** → `load-tmdl-files.md`
- **Add an annotation** → `annotations.md`

## Mirror to disk

If you intend the change to persist beyond the current Desktop session, also write to `<project>.SemanticModel/definition/tables/<table>.tmdl` via `../../02-build/model/` — otherwise next reload may overwrite.
