# Column (DataColumn) — CRUD

## Create

```powershell
$col = New-Object Microsoft.AnalysisServices.Tabular.DataColumn
$col.Name         = "OrderDate"
$col.DataType     = [Microsoft.AnalysisServices.Tabular.DataType]::DateTime
$col.SourceColumn = "OrderDate"       # must match M output exactly
$col.DisplayFolder= "1. Dates"
$col.SummarizeBy  = "None"
$model.Tables["Sales"].Columns.Add($col)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["Sales"].Columns["OrderDate"]
$model.Tables["Sales"].Columns | Where-Object { -not $_.IsHidden }
```

## Update

```powershell
$col = $model.Tables["Sales"].Columns["OrderDate"]
$col.SummarizeBy = "None"
$col.IsHidden    = $false
$col.FormatString = "yyyy-MM-dd"
$model.SaveChanges()
```

## Delete

```powershell
$t = $model.Tables["Sales"]
$t.Columns.Remove($t.Columns["OrderDate"])
$model.SaveChanges()
```

## DataType enum values

`Int64`, `Double`, `Decimal`, `String`, `Boolean`, `DateTime`, `Binary`, `Variant`, `Automatic`, `Unknown`.

## SummarizeBy enum values

`Default`, `None`, `Sum`, `Min`, `Max`, `Count`, `Average`, `DistinctCount`.

Key/attribute columns → `None`. Additive facts → `Sum`. Rates/percentages → `None` (can't be meaningfully summed).
