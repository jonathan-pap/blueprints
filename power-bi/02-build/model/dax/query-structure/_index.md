# query-structure/ — Tier 2 query restructuring patterns

> **STOP — Requires user approval before applying any change.** Explain impact on query output and wait for explicit confirmation.

> **Scope: Desktop-Achievable Changes Only.** Every Tier 2 recommendation must map to an action the report author can perform in Power BI Desktop's UI. The agent optimizes the *generated* DAX query, but the user implements changes through the Desktop interface — not by editing DAX directly in the query pane.

Examples of valid Tier 2 changes:

- Changing the axis/groupby field (e.g., swap `Calendar Date` for `Calendar Month` on a visual axis)
- Removing or adding visual-level filters (e.g., drop an unneeded slicer selection)
- Changing filter values (e.g., narrow a date range filter)
- Removing measure value filters (e.g., remove a "Top N" or "> threshold" filter from a visual)
- Changing aggregation type on a column (e.g., Sum → Average)

## Patterns

- `qry001-remove-unneeded-filters.md` — every filter adds a WHERE clause; experiment to find dead filters
- `qry002-eliminate-report-measure-filters.md` — eliminate `__ValueFilterDM` (measure-as-filter doubles execution)
- `qry003-reduce-query-grain.md` — daily → monthly groupby slashes row count 30×
- `qry004-remove-blank-suppression.md` — `+ 0` / `IF(ISBLANK)` / `COALESCE` force evaluation of every groupby combination (changes result shape)

## Decision

Use only when Tier 1 patterns are exhausted and the output change is acceptable to the user. See `../decision-guide.md` for the escalation triggers.

## Workflow

Per `../optimization-workflow.md` Phase 3:

1. Explain the specific change (e.g., "Group by YearMonth instead of Date reduces result rows from 365K to 12K").
2. Explain what changes in output and what perf user gains.
3. Wait for explicit approval.
4. If approved, modify query, run full baseline cycle, present results.
