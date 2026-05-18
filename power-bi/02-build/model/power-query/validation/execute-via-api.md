# Execute via Power Query API (full validation)

Full validation that runs the expression and returns actual data. Catches syntax errors, missing columns, data source issues, and type problems in one step.

## Prerequisites

- A runner dataflow in the workspace with the data source connection bound (see the `executing-power-query` skill in the `etl` plugin for the full setup procedure)
- `fab` CLI authenticated

## Step 1 — Extract the expression and parameters

See `../extract-expressions.md`.

## Step 2 — Build the mashup document

Wrap the expression in a section document, inlining parameter values as `shared` declarations:

```
section Section1;
shared SqlEndpoint = "myserver.database.windows.net";
shared Database = "MyDatabase";
shared Result = let
    Source = Sql.Database(SqlEndpoint, Database),
    Data = Source{[Schema="dbo", Item="Orders"]}[Data],
    #"Select Columns" = Table.SelectColumns(Data, {"OrderId", "Amount"}),
    Limited = Table.FirstN(#"Select Columns", 100)
in Limited;
```

Key points:

- Replace `#"SqlEndpoint"` references with `SqlEndpoint` (the shared declaration)
- The `shared Result = ...` name must match the `queryName` in the API call
- Add `Table.FirstN` to limit rows for large tables
- For incremental refresh, inline `RangeStart` and `RangeEnd` with concrete date values

## Step 3 — Execute

```bash
TOKEN=$(az account get-access-token \
  --resource https://api.fabric.microsoft.com --query accessToken -o tsv)

curl -s -o /tmp/pq_result.bin -X POST \
  "https://api.fabric.microsoft.com/v1/workspaces/${WS_ID}/dataflows/${DF_ID}/executeQuery" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "$(jq -n --arg m "$MASHUP" '{queryName:"Result",customMashupDocument:$m}')"
```

Or use `../scripts/execute_m.py` for the wrapped version.

## Step 4 — Read and validate results

```bash
uv run --with pyarrow python3 -c "
import pyarrow.ipc as ipc, io, json

with open('/tmp/pq_result.bin', 'rb') as f:
    table = ipc.open_stream(io.BytesIO(f.read())).read_all()
    df = table.to_pandas()

if 'PQ Arrow Metadata' in df.columns:
    meta = df['PQ Arrow Metadata'].dropna()
    if len(meta) > 0 and len(df.columns) == 1:
        error = json.loads(meta.iloc[0])
        print('ERROR:', error.get('Error', error))
    else:
        cols = [c for c in df.columns if c != 'PQ Arrow Metadata']
        print(f'Columns: {cols}')
        print(df[cols].head(10).to_string(index=False))
        print(f'({len(df)} rows, {len(cols)} columns)')
        print(f'Types: {dict(df[cols].dtypes)}')
else:
    print(f'Columns: {list(df.columns)}')
    print(df.head(10).to_string(index=False))
    print(f'({len(df)} rows)')
"
```

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `Credentials are required to connect to the SQL source` | Connection not bound to runner dataflow | Bind via `updateDefinition` |
| `Query name not found` | `queryName` ≠ `shared` name in mashup | Ensure both are `Result` |
| `Expression.Error: The column '...' was not found` | Column name mismatch | Check source schema |
| `DataSource.Error: ... could not be reached` | Server unreachable / wrong endpoint | Verify connection details |
| Timeout (90 seconds) | Query too expensive | Add `Table.FirstN` to limit rows |
