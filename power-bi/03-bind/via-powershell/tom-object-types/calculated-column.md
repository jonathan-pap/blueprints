# Calculated column — CRUD

A column whose value is computed by DAX, not loaded from source. Different class than `DataColumn`.

## Create

```powershell
$col = New-Object Microsoft.AnalysisServices.Tabular.CalculatedColumn
$col.Name        = "Year"
$col.DataType    = [Microsoft.AnalysisServices.Tabular.DataType]::Int64
$col.Expression  = "YEAR('Sales'[OrderDate])"
$col.SummarizeBy = "None"
$model.Tables["Sales"].Columns.Add($col)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["Sales"].Columns | Where-Object {
  $_ -is [Microsoft.AnalysisServices.Tabular.CalculatedColumn]
}
```

## Update expression

```powershell
$col = $model.Tables["Sales"].Columns["Year"]
$col.Expression = "YEAR('Sales'[InvoiceDate])"
$model.SaveChanges()
```

## Delete

Same as DataColumn:

```powershell
$t.Columns.Remove($t.Columns["Year"])
$model.SaveChanges()
```

## Trigger recalc

Calculated columns recompute on data refresh. Force without source query:

```powershell
$model.RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Calculate)
$model.SaveChanges()
```
