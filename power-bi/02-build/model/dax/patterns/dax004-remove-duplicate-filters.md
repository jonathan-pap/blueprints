# DAX004 — Remove duplicate and redundant filters

Applying the same filter condition twice — whether as duplicate CALCULATE arguments or as a variable that restates an existing predicate — causes redundant SE evaluation.

## Anti-pattern — same predicate in CALCULATE + FILTER

```dax
CALCULATE(
    SUM('Sales'[Amount]),
    'Sales'[Year] = 2023,
    FILTER('Sales', 'Sales'[Year] = 2023)
)
```

## Anti-pattern — redundant filter variable

```dax
VAR FilteredValues = CALCULATETABLE(DISTINCT('Table'[Key1]), 'Table'[Amount] > 1000)
VAR Result =
    CALCULATETABLE(
        SUMMARIZECOLUMNS('Table'[Key2], "TotalQty", SUM('Table'[Quantity])),
        'Table'[Amount] > 1000,
        'Table'[Key1] IN FilteredValues   -- redundant: already filtered by Amount > 1000
    )
```

## Preferred — single filter, no duplication

```dax
CALCULATE(SUM('Sales'[Amount]), 'Sales'[Year] = 2023)

VAR Result =
    CALCULATETABLE(
        SUMMARIZECOLUMNS('Table'[Key2], "TotalQty", SUM('Table'[Quantity])),
        'Table'[Amount] > 1000
    )
```

## Signal

Duplicate or redundant CALCULATE filter predicates.
