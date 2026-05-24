# Find a field's canonical name

> **MANDATORY before any `pbir add visual` / `pbir visuals bind` call.** Field names you remember or infer from English are NOT canonical — always verify against the live model first. The `validate-visual-binding` hook (`../../../04-review/hooks/validate-visual-binding.sh`) blocks binding commands with unknown fields, but the goal is to never trigger it.

Run before any binding. Returns the exact table and field names the model uses.

## All fields

```bash
pbir model "<project>.Report" -d
```

## One table

```bash
pbir model "<project>.Report" -d -t Sales
```

## Fields already used in the report

```bash
pbir fields list "<project>.Report"
```

## Verify values exist (e.g., before a slicer)

```bash
pbir model "<project>.Report" -q "EVALUATE VALUES('Geography'[Region])"
```

## Save model dump for reference

```bash
pbir model "<project>.Report" -d -o /tmp/model.json
```

## Pipe to grep for quick lookup

```bash
pbir model "<project>.Report" -d | grep -i "revenue"
```

## Output contains

For each field: table name (single-quoted if it contains spaces), field name, kind (`Column` or `Measure`), data type. The kind determines how you pass it to `bind-field.md` — see `column-vs-measure.md`.

## When this isn't enough

- **Thin PBIP** (no `.SemanticModel/` folder on disk) → use Power BI MCP: `../../../03-bind/via-mcp/list-tables.md` + `list-measures.md`.
- **Need live values** (verify what a measure actually returns) → `../../../03-bind/via-mcp/query-dax.md` (preferred) or `../../../03-bind/via-powershell/query-dax.md` (alternative).
- **Validate a DAX expression syntactically** → `../../../03-bind/via-mcp/validate-dax.md`.
