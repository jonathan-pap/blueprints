# DAX019 — Lift time intelligence to outer CALCULATE for vertical fusion

TI functions (DATESYTD, DATEADD, etc.) break vertical fusion — each TI-modified measure gets its own SE query. Keep base measures TI-free and apply TI once in an outer wrapper.

> **Custom time intelligence (VAR-based predicates):** When measures use manual date anchoring via `CALCULATE(expr, Column = _var)` instead of built-in TI functions, DAX019 does not apply — see `dax017-boolean-multiplier.md` for the boolean multiplier workaround.

## Anti-pattern — each measure applies TI independently (no fusion)

```dax
MEASURE 'Sales'[Revenue YTD] = CALCULATE([Revenue], DATESYTD('Date'[Date]))
MEASURE 'Sales'[Cost YTD]    = CALCULATE([Cost],   DATESYTD('Date'[Date]))
MEASURE 'Sales'[Margin YTD] =
    [Revenue YTD] - [Cost YTD]
```

## Preferred — base measures fuse, TI applied once

```dax
MEASURE 'Sales'[Margin YTD] =
    CALCULATE([Revenue] - [Cost], DATESYTD('Date'[Date]))
```

## Signal

Multiple TI-modified measures hitting the same fact table.

## See also

- `dax020-horizontal-fusion.md` — same principle for slice measures
- `../engine/fusion.md` — fusion mechanics
- `../model-tuning/mdl006-row-based-ti-table.md` — model-level alternative
