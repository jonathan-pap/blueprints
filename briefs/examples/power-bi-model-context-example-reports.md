# Model Context Brief — "example reports"

> Generated from the on-disk TMDL at `power-bi/projects/test/example reports.SemanticModel/` on 2026-08-12. A map of the model
> so an agent can work against **real object names** without introspecting it live. Follows the template
> at [`../../../../briefs/model-context-brief.md`](../model-context-brief.md).
> Row counts aren't in TMDL (data lives in the model cache) — refresh in Desktop to confirm.

## 1. Identity & purpose

- **Model / dataset name:** `example reports`
- **Domain:** two subject areas in one model — **(a)** a global **item-marketplace price tracker** (daily
  OHLC prices per item) and **(b)** the classic **Financial Sample** (sales by segment/country/product).
- **Purpose:** a **demo / gallery** model — showcases native visuals, SVG in-cell micro-charts, and DAX
  recipes (candlestick, pareto, actual-vs-target, waterfall, disconnected-selection emphasis).
- **Audience:** developers / learners (example + test model, not production).
- **Source:** synthetic — Microsoft **Financial Sample** + generated daily market OHLC data.

## 2. Environment

- **Working with:** Power BI Desktop / Tabular Editor.
- **Model source:** PBIP/TMDL folder — `power-bi/projects/test/example reports.SemanticModel`.
- **MCP available?** yes (Modeling MCP, when Desktop is open) · **Live connection?** yes (local instance)
  · **On-disk TMDL readable?** yes (this brief was generated from it).
- **Host:** Power BI (PBIP).

## 3. Tables

_Two facts (one star, one flat) + 2 dimensions + a measures home + 5 disconnected calc tables._

| Table | Role | Grain (one row per…) | Approx rows | Notes |
|---|---|---|---|---|
| `FactMarketPriceDaily` | fact | item × day | (data) | OHLC: Open/High/Low/Close/Avg + Volume, ListingsCount |
| `DimDate` | dimension | day | (data) | date dimension for the **market star** |
| `DimItem` | dimension | item | (data) | ItemName, ItemCategory |
| `financials` | fact (flat) | Segment×Country×Product×Discount×Month | ~700 | Financial Sample; **standalone, no relationships** |
| `_Measures` | calc (measures home) | — (ROW placeholder) | 1 | holds all 77 measures |
| `financials Date Slicer` | disconnected calc | `VALUES(financials[Date])` | — | drives time-window recipe |
| `Price Slicer` | disconnected calc | `VALUES(financials[Sale Price])` | — | drives numeric-band recipe |
| `Product Slicer` | disconnected calc | `VALUES(financials[Product])` | — | drives category-spotlight recipe |
| `Year Slicer` | disconnected calc | `VALUES(financials[Year])` | — | drives comparison-period recipe |
| `Waterfall Steps` | disconnected calc | step (Sales/COGS/Profit) | 3 | drives the waterfall recipe |

- **Schema shape:** a **star** (FactMarketPriceDaily + DimDate + DimItem) **beside a flat table** (financials),
  plus 5 **intentionally disconnected** calc tables.

## 4. Key & special columns

| Table | Column | Type | Role | Notes |
|---|---|---|---|---|
| `FactMarketPriceDaily` | `DateKey` | Int64 | FK | → DimDate |
| `FactMarketPriceDaily` | `ItemKey` | Int64 | FK | → DimItem |
| `FactMarketPriceDaily` | `OpenPrice`/`ClosePrice`/`HighPrice`/`LowPrice`/`AvgPrice` | Double | measure source | candlestick OHLC |
| `FactMarketPriceDaily` | `Volume`, `ListingsCount` | Int64 | measure source | volume pane |
| `DimDate` | `DateKey` | Int64 | PK | |
| `DimDate` | `Date` | DateTime | **date column** | date-table date |
| `DimItem` | `ItemKey` | Int64 | PK | |
| `financials` | `Date` | DateTime | **date column** (financials context) | inline; no date dimension |
| `financials` | `Product` / `Segment` / `Country` | String | attribute + slicer source | |
| `financials` | `Sale Price` / `Year` | Int64 | slicer source | feed Price / Year slicers |
| `financials` | `Sales` / `COGS` / `Profit` / `Units Sold` | Double | measure source | headline measures |
| `financials` | `MonthKey` | String | calc column | `FORMAT(Month Number,"00") & FORMAT(Year,"0000")` |

