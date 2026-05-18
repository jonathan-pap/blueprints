# Add a calculated column (TMDL)

A column whose value comes from a DAX expression, not from a source query.

## Pattern

```tmdl
column 'Year'
    type: calculated
    dataType: int64
    isDataTypeInferred
    displayFolder: 1. Dates
    lineageTag: <generate-new-guid>
    summarizeBy: none
    expression: YEAR('Sales'[OrderDate])
```

## Multi-line DAX

```tmdl
column 'Order Status'
    type: calculated
    dataType: string
    isDataTypeInferred
    lineageTag: <guid>
    summarizeBy: none
    expression =
            SWITCH(
                TRUE(),
                'Sales'[Shipped] = TRUE,         "Shipped",
                'Sales'[OrderDate] < TODAY()-7,  "Late",
                                                 "Pending"
            )
```

## Differences from a regular column

- `type: calculated` — required (default is `data`).
- `expression:` instead of `sourceColumn:` — no source query, DAX produces values.
- `isDataTypeInferred` — common; lets the engine infer from the expression result.

## Recompute

Calculated columns recompute when:
- The table is refreshed.
- A `calculate`-type refresh is triggered (no source query, just recalc).

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
