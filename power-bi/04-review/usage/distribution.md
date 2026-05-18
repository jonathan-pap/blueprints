# Distribution audit — who has access

Lists every user / group / role with access to a report, resolving group memberships via Microsoft Graph.

## Script

```bash
python ../scripts/get_report_distribution.py -w <workspace-id> -r <report-id> \
  -o ../../outputs/$(date +%Y-%m-%d)-<report>-distribution.csv
```

## Output

CSV with columns: principal_name, principal_type, access_method, role, expanded_member_count.

Access methods:
- `direct` — user added individually to the workspace or report.
- `via-role` — user is a Member / Contributor / Viewer of the workspace.
- `via-group` — user is in a group with access.
- `via-app` — accessed via a published app.

## Calculate audience reach

Combine distribution count with `workspace.md` viewer count:

```
reach = unique_viewers_last_28_days / total_users_with_access
```

A reach of < 30% over 28 days is low. Either the report isn't useful, isn't discoverable, or has the wrong audience.

## Sensitive data

The output contains identifying info. Don't commit to a public repo. Add to `.gitignore`:

```
outputs/*-distribution.csv
```

## Auth

Service principal + Graph permissions: `GroupMember.Read.All`. Document the auth context in the output header.
