# Add a measure (via MCP)

Create a measure in the live model. Saves to the model immediately.

## Tool call

```
mcp__powerbi__add_measure({
  workspace:     "<workspace>",
  dataset:       "<model-name>",
  table:         "<table-name>",
  name:          "Total Revenue",
  expression:    "SUM('Sales'[Amount])",
  formatString:  "#,##0",
  displayFolder: "1. Revenue",
  description:   "..."
})
```

## Before calling

1. `validate-dax.md` to syntax-check the expression.
2. `list-measures.md` filtered to the table to confirm the name isn't already taken.

## After calling

- The new measure is immediately visible to visuals and to subsequent `list-measures` calls.
- Save the same change to disk so it survives a model reload — either let Power BI Desktop persist on next save, or write to `<project>.SemanticModel/definition/tables/<table>.tmdl` via `../../02-build/model/`.

## Mutation safety

- Mutations are not undoable via Ctrl+Z in Power BI Desktop.
- Test on a backup project first if uncertain.

## Fallback (no MCP)

`../via-powershell/modify-tom.md` (buffered TOM mutation + `SaveChanges()`).
