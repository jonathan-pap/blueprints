# Export visual data to Excel for QA

QA teams often want the raw numbers behind each visual to verify against source systems.

## Per visual

In Power BI Desktop: right-click any visual → Export data → Summarized data or Underlying data.

## Bulk export via DAX

For every visual on a page, run the underlying DAX (see `../../02-build/report/semantic-model/infer-dax-from-visual.md`) against the live model (`../../03-bind/via-mcp/query-dax.md`) and save results as CSV.

## Script pattern

Power BI doesn't ship a bulk-export CLI. The conventional script:

```bash
# 1. Discover visuals on the page
pbir tree "<project>.Report/Overview.Page" -v -F json > /tmp/visuals.json

# 2. For each visual, infer the query (manual or scripted)
# 3. Run each query via MCP or PowerShell
# 4. Concatenate results into one Excel workbook (Python + openpyxl)

python ../scripts/export_visuals_to_excel.py "<project>.Report/Overview.Page" \
  -o ../../outputs/$(date +%Y-%m-%d)-<project>-export.xlsx
```

(Script lives in `../scripts/` — refer to it directly for the implementation.)

## Tab structure

One tab per visual. Tab name = visual title (truncated to Excel's 31-char limit). First row = column headers; rows below = data.

## Use case

- Hand-off to QA team for source-system reconciliation.
- Snapshot before a major model change (compare pre/post).
- Stakeholder asks "where did this number come from?" — point at the Excel.

## After

Add the export filename to the audit report so it's tracked alongside other outputs.
