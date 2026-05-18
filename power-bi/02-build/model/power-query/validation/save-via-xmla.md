# Save via XMLA / TOM (syntax check)

Analysis Services validates M syntax when a partition expression is saved. Faster than executing, but only catches structural errors — won't detect wrong column names or data source issues.

## Via TMDL deployment

```bash
# Edit the partition expression in the TMDL file
# Open: <Model>.SemanticModel/definition/tables/Orders.tmdl
# Modify the partition expression under the "partition" block, then deploy:
fab import "<Workspace>.Workspace/<Model>.SemanticModel" -i ./<Model>.SemanticModel -f
```

If the expression has syntax errors, AS returns an error like:

```
Token Eof expected.
Expression.SyntaxError: Token Literal expected.
```

## Via Tabular Editor

Edit the partition expression in TE, save to the model. Same validation runs.

## Via TOM (PowerShell)

For thick PBIP projects with Desktop open, you can save via TOM — see `../../../03-bind/via-powershell/load-tmdl-files.md`.

## What XMLA validation catches

- Missing or mismatched `let`/`in` blocks
- Undefined step references (e.g., referencing `#"Step3"` that doesn't exist)
- Invalid M function names
- Syntax errors (missing commas, unbalanced brackets)
- Invalid type names in `TransformColumnTypes`

## What XMLA validation misses

- Wrong column names (the expression is syntactically valid but the column doesn't exist at the source)
- Data source connectivity issues
- Runtime errors (division by zero, type conversion failures on actual data)
- Performance issues (broken query folding)

For runtime-correctness validation, use `execute-via-api.md`.

## When to use this vs API execution

- **XMLA save** — quick iteration during authoring; immediate feedback on syntax
- **API execution** — before committing / deploying; catches everything XMLA misses

Typical workflow: iterate with XMLA save (fast loop), then run API execute once before deploying.
