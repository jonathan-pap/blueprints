# DAX010 — Apply filters using CALCULATETABLE instead of FILTER

CALCULATETABLE modifies filter context directly for better query plans.

## Anti-pattern

```dax
FILTER('Sales', 'Sales'[Year] = 2023)
```

## Preferred

```dax
CALCULATETABLE('Sales', 'Sales'[Year] = 2023)
```

## Signal

SE rows far exceed final result count. FE filtering post-materialization instead of pushing to SE.
