# Infer the DAX a visual is generating

Power BI generates a DAX query per visual at runtime — usually `SUMMARIZECOLUMNS`. You can
reconstruct it from the visual JSON (`query.queryState.<Role>.projections`), which is enough to
sanity-check a binding or hand a measure author the query without a live trace.

## Read the bindings

```bash
pbir visuals bind "<...>/Visual.Visual" --show
```

Output lists each role + bound field. Or read `visual.json` `query.queryState` directly.

## Projections → columns and measures

| Projection field | Becomes |
|---|---|
| `Column` (`SourceRef.Entity`) | a grouping key in `SUMMARIZECOLUMNS` |
| `Measure` (`SourceRef.Entity`) | `"Alias", 'Table'[Measure]` |
| `Measure` with `Schema: "extension"` | a `DEFINE MEASURE` **and** an entry in `SUMMARIZECOLUMNS` |

## Roles by visual type

| Visual | Grouping roles | Measure roles |
|---|---|---|
| `card` (old) | — | Values |
| `cardVisual` (new) | — | **Data** (not Values) |
| `lineChart` | Category | Y (Y2 for combo) |
| `barChart`/`columnChart` (+clustered/100%) | Category | Y |
| `areaChart` (+stacked/100%) | Category, Series | Y |
| `waterfallChart`/`ribbonChart`/`donutChart` | Category | Y |
| `kpi` | TrendLine | Indicator, Goal |
| `slicer` | Values | — |
| `tableEx` | Values (columns) | Values (measures) |
| `pivotTable` (matrix) | Rows, Columns | Values |
| `scatterChart` | Category | X, Y, Size, Tooltips |

## Worked examples

**Bar / line** — `Category: Date.Month`, `Y: Orders.Order Lines`:

```dax
EVALUATE
SUMMARIZECOLUMNS(
    'Date'[Month],
    'Date'[Month Number],          -- sort column auto-added when Month has sortByColumn
    "Order_Lines", 'Orders'[Order Lines]
)
```

> **sortByColumn auto-add:** if the grouping column has a `sortByColumn`, that sort column is
> added to the grouping automatically. (This is why the `MonthKey`/`Month Number` columns show
> up in traces.) See [../../model/object-types/column-properties.md](../../model/object-types/column-properties.md).

**Card** — no grouping, so the measure is wrapped in `IGNORE()`:

```dax
EVALUATE SUMMARIZECOLUMNS( "Total_Revenue", IGNORE('Sales'[Total Revenue]) )
```

`cardVisual` produces the same query but reads its measure from the **`Data`** role, not `Values`.

**KPI with an extension (report-local) measure** — the extension measure lands in a `DEFINE`:

```dax
DEFINE
    MEASURE 'Orders'[Order Lines (PY)] = CALCULATE([Order Lines], SAMEPERIODLASTYEAR('Date'[Date]))
EVALUATE
SUMMARIZECOLUMNS(
    'Date'[Year],
    "Order_Lines",        'Orders'[Order Lines],
    "Order_Lines__PY_",   'Orders'[Order Lines (PY)]
)
```

Spot extension measures by `"Schema": "extension"` in the projection. See [../calculations/thin-report-measure.md](../calculations/thin-report-measure.md).

## The slicer exception

Slicers do **not** use `SUMMARIZECOLUMNS`. They use `CALCULATETABLE + SUMMARIZE + VALUES` to
fetch the distinct member list. Don't expect a slicer's query to mirror a chart's.

## Filters → wrappers

Page/visual filters wrap the query (in metadata they're sparse; the real `TREATAS`/filter
context shows in a trace):

```dax
EVALUATE
CALCULATETABLE( SUMMARIZECOLUMNS(...), 'Date'[Calendar Year] = 2026 )
```

## To capture the exact runtime query

Use the live trace: [../../../03-bind/via-powershell/query-listener.md](../../../03-bind/via-powershell/query-listener.md). The trace shows the actual DAX with
all filter context applied — the authoritative version when inference and reality disagree.
