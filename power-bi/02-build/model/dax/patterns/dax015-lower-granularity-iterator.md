# DAX015 — Move calculation to lower granularity

When an iterator scans a high-cardinality table but the calculation depends on a low-cardinality attribute, iterate over the attribute instead.

## Anti-pattern

```dax
-- 100K customers but only 5 distinct DiscountRate values → 100K context transitions
SUMX('Customer', CALCULATE(SUM('Sales'[Amount])) * 'Customer'[DiscountRate])
```

## Preferred

```dax
-- 5 iterations instead of 100K
SUMX(
    VALUES('Customer'[DiscountRate]),
    CALCULATE(SUM('Sales'[Amount])) * 'Customer'[DiscountRate]
)
```

## Signal

High-cardinality iterator (many distinct rows) where the calculation uses a low-cardinality attribute (few distinct values).
