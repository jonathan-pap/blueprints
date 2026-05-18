# DAX006 — Pre-materialize context transitions with SUMMARIZECOLUMNS

Materializing context transition results in SUMMARIZECOLUMNS and iterating over pre-calculated values improves query plan.

## Anti-pattern

```dax
SUMX(
    VALUES('Product'[Attribute]),
    CALCULATE(SUM('Sales'[Amount]))
)
```

## Preferred

```dax
SUMX(
    SUMMARIZECOLUMNS(
        'Product'[Attribute],
        "@Amount", SUM('Sales'[Amount])
    ),
    [@Amount]
)
```

## Signal

`SUMX(VALUES(col), CALCULATE(...))` pattern in measure.
