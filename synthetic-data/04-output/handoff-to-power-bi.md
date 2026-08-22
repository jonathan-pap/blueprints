# Hand off generated data to a Power BI model

> Deliver synthetic data straight into a Power BI project so a model is populated without hunting
> for real source data. Targets the sibling `power-bi/` blueprint by path — fully decoupled.

## Two modes

| Mode | What it does | When |
|---|---|---|
| **CSV-for-import** | point Power Query at the dataset's `latest/` folder, then Get Data | simplest; user wires it once in Desktop |
| **TMDL table splice** | write a table into `<project>.SemanticModel/definition/tables/` so it appears on next open | no manual import; mirrors how `power-bi/projects/test/_build-svg-gallery.py` splices TMDL |

For a multi-table dataset, import from the stable run folder — `outputs/<job>/latest/` never changes
on regeneration, so the Power Query connection survives every re-run (only the data refreshes):

```text
synthetic-data/outputs/<job>/latest/<Table>.csv
```

## Where it writes (cross-blueprint, by path)

This blueprint never reaches into the Power BI repo internally — you supply the destination.
Default sibling target:

```text
../power-bi/projects/<project>/<project>.SemanticModel/definition/tables/<Table>.tmdl
../power-bi/projects/<project>/                                            # CSV dropped here or in outputs/
```

Confirm the destination project before writing. Power BI Desktop must be **closed** during a
TMDL splice — Desktop re-saves and would clobber an open model (see the power-bi blueprint's
"Desktop clobbers TMDL" rule).

## Worked example — populate `financials`

The `power-bi/projects/test` model has a `financials` table (Product, Segment, Month, Sales,
Profit, Discount). To generate 5,000 plausible rows:

1. **01-brief** → purpose "populate PBI test model", entity `financials`, 5,000 rows, seed fixed.
2. **02-schema** → match the existing columns + types; Segment/Product as weighted categoricals; Sales skewed; Discount 0–0.4; Month across a date range.
3. **03-generate** → Faker + distribution sampling; record seed.
4. **04-output (this file)** →
   - **CSV mode:** write `outputs/2026-05-24-test-financials.csv`; import in Desktop.
   - **TMDL mode:** write a `financials` table (or a staging table) into the test `.SemanticModel`, CRLF-preserving and idempotent, with Desktop closed.
5. **05-review** → schema conformance + key integrity + PII-leakage audit before delivery.

## Matching an existing model's schema

Read the target table's real column names/types first (so generated columns line up):

```bash
pbir model "../power-bi/projects/<project>/<project>.Report" -d
```

Use the canonical `Table.Field` names — don't guess from English. (This is the same
canonical-name discipline the power-bi blueprint enforces before binding.)

## The splice script (config-driven jobs) — SHIPPED

For any star built with the config engine, the TMDL-splice mode is one command:

```bash
python 04-output/handoff_to_pbi.py projects/<job>/config.yaml --target ../power-bi/projects/<project>
```

It reads the job's config + `outputs/<job>/latest/` CSVs and writes into `<project>.SemanticModel/definition/`:
`expressions.tmdl` (a `SourceFolder` parameter pointing at `latest/` — one place to repoint the whole
model), one typed import table per CSV (M partition: `Csv.Document(File.Contents(SourceFolder & "<Table>.csv"))`,
keys hidden/`isKey`, fact measure columns hidden + summed, floats rounded 2dp), `DimDate` marked as the
date table with sort-by columns wired, fact→dim `relationships.tmdl` on the `<Dim>Key` columns, a
`_Measures` home seeded with `Total <measure>` / row count / averages, and the `ref table` lines in
`model.tmdl` (idempotent). Desktop must be **closed** during the splice; the first open needs a Refresh.
Worked end-to-end: `projects/quest-ledger` → `../power-bi/projects/demo`.

## Hard rules

- Confirm the destination project path before writing; never write into an open Desktop model.
- Synthetic only — never hand off real records into a shared model.
- Validate via `../05-review/context.md` before the hand-off.
