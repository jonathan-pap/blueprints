# Calculated table — CRUD

A table whose rows come from a DAX expression, not from M. Implemented as a `Table` with a `Partition` of type `CalculatedPartitionSource`.

## Create

```powershell
$table = New-Object Microsoft.AnalysisServices.Tabular.Table
$table.Name = "Date"

# Add an empty placeholder column so the table is valid pre-refresh
# (columns will be inferred from the DAX expression on first refresh)

$p = New-Object Microsoft.AnalysisServices.Tabular.Partition
$p.Name   = "Date-Partition"
$p.Source = New-Object Microsoft.AnalysisServices.Tabular.CalculatedPartitionSource
$p.Source.Expression = "CALENDAR(DATE(2020,1,1), DATE(2030,12,31))"
$table.Partitions.Add($p)

$model.Tables.Add($table)
$model.SaveChanges()

$model.Tables["Date"].RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Full)
$model.SaveChanges()
```

After refresh, the DAX expression's columns become real columns on the table.

## Read

```powershell
$model.Tables | Where-Object {
  $_.Partitions[0].Source -is [Microsoft.AnalysisServices.Tabular.CalculatedPartitionSource]
}
```

## Update expression

```powershell
$model.Tables["Date"].Partitions[0].Source.Expression = "CALENDAR(DATE(2018,1,1), DATE(2030,12,31))"
$model.Tables["Date"].RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Full)
$model.SaveChanges()
```

## Delete

```powershell
$model.Tables.Remove($model.Tables["Date"])
$model.SaveChanges()
```
