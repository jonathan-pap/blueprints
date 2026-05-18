# Add a role (RLS / OLS, TMDL)

Each role gets its own file in `<project>.SemanticModel/definition/roles/<RoleName>.tmdl`.

## RLS pattern (row-level security)

```tmdl
role 'Sales Managers'
    modelPermission: read

    tablePermission 'Customers' = [Region] = USERPRINCIPALNAME()
```

The filter expression after `=` is DAX, evaluated per query against the user's identity.

## RLS with dynamic membership

```tmdl
role 'Account Managers'
    modelPermission: read

    tablePermission 'Customers' =
            VAR _user = USERPRINCIPALNAME()
            VAR _regions = CALCULATETABLE(
                VALUES('UserRegion'[Region]),
                'UserRegion'[UserPrincipalName] = _user
            )
            RETURN
                [Region] IN _regions
```

## OLS pattern (object-level security — column hide)

```tmdl
role 'No Salary'
    modelPermission: read

    tablePermission 'Employees'
        columnPermission 'Salary' = none
        columnPermission 'Bonus'  = none
```

## modelPermission values

`none`, `read`, `readRefresh`, `refresh`, `administrator`.

## Adding members

External-identity members (Entra ID users / groups) are usually managed at the workspace level in Fabric / Power BI Service, NOT in the TMDL file. For testing locally:

```tmdl
role 'Sales Managers'
    modelPermission: read

    member 'CONTOSO\sales-managers@contoso.com'
        memberType: user

    tablePermission 'Customers' = [Region] = USERPRINCIPALNAME()
```

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Test in Desktop with "View as" → pick role.
