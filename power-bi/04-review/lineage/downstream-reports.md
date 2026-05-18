# Find downstream reports

Trace all Power BI reports bound to a semantic model across the tenant. Workspace contributor access is sufficient — no admin role needed.

## Setup (one-time)

```bash
pip install azure-identity requests
az login    # or DefaultAzureCredential equivalent
```

## Run

```bash
# By workspace + model name
python scripts/get-downstream-reports.py "Workspace Name" "Model Name"

# By dataset GUID (avoids workspace/model name disambiguation)
python scripts/get-downstream-reports.py --dataset-id <guid>

# JSON output for further processing
python scripts/get-downstream-reports.py "Workspace" "Model" --json
```

## How it works

1. Lists every workspace the authenticated user can access.
2. Queries each workspace's reports in parallel (8 workers) checking `datasetId`.
3. Groups results by workspace.

Typical runtime: under 10 seconds for ~100 workspaces.

## Read the output

| Field | Meaning |
|---|---|
| Report format `PBIR` | Modern format, editable as JSON |
| Report format `PBIRLegacy` | Legacy format, needs conversion (see `../../02-build/report/validate/convert-legacy.md`) |
| Reports in unexpected workspaces | Copies, forks, or thin reports pointing at a shared model |
| Many downstream reports | High-impact model — changes require coordination |

## Save the output

```bash
python scripts/get-downstream-reports.py "Workspace" "Model" --json \
  > ../../outputs/$(date +%Y-%m-%d)-<model>-downstream-reports.json
```

## Limitations

- **Only Power BI reports.** See `other-consumers.md` for what's missed.
- **Only workspaces the auth identity can access.** For tenant-wide coverage, use `--dataset-id` with a tenant-admin token and the `admin/reports` API.
- **Not for bulk inventory** across many models. Repeated invocation = throttling risk. Use `fab api "admin/workspaces/getInfo"` for admin-mode bulk lineage.
