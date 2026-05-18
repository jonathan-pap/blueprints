# SQL with `Value.NativeQuery`

For complex SQL that can't be expressed cleanly in M.

## Pattern

```m
let
    Source = Sql.Database("server", "db"),
    Data = Value.NativeQuery(Source,
        "SELECT * FROM dbo.MyView WHERE Year = 2024",
        null, [EnableFolding=true])
in
    Data
```

`Value.NativeQuery` with `EnableFolding=true` allows subsequent M steps to fold on top of the native query.

## When to use

- Complex SQL (CTEs, window functions, recursive queries) that M can't translate efficiently
- Existing SQL views you want to consume as-is
- SQL features that don't have M equivalents (HINTS, JOIN strategies, etc.)
- Performance-tuned SQL where you want full control over the query plan

## When NOT to use

- Simple SELECT with filter / project — M folds these cleanly; native query is unnecessary complexity
- The user might modify the M later via Power Query Editor — native SQL is harder to evolve in the UI

## With incremental refresh

`Value.NativeQuery` works with `RangeStart` / `RangeEnd`, but you have to interpolate the values into the SQL string:

```m
let
    Source = Sql.Database("server", "db"),
    Sql = "SELECT * FROM dbo.Orders WHERE OrderDate >= '" &
           DateTime.ToText(RangeStart, "yyyy-MM-dd") & "' AND OrderDate < '" &
           DateTime.ToText(RangeEnd, "yyyy-MM-dd") & "'",
    Data = Value.NativeQuery(Source, Sql, null, [EnableFolding=true])
in
    Data
```

**Careful:** ensure values are quoted / escaped correctly. SQL injection isn't a real concern here (server-side query, controlled inputs) but malformed dates break the query silently.

## Parameter binding (safer than string interpolation)

Power Query supports SQL parameter binding via the `Value.NativeQuery` third argument:

```m
Value.NativeQuery(Source,
    "SELECT * FROM dbo.Orders WHERE OrderDate >= @StartDate AND OrderDate < @EndDate",
    [StartDate=RangeStart, EndDate=RangeEnd],
    [EnableFolding=true])
```

Prefer this when supported by the source.

## See also

- `../best-practices/query-folding.md` — `EnableFolding=true` is critical
- `incremental-refresh.md` — `RangeStart` / `RangeEnd` integration
