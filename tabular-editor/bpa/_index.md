# bpa — Best Practice Analyzer rule sets

> BPA scans a tabular model against a **rule set** (JSON) and flags objects that violate best practices
> — naming, formatting, performance, data quality. Built into **both** TE2 (*Tools → Manage BPA Rules /
> Best Practice Analyzer*) and TE3. Rules run in both; keep any `FixExpression` C# portable
> ([`../compatibility.md`](../compatibility.md)).

## Files

- [`authoring.md`](authoring.md) — the rule JSON shape, scopes, `Expression` (Dynamic LINQ) + optional
  `FixExpression` (C#), and where rule sets live (local / model annotation / shared file or URL)
- [`rules/`](rules/) — the rule-set JSON files
  - [`rules/custom-rules.json`](rules/custom-rules.json) — starter house rules (naming + format + hygiene)

## Run a rule set

- **UI:** *Tools → Best Practice Analyzer* (TE2/TE3), pick the rule set, review, apply fixes.
- **CLI (headless / CI gate):**

  ```bash
  # TE2 (free) — analyze, non-zero exit on violations = CI gate
  TabularEditor.exe "<model.bim | conn>" -A "tabular-editor/bpa/rules/custom-rules.json"

  # TE3
  TabularEditor3.exe "<model | PBIP folder>" -A "tabular-editor/bpa/rules/custom-rules.json"
  ```

  For Power BI, `pbir bpa run` is an alternative execution path — see
  [`../../power-bi/04-review/bpa/`](../../power-bi/04-review/bpa/). This blueprint owns the **rule library**;
  run it via TE *or* `pbir`.

## Get Microsoft's default set as a starting point

The community/Microsoft default `BPARules.json` is the canonical base — copy it, then add/override with
your house rules in [`rules/`](rules/). (In TE: *Tools → Manage BPA Rules → Import*.)
