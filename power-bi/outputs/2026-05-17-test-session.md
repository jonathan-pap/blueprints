# 2026-05-17 — `test` project session summary

End-to-end walkthrough of the blueprint on the `test` project: scaffold pages → plot unbound visuals → add measures → bind visuals → validate.

## What was built

### Pages (4)

Started from a default Page 1, ended with four pages all using clean display-name folder paths.

- `Overview.Page` — 8 visuals
- `Trends.Page` — 4 visuals
- `Distribution.Page` — 4 visuals
- `Showcase.Page` — 10 visuals

### Visuals (22 user-added + 4 auto page titles = 26 total)

#### Overview (KPI dashboard pattern)

- Revenue / Orders / Margin / Customers — 4 KPIs in equal-gap row at y=120
- Revenue Trend (lineChart) + By Region (clusteredBarChart) side-by-side at y=276
- Order Details (tableEx) full-width at y=512

#### Trends

- Revenue Over Time (areaChart) full-width
- Revenue & Margin % (lineStackedColumnComboChart) + Margin vs Volume (scatterChart) side-by-side

#### Distribution

- Revenue Share by Category (donutChart) + Q4 Bridge (waterfallChart) side-by-side
- Sales by Region & Quarter (pivotTable) full-width below

#### Showcase

- Row of 4: Legacy Card + cardVisual + gauge + slicer
- Row of 2: columnChart + stackedAreaChart
- Decorative row: textbox + actionButton + shape

### Model additions

Added `_Measures` table (hidden, calculated, single-row) with 9 measures across 4 display folders:

- **Headline**: Total Sales, Total Units, Total Profit, Total COGS
- **Ratios**: Profit %, Discount %
- **Time Intelligence**: Sales PY, Sales YTD
- **Averages**: Avg Sale Price

All reference the pre-existing `financials` table (Microsoft Financial Sample, 16 columns).

### Bindings (44 field references across 18 user-added visuals; 4 auto titles + 4 decorative untouched)

Validation confirms all 44 resolve against the model. See `2026-05-17-test-validation.log` and `2026-05-17-test-tree.txt` for the full list.

## Workflow path taken

Tier 1 (on-disk TMDL) chosen because Power BI MCP isn't installed in this environment. See `03-bind/via-mcp/check-mcp-available.md` for the detection logic.

Atomic files actively used:

- Layout: `02-build/report/layout/{page-dimensions, position-visual, align-visuals-row}.md`
- Page setup: `02-build/report/page/{add-page, rename-page}.md` (both updated this session with CLI syntax fixes)
- Visual scaffolding: 12 different `02-build/report/add-visual/*.md` files
- Measures: `02-build/model/add/measure.md` + `object-types/model-properties.md` for the `ref table` registration
- Binding: `02-build/report/bind/{find-canonical-name, bind-field, column-vs-measure}.md`
- Validation: `02-build/report/validate/validate.md`

## Blueprint bugs found and fixed during the session

| File | Bug | Fix |
|---|---|---|
| `02-build/report/page/rename-page.md` | Old positional `pbir pages rename ... "Overview"` syntax | Now uses `--to "Overview" -f` + added batch `-p "{displayName}" -f` example |
| `02-build/report/page/add-page.md` | Shorthand `pbir add page test.Report -n X` errors with "thin reports require a connection" | Now uses explicit `pbir add page "test.Report/X.Page" -n "X"` form + note about hash folder names |
| `02-build/report/add-visual/gauge.md` | Listed role as `Value` | Corrected to `Y` + tip to run `--list-roles` |
| `02-build/report/add-visual/combo-chart.md` | Listed roles as `ColumnY` / `LineY` | Corrected to `Y` (columns) / `Y2` (line) |

## Validation result

`pbir validate test.Report --all`: **Valid (7 warnings, 1 info)** — see `2026-05-17-test-validation.log`.

All 7 warnings are cosmetic (KPI sizing recommendations, table sizing, gauge sizing) — none block opening in Desktop or rendering visuals.

## To open

```bash
# Open the project in Power BI Desktop
start projects/test.pbip
```

Data loads from the bundled `Financial Sample.xlsx` referenced by the `financials` table's M expression. All 18 user-added visuals render with real numbers; the 4 auto-title textboxes and 3 decorative shapes/buttons are unbound by design.

## Files in this snapshot

- `2026-05-17-test-session.md` — this file
- `2026-05-17-test-validation.log` — `pbir validate --all` output
- `2026-05-17-test-model-snapshot.txt` — `pbir model -d` output (tables, columns, measures)
- `2026-05-17-test-tree.txt` — `pbir tree -v` output (pages, visuals, bindings)
