# Model Context Brief (template)

> **Fill this in when the agent can't read your model** — no Power BI MCP, no live connection, no
> on-disk TMDL it can open. It hands the agent the model's shape + purpose so it works against **real
> object names** instead of guessing, whichever blueprint you're in (Power BI report work,
> Tabular Editor scripts/BPA, etc.).
>
> **Cross-cutting** — unlike the blueprint-specific templates, this one lives in the `briefs/` hub
> because it describes an *existing* model for *any* blueprint. Copy it, fill the blanks, and save the
> copy next to the work: `<blueprint>/projects/<name>/model-context.md` (or wherever you point the agent).
>
> **Rule for the agent:** with no way to introspect the model, treat a filled brief as the source of
> truth. If a needed detail is missing, **ask — don't invent** a table/column/measure name. Anything
> you rely on that isn't stated here, flag as an assumption.

Replace every `<…>` and delete the _italic hints_.

---

## 1. Identity & purpose

- **Model / dataset name:** `<e.g. Sales Analytics>`
- **Domain:** `<e.g. B2B wholesale sales>`
- **Purpose (decisions it supports):** `<e.g. monthly revenue + margin review by region/product>`
- **Audience / consumers:** `<e.g. sales ops, finance>`
- **Source system(s):** `<e.g. Dynamics 365 → Fabric Lakehouse>`

## 2. Environment (how the agent will touch it)

- **Working with:** `<Power BI Desktop | Tabular Editor 2 | Tabular Editor 3 | other>`
- **Model source:** `<PBIP/TMDL folder path | .bim path | live localhost:<port> | describe-only (no access)>`
- **MCP available?** `<no>` · **Live connection possible?** `<no>` · **On-disk TMDL readable?** `<no>`
- **Compatibility level:** `<e.g. 1600>` · **Host:** `<Power BI | Azure AS | SSAS | Fabric>`

## 3. Tables (the star)

_One row per table. Role = fact / dimension / calculated / parameter / disconnected._

| Table | Role | Grain (one row per…) | Approx rows | Notes |
|---|---|---|---|---|
| `<FactSales>` | fact | `<order line>` | `<2.4M>` | `<additive measures>` |
| `<DimDate>` | dimension | `<day>` | `<3,650>` | `<marked as date table>` |
| `<DimProduct>` | dimension | `<product>` | `<1,200>` | |
| `<_Measures>` | calc (measures-only) | — | — | `<home table for measures>` |

- **Schema shape:** `<star | snowflake | other>`

## 4. Key & special columns

_The columns work targets: keys, dates, sort-by, measure sources. Skip plain attributes._

| Table | Column | Type | Role | Notes |
|---|---|---|---|---|
| `<FactSales>` | `<ProductKey>` | Int64 | FK | `<→ DimProduct>` |
| `<DimDate>` | `<Date>` | DateTime | date (PK) | `<the date-table date column>` |
| `<DimDate>` | `<Month Name>` | String | attribute | `<sort by MonthNumber>` |
| `<FactSales>` | `<Sales Amount>` | Decimal | measure source | |

## 5. Relationships

| From (many) | Column | To (one) | Column | Active? | Cross-filter |
|---|---|---|---|---|---|
| `<FactSales>` | `<ProductKey>` | `<DimProduct>` | `<ProductKey>` | yes | single |
| `<FactSales>` | `<OrderDateKey>` | `<DimDate>` | `<DateKey>` | yes | single |

## 6. Date table (critical for time-intelligence)

- **Date table:** `<DimDate>` · **Date column (DAX):** `<'DimDate'[Date]>`
- **Marked as date table?** `<yes>` · **Fiscal year start:** `<January | e.g. July>`
- **Contiguous / covers all fact dates?** `<yes>`

## 7. Measures

- **Measures live in:** `<_Measures>` _(home table)_
- **Naming convention:** `<e.g. 'Total <thing>' for base; '<base> YoY %' for derived>`
- **Key base measures** _(name → what it computes, plain English)_:

| Measure | Computes | Format | Folder |
|---|---|---|---|
| `<Total Sales>` | `<SUM of Sales Amount>` | `<$#,##0>` | `<Headline>` |
| `<Total Cost>` | `<SUM of Cost>` | `<$#,##0>` | `<Headline>` |
| `<Margin %>` | `<(Sales-Cost)/Sales>` | `<0.0%>` | `<Ratios>` |

## 8. Conventions & standards

- **Tables / columns:** `<e.g. PascalCase, Dim*/Fact* prefixes>`
- **Measures:** `<e.g. Title Case, no prefixes>`
- **Technical/key columns:** `<e.g. end with 'Key', hidden>`
- **Format strings:** `<currency $#,##0 · percent 0.0% · integer #,##0>`
- **Display folders:** `<used? scheme?>`

## 9. Constraints — do NOT touch / handle with care

- **Calculation groups:** `<none | name + purpose>`
- **RLS roles / security:** `<none | roles>`
- **Perspectives / translations:** `<none>`
- **Partitions / refresh:** `<notes; e.g. incremental refresh on FactSales>`
- **Off-limits objects:** `<anything the agent must not modify or rename>`

## 10. The task

- **Goal:** `<e.g. add PY/YTD/YoY% for Headline measures; format every measure; run BPA + fix>`
- **Scope:** `<whole model | specific tables/measures>`
- **Deliverable:** `<measures | C# script(s) | BPA rule set | report visuals | documentation>`
- **Definition of done:** `<e.g. BPA clean at severity ≥2; every measure formatted + foldered>`