## 5. Relationships

| From (many) | Column | To (one) | Column | Active? | Cross-filter |
|---|---|---|---|---|---|
| `FactMarketPriceDaily` | `DateKey` | `DimDate` | `DateKey` | yes | single |
| `FactMarketPriceDaily` | `ItemKey` | `DimItem` | `ItemKey` | yes | single |

- **`financials` is standalone** (flat Financial Sample — no relationships).
- **All 5 slicer/step tables are disconnected by design** — do **not** relate them; the recipes harvest the
  selection with `SELECTEDVALUE` / `MIN` / `MAX` so it doesn't filter the data.

## 6. Date table

- **Market star:** `DimDate`, date column `'DimDate'[Date]` — the date dimension for `FactMarketPriceDaily`.
- **Financials context:** uses the **inline** `'financials'[Date]` (there is no relationship from financials
  to DimDate), so financials time-intelligence runs off its own Date column. **Two date contexts — mind
  which measure uses which.** Confirm "Mark as date table" on `DimDate` in Desktop.

## 7. Measures

- **Measures live in:** `_Measures` (77 measures, 14 numbered display folders).
- **Naming convention:** Title Case, no prefixes; `Total <thing>` for headline; recipe measures grouped by
  numbered folder.

| Folder | Count | Purpose |
|---|---|---|
| `1. Headline` | 4 | `Total Sales/Units/Profit/COGS` (SUM over financials) |
| `2. Ratios` | 2 | `Profit %`, `Discount %` |
| `3. Time Intelligence` | 2 | `Sales PY`, `Sales YTD` (on `financials[Date]`) |
| `4. Averages` | 1 | `Avg Sale Price` |
| `13. OHLC Candlestick` | 23 | Open/Close/High/Low + body/wick/volume/MA/tooltip (on FactMarketPriceDaily) |
| `5. SVG` + `7. SVG gallery` | 4 + 10 | in-cell SVG micro-charts (sparkline, bullet, lollipop, boxplot…) |
| `6. Time window` / `7. Numeric band` / `8. Comparison period` / `9. Spotlight` | 2/2/3/1 | disconnected-selection harvesters + emphasis colors |
| `A. Pareto (model)` | 5 | cumulative %, bar color, # products to 80% |
| `B. Actual vs Target` | 11 | target, delta, %, min/max, narrative |
| `C. Waterfall` | 7 | `WF Base`/`Body`/`Label`/`Axis Max`/`Anchor` (P&L bridge Sales→COGS→Profit) |

## 8. Conventions & standards

- **Tables:** `Dim*` / `Fact*` for the star; `financials` flat (Financial Sample naming); disconnected
  helpers named `<X> Slicer` / `Waterfall Steps`; `_Measures` (underscore) is the measures home.
- **Columns:** `*Key` = integer surrogate keys (FK/PK).
- **Measures:** Title Case; organized into `<n>. <Group>` display folders.
- **Format:** currency `$`, percent, integer — set per measure.

## 9. Constraints — handle with care

- **Disconnected tables are intentional** — never add relationships for `*Slicer` or `Waterfall Steps`;
  they drive recipe harvesters. Relating them would break the emphasis logic.
- **`financials` is deliberately flat** (no dimensions) — the Financial Sample as shipped.
- **`Waterfall Steps` is a calc table** — needs a refresh to compute after model load.
- **No** calculation groups, RLS roles, perspectives, or translations detected.

## 10. The task

_(Documentation brief — no task yet.)_ State your goal here when you want work done, e.g.:
- **Goal:** `<e.g. mass-format all measures; add YTD/PY for headline measures; run BPA + fix>`
- **Scope:** `<whole model | specific tables/measures>`
- **Deliverable:** `<measures | TE script | BPA rule set | report visuals | documentation>`
