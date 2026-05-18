# DAX018 — Replace DIVIDE with division operator in iterators

DIVIDE() includes divide-by-zero protection that forces FE callbacks inside iterators. Use the native `/` operator to keep the expression SE-native.

**Only use `/` when the denominator is guaranteed non-zero.** If zero is possible, pre-filter:

```dax
CALCULATETABLE('Items', 'Items'[LocationAdjustment] <> 0)
```

## Anti-pattern

```dax
SUMX('Fact', 'Fact'[BaseAmount] * DIVIDE(RELATED('Items'[Discount]), RELATED('Items'[LocationAdjustment])))
```

## Preferred

```dax
SUMX('Fact', 'Fact'[BaseAmount] * (RELATED('Items'[Discount]) / RELATED('Items'[LocationAdjustment])))
```

## Signal

`DIVIDE()` inside an iterator. `CallbackDataID` in xmSQL.

## When to keep DIVIDE

Outside iterators (final result expressions), DIVIDE is fine and protects against div-by-zero. The penalty is only inside row-by-row scans.
