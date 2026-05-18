# validation/ — atomic files

Two complementary approaches to validate M expressions:

- `execute-via-api.md` — **full validation** that runs the expression against real data; catches syntax, missing columns, data source issues, type problems
- `save-via-xmla.md` — **fast syntax check** by saving to the model (XMLA/TOM); catches structural errors only
- `step-debugging.md` — preview intermediate steps by truncating the `let...in`
- `checklist.md` — pre-deploy validation sequence (syntax → data → types → nulls → row count → folding)

## When to use which

| Need | Use |
|---|---|
| Full data validation (correct columns, types, values) | `execute-via-api.md` |
| Quick syntax check | `save-via-xmla.md` |
| Step-by-step debugging | `step-debugging.md` |
| Performance testing (check folding) | `execute-via-api.md` with full data, observe timing |

## See also

- `../scripts/execute_m.py` — the executeQuery API wrapper
- `../scripts/preview_partition.py` — combines extract + step preview
