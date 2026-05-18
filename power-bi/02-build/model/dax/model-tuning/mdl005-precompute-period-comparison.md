# MDL005 — Pre-compute period comparison columns

> Tier 3 — user approval required. Requires source-side or Power Query work.

Period-over-period calcs (YoY, MoM) require two SE scans. Pre-computing prior-period values as **physical columns** on the fact row reduces it to one scan.

## Before — two scans

```dax
YoY = SUM('Fact'[Sales]) - CALCULATE(SUM('Fact'[Sales]), SAMEPERIODLASTYEAR('Date'[Date]))
```

Each `CALCULATE` with TI adds an SE scan with a date-filtered key set.

## After — one scan

```dax
YoY = SUM('Fact'[Sales]) - SUM('Fact'[SalesLY])
```

Where `[SalesLY]` is a physical column populated at ETL / Power Query time — looked up from last year's row at the same key.

## Implementation

In Power Query or upstream:

```sql
SELECT
    OrderDate,
    ProductKey,
    Sales,
    -- Self-join to find prior year's same row
    LY.Sales AS SalesLY
FROM Fact F
LEFT JOIN Fact LY
    ON LY.OrderDate = DATEADD(year, -1, F.OrderDate)
   AND LY.ProductKey = F.ProductKey
```

## Trade-off

- **Wider fact table** — each row now carries the prior-year value (~doubles the storage of the metric column).
- **Eliminates the TI scan entirely** — every YoY query becomes a single-scan aggregation.
- **Best for fixed period comparisons on large DQ tables** where the TI scan dominates query time.

## When NOT to use

- Few measures use the period comparison (write the few that do as DAX TI)
- Multiple lag periods needed (3m, 6m, 1y, 2y) — proliferates columns
- Date grain is high-cardinality enough that the lookup join at ETL is itself slow

## See also

- `mdl006-row-based-ti-table.md` — alternative: one table that materializes all periods
