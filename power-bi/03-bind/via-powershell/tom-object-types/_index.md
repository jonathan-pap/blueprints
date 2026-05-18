# tom-object-types/ — atomic files

> Per-object-type CRUD via TOM. All examples assume `$model` is connected (see `../quickstart.md`). Each file ≤ 60 lines.

## Cross-cutting

- `gotchas.md` — RowNumberColumn, table-creation column rule, relationship-to-new-table batch rule

## Objects

- `table.md`
- `column.md` (DataColumn — the common case)
- `calculated-column.md`
- `calculated-table.md`
- `measure.md`
- `relationship.md`
- `hierarchy.md`
- `partition.md`
- `role.md` (RLS / OLS)
- `perspective.md`
- `culture.md`
- `annotation.md`
- `expression.md` (named M / parameters)
- `data-source.md`

## Discover unknown properties

For object types or properties not covered here, use reflection rather than guessing:

```powershell
[Microsoft.AnalysisServices.Tabular.Table].GetProperties() |
  Where-Object { $_.CanWrite } |
  ForEach-Object { "$($_.Name) : $($_.PropertyType.Name)" }
```

External reference: [Microsoft.AnalysisServices.Tabular namespace docs](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular).
