# Brief — demo financials (EXAMPLE)

> Filled example of `synthetic-data/01-brief/brief-template.md`. Generates the `financials` table
> the [Power BI — Sales Overview](power-bi-sales-overview.md) report runs on. Copy to
> `synthetic-data/projects/<name>/brief.md` and adapt.

Last updated: 2026-05-24

## 1. Purpose & consumer

- **Purpose:** populate a Power BI demo model with believable sales data.
- **Who/what consumes it:** the Power BI "Sales Overview" report (and its variance + Pareto pages).
- **Realism level:** business-plausible — skewed sales, weighted segments, a profit/discount relationship that makes the KPIs move.

## 2. Datasets & volume

| Entity / table | Rows | Notes |
|---|---|---|
| financials | 5,000 | single flat fact table (matches the demo model) |

## 3. Schema source

- [x] Match an existing schema: the test model's `financials` columns
- [ ] From scratch
- [ ] Mimic a real dataset

## 4. Fields, types & distributions

| Field | Type | Domain / pattern | Distribution | Null % |
|---|---|---|---|---|
| Product | category | {Carretera, Montana, Paseo, Velo, VTT, Amarilla} | weighted | 0 |
| Segment | category | {Government, Midmarket, Enterprise, Small Business, Channel Partners} | 30/25/20/15/10 | 0 |
| Country | category | {US, Canada, France, Germany, Mexico} | uniform | 0 |
| Month | date | 2014-01 … 2014-12 | uniform across months | 0 |
| Units Sold | integer | 100–4000 | right-skewed | 0 |
| Sale Price | decimal | {7, 20, 125, 250, 300, 350} by product | — | 0 |
| Sales | decimal | = Units Sold × Sale Price | derived | 0 |
| Discount % | decimal | 0–0.40 | beta (mostly low) | 2 |
| Profit | decimal | Sales × margin − discount effect | derived | 0 |

## 5. Constraints & relationships

- **Keys:** none required (flat fact); add a surrogate `id` if convenient.
- **Relationships:** none (single table).
- **Business rules:** `Sales = Units Sold × Sale Price`; `Profit < Sales`; `Discount %` applied before profit.
- **Temporal:** all 12 months of 2014 represented so the trend + variance pages fill out.

## 6. Reproducibility

- **Seed:** 42 (recorded in `seed.txt`).

## 7. Privacy / PII

- Fully synthetic; no real records or PII involved.

## 8. Output target

- **Format(s):** CSV (and/or TMDL table).
- **Destination:** Power BI model.
- **Power BI hand-off?** yes → `../power-bi/projects/test/test.SemanticModel/` (see `synthetic-data/04-output/handoff-to-power-bi.md`). Desktop closed during a TMDL splice.

## 9. Open questions

- [ ] One year (2014) or multi-year so the report can show YoY later?
- [ ] Generate a surrogate key, or keep the fact table key-less?
