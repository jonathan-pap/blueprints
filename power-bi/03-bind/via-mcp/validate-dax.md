# Validate a DAX expression (via MCP)

Syntax-check without executing. Faster than running, and won't fail on permission or refresh errors.

## Tool call

```
mcp__powerbi__validate_dax({
  workspace: "<workspace>",
  dataset:   "<model-name>",
  expression: "SUM('Sales'[Amount])"
})
```

Returns `{ ok: bool, errors: [{ line, column, message }] }`.

## Use cases

- Pre-check a measure DAX before calling `add-measure.md`.
- Verify a thin-report measure expression before saving to `reportExtensions.json`.
- Lint TMDL on commit (loop through `<table>.tmdl` and validate each `measure` block).

## If the server doesn't expose validate-only

Fall back to `query-dax.md` with a trivial wrapper:

```dax
EVALUATE ROW("ok", <expression-being-tested>)
```

If the query parses, the expression parses. (Caveat: still scans data, so slower.)

## Fallback (no MCP)

`../via-powershell/query-dax.md` with the same wrapper trick.
