# Role properties (RLS / OLS)

## Required

- Role name (after `role`)
- `modelPermission` — `none`, `read`, `readRefresh`, `refresh`, `administrator`

## RLS (row-level security)

Add a `tablePermission` block with a DAX `FilterExpression`:

```tmdl
role 'Sales Managers'
    modelPermission: read

    tablePermission 'Customers' = [Region] = USERPRINCIPALNAME()
```

The filter is DAX, evaluated per query.

## OLS (object-level security)

Add `columnPermission` inside a `tablePermission`. `= none` hides the column for this role:

```tmdl
role 'No Salary'
    modelPermission: read

    tablePermission 'Employees'
        columnPermission 'Salary' = none
        columnPermission 'Bonus'  = none
```

## Members

External-identity members are usually managed at the workspace level. For local testing:

```tmdl
member 'CONTOSO\user@contoso.com'
    memberType: user
```

`memberType`: `user`, `group`, `app`, `external`.

## Testing in Desktop

Modeling → "View as" → pick a role → confirm filters apply correctly.

## See also

- `../add/role.md` — full RLS / OLS authoring patterns
