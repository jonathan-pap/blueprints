# Run a DAX query (via MCP)

Execute DAX against the live model. Use when you need real values (not just structure).

## Tool call

```
mcp__powerbi__query_dax({
  workspace: "<workspace>",
  dataset:   "<model-name>",
  query:     "EVALUATE SUMMARIZECOLUMNS('Date'[Year], \"@Total\", SUM('Sales'[Amount]))"
})
```

Returns a table of rows. Column names come back **fully qualified** (`'Sales'[Amount]`) — handle them by index, not by short name.

## DAX rules (must follow)

- Fully qualify column refs: `'Sales'[Amount]`, never `[Amount]`.
- Table names always single-quoted, even simple ones: `'Sales'`.
- Measure refs are always unqualified: `[Total Revenue]`.

## Common query shapes

```dax
EVALUATE 'Sales'                                              -- full table
EVALUATE CALCULATETABLE('Sales', 'Sales'[Region] = "West")    -- filtered
EVALUATE SUMMARIZECOLUMNS('Date'[Year], "@Total", [Revenue])  -- aggregated
EVALUATE ROW("Result", COUNTROWS('Sales'))                    -- scalar
EVALUATE TOPN(5, 'Sales')                                     -- preview
```

## Validation pattern

If you only want to syntax-check (not execute), use `validate-dax.md` instead — it runs the parser without scanning data.

## Fallback (no MCP)

`../via-powershell/query-dax.md` — same DAX, ADOMD.NET transport.
