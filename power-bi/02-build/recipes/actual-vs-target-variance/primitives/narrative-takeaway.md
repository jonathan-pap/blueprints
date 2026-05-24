# P5 — Narrative takeaway

The finishing touch: a one-sentence, data-driven **subtitle** that summarises the chart —
*"In 2024, we beat the target in 7 months, with the strongest overperformance in March and
the longest winning streak of 4 months."* It's a single text measure bound to the visual's
`subTitle`. Optional, but it turns a chart into a briefing.

## The sentence measure

```dax
TAKEAWAY =
VAR _Year    = SELECTEDVALUE ( <AXIS_TABLE>[<YEAR_COLUMN>] )
VAR _Wins    = [Number Successful Months]
VAR _Best    = [Best Month]
VAR _Streak  = [Longest Winning Streak]
RETURN
"In " & _Year & ", we beat the target in " & _Wins &
" months, with the strongest overperformance in " & _Best &
" and the longest winning streak of " & _Streak & " months."
```

## Supporting measures

```dax
Number Successful Months =
COUNTROWS ( FILTER ( VALUES ( <AXIS_TABLE>[<MONTH_KEY_COLUMN>] ), CALCULATE ( [Delta] ) > 0 ) )

Best Month =                       -- name of the month with the largest positive Delta
VAR _M = ADDCOLUMNS ( VALUES ( <AXIS_TABLE>[<MONTH_KEY_COLUMN>] ), "@d", CALCULATE ( [Delta] ) )
VAR _Top = TOPN ( 1, FILTER ( _M, [@d] > 0 ), [@d], DESC )
RETURN MAXX ( _Top, /* format the key as a month name */ <AXIS_TABLE>[<MONTH_KEY_COLUMN>] )

Longest Winning Streak =           -- gaps-and-islands over the win/loss sequence
VAR _M =
    ADDCOLUMNS ( VALUES ( <AXIS_TABLE>[<MONTH_KEY_COLUMN>] ),
        "@key", <ordinal month number>,
        "@win", IF ( CALCULATE ( [Delta] ) > 0, 1, 0 ) )
VAR _Wins = FILTER ( _M, [@win] = 1 )
VAR _Grouped = ADDCOLUMNS ( _Wins, "@grp", [@key] - RANKX ( _Wins, [@key],, ASC, DENSE ) )
VAR _Streaks = GROUPBY ( _Grouped, [@grp], "@len", COUNTX ( CURRENTGROUP (), 1 ) )
RETURN COALESCE ( MAXX ( _Streaks, [@len] ), 0 )
```

The streak measure is the classic **gaps-and-islands** pattern: rank the winning months, and
consecutive wins share `key − rank`; group by that and the biggest group is the longest streak.
See the full, ready forms in [variance-measures.tmdl](../templates/variance-measures.tmdl).

## Bind it to the subtitle — `visualContainerObjects.subTitle`

```json
"subTitle": [ { "properties": {
  "show": { "expr": { "Literal": { "Value": "true" } } },
  "text": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "TAKEAWAY" } } },
  "titleWrap": { "expr": { "Literal": { "Value": "true" } } },
  "italic": { "expr": { "Literal": { "Value": "true" } } }
} } ]
```

The subtitle accepts a **measure** as its text (not just a literal) — that's what makes it
respond to the slicer / filter context.

## Rules

- **`titleWrap: true`** or a long sentence clips on one line.
- The supporting measures iterate `VALUES(<MONTH_KEY_COLUMN>)` in the **current filter
  context** (respecting the year slicer), so the sentence updates as the user filters.
- Keep `<MONTH_KEY_COLUMN>` sortable (`"012024"`, `"022024"` …) so streaks and "best" order
  correctly.

## Skip it

For the lean version, omit all P5 measures and the subtitle binding → the
[minimal variant](../variants/minimal-no-narrative.md).

## Done

Back to [workflow.md](../workflow.md) for the ordered build + validation, or pick a [variant](../variants/).
