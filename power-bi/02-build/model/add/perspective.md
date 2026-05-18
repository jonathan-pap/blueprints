# Add a perspective (TMDL)

A named subset of model objects shown to a specific audience. File: `<project>.SemanticModel/definition/perspectives/<Name>.tmdl`.

## Pattern

```tmdl
perspective 'Executive View'

    perspectiveTable 'Sales'

        perspectiveMeasure 'Total Revenue'
        perspectiveMeasure 'Total Margin'
        perspectiveColumn 'Region'
        perspectiveColumn 'Year'

    perspectiveTable 'Customers'

        perspectiveColumn 'Key Account Name'
```

## Rules

- One `perspective` per file.
- List only the objects that should appear; everything else is hidden.
- `perspectiveTable` contains `perspectiveMeasure`, `perspectiveColumn`, `perspectiveHierarchy` children.
- Empty `perspectiveTable` means "include the table itself but no members" (unusual).

## When to use perspectives vs roles

- **Perspective** — hides for clarity. Users can still query hidden objects via DAX if they know the names. No security.
- **Role** (OLS) — hides for security. Hidden objects cannot be queried at all.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. In Desktop, Connect dialog → choose perspective.
