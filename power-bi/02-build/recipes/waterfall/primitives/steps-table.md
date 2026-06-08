# P1 — Steps disconnected table

The disconnected calculated table that sits on the chart's Category role and drives every
measure's `SELECTEDVALUE` switch. Template: [waterfall-steps-table.tmdl](../templates/waterfall-steps-table.tmdl).

## The DAX

For an N-step waterfall, build a single calculated table via `UNION` of one-row
`SELECTCOLUMNS` expressions:

```dax
<STEPS_TABLE> =
UNION (
    SELECTCOLUMNS ( { ( "<Step 1 name>", 1 ) }, "Step", [Value1], "StepSort", [Value2] ),
    SELECTCOLUMNS ( { ( "<Step 2 name>", 2 ) }, "Step", [Value1], "StepSort", [Value2] ),
    SELECTCOLUMNS ( { ( "<Step 3 name>", 3 ) }, "Step", [Value1], "StepSort", [Value2] ),
    -- ... one row per step, StepSort = 1..N in display order
)
```

Where:
- `<Step N name>` is the step's display label (from Q1).
- `StepSort` is 1..N — the visual ordering on the category axis.
- `Value1` / `Value2` are auto-named columns of an inline row constructor; the `SELECTCOLUMNS`
  renames them to `Step` and `StepSort`.

## Columns

After creation, two follow-up settings make the axis behave correctly:

| Column | Property | Why |
|---|---|---|
| `Step` | `sortByColumn = StepSort` | Forces the axis to honor the step order regardless of alphabetical naming |
| `StepSort` | `isHidden = true` | Helper only; never displayed |

Both should also have `summarizeBy = None` (the auto-summarize default would be `Sum` for
`StepSort`, which is meaningless here).

## Why a calculated table, not Power Query?

- **Self-contained** — no Power Query M, no external CSV, fully visible in TMDL.
- **Refreshes with the model** — no separate data source to manage.
- **Trivially editable** — adding or renaming a step is one line in the `UNION`.
- **Survives lineage updates** — no source-column dependencies that break on rename.

The trade-off: refreshing the table requires a model refresh (or `RefreshWithXMLA` via the
MCP) before values populate. Templates and the workflow account for this.

## Disconnected — no relationships

The table has **no relationships** to any fact table. That's the point:

- The chart's Category role uses `<STEPS_TABLE>[Step]` purely as a labeled axis.
- Measures read which step is being evaluated via `SELECTEDVALUE(<STEPS_TABLE>[Step])`.
- Filter context doesn't propagate from `<STEPS_TABLE>` to facts — the step is just a
  "what should this measure return right now" switch.

If you accidentally create a relationship (e.g. by reusing a name that matches a fact column),
the `SELECTEDVALUE` switch can return BLANK when filter context filters facts to zero rows.
**Verify no relationships are auto-suggested** after creating the table.

## MCP gotcha

When creating the table via `mcp__powerbi-modeling-mcp__table_operations` Create, do NOT
include a `columns` array in the payload — calculated tables derive columns from the DAX
expression, and the MCP rejects pre-declared columns:

```
Error creating table 'X': Columns cannot be specified for calculated tables.
```

Pass only `name`, `description`, and `daxExpression`. Then update column properties
(`sortByColumn`, `isHidden`, `summarizeBy`) in a follow-up `column_operations` Update call.

## Next

[P2 — floater + body measures](floater-body-measures.md) — the engine that reads `Step` via
`SELECTEDVALUE` and emits the right value per row.
