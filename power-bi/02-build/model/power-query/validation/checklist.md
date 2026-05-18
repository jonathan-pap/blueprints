# Pre-deploy validation checklist

Before deploying a new or modified partition expression:

1. **Syntax** — save to model (XMLA) to catch structural errors → `save-via-xmla.md`
2. **Data** — execute via API with `Table.FirstN(_, 100)` to verify correct columns and values → `execute-via-api.md`
3. **Types** — check `df.dtypes` matches expected semantic model column types
4. **Nulls** — check `df.isnull().sum()` for unexpected nulls from type casting
5. **Row count** — execute without `Table.FirstN` (or with a large limit) to verify filter logic
6. **Folding** — for large tables, verify the query completes within 90 seconds (indicates folding is working)

## After deploying

- **Refresh the table** — confirm full load works at scale
- **Spot-check downstream measures** — run a few DAX queries to ensure dependent measures still return expected values
- **Validate dependent reports** — open Power BI Desktop and check visuals don't show broken-field badges

## If folding is suspect

Use `../best-practices/query-folding.md` "Verifying folding" — right-click step → "View Native Query" in Desktop. Or run the API execution against a large table and time it.

## If types don't match

Compare:

```bash
# Source schema
fab table schema "WS.Workspace/lh.Lakehouse/Tables/orders"

# Model expected
grep -A2 "column " "<model>.SemanticModel/definition/tables/Orders.tmdl"
```

Add `Table.TransformColumnTypes` to reconcile.
