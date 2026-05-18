# 2026-05-17 — `test` demo gallery

12 new pages added to the `test` project, each demonstrating one visual family with bound demo data from the `financials` table + `_Measures`. Existing 4 pages (Overview, Trends, Distribution, Showcase) unchanged.

## New demo pages

| Page | Visuals | Visual types |
|---|---|---|
| **Demo-Cards** | 4 | card, cardVisual, kpi, multiRowCard |
| **Demo-LineCharts** | 4 | lineChart, areaChart, stackedAreaChart, hundredPercentStackedAreaChart |
| **Demo-BarCharts** | 3 | barChart, clusteredBarChart, hundredPercentStackedBarChart |
| **Demo-ColumnCharts** | 3 | columnChart, clusteredColumnChart, hundredPercentStackedColumnChart |
| **Demo-Combo** | 3 | lineClusteredColumnComboChart, lineStackedColumnComboChart, ribbonChart |
| **Demo-PartToWhole** | 4 | donutChart, pieChart, funnel, treemap |
| **Demo-Tables** | 2 | tableEx, pivotTable |
| **Demo-Scatter** | 1 | scatterChart |
| **Demo-Waterfall** | 1 | waterfallChart |
| **Demo-Gauge** | 3 | gauge × 3 (Profit %, Discount %, Total Profit) |
| **Demo-Slicers** | 3 | slicer, advancedSlicerVisual, listSlicer |
| **Demo-Containers** | 4 | textbox, actionButton, shape, bookmarkNavigator |

**12 pages, 35 demo visuals, ~70 field bindings.**

## Total project state

- **16 pages** (4 original + 12 demo)
- **73 visuals** including auto page-titles
- **Valid (9 warnings, 1 info)** — all warnings are cosmetic (KPI sizing, gauge sizing, table sizing)
- All 35 demo visuals bind to the same `financials` table + `_Measures` measures already in the model

## Bug + workaround surfaced during the build

`pbir add visual <type>` auto-generates a visual `name` field as `<title>-<type>-<hash>`. For visual types with very long names (`hundredPercentStackedAreaChart`, `lineClusteredColumnComboChart`, etc.) the auto-name exceeds the PBIR schema name length limit and creation fails.

**Fix:** pass explicit short `--name "shortname"` for long-typed visuals.

Should add this gotcha to `02-build/report/add-visual/_index.md` and the specific atomic files for stacked-100 and combo charts (the affected types).

## Files in this snapshot

- `2026-05-17-test-demo-gallery.md` — this file
- `2026-05-17-test-demo-gallery-validation.log` — `pbir validate --all` output
- `2026-05-17-test-demo-gallery-tree.txt` — `pbir tree -v` showing all 73 visuals with bindings

## To view

Open `projects/test.pbip` in Power BI Desktop. Cycle through the 16 pages (page selector at the bottom). The Demo-* pages give a one-page-per-visual-family showcase.
