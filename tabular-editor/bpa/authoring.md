# Authoring BPA rules

A rule set is a JSON **array of rule objects**. Each rule scopes to an object type, tests a boolean
**`Expression`** (Dynamic LINQ over the model objects), and optionally auto-fixes with a C#
**`FixExpression`**. Rules run in TE2 and TE3.

## Rule shape

```jsonc
{
  "ID": "MEASURES_MUST_HAVE_FORMAT_STRING",
  "Name": "Measures must have a format string",
  "Category": "Formatting",
  "Description": "Every measure should set a FormatString so visuals render consistently.",
  "Severity": 2,                       // 1 info · 2 warning · 3 error
  "Scope": "Measure",                  // Model, Table, Measure, Column, Hierarchy, Relationship, Partition, ...
  "Expression": "string.IsNullOrEmpty(FormatString)",   // TRUE = violation
  "FixExpression": "FormatString = \"#,##0\"",           // optional; C# applied on 'Apply Fix'
  "CompatibilityLevel": 1200
}
```

- **`Scope`** — which objects the `Expression` runs against (one or several, comma-separated).
- **`Expression`** — Dynamic LINQ evaluated per object; **`true` means the object violates the rule**.
  Use the same shared properties the scripts use (`Name`, `FormatString`, `DisplayFolder`, `Description`,
  `IsHidden`, `DataType`, `SummarizeBy`, `Expression`, …) so rules behave the same in TE2 and TE3.
- **`FixExpression`** — optional C#; follows the **[script portability rules](../compatibility.md)**
  (C# 7, shared API, no `SaveChanges()`).
- **`Severity`** — 1/2/3; CI gates typically fail on 3 (and optionally 2).

## Example rules

```jsonc
[
  {
    "ID": "MEASURE_NO_FORMAT_STRING", "Name": "Measure has no format string",
    "Category": "Formatting", "Severity": 2, "Scope": "Measure",
    "Expression": "string.IsNullOrEmpty(FormatString)",
    "FixExpression": "FormatString = \"#,##0\""
  },
  {
    "ID": "COLUMN_KEY_SHOULD_NOT_SUMMARIZE", "Name": "Numeric key should not summarize",
    "Category": "Data Model", "Severity": 2, "Scope": "Column",
    "Expression": "(Name.EndsWith(\"Key\") || Name.EndsWith(\"Id\")) && SummarizeBy != \"None\"",
    "FixExpression": "SummarizeBy = TabularEditor.TOMWrapper.AggregateFunction.None"
  },
  {
    "ID": "OBJECT_NO_DESCRIPTION", "Name": "Visible measure has no description",
    "Category": "Metadata", "Severity": 1, "Scope": "Measure",
    "Expression": "!IsHidden && string.IsNullOrEmpty(Description)"
  }
]
```

## Where rule sets live

- **File** (this repo) — `rules/*.json`, run via CLI `-A <file>` or imported into TE. Best for source
  control + CI.
- **Model annotation** — stored inside the model (`BestPracticeAnalyzer` annotation); travels with the
  model. Set in TE's *Manage BPA Rules*.
- **Shared URL** — a central rule set fetched by URL; good for org-wide standards.

## After

Run it (`_index.md`), review violations, apply fixes, then validate with
[`../../power-bi/04-review/`](../../power-bi/04-review/) for Power BI models.
