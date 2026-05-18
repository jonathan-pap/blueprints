# DAX012 — Use ALLEXCEPT instead of ALL and VALUES restoration

When clearing filter context with ALL() and then restoring specific columns via VALUES(), ALLEXCEPT achieves the same in one operation.

## Anti-pattern

```dax
CALCULATE([Total Sales], ALL('Sales'), VALUES('Sales'[Region]))
```

## Preferred

```dax
CALCULATE([Total Sales], ALLEXCEPT('Sales', 'Sales'[Region]))
```

## Important nuance

Only valid when `'Sales'[Region]` is actively filtered. Without it:

- `VALUES` returns all regions (no-op restore)
- `ALLEXCEPT` still clears other filters

The two forms are **not equivalent** when Region is unfiltered — `ALL + VALUES` is required.

## Signal

`ALL(table), VALUES(table[col])` in same CALCULATE.
