# Hierarchy — CRUD

A user-facing drill path made of `Level` objects, each pointing at a column.

## Create

```powershell
$h = New-Object Microsoft.AnalysisServices.Tabular.Hierarchy
$h.Name = "Calendar"

$l1 = New-Object Microsoft.AnalysisServices.Tabular.Level
$l1.Name = "Year";    $l1.Ordinal = 0; $l1.Column = $model.Tables["Date"].Columns["Year"]
$h.Levels.Add($l1)

$l2 = New-Object Microsoft.AnalysisServices.Tabular.Level
$l2.Name = "Quarter"; $l2.Ordinal = 1; $l2.Column = $model.Tables["Date"].Columns["Quarter"]
$h.Levels.Add($l2)

$l3 = New-Object Microsoft.AnalysisServices.Tabular.Level
$l3.Name = "Month";   $l3.Ordinal = 2; $l3.Column = $model.Tables["Date"].Columns["Month"]
$h.Levels.Add($l3)

$model.Tables["Date"].Hierarchies.Add($h)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["Date"].Hierarchies["Calendar"].Levels | Sort-Object Ordinal
```

## Update — add a level

```powershell
$h = $model.Tables["Date"].Hierarchies["Calendar"]
$l4 = New-Object Microsoft.AnalysisServices.Tabular.Level
$l4.Name = "Day"; $l4.Ordinal = 3; $l4.Column = $model.Tables["Date"].Columns["Day"]
$h.Levels.Add($l4)
$model.SaveChanges()
```

## Delete

```powershell
$model.Tables["Date"].Hierarchies.Remove($h)
$model.SaveChanges()
```
