# MDL010 — Set IsAvailableInMDX on disconnected slicer tables

> Tier 3 — user approval required.

Disconnected slicer tables (e.g., a `'Reporting Scenario'[Scenario]` parameter table with no model relationship) are commonly used with `SELECTEDVALUE` inside `IF`/`SWITCH`. When the slicer has no active selection, `SELECTEDVALUE` returns BLANK.

With `IsAvailableInMDX = false` on the column, the engine can statically resolve the unfiltered state and eliminate the dead branch without an extra SE scan.

With `IsAvailableInMDX = true` (the default), the engine cannot determine this statically — it queries the table and generates two evaluation branches even though only one will execute.

## Pattern

A disconnected slicer table:

```tmdl
table 'Reporting Scenario'
    column Scenario
        dataType: string
        isAvailableInMDX: false   ← set this for the optimization
        summarizeBy: none
        sourceColumn: Scenario

    partition 'Reporting Scenario' = calculated
        source = DATATABLE("Scenario", STRING, {{"Plan"},{"Forecast"},{"Actual"}})
```

A measure using it:

```dax
MEASURE 'Sales'[Active Metric] =
    SWITCH(
        SELECTEDVALUE('Reporting Scenario'[Scenario]),
        "Plan",     [Plan Revenue],
        "Forecast", [Forecast Revenue],
        "Actual",   [Actual Revenue],
        [Actual Revenue]   -- default when nothing selected
    )
```

When the slicer is unselected, `SELECTEDVALUE` returns BLANK → SWITCH falls through to the default. With `isAvailableInMDX: true`, the engine still scans the disconnected table; with `false`, it skips.

## Scope

This optimization **only applies when the slicer column is unfiltered**. When a selection is active, the branch is always evaluated regardless of this property — the static resolution path isn't available.

## When to apply

- Disconnected parameter tables with SELECTEDVALUE in measures
- Hidden columns (almost always safe to set false)
- High-cardinality columns NOT used in Excel PivotTables via MDX

## When NOT to set false

- The column is genuinely consumed via Analyze in Excel / MDX queries
- It's a measure-only auxiliary column where Excel hierarchy matters
