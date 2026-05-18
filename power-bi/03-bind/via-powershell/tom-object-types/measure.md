# Measure — CRUD

## Create

```powershell
$m = New-Object Microsoft.AnalysisServices.Tabular.Measure
$m.Name          = "Total Revenue"
$m.Expression    = "SUM('Sales'[Amount])"
$m.FormatString  = "#,##0"
$m.DisplayFolder = "1. Revenue"
$m.Description   = "Sum of Sales[Amount] in current filter context"
$model.Tables["Sales"].Measures.Add($m)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["Sales"].Measures["Total Revenue"]
$model.Tables.SelectMany({ $_.Measures }) | Sort-Object Name   # all measures
```

## Update

```powershell
$m = $model.Tables["Sales"].Measures["Total Revenue"]
$m.Expression   = "SUMX('Sales', 'Sales'[Qty] * 'Sales'[Price])"
$m.FormatString = "#,##0.00"
$model.SaveChanges()
```

## Delete

```powershell
$t = $model.Tables["Sales"]
$t.Measures.Remove($t.Measures["Total Revenue"])
$model.SaveChanges()
```

## Dynamic format strings

For format computed by DAX (often via a calculation group):

```powershell
$m.FormatStringDefinition = New-Object Microsoft.AnalysisServices.Tabular.FormatStringDefinition
$m.FormatStringDefinition.Expression = 'IF([Variance] < 0, "-#,##0;0", "+#,##0;0")'
# When FormatStringDefinition is set, FormatString is ignored.
```
