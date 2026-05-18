# DAX003 — Cache repeated and context-independent expressions in variables

Evaluating the same measure multiple times or placing context-independent expressions inside iterators causes redundant SE queries. Cache in a variable.

## Anti-pattern — repeated measure reference

```dax
VAR TotalA = [Sales Amount] * 1.1
VAR TotalB = [Sales Amount] * 0.9
VAR TotalC = [Sales Amount] + 1000
```

## Preferred

```dax
VAR _SalesAmount = [Sales Amount]
VAR TotalA = _SalesAmount * 1.1
VAR TotalB = _SalesAmount * 0.9
VAR TotalC = _SalesAmount + 1000
```

## Anti-pattern — same measure iterated twice

```dax
VAR A = SUMX(VALUES('Sales'[ProductKey]), [Total Sales])
VAR B = AVERAGEX(VALUES('Sales'[ProductKey]), [Total Sales])
```

## Preferred — materialize once

```dax
VAR Base = SUMMARIZECOLUMNS('Sales'[ProductKey], "@TotalSales", [Total Sales])
VAR A = SUMX(Base, [@TotalSales])
VAR B = AVERAGEX(Base, [@TotalSales])
```

## Anti-pattern — context-independent expression inside iterator

```dax
SUMX('Sales', 'Sales'[Quantity] * [Average Price] * 1.1)
// [Average Price] doesn't change per row
```

## Preferred

```dax
VAR _AvgPrice = [Average Price]
RETURN SUMX('Sales', 'Sales'[Quantity] * _AvgPrice * 1.1)
```

## Signal

Same measure evaluated multiple times. Same measure iterated twice. Context-independent expression inside an iterator.
