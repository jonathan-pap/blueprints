# DAX005 — SUMMARIZE with complex table expression

Wrap the table expression with CALCULATETABLE instead of using SUMMARIZE on a complex first argument.

## Anti-pattern

```dax
SUMMARIZE(
    CALCULATETABLE('Sales', 'Sales'[Year] = 2023, 'Sales'[CustomerKey] IN SellingPOCs),
    'Sales'[CustomerKey],
    "DistinctSKUs", DISTINCTCOUNT('Sales'[StoreKey])
)
```

## Preferred

```dax
CALCULATETABLE(
    SUMMARIZECOLUMNS(
        'Sales'[CustomerKey],
        "DistinctSKUs", DISTINCTCOUNT('Sales'[StoreKey])
    ),
    'Sales'[Year] = 2023,
    'Sales'[CustomerKey] IN SellingPOCs
)
```

## Signal

`SUMMARIZE` with complex or filtered table as first argument.
