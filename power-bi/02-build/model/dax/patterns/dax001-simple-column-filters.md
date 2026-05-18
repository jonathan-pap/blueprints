# DAX001 — Simple column filter predicates as CALCULATE args

CALCULATE accepts simple boolean column predicates directly. These are more efficient than wrapping a table in FILTER (causes excessive materialization). Split `&&` into separate filter arguments.

## Anti-pattern — FILTER with table expression uses an iterator

```dax
CALCULATE(
    SUM('Sales'[Amount]),
    FILTER('Product', 'Product'[Category] = "Electronics")
)
```

## Preferred — column predicate, no iterator

```dax
CALCULATE(
    SUM('Sales'[Amount]),
    KEEPFILTERS('Product'[Category] = "Electronics")
)
```

## Anti-pattern — `&&` joins predicates into a single iterator argument

```dax
CALCULATETABLE('Sales', 'Sales'[Region] = "West" && 'Sales'[Amount] > 1000)
```

## Preferred — separate predicates for better query plan

```dax
CALCULATETABLE('Sales', 'Sales'[Region] = "West", 'Sales'[Amount] > 1000)
```

## Signal

`FILTER(Table, ...)` as CALCULATE argument, or `&&` joining predicates in a single filter.
