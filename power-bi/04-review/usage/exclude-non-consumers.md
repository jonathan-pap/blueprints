# Exclude non-consumers from usage metrics

Raw viewer counts inflate when service principals, IT, and report developers are included. Filter them out for adoption-relevant metrics.

## Who counts as a non-consumer

- **Service principals** (type `App`) — automation, refresh accounts.
- **Report developers** — typically members of an `IT` or `BI` group, or have `Contributor` / `Member` role on the workspace.
- **IT / support** — opens reports to troubleshoot, not for the business decision.
- **You and your team** — anyone who built the report.

## Heuristics

The usage scripts in `../scripts/` accept exclusion flags:

```bash
python ../scripts/get_report_detail.py -w <ws> -r <r> \
  --exclude-service-principals \
  --exclude-group "BI Team" \
  --exclude-group "IT" \
  --exclude-user "you@contoso.com"
```

## Resolve groups via Graph

The exclusion happens client-side — the script calls Microsoft Graph to expand group memberships, then filters.

Requires Graph permission: `GroupMember.Read.All`.

## Document the filter

When sharing usage outputs, include in the file header what was excluded:

```
2026-05-17-sales-overview-usage.md

Excludes: 4 service principals, BI Team (12 members), IT (8 members)
Net consumer count: 47 of 71 with access
```

Otherwise stakeholders mistake the filtered count for total users.
