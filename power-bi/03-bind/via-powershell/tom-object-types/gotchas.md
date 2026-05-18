# TOM gotchas (read once)

Three cross-cutting pitfalls that bite most TOM scripts.

## 1. RowNumberColumn is internal

Every table has a hidden `RowNumberColumn` auto-created by VertiPaq. Cannot create / modify / delete it.

```powershell
# Always filter it out when enumerating
$userColumns = $table.Columns |
  Where-Object { $_ -isnot [Microsoft.AnalysisServices.Tabular.RowNumberColumn] }
```

## 2. Table creation requires explicit columns

PBI Desktop's TOM does NOT auto-discover columns from M expressions (Tabular Editor UI does, TOM via PBI Desktop does not). Define every column explicitly with a `SourceColumn` matching the M output:

```powershell
$col = New-Object Microsoft.AnalysisServices.Tabular.DataColumn
$col.Name         = "Order Date"
$col.DataType     = [Microsoft.AnalysisServices.Tabular.DataType]::DateTime
$col.SourceColumn = "Order Date"   # must match the M expression output exactly
$table.Columns.Add($col)
```

## 3. Relationships to newly-created tables — batch them

Reference the column **object**, not a name lookup. Add the table and relationship in the same `SaveChanges()`:

```powershell
$col = New-Object Microsoft.AnalysisServices.Tabular.DataColumn
$col.Name = "CustomerID"; $col.DataType = "Int64"; $col.SourceColumn = "CustomerID"
$newTable.Columns.Add($col)

$rel = New-Object Microsoft.AnalysisServices.Tabular.SingleColumnRelationship
$rel.FromColumn = $col                                              # the object
$rel.ToColumn   = $model.Tables["Customers"].Columns["CustomerID"]

$model.Tables.Add($newTable)
$model.Relationships.Add($rel)
$model.SaveChanges()                                                # one batch
```

Looking up the column by name BEFORE save fails with "invalid table ID 0" — server hasn't assigned internal IDs yet.
