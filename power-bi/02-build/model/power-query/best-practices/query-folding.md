# Query folding

The most important Power Query performance concept. The M engine translates compatible steps into native data source queries (e.g., SQL). When folding works, the data source does the heavy lifting. When it breaks, the mashup engine pulls all data into memory and processes it locally.

## Why it matters

- Folded query against a 10 M row table sends `SELECT TOP 1000 ... WHERE ...` to SQL Server → fast
- Non-folded query pulls all 10 M rows into the mashup engine, then filters locally → slow + memory-heavy
- For large tables, broken folding causes refresh timeouts or out-of-memory errors

## Steps that fold (SQL sources)

| M function | SQL equivalent |
|---|---|
| `Table.SelectColumns` | `SELECT col1, col2` |
| `Table.RemoveColumns` | `SELECT` (excluding columns) |
| `Table.SelectRows` | `WHERE` |
| `Table.Sort` | `ORDER BY` |
| `Table.FirstN` | `TOP N` |
| `Table.Group` | `GROUP BY` |
| `Table.TransformColumnTypes` | `CAST` |
| `Table.RenameColumns` | `AS` alias |
| `Table.ExpandTableColumn` | `JOIN` |
| `Table.NestedJoin` | `JOIN` |
| `Table.Distinct` | `DISTINCT` |
| `Table.Skip` | `OFFSET` |

## Steps that break folding

Once folding breaks, all subsequent steps also run locally. Primarily SQL Server via `Sql.Database`; other sources may differ.

**Table construction:** `Table.Buffer`, `List.Buffer`, `Table.StopFolding`, `#table` constructor, `Table.FromList`, `Table.FromRecords`, `Table.FromRows`, `Table.FromValue`, `Table.FromColumns`.

**Row position:** `Table.AddIndexColumn`, `Table.LastN`, `Table.RemoveLastN`, `Table.Range` (mid), `Table.Repeat`, `Table.AlternateRows`, `Table.InsertRows`, `Table.RemoveRows` (by position), `Table.ReverseRows`, `Table.FindText`.

**Text functions inside `Table.TransformColumns` / `Table.AddColumn`:** `Text.Proper`, `Text.Combine` (multi-col merge), `Text.Insert`, `Text.Remove`, `Text.RemoveRange`, `Text.Select`, `Text.Split`, `Text.SplitAny`, `Text.BeforeDelimiter`, `Text.AfterDelimiter`, `Text.BetweenDelimiters`, `Text.PadStart`, `Text.PadEnd`, `Text.Reverse`, `Text.Format`, `Text.ToList`, `Text.Clean`, `Text.From` with format/culture.

**Column splitting / combining:** `Table.SplitColumn`, `Table.CombineColumns`, all `Splitter.*` functions.

**Pivot / structure:** `Table.Transpose`, `Table.DemoteHeaders`, `Table.PromoteHeaders`.

**Fill / imputation:** `Table.FillDown`, `Table.FillUp` (stateful row scanning).

**Error handling:** `Table.RemoveRowsWithErrors`, `Table.SelectRowsWithErrors`, `try...otherwise` in row context.

**Schema / metadata:** `Table.Schema`, `Table.ColumnNames`, `Value.Type`, `Type.Is`.

**Custom functions / iteration:** User-defined `(x) => ...` lambdas in row context, `Table.TransformRows`, `List.Generate`, `List.Accumulate`, `List.Transform` with complex logic.

**Record / list columns:** `Table.ExpandListColumn`, `Table.ExpandRecordColumn` (except after same-source NestedJoin), `Record.*` functions, `Table.ToRecords`, `Table.ToRows`, `Table.ToList`, `Table.Column`.

**Date/time in row context:** `Date.ToText` with format, `Date.IsInCurrentMonth`-style relative filters, `Date.DayOfWeekName`, `Date.MonthName` (locale-dependent).

**Misc:** `Table.Profile`, `Table.Max`/`Table.Min` (returning row), `Table.Contains*`, `Table.IsDistinct`.

## Sometimes folds (source-dependent)

- `Table.AddColumn` — folds if expression uses only SQL-translatable functions; breaks with complex M
- `Table.TransformColumns` — folds for `Text.Upper`, `Text.Lower`, `Text.Trim`, `Number.Round`; breaks for `Text.Proper`, complex lambdas
- `Table.TransformColumnTypes` — folds for compatible casts; breaks for locale-specific or M-only types
- `Table.ReplaceValue` — folds with literal; breaks with patterns
- `Table.Pivot` / `Table.Unpivot` — folds on SQL Server; breaks on other sources
- `Table.NestedJoin` — folds when both sources are same SQL connection; breaks across sources
- `Table.Combine` — folds as UNION ALL when same SQL source
- `Table.SelectRows` with `Text.Contains` — folds as `LIKE '%value%'`
- `Table.Group` — folds with standard aggregations; breaks with custom functions
- `Value.NativeQuery` — subsequent steps fold only if `EnableFolding=true`
- `Text.Start` / `Text.End` — often fold as `LEFT()` / `RIGHT()`; `Text.Middle` often does not
- `Date.Year`, `Date.Month`, `Date.Day` — fold as `YEAR()`, etc.
- `Date.AddDays` / `Date.AddMonths` — fold as `DATEADD()`

## Environmental fold-breakers

Not functions, but conditions:

- Merging / appending from different data sources
- Incompatible data privacy levels (Data Privacy Firewall intervenes)
- Source is flat file (CSV, Excel, JSON, XML) — no query engine
- Source is `Web.Contents` / API — no SQL engine
- Custom SQL without `EnableFolding=true`
- Any step after a fold-breaking step (chain broken; cannot re-fold)

## Verifying folding

- **In Power Query Online / Desktop:** right-click a step → "View Native Query". If greyed out, doesn't fold.
- **Programmatically:** execute via the executeQuery API. If a query on a large table completes well within timeout, folding is likely working. If it times out or is slow, folding may be broken.

## See also

- `../safe-pattern.md` — order of M steps to maximize folding
- `anti-patterns.md` — common folding mistakes
- `../patterns/native-query.md` — when to use Value.NativeQuery to bypass folding limits
