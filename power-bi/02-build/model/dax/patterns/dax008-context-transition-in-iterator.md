# DAX008 — Context transition in iterator

Context transition is powerful but expensive. Three optimization strategies:

## 1. Remove it completely

```dax
// Instead of: SUMX('Sales', [Sales Amount])
// Use:
SUMX('Sales', 'Sales'[Unit Price] * 'Sales'[Quantity])
```

## 2. Reduce number of columns

```dax
// Instead of: SUMX('Account', [Total Sales])
// Use:
SUMX(VALUES('Account'[Account Key]), [Total Sales])
```

## 3. Reduce cardinality before iteration

```dax
// Instead of: SUMX('Account', [Total Sales] * 'Account'[Corporate Discount])
// Use:
SUMX(VALUES('Account'[Corporate Discount]), [Total Sales] * 'Account'[Corporate Discount])
```

## Signal

Context transition inside an iterator over a large table. Often paired with callbacks in the trace.

## See also

- `dax015-lower-granularity-iterator.md` — when low-cardinality attribute drives the optimization
- `dax006-pre-materialize-context-transition.md` — materialize once with SUMMARIZECOLUMNS
