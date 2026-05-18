# DAX007 — Replace IF with INT for boolean conversion

INT with boolean expressions avoids conditional logic callbacks that IF statements trigger.

## Anti-pattern

```dax
SUMX(
    'Products',
    IF([Sales Amount] > 10000000, 1, 0)
)
```

## Preferred

```dax
SUMX(
    'Products',
    INT([Sales Amount] > 10000000)
)
```

## When the result is a count, eliminate the iterator entirely

```dax
-- Anti-pattern: iterator + conditional = callback
SUMX('Sales', IF('Sales'[Amount] > 1000, 1, 0))

-- Preferred: native SE aggregation, no iterator, no callback
CALCULATE(COUNTROWS('Sales'), 'Sales'[Amount] > 1000)
```

## Signal

Conditional logic (`IF`, `IIF`) inside row iterator. `CallbackDataID` in xmSQL.
