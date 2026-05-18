# Incremental refresh partitions

Incremental refresh partitions use `RangeStart` and `RangeEnd` parameters. Configure in Power BI Desktop; Power BI auto-partitions the table by date.

## Pattern

```m
let
    Source = Sql.Database(#"SqlEndpoint", #"Database"),
    Data = Source{[Schema="dbo", Item="Orders"]}[Data],
    #"Filtered" = Table.SelectRows(Data, each
        [OrderDate] >= #"RangeStart" and [OrderDate] < #"RangeEnd")
in
    #"Filtered"
```

## Critical: filter must fold

If the `RangeStart` / `RangeEnd` filter doesn't fold to a SQL WHERE clause, incremental refresh defeats its own purpose — every partition pulls all data, then filters locally.

To verify: right-click the filter step in Desktop → "View Native Query" should show:

```sql
SELECT * FROM dbo.Orders WHERE OrderDate >= '...' AND OrderDate < '...'
```

If "View Native Query" is greyed out, folding is broken. Common causes:

- `Table.AddColumn` with custom logic before the filter step
- Source doesn't support folding (CSV, JSON, API)
- Type mismatch — `RangeStart` / `RangeEnd` must be `DateTime`, source column too

## When testing

Inline concrete date values for `RangeStart` and `RangeEnd` in the mashup document (per `../validation/execute-via-api.md`):

```
shared RangeStart = #datetime(2024, 1, 1, 0, 0, 0);
shared RangeEnd   = #datetime(2024, 2, 1, 0, 0, 0);
```

## Configuration

After the partition expression is set up, configure incremental refresh in Power BI Desktop:

- Right-click the table → Incremental refresh
- Set archive window (e.g., 3 years store)
- Set incremental window (e.g., 30 days refresh per cycle)
- Detect data changes: optional column-based change detection to skip unchanged partitions

After publish, the first refresh creates partitions for the full archive window. Subsequent refreshes only touch the incremental window.

## See also

- `../validation/execute-via-api.md` — test the partition with inline dates
- `../../../03-bind/via-powershell/refresh-troubleshooting.md` — incremental refresh failure modes
