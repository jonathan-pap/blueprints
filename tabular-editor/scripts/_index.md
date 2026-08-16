# Script library — TE2 + TE3

Every script here runs unchanged in Tabular Editor 2 and 3 (see [`../compatibility.md`](../compatibility.md))
and works from the UI, CLI, or CI (see [`../run.md`](../run.md)). Each starts with a comment noting its
**target** (selection vs whole-model) and any prereqs. None call `SaveChanges()` — **save after running**.

| Script | Does | Target | Notes |
|---|---|---|---|
| [`format-measures.cs`](format-measures.cs) | Apply currency/percent/int format + a display folder by naming heuristic | selection → whole model | tune the heuristics to your naming |
| [`create-time-intelligence.cs`](create-time-intelligence.cs) | Add `PY`, `YTD`, `YoY %` for each base measure | selection → whole model | set the date column; skips existing + the folder itself |
| [`document-model.cs`](document-model.cs) | Export all measures to a Markdown table | whole model | edit the output `path` |
| [`hide-technical-columns.cs`](hide-technical-columns.cs) | Hide `*Key`/`*Id`/`_*` columns; `SummarizeBy=None` on numeric keys | whole model | tune the key heuristic |
| [`add-measure-metadata-tags.cs`](add-measure-metadata-tags.cs) | Append `[Type, Created on, Created by]` to each measure's Description; **idempotent** (skips already-tagged) | selection → whole model | set `createdBy`; **Type classified from DAX** (sum/average/count/percent/technical/date reference/other) |
| [`check-measure-variables.cs`](check-measure-variables.cs) | Report measures whose DAX `VAR`s don't start with `_` | selection → whole model | report-only; pairs with the `MEASURE_VAR_UNDERSCORE_PREFIX` BPA rule |

## Adding a script

1. Write it against the shared API + C# 7 syntax; feedback via `Output()`; give `Selected.*` a
   whole-model fallback. Run the checklist in [`../compatibility.md`](../compatibility.md#quick-self-check-before-adding-a-script).
2. Head the file with a `// name — one-line purpose`, its target, and any prereqs.
3. Add a row above.
4. Test in **both** TE2 and TE3 (the free TE2 is the stricter target — if it runs there, TE3 is fine).
