# Relationship — CRUD

## Create

```powershell
$rel = New-Object Microsoft.AnalysisServices.Tabular.SingleColumnRelationship
$rel.FromColumn = $model.Tables["Sales"].Columns["CustomerID"]
$rel.ToColumn   = $model.Tables["Customers"].Columns["CustomerID"]
$rel.FromCardinality = "Many"
$rel.ToCardinality   = "One"
$rel.CrossFilteringBehavior  = "OneDirection"
$rel.SecurityFilteringBehavior = "OneDirection"
$rel.IsActive = $true
$model.Relationships.Add($rel)
$model.SaveChanges()
```

When creating a relationship to a *newly created* table, see `gotchas.md` § 3 — batch in one `SaveChanges()` and reference the column object.

## Read

```powershell
$model.Relationships | ForEach-Object {
  "$($_.FromTable.Name)[$($_.FromColumn.Name)] → $($_.ToTable.Name)[$($_.ToColumn.Name)]  Active=$($_.IsActive)"
}
```

## Update

```powershell
$rel = $model.Relationships | Where-Object {
  $_.FromTable.Name -eq "Sales" -and $_.ToTable.Name -eq "Customers"
}
$rel.IsActive = $false
$rel.CrossFilteringBehavior = "BothDirections"
$model.SaveChanges()
```

## Delete

```powershell
$model.Relationships.Remove($rel)
$model.SaveChanges()
```

## Enum values

- `Cardinality`: `One`, `Many`, `None`
- `CrossFilteringBehavior`: `OneDirection`, `BothDirections`, `Automatic`
- `SecurityFilteringBehavior`: `OneDirection`, `BothDirections`, `None`
