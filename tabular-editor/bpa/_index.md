# bpa — Best Practice Analyzer rule sets

> BPA scans a tabular model against a **rule set** (JSON) and flags objects that violate best practices
> — naming, formatting, performance, data quality. Built into **both** TE2 (*Tools → Manage BPA Rules /
> Best Practice Analyzer*) and TE3. Rules run in both; keep any `FixExpression` C# portable
> ([`../compatibility.md`](../compatibility.md)).

## Files

- [`authoring.md`](authoring.md) — the rule JSON shape, scopes, `Expression` (Dynamic LINQ) + optional
  `FixExpression` (C#), and where rule sets live (local / model annotation / shared file or URL)
- [`rules/`](rules/) — the rule-set JSON files
  - [`rules/BPARules-PowerBI.json`](rules/BPARules-PowerBI.json) — **the standard set** (26 rules: Model Layout, Naming, DAX, Performance, Formatting, Metadata) from Tabular Editor's [BestPracticeRules](https://github.com/TabularEditor/BestPracticeRules) repo. Start here.
  - [`rules/custom-rules.json`](rules/custom-rules.json) — neutral **starter** house rules (naming + format + hygiene) to fork/keep
  - [`rules/jpa-house-rules.json`](rules/jpa-house-rules.json) — **JPA personal namespace**: measure `VAR` must start with `_`; measure must carry the `[Type/Created on/Created by]` metadata tag

## Run a rule set

- **UI:** *Tools → Best Practice Analyzer* (TE2/TE3), pick the rule set, review, apply fixes.
- **CLI (headless / CI gate):**

  ```bash
  # TE2 (free) — analyze, non-zero exit on violations = CI gate
  TabularEditor.exe "<model.bim | conn>" -A "tabular-editor/bpa/rules/BPARules-PowerBI.json"

  # TE3 — run the standard set + your namespaced house rules together (stack -A per file)
  TabularEditor3.exe "<model | PBIP folder>" -A "tabular-editor/bpa/rules/BPARules-PowerBI.json" -A "tabular-editor/bpa/rules/jpa-house-rules.json"
  ```

  For Power BI, `pbir bpa run` is an alternative execution path — see
  [`../../power-bi/04-review/bpa/`](../../power-bi/04-review/bpa/). This blueprint owns the **rule library**;
  run it via TE *or* `pbir`.

## The standard set (included) + your house rules

The canonical base — [`rules/BPARules-PowerBI.json`](rules/BPARules-PowerBI.json) — is vendored here from
Tabular Editor's [BestPracticeRules](https://github.com/TabularEditor/BestPracticeRules) repo (the
`BPARules-PowerBI.json` variant, tuned for Power BI models). Apply it first; layer your own rules via
[`rules/custom-rules.json`](rules/custom-rules.json).

Refresh the standard set any time:

```bash
curl -fsSL https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-PowerBI.json \
  -o tabular-editor/bpa/rules/BPARules-PowerBI.json
```

In the TE UI: *Tools → Manage BPA Rules → Import* the file (or point the CLI `-A` at it). To run **both**
sets at once, pass each with its own `-A`, or merge the JSON arrays into one file.
