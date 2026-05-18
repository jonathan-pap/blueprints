# Extract M expressions from a deployed model

Pull partition M and shared parameters from a Fabric / Service model.

## Get partition expression

```bash
fab get "<Workspace>.Workspace/<Model>.SemanticModel" -f \
  -q "definition.parts[?path=='definition/tables/<Table>.tmdl'].payload"
```

Returns the full TMDL text for the table; the partition expression lives inside the `partition` block.

## Get shared M parameters

```bash
fab get "<Workspace>.Workspace/<Model>.SemanticModel" -f \
  -q "definition.parts[?path=='definition/expressions.tmdl'].payload"
```

`expressions.tmdl` contains `expression` declarations — shared parameters like `SqlEndpoint`, `Database`, plus any reusable M queries.

## For thick PBIP projects on disk

No fab needed — read the file directly:

```bash
cat "<project>.SemanticModel/definition/tables/<Table>.tmdl"
cat "<project>.SemanticModel/definition/expressions.tmdl"
```

## Workflow

1. Extract — get the M source.
2. Modify locally — make your edits in a text editor or via Power Query Editor (Desktop).
3. Validate — execute via API (`validation/execute-via-api.md`) or save via XMLA (`validation/save-via-xmla.md`).
4. Deploy — `fab import` for remote; reopen in Desktop for thick PBIP.

## See also

- `partition-anatomy.md` — structure of what you'll extract
- `validation/_index.md` — how to test before deploying
