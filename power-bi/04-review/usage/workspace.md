# Workspace-wide usage rollup

How are reports in a Fabric / Power BI workspace being used?

## Script

```bash
python ../scripts/get_report_usage.py -w <workspace-id> \
  -o ../../outputs/$(date +%Y-%m-%d)-<workspace>-usage.json
```

Returns per-report: view count, rank in workspace, page-view distribution, load times.

## Include cross-workspace last-visited (Tier 3, optional)

```bash
python ../scripts/get_report_usage.py -w <workspace-id> --include-datahub \
  -o ../../outputs/$(date +%Y-%m-%d)-<workspace>-usage.json
```

Uses the undocumented DataHub V2 API — no tenant-admin role required, good for "is this report used at all" without admin access.

## Read the output

Key signals:
- **Audience reach**: % of users with access who actually viewed in last 7 / 28 / 60 days.
- **View trends**: stable / growing / declining over the rolling 7-day average.
- **Page-view distribution**: concentrated on one page or spread? Concentration may indicate low-value pages.

## Acting on the data

- Reach < 30% in 28 days → low adoption. Consider deprecating or running adoption campaign.
- Reach > 80% with declining trend → was useful, drifted. Investigate why.
- All views on one page → consider trimming the report to that page.

## Auth

Service principal recommended. Document which auth identity was used in the output artifact's header.

## See also

- `report-detail.md` — single-report deep dive
- `distribution.md` — who has access
- `exclude-non-consumers.md` — filter out devs / IT / service accounts
