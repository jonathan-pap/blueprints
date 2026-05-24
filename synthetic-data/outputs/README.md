# outputs/ — output layer

Generated datasets, dated. Naming:

```text
outputs/YYYY-MM-DD-<job>-<dataset>.<ext>
```

Example: `2026-05-24-demo-financials.csv`. Dates are absolute, never relative.

Bulky data files (`*.csv`, `*.parquet`, `*.json`, …) are git-ignored by default (see
`../.gitignore`) so the repo stays light. To track a small sample deliberately:

```bash
git add -f outputs/2026-05-24-demo-financials.csv
```
