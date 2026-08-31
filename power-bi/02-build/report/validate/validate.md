# Validate

**Validate the unit you changed — and the unit is rarely one visual.**

`pbir validate` is whole-report only; it cannot scope to a file. On a 93-visual report it takes ~2s,
so running it after each of ten template-driven writes spends ~20s re-checking work already checked,
to verify one new visual. Cadence by how the write happened:

| Situation | What to run |
|---|---|
| Any file write | Nothing — the `validate-pbir.sh` hook already does file-scoped syntax + schema, automatically |
| Hand-edited JSON, a visual type you haven't used, an unfamiliar property | `pbir validate` **now** — this is where schema mistakes live, and validating immediately localizes the error to the edit that caused it |
| Scripted/template writes of N visuals | Once when the page is done — `json.dump` can't emit malformed JSON, and the shape came from a template that already validated |
| Every finished page | `pbir validate` **plus** [`lint-report-traps.sh --page`](../../../04-review/hooks/lint-report-traps.sh) (~0.15s) — the trap lint is the one that catches defects a reader would notice |

Schema validation proves the JSON is well-formed. It has never caught a report that *looked* wrong —
that's [`build-traps.md`](build-traps.md) and the render.

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
