# Step-by-step debugging

When an expression fails or produces unexpected results, preview intermediate steps by changing the `in` clause.

## Pattern

```
section Section1;
shared SqlEndpoint = "myserver.database.windows.net";
shared Database = "MyDB";
shared Result = let
    Source = Sql.Database(SqlEndpoint, Database),
    Data = Source{[Schema="dbo", Item="Orders"]}[Data],
    #"Filtered" = Table.SelectRows(Data, each [Status] <> "Cancelled"),
    #"Selected" = Table.SelectColumns(#"Filtered", {"OrderId", "Amount"})
in Data;  -- Change this to inspect different steps
```

## What each target shows

| `in` target | What it shows |
|---|---|
| `in Source` | Table listing from the database |
| `in Data` | All columns from the source table |
| `in #"Filtered"` | After row filtering |
| `in #"Selected"` | After column selection (final) |

## For each step, check

- Column names and count (did a rename/select work?)
- Row count (did a filter apply correctly?)
- Data types (`df.dtypes` in Python)
- Null counts (`df.isnull().sum()`)
- Sample values (do they look right?)

## Use the script

`../scripts/preview_partition.py` automates this — pass a step name, get the data at that point.

```bash
python ../scripts/preview_partition.py \
  --workspace "WS" --model "Model" --table "Sales" --step "Filtered"
```

## Combine with execute-via-api

Wrap the truncated expression in `execute-via-api.md`'s mashup template, set the `in` target to the step you want to inspect, run. Repeat for each step until you find the breakage.
