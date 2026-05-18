# Refresh troubleshooting

Common refresh failures, causes, and resolutions. Use after `refresh-model.md` triggered a refresh and it failed, or when scheduled refreshes report errors.

## Step 1 — Check refresh history

```bash
WS_ID=$(fab get "MyWorkspace.Workspace" -q "id" | tr -d '"')
MODEL_ID=$(fab get "MyWorkspace.Workspace/MyModel.SemanticModel" -q "id" | tr -d '"')
fab api -A powerbi "groups/$WS_ID/datasets/$MODEL_ID/refreshes?\$top=5"
```

Look at `status` and `serviceExceptionJson` for the specific error and which table / partition failed.

## Credential and authentication errors

| Error | Cause | Resolution |
|---|---|---|
| `DatasourceHasNoCredentialError` | Credentials missing / not configured | Set credentials in dataset settings (Power BI Service); re-authenticate via OAuth for cloud connections |
| `OAuthTokenRefreshFailedError` | OAuth token expired during refresh (SharePoint, Dynamics) | Token expires after ~1h; reduce data volume per query or switch to service principal |
| Access forbidden / 403 | Insufficient workspace permissions | Verify workspace contributor or higher |
| Credentials lost after `fab cp` | Personal / gateway-bound creds don't transfer | Re-authenticate in dataset settings; only shared cloud connections transfer automatically |

## Data source and gateway errors

| Error | Cause | Resolution |
|---|---|---|
| `GatewayNotReachable` | On-prem gateway offline or outdated | Install latest gateway; check status in admin portal |
| Unsupported data source for refresh | Source type not supported | Use a gateway or switch connector |
| `Web.Page` connector fails | Requires gateway after Nov 2016 | Configure on-prem data gateway |
| Connection timeout / lost | Transient network or long M query | Retry; for persistent: `Table.Buffer` for complex joins; check source timeouts |

## Type and schema errors

| Error | Cause | Resolution |
|---|---|---|
| Type mismatch | Source column type ≠ model `dataType` | Add `Table.TransformColumnTypes` in partition; or fix model column type |
| Column does not exist in rowset | Source column renamed / removed / re-cased | Check source schema; add `Table.RenameColumns` |
| Duplicate value on key column | Source duplicates on "one" side | `Table.Distinct` in partition; fix source; or review if column should be key |
| `ANY` type column with TRUE/FALSE | Booleans convert -1/0 in service (differs from Desktop) | Set explicit types in Power Query before publishing |

## Timeout and size errors

| Error | Cause | Resolution |
|---|---|---|
| Scheduled refresh timeout (2 h shared / 5 h Premium) | Model too large for window | Reduce size; incremental refresh; partition refresh via XMLA |
| Uncompressed data limit exceeded | Shared capacity: 10 GB limit during refresh | Filter in Power Query; move to Premium |
| Model size exceeds capacity limit | Model > capacity max | Enable large model storage (Premium); reduce; upgrade |
| Data source query timeout | Source has its own timeout | Override via `CommandTimeout` in connection string |
| Initial incremental refresh timeout | First refresh loads all history | Bootstrap via XMLA to create partition objects without loading |

## Incremental refresh errors

| Error | Cause | Resolution |
|---|---|---|
| Query not folded | `RangeStart`/`RangeEnd` filter not pushed to source | Verify folding via source profiling; ensure filter step folds; types match (both `DateTime`) |
| Type mismatch on parameters | `RangeStart`/`RangeEnd` type ≠ date column | Both must be `DateTime`; use conversion function if source uses integer keys |
| Partition-key conflicts | Date column updated at source after initial partition | Refresh affected partitions from change date forward via XMLA |
| Data truncated | Source returns > 64 MB compressed (Azure DX, Log Analytics) | Smaller refresh/store periods so each partition < limit |
| Duplicate values after date change | Transaction dates changed at source → row in two partitions | Refresh from change point forward; avoid updating partition date column |

## Capacity and throttling

| Error | Cause | Resolution |
|---|---|---|
| Refresh throttled | Too many concurrent on capacity | Off-peak; stagger schedules; check SKU concurrent limits |
| `Capacity level limit exceeded` | Capacity-wide concurrent limit hit | Retry later; reduce overlapping schedules |
| Memory error during refresh | Insufficient memory (~2× model size needed) | Increase `Max Memory %`; reduce complexity; scale-out for refresh isolation |
| `Container exited unexpectedly (0x0000DEAD)` | Internal service error | Disable scheduled refresh; republish; re-enable |

## Calculated table / column errors

| Error | Cause | Resolution |
|---|---|---|
| Circular dependency on refresh | `SummarizeColumns` inside `CalculateTable` introduced new deps (Sept 2024 change) | Add grouped tables as explicit filters inside `SummarizeColumns` |
| Calculated tables empty after `dataOnly` | `dataOnly` clears but doesn't rebuild | Follow with `calculate` refresh |
| `calculate` refresh times out | Many calc groups or large calc tables | Refresh calc tables individually via XMLA; increase timeout |

## Step 2 — Isolate the failing table

Refresh one table at a time to find the culprit:

```bash
# Dimensions first
fab api -A powerbi "groups/$WS_ID/datasets/$MODEL_ID/refreshes" \
  -X post -i '{"type":"Full","objects":[{"table":"Customers"}]}'

# Then facts
fab api -A powerbi "groups/$WS_ID/datasets/$MODEL_ID/refreshes" \
  -X post -i '{"type":"Full","objects":[{"table":"Invoices"}]}'

# Then calculated tables
fab api -A powerbi "groups/$WS_ID/datasets/$MODEL_ID/refreshes" \
  -X post -i '{"type":"Calculate"}'
```

## Step 3 — Compare source schema to model schema

```bash
# Source schema (lakehouse example)
fab table schema "MyWorkspace.Workspace/MyLakehouse.Lakehouse/Tables/invoices"

# Model column types
fab export "MyWorkspace.Workspace/MyModel.SemanticModel" -o ./model-export -f
grep -A1 "column " ./model-export/MyModel.SemanticModel/definition/tables/Invoices.tmdl
```

If they don't match, add type conversion in the partition expression.

## Step 4 — Verify query folding

For incremental refresh, confirm the filter is pushed to source:

- Desktop: right-click filter step in Power Query → "View Native Query" → check WHERE clause
- Source side: SQL Profiler or query logs to verify single filtered query per partition

## Step 5 — Check capacity state

```bash
fab get "MyWorkspace.Workspace" -q "capacityId"
fab api -A powerbi "capacities" -q "value[].{name:displayName, state:state, sku:sku}"
```

Workspace without a capacity (or suspended capacity) fails all refresh operations.

## Strategies for large models

When models are too large or slow for a single refresh:

- **Partition-level refresh** — refresh individual partitions via Enhanced REST API or XMLA (Premium / Fabric only)
- **Incremental refresh** — auto-partition by date; only recent data refreshes per cycle. `RangeStart`/`RangeEnd` parameters in Power Query
- **Aggregations** — pre-aggregate large facts at coarser grain (monthly by category); detail falls through to DirectQuery
- **Hybrid tables** — import historical + DirectQuery recent; related tables must be Dual storage
- **Scale-out** — semantic model scale-out on Premium isolates refresh from query workloads
