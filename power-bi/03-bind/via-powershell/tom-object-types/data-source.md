# Data source — CRUD

Legacy connection definitions (provider data sources). Modern PBI uses M expressions for connections; data sources are still seen in older models.

## Create (structured)

```powershell
$ds = New-Object Microsoft.AnalysisServices.Tabular.StructuredDataSource
$ds.Name             = "SalesDB"
$ds.Description      = "Production Sales DB"
$ds.ConnectionDetails = '{"protocol":"tds","address":{"server":"srv","database":"db"}}'
$ds.Credential        = '{"AuthenticationKind":"UsernamePassword","Username":"user","EncryptConnection":true}'
$model.DataSources.Add($ds)
$model.SaveChanges()
```

## Read

```powershell
$model.DataSources | Select-Object Name, Description
```

## Update

```powershell
$ds = $model.DataSources["SalesDB"]
$ds.Description = "Read-replica"
$model.SaveChanges()
```

## Delete

```powershell
$model.DataSources.Remove($model.DataSources["SalesDB"])
$model.SaveChanges()
```

## When you see one

In modern PBIP projects, prefer named expressions (`expression.md`) over data sources. Migrate when you can.
