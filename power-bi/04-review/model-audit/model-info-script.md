# `get_model_info.py` — model metadata snapshot

CLI wrapper that pulls high-level metadata about a deployed model in one call. First thing to run in any audit.

## Run

```bash
python scripts/get_model_info.py -w <workspace-id> -m <model-id>
```

## What it returns

- **Storage mode** — Import / DirectQuery / Direct Lake (each has different audit emphasis)
- **Model size** — bytes / MB; flags large models (>1 GB)
- **Connected reports** — count of downstream Power BI reports
- **Deployment pipeline** — Dev / Test / Prod stage (if pipeline configured)
- **Endorsement status** — Promoted / Certified / None
- **Sensitivity label** — Confidential / Internal / etc.
- **Data sources** — list of source connections
- **Refresh schedule** — frequency, time window
- **Last refresh** — timestamp + status (Completed / Failed)
- **Capacity SKU** — F2, F4, … F2048, Premium Per User, Pro, etc.

## Use the output to scope the audit

- **Storage mode** → Direct Lake adds DL-specific checks (parquet file count, V-Order, DQ fallback risk)
- **Model size** → large models trigger memory + refresh checks first
- **Endorsement** → Certified raises the bar on documentation and naming
- **Capacity SKU** → small SKU + large model = expect refresh / query issues
- **Many connected reports** → impact analysis (use `../lineage/downstream-reports.md`) before recommending model changes

## Save the snapshot

```bash
python scripts/get_model_info.py -w <ws> -m <model> -o ../../outputs/$(date +%Y-%m-%d)-<model>-info.json
```

Becomes part of the audit output bundle alongside the audit markdown.

## Auth

Uses `DefaultAzureCredential`. Same auth pattern as `../lineage/scripts/get-downstream-reports.py`.

```bash
az login    # or service principal env vars
```

## Permissions

Workspace contributor or higher on the source workspace. Tenant admin not required for the basic info — required only for cross-tenant scanning.
