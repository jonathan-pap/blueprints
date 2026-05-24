# Property catalogue — finding the right container/property

> 49 visual types, ~12,600 property slots. Don't guess property names — **discover** them with
> `pbir schema`, then set with `pbir set`. This file is the map: universal containers (on every
> visual) + a per-type container index so you know what to ask `pbir schema describe` about.

## Discovery commands (use these first)

```bash
pbir schema types                       # list all visual types
pbir schema containers card             # containers available on a type
pbir schema describe card.title         # properties of a container: types, ranges, enums
pbir schema roles barChart              # canonical data roles for a type
pbir visuals format "<path>" -v         # current values on a live visual
pbir visuals properties -s "marker"     # fuzzy-search a property across all types
pbir set "<path>.container.property" --value X   # set any property
```

`pbir schema describe "type.container"` is the authoritative source for any property's exact
name, type, range, and allowed enum values. The tables below tell you *which* container to ask about.

## Universal containers (present on all / most visual types)

Set via `pbir set "<path>.CONTAINER.PROPERTY" --value X`.

| Container | Key properties |
|---|---|
| `background` | color, show, transparency |
| `border` | color, radius, show, width |
| `divider` | color, show, style (solid/dashed/dotted), width, ignorePadding |
| `dropShadow` | preset, position (Outer/Inner), angle, color, shadowBlur, shadowDistance, shadowSpread, transparency, show |
| `general` | formatString |
| `lockAspect` | show |
| `padding` | top, bottom, left, right |
| `spacing` | verticalSpacing, spaceBelowTitle, spaceBelowSubTitle, spaceBelowTitleArea, customizeSpacing |
| `stylePreset` | name |
| `title` | text, show, alignment, bold/italic/underline, fontColor, fontFamily, fontSize (6–45), heading, background, titleWrap |
| `subTitle` | same shape as `title` |
| `visualHeader` | show, background, border, foreground, transparency + ~20 `show*Button` toggles |
| `visualHeaderTooltip` | text, section, type (Default/Canvas), font*, background |
| `visualTooltip` | show, section, type, font*, fontColor, background |
| `visualLink` | type, show, bookmark, webUrl, drillthroughSection, navigationSection, tooltip |

> Reminder: prefer pushing shared formatting to the **theme**, not per-visual overrides. These
> universal containers are for the exceptions. See [../format/apply-theme-to-report.md](../format/apply-theme-to-report.md).

## Type-specific container index

Property counts in parens; run `pbir schema describe "type.container"` for details. Charts that
share a count (303) share the same container set.

**Column & bar** — `columnChart`/`barChart` (303): categoryAxis, dataPoint, **error**, labels, legend, plotArea, ribbonBands, smallMultiplesLayout, subheader, totals, trend, valueAxis, referenceLine¹, zoom. `clusteredBarChart`/`clusteredColumnChart`/`hundredPercentStacked*` share this set (¹clustered have `referenceLine`; plain/stacked have `ribbonBands`+`totals`).

**Line / area / combo**
- `lineChart` (430): anomalyDetection, **error**, forecast, **markers**, **lineStyles**, referenceLine, scalarKey, seriesLabels, trend, y2Axis, zoom, + axes/dataPoint/labels/legend/plotArea.
- `areaChart` (348), `stackedAreaChart`/`hundredPercentStackedAreaChart` (332): markers, lineStyles, scalarKey, seriesLabels, totals, y2Axis.
- `lineClusteredColumnComboChart` (378), `lineStackedColumnComboChart` (356): lineStyles, markers, seriesLabels, error, referenceLine.
- `ribbonChart` (303): ribbonBands.

**Part-to-whole & flow**
- `pieChart`/`donutChart` (36): slices, labels, legend, dataPoint.
- `treemap` (31): categoryLabels, dataPoint, labels, layout, legend.
- `funnel` (33): categoryAxis, dataPoint, labels, percentBarLabel.
- `waterfallChart` (105): breakdown, sentimentColors, categoryAxis/valueAxis, labels, legend.
- `scatterChart` (215): bubbles, fillPoint, markers, ratioLine, referenceLine, plotAreaShading, colorByCategory, clustering.

**Cards / KPI / gauge**
- `card` (18): categoryLabels, labels, wordWrap.
- `cardVisual` (394): cardCalloutArea, referenceLabel*, label, value, grid, accentBar, image, smallMultiples*.
- `multiRowCard` (27): card, cardTitle, categoryLabels, dataLabels.
- `kpi` (43): goals, indicator, status, trendline, lastDate.
- `gauge` (33): axis, target, calloutValue, dataPoint, labels.

**Tables & slicers**
- `tableEx` (76): values, columnHeaders, columnFormatting, columnWidth, grid, total, sparklines, clustering, accessibility.
- `pivotTable` (140): rowHeaders, columnHeaders, values, subTotals, rowTotal, columnTotal, grid, sparklines, columnFormatting, columnWidth, blankRows.
- `slicer` (69): data, items, header, selection, searchBox, slider, date, dateRange, numericInputStyle.
- `listSlicer` (202) / `advancedSlicerVisual` (192) / `textSlicer` (54): rich data/label/value/selection + fill/glow/outline/shadow custom.

**Report elements**
- `textbox` (5): text, values.
- `shape` (56): fill, outline, glow, shadow, rotation, shape, text.
- `actionButton` (76): fill, icon, outline, shadow, glow, shape, text, rotation.
- `image` (28): image, imageScaling.
- `bookmarkNavigator` (74): bookmarks, accentBar, fill, outline, shadow, glow, shape, text, layout.

**Maps & AI** — `azureMap` (156), `filledMap` (34), `map` (45), `shapeMap` (22), `decompositionTreeVisual` (47), `keyDriversVisual` (17), `qnaVisual` (30), `aiNarratives` (9), `scorecard` (93), `rdlVisual` (20), `pythonVisual`/`scriptVisual` (2: script).

## Entity types (non-visual)

| Entity | Containers |
|---|---|
| `page` | background, outspace, outspacePane, pageSize, filterCard, pageInformation, pageRefresh, personalizeVisual |
| `report` | settings, outspacePane, section |
| `theme` | colors, textClasses |
| `filter_config` | shell |
| `bookmark_config` | options |

## Related

- [selectors.md](selectors.md) — scoping a property to points/series/states
- [expressions.md](expressions.md) — the `expr` value forms a property takes
- [../add-visual/_index.md](../add-visual/_index.md) — per-chart build recipes (roles + create)
- [../format/override-property.md](../format/override-property.md) — the `pbir set` override workflow
