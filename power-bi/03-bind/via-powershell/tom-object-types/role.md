# Role (RLS / OLS) — CRUD

## Create with RLS filter

```powershell
$role = New-Object Microsoft.AnalysisServices.Tabular.ModelRole
$role.Name            = "Sales Managers"
$role.ModelPermission = "Read"

$tp = New-Object Microsoft.AnalysisServices.Tabular.TablePermission
$tp.Table         = $model.Tables["Customers"]
$tp.FilterExpression = "[Region] = USERPRINCIPALNAME()"
$role.TablePermissions.Add($tp)

$model.Roles.Add($role)
$model.SaveChanges()
```

## Read

```powershell
$model.Roles | Select-Object Name, ModelPermission
$model.Roles["Sales Managers"].TablePermissions |
  ForEach-Object { "$($_.Table.Name): $($_.FilterExpression)" }
```

## Update

```powershell
$role = $model.Roles["Sales Managers"]
$role.TablePermissions["Customers"].FilterExpression = "[Region] IN VALUES('UserRegion'[Region])"
$model.SaveChanges()
```

## Add a member

```powershell
$m = New-Object Microsoft.AnalysisServices.Tabular.ExternalModelRoleMember
$m.MemberName     = "DOMAIN\user@contoso.com"
$m.MemberType     = "User"
$role.Members.Add($m)
$model.SaveChanges()
```

## Delete

```powershell
$model.Roles.Remove($model.Roles["Sales Managers"])
$model.SaveChanges()
```

## ModelPermission enum

`None`, `Read`, `ReadRefresh`, `Refresh`, `Administrator`.
