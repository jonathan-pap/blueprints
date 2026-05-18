# DAX014 — Use COUNTROWS instead of DISTINCTCOUNT on key columns

Use when the column is a primary key (one-side of a relationship).

## Anti-pattern

```dax
DISTINCTCOUNT('Product'[ProductKey])
```

## Preferred

```dax
COUNTROWS('Product')
```

## Why it works

A primary key column has one distinct value per row. DISTINCTCOUNT scans the dictionary; COUNTROWS just counts. Same result, faster.

## For non-key columns

If DISTINCTCOUNT is on a non-key column and is a bottleneck, see `dax011-distinct-count-alternatives.md` for SUMX(VALUES(), 1).

## Signal

`DISTINCTCOUNT` on a known key column.
