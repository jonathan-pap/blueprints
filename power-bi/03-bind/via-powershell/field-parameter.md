# Create a field parameter (TOM)

A field parameter is a calculated table that lets users swap which measure/column a visual displays. Power BI Desktop creates these via a wizard, but creating them via TOM gives full control — and MCP rarely exposes the equivalent.

## What gets created

- One calculated table with three columns: display name, hidden field reference, ordinal.
- A sort-by-column relationship on the ordinal.
- An `ExtendedProperty` annotation marking the table as a field parameter.

## Use the canned script

```bash
pwsh -ExecutionPolicy Bypass -File scripts/create-field-parameter.ps1 \
  -Port <PORT> \
  -TableName "Metric Selector" \
  -Fields @("Sales.Revenue","Sales.Margin","Sales.Order Count")
```

## What it generates (DAX)

```dax
"Metric Selector" =
{
    ("Revenue",     NAMEOF('Sales'[Revenue]),     0),
    ("Margin",      NAMEOF('Sales'[Margin]),      1),
    ("Order Count", NAMEOF('Sales'[Order Count]), 2)
}
```

Plus a `sortByColumn` on the ordinal column, plus an annotation:

```
extendedProperty ParameterMetadata =
{ "version": 3, "kind": 2 }
```

## After

- Bind the field parameter's display column to a slicer or to the visual's `Values` role.
- Save the TMDL to disk afterwards (`../../02-build/model/`) so it survives a project reload.
- Validate via `../../04-review/hooks/validate-tmdl.sh`.

## See also

- `modify-tom.md` — general TOM mutation pattern
- `scripts/create-field-parameter.ps1` — the script's source
