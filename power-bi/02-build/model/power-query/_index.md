# power-query/ — atomic files

> Author, validate, and test Power Query M expressions in semantic model partitions.

## Foundation

- `partition-anatomy.md` — structure of a partition expression; key elements
- `safe-pattern.md` — order of M steps for max query folding
- `extract-expressions.md` — pull existing partition M and shared parameters from a deployed model

## Best practices

- `best-practices/query-folding.md` — what folds, what breaks folding, how to verify
- `best-practices/column-pruning.md` — remove columns early
- `best-practices/row-filtering.md` — filter rows early
- `best-practices/type-handling.md` — apply types early; common type mappings
- `best-practices/anti-patterns.md` — pull-then-filter, unnecessary Table.Buffer, cross-query refs, excessive steps
- `best-practices/naming-conventions.md` — step names, parameters
- `best-practices/error-handling.md` — when try…otherwise is appropriate; when it hides bugs

## Validation

- `validation/_index.md` — comparison: execute via API vs save via XMLA
- `validation/execute-via-api.md` — full data validation via executeQuery API
- `validation/save-via-xmla.md` — fast syntax-only validation
- `validation/step-debugging.md` — preview intermediate steps by changing the `in` clause
- `validation/checklist.md` — pre-deploy validation sequence

## Common patterns

- `patterns/incremental-refresh.md` — `RangeStart`/`RangeEnd` partitions
- `patterns/lakehouse-source.md` — Fabric Lakehouse navigation
- `patterns/native-query.md` — `Value.NativeQuery` with EnableFolding

## Scripts

- `scripts/execute_m.py` — execute M expressions via Fabric API (validates against real data)
- `scripts/preview_partition.py` — preview partition data at any step (uses `fab get` + `execute_m.py`)

## When to enter

User asks: "write Power Query", "fix Power Query", "test a partition", "preview partition data", "debug Power Query step", "optimize Power Query", or mentions "M code", "M expression", "partition expression", "query folding".

## Source

Upstream `_examples/semantic-models/skills/power-query/`.
