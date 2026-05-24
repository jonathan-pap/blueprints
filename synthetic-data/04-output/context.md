# 04-output — serialize & deliver

> Turn generated rows into files or loaded tables. Plain formats for general use, plus a
> Power BI hand-off that drops data straight into a semantic model.

## Targets

| Target | Use |
|---|---|
| **CSV / TSV** | universal import (any BI tool, Excel, DB bulk load) |
| **JSON / NDJSON** | APIs, document stores, nested data |
| **Parquet** | columnar, large volumes, analytics engines |
| **SQL INSERT** | seed scripts for a database |
| **Database load** | write directly to a table via a connection |
| **Power BI hand-off** | CSV-for-import or a TMDL table into a `.SemanticModel` → [handoff-to-power-bi.md](handoff-to-power-bi.md) |

## Conventions

- Name outputs `outputs/YYYY-MM-DD-<job>-<dataset>.<ext>` (absolute dates).
- Large datasets are git-ignored by default (see `../.gitignore`); commit small samples deliberately.
- Partition / compress large outputs where the consumer supports it.

## Planned atomic files (grow as needed)

- `format-csv.md`, `format-json-ndjson.md`, `format-parquet.md`, `format-sql-insert.md`
- `load-to-database.md` — connection-based table load
- `handoff-to-power-bi.md` — **written** (the bridge to the `power-bi/` blueprint)

## Hard rules

- Run `../05-review/context.md` before delivering.
- The Power BI hand-off writes into a PBI project folder by an explicit path — confirm the destination before writing.
