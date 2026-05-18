# Perspective — CRUD

A perspective hides/shows model objects per audience without changing the model. Each perspective lists which tables/columns/measures are visible.

## Create

```powershell
$pers = New-Object Microsoft.AnalysisServices.Tabular.Perspective
$pers.Name = "Executive View"
$model.Perspectives.Add($pers)

$pt = New-Object Microsoft.AnalysisServices.Tabular.PerspectiveTable
$pt.Table = $model.Tables["Sales"]
$pers.PerspectiveTables.Add($pt)

$pm = New-Object Microsoft.AnalysisServices.Tabular.PerspectiveMeasure
$pm.Measure = $model.Tables["Sales"].Measures["Total Revenue"]
$pt.PerspectiveMeasures.Add($pm)

$model.SaveChanges()
```

## Read

```powershell
$model.Perspectives | ForEach-Object {
  "$($_.Name): " + ($_.PerspectiveTables | ForEach-Object { $_.Table.Name }) -join ", "
}
```

## Update — add a column to the perspective

```powershell
$pt = $model.Perspectives["Executive View"].PerspectiveTables["Sales"]
$pc = New-Object Microsoft.AnalysisServices.Tabular.PerspectiveColumn
$pc.Column = $model.Tables["Sales"].Columns["Region"]
$pt.PerspectiveColumns.Add($pc)
$model.SaveChanges()
```

## Delete

```powershell
$model.Perspectives.Remove($model.Perspectives["Executive View"])
$model.SaveChanges()
```
