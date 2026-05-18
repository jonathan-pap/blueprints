# DAX011 — Distinct count alternatives

Depending on cardinality and data layout, moving DISTINCTCOUNT to SUMX(VALUES(), 1) can improve performance by forcing FE evaluation.

## Storage Engine bound (default)

```dax
DISTINCTCOUNT('Sales'[CustomerKey])
```

## Formula Engine bound (sometimes faster)

```dax
SUMX(VALUES('Sales'[CustomerKey]), 1)
```

## When to use which

- Low-to-mid cardinality column, SE has plenty of headroom → DISTINCTCOUNT is fine
- High-cardinality column where SE scan dominates → SUMX(VALUES(...), 1) shifts work to FE, which may parallelize better in conjunction with other measures

Always test both. The decision is data-shape-dependent.

## Signal

`DISTINCTCOUNT` in measure expression. Look for high SE Duration on a SUM-friendly aggregation.

## See also

- `dax014-countrows-not-distinctcount.md` — when DISTINCTCOUNT is on a key column
