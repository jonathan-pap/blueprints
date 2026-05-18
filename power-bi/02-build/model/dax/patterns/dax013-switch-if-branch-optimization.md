# DAX013 — SWITCH/IF branch optimization in SUMMARIZECOLUMNS

SWITCH/IF inside SUMMARIZECOLUMNS enables branch optimization — the engine evaluates only the matching branch. When this fails, it materializes a full cartesian product.

## Three things break it

### 1. Multiple aggregations in one branch

Merge into a single SUMX:

```dax
SUMX('Sales', 'Sales'[SalesAmount] - 'Sales'[TotalCost])
```

### 2. Mismatched data types across branches

An implicit cast breaks the optimization. Use explicit conversion:

```dax
CONVERT(SUM('Sales'[OrderQuantity]), CURRENCY)
```

### 3. Context transition inside a branch iterator

A measure reference that requires a context transition (e.g., `SUMX(Sales, 'Sales'[Quantity] * [selection])`) forces a full crossjoin.

If the measure is context-independent, cache it before the iterator:

```dax
VAR _UnitDiscount = [Unit Discount]
RETURN SUMX('Sales', 'Sales'[Quantity] * _UnitDiscount)
```

## Signal

`SWITCH` or `IF` as primary expression body in measure.
