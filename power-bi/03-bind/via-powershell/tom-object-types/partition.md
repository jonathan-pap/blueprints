# Partition — CRUD

A partition is the source query for a table. Most tables have one M partition; calculated tables have a `CalculatedPartitionSource`.

## Create (M partition)

```powershell
$p = New-Object Microsoft.AnalysisServices.Tabular.Partition
$p.Name   = "Sales-Q1"
$p.Source = New-Object Microsoft.AnalysisServices.Tabular.MPartitionSource
$p.Source.Expression = @'
let
    Source = Sql.Database("srv","db"),
    Sales  = Source{[Schema="dbo",Item="Sales"]}[Data],
    Q1     = Table.SelectRows(Sales, each [OrderDate] >= #date(2026,1,1) and [OrderDate] < #date(2026,4,1))
in
    Q1
'@
$model.Tables["Sales"].Partitions.Add($p)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["Sales"].Partitions | Select-Object Name, Mode
$model.Tables["Sales"].Partitions[0].Source.Expression
```

## Update

```powershell
$p = $model.Tables["Sales"].Partitions["Sales-Q1"]
$p.Source.Expression = "<new M expression>"
$model.SaveChanges()
```

## Delete

```powershell
$model.Tables["Sales"].Partitions.Remove($p)
$model.SaveChanges()
```

## Refresh

```powershell
$p.RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Full)
$model.SaveChanges()
```

## Mode enum

`Import`, `DirectQuery`, `Default`, `Push`, `Dual`, `DirectLake`.
