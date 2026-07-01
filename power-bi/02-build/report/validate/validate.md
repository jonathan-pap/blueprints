# Validate

Run after every mutation. Non-negotiable.

## Command

```bash
pbir validate "<project>.Report"
```

Add **`--semantic`** (pbir ≥ 0.9.25) to also check `visualType` ids + object names against the visual
catalog — it catches `stackedColumnChart` (→ `columnChart`) and typo'd object names before Desktop
silently refuses to render. Full mode table (`--fields`/`--qa`/`--semantic`/`--all`):
[`../../../04-review/audit/pbir-validate.md`](../../../04-review/audit/pbir-validate.md#validation-modes-0925).

## Verify structure too

```bash
pbir tree "<project>.Report" -v
```

## What it catches

- JSON syntax errors
- Missing required fields per Microsoft's PBIR schemas
- Visuals positioned outside page bounds
- Bindings to non-existent fields (when the model is reachable)
- Schema URL mismatches

## On failure

- JSON syntax → `jq empty <file>.json` to find the line
- Missing field → run `../bind/find-canonical-name.md` to confirm the real name
- Out-of-bounds → see `../layout/page-dimensions.md`
- Broken field ref → `fix-broken-field-reference.md`

## Hook variant

Per-project automated validation is in `../../../04-review/hooks/validate-pbir.sh` — wire it on PostToolUse so every Write triggers it.
