# Delete a measure (via MCP)

Removes a measure from the live model. Destructive and not undoable from the model side: confirm with the user first, and check no visual still binds to it — a report bound to a deleted measure breaks at render time, not at delete time.

## Tool call

```
mcp__powerbi__delete_measure({
  workspace: "<workspace>",
  dataset:   "<model-name>",
  table:     "<table-name>",
  name:      "Total Revenue"
})
```

## Before calling

Find every reference to the measure first — they'll all break:

```bash
pbir fields find "<project>.Report" -f "<table>.Total Revenue"
grep -rn "\[Total Revenue\]" "<project>.SemanticModel/" "<project>.Report/"
```

If anything references it, decide whether to delete the references, rebind them (`../../02-build/report/bind/swap-field.md`), or cancel.

## After

- Mirror the deletion to TMDL on disk (`../../02-build/model/`).
- Validate the report — every visual that used the measure will be broken until rebound or removed: `../../02-build/report/validate/validate.md` → `../../02-build/report/validate/fix-broken-field-reference.md`.

## Fallback (no MCP)

`../via-powershell/modify-tom.md` — `$table.Measures.Remove($table.Measures["Total Revenue"])` + `SaveChanges()`.
