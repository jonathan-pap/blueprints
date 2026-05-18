# xmSQL — Storage Engine query language

xmSQL is the human-readable representation of SE scan activity in trace events. Shows which tables are scanned, which columns are aggregated, which filters apply, how joins resolve.

Syntax resembles SQL with key differences.

## Implicit GROUP BY

Every column in the SELECT list is automatically a grouping column — no GROUP BY keyword.

## Computed expressions

Row-level calculations use a `WITH` block with `:=`, referenced in aggregations via `@`:

```
WITH $Expr0 := ( 'Sales'[UnitPrice] * 'Sales'[OrderQuantity] )
SELECT Product[Category], SUM ( @$Expr0 )
FROM Sales
    LEFT OUTER JOIN Product ON 'Sales'[ProductKey] = Product[ProductKey]
```

## Joins are always LEFT OUTER

The many-side table is `FROM`, the one-side is joined in.

## Semi-join projections

Appear as `DEFINE TABLE $Filter0 ... ININDEX` — an initial dimension scan builds a key index injected into the fact WHERE clause.

## Callbacks

`CallbackDataID` or `EncodeCallback` in the xmSQL text means the SE had to call back to the FE for a per-row expression it couldn't evaluate natively.

Example trigger:

```dax
SUMX('Sales', IF('Sales'[Amount] > 1000, 1, 0))
-- xmSQL contains CallbackDataID because IF is not SE-native
```

Fix patterns (per `../decision-guide.md`):

- DAX002 — replace ADDCOLUMNS / SUMMARIZE with SUMMARIZECOLUMNS
- DAX007 — replace IF with INT for boolean conversion
- DAX008 — fix context transition in iterator
- DAX018 — replace DIVIDE with `/` in iterators

## Reading xmSQL in a trace

In server timing traces, the `VertiPaqSEQueryEnd.TextData` field contains the xmSQL for that scan. Look for:

- **`CallbackDataID`** → callback present, fix the FE-only expression
- **`DEFINE TABLE ... ININDEX`** → semi-join, often expensive when compound-tuple
- **Wide SELECT lists** → many columns being materialized; reduce with column pruning
- **No WHERE clause** → all rows scanned; check whether a filter should push down

## See also

- `architecture.md` — FE vs SE
- `trace-metrics.md` — extracting metrics from `VertiPaqSEQueryEnd`
- `trace-analysis.md` — full event waterfall and what-to-look-for
