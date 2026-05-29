# outputs/ — output layer

Generated datasets. Two shapes:

**Single-file dataset** — flat + dated:

```text
outputs/YYYY-MM-DD-<job>-<dataset>.<ext>      e.g. 2026-05-24-demo-financials.csv
```

**Multi-table dataset** — a run folder with clean table names (no long shared prefix):

```text
outputs/<job>/
├── latest/                  current run — Power BI hand-off imports from here (stable path)
│   ├── DimItem.csv
│   ├── FactTrade.csv
│   └── _manifest.json       seed, scale, date range, per-table row counts
└── runs/                    snapshots, only when the generator runs with --archive
    └── YYYY-MM-DD-<scale>/
```

`latest/` is overwritten each run; `_manifest.json` keeps the folder self-describing. Dates are
absolute, never relative.

Bulky data files (`*.csv`, `*.parquet`, `*.json`, …) are git-ignored by default (see
`../.gitignore`) so the repo stays light — including everything under `outputs/<job>/`. To track a
small sample or a manifest deliberately:

```bash
git add -f outputs/grand-exchange/latest/_manifest.json
```
