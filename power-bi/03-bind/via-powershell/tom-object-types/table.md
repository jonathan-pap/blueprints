# Table — CRUD

## Create

```powershell
$table = New-Object Microsoft.AnalysisServices.Tabular.Table
$table.Name        = "NewTable"
$table.Description = "Fact table for orders"

# Columns must be explicit — see gotchas.md
$c1 = New-Object Microsoft.AnalysisServices.Tabular.DataColumn
$c1.Name = "OrderID"; $c1.DataType = "Int64"; $c1.SourceColumn = "OrderID"
$table.Columns.Add($c1)

# M partition
$p = New-Object Microsoft.AnalysisServices.Tabular.Partition
$p.Name   = "NewTable-Partition"
$p.Source = New-Object Microsoft.AnalysisServices.Tabular.MPartitionSource
$p.Source.Expression = 'let Source = Sql.Database("srv","db"), Orders = Source{[Schema="dbo",Item="Orders"]}[Data] in Orders'
$table.Partitions.Add($p)

$model.Tables.Add($table)
$model.SaveChanges()
```

After save, the table has metadata only — no data. Refresh to populate VertiPaq:

```powershell
$model.Tables["NewTable"].RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Full)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["NewTable"]                     # by name
$model.Tables | Where-Object { $_.IsHidden }  # filter
```

## Update

```powershell
$table = $model.Tables["NewTable"]
$table.Description = "Updated description"
$table.IsHidden    = $true
$model.SaveChanges()
```

## Delete

```powershell
$model.Tables.Remove($model.Tables["NewTable"])
$model.SaveChanges()
```
