# Thin-report measure

DAX measure scoped to the report, not the model. Lives in `<project>.Report/definition/reportExtensions.json`. Use when the measure is report-specific and should NOT pollute the shared model.

## CLI

```bash
pbir extensions add measure "<project>.Report" \
  --name "Revenue Variance" \
  --table "_Report" \
  --expression "[Revenue] - [Revenue 1YP]" \
  --format-string "+#,##0;-#,##0"
```

## When to use

- Conditional-formatting helper measure for one report
- Variance/gap measure tied to a specific page's KPIs
- Quick formatting expression that isn't worth adding to the model

## When NOT to use

- The measure is useful in other reports → add to the model via `../../model/`
- The measure is a true business definition → it belongs in the model

## After

`../validate/validate.md`.
