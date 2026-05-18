# Expression (named M / parameter) — CRUD

A `NamedExpression` is a top-level M definition: parameters and shared query fragments. Lives in `expressions.tmdl` on disk.

## Create (parameter)

```powershell
$e = New-Object Microsoft.AnalysisServices.Tabular.NamedExpression
$e.Name       = "EnvName"
$e.Kind       = [Microsoft.AnalysisServices.Tabular.ExpressionKind]::M
$e.Expression = '"prod" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
$model.Expressions.Add($e)
$model.SaveChanges()
```

## Create (shared M query)

```powershell
$e = New-Object Microsoft.AnalysisServices.Tabular.NamedExpression
$e.Name = "Server Query"
$e.Kind = "M"
$e.Expression = 'let Source = Sql.Database(EnvName, "db") in Source'
$model.Expressions.Add($e)
$model.SaveChanges()
```

## Read

```powershell
$model.Expressions | Select-Object Name, Kind
$model.Expressions["EnvName"].Expression
```

## Update

```powershell
$model.Expressions["EnvName"].Expression = '"staging" meta [IsParameterQuery=true, Type="Text"]'
$model.SaveChanges()
```

## Delete

```powershell
$model.Expressions.Remove($model.Expressions["EnvName"])
$model.SaveChanges()
```

## Namespace collision

Named expressions and tables **share a namespace**. `expression Sales` and `table Sales` collide and PBI Desktop fails the load. Suffix M expressions with ` Query` or ` Source`:

```powershell
$e.Name = "Sales Query"
# Then partitions reference it via: source = #"Sales Query"
```
