# TE2 ⇄ TE3 compatibility — the "works in both" ruleset

> Tabular Editor 2 (free) and Tabular Editor 3 (paid) both run **Roslyn C#** against the same
> Tabular Object Model wrapper, but TE2 ships an **older compiler** and a **smaller API**. Follow these
> rules and one script runs unchanged in both. Every script in [`scripts/`](scripts/) obeys them.

## 1. C# syntax — stay at C# 7

TE2's bundled Roslyn is older. Avoid newer syntax; prefer the classic form.

| Avoid (TE3-only / newer) | Use instead (both) |
|---|---|
| switch expressions (`x switch { ... }`) | classic `switch` / `if`-`else` |
| `using` declarations (`using var x = …;`) | `using (var x = …) { }` |
| target-typed `new` (`List<int> x = new();`) | `new List<int>()` |
| records, top-level statements | plain classes / statements |
| nullable ref types (`string?`), `!` null-forgiving | plain reference types |
| range/index (`a[^1]`, `a[1..]`) | `a[a.Count-1]`, `.Skip/.Take` |

Fine in both: `var`, string interpolation `$"..."`, LINQ (`System.Linq` is auto-imported), `foreach`,
lambdas, `System.Text.StringBuilder`, `System.IO.File`.

## 2. API surface — use the shared members only

These exist in **both** and are the backbone of portable scripts:

- **Collections:** `Model.Tables`, `Model.AllMeasures`, `Model.AllColumns`, `Model.Relationships`,
  `table.Measures`, `table.Columns`, `Selected.Measures`, `Selected.Columns`, `Selected.Tables`.
- **Create:** `table.AddMeasure(name, expression, displayFolder)`, `table.AddCalculatedColumn(...)`,
  `Model.AddCalculatedTable(...)`.
- **Common properties:** `.Name`, `.Expression`, `.FormatString`, `.DisplayFolder`, `.Description`,
  `.IsHidden`, `.DataType`, `.SummarizeBy`, `.DaxObjectName` (the `[Measure]` / `Table[Column]` ref),
  `.DaxObjectFullName`.
- **Enums:** `DataType.Int64/Decimal/Double/String/DateTime/Boolean`, `AggregateFunction.None/Sum/...`.
- **Output:** `Output(obj)` — TE3 shows a grid/inspector, TE2 a value/messagebox. Safe in both.

**Avoid (TE3-only, or behaves differently):**

- Custom UI — `ScriptHelper.*` dialogs, `System.Windows.Forms`/WPF windows. TE3 is WPF, TE2 WinForms;
  a script that pops its own dialog won't be portable. **Use `Output()` for all feedback.**
- `Info()` / `Warning()` / `Error()` helper toasts — TE3-first; prefer `Output()`.
- The TE3 **macro** API, `Model.Database`, C# Script *debugging* features, `FormatDax()` on some
  builds — don't rely on them in shared scripts.
- Do **not** call any `SaveChanges()` from the script — TE applies changes on **save** (UI Ctrl+S, or
  the CLI save flag). Scripts only *mutate the model in memory*.

## 3. Selection vs whole-model (UI vs CLI)

`Selected.*` is populated by the **UI selection** — it's **empty when run headless (CLI/CI)**. Write
scripts to work both ways:

```csharp
// portable target: fall back to the whole model when nothing is selected
var targets = Selected.Measures.Any() ? Selected.Measures : (IEnumerable<Measure>)Model.AllMeasures;
```

Each library script notes its target at the top and uses this pattern where it matters.

## 4. Model source (PBIP/TMDL vs .bim vs live)

- **TE3** opens a **PBIP / TMDL** folder directly — point it at `projects/<p>/<name>.SemanticModel`.
- **TE2** works with a saved **`.bim` / `Model.bim`** or a **live connection**
  (`localhost:<port>` — the same local Desktop instance the [`../power-bi/03-bind/`](../power-bi/03-bind/) MCP/TOM path
  uses). It does *not* open a TMDL folder natively. For a PBIP-only project, connect TE2 **live** to
  the open Desktop model, or serialize to `.bim` first.
- Scripts here are **source-agnostic** — they touch model objects, not files — so the same `.cs` runs
  whichever way the model was opened.

## Quick self-check before adding a script

- [ ] No C# 8+ syntax (see the table).
- [ ] Only shared API members + enums.
- [ ] Feedback via `Output()` only; no custom dialogs.
- [ ] Works headless — `Selected.*` has a whole-model fallback.
- [ ] No `SaveChanges()` in the script body.
