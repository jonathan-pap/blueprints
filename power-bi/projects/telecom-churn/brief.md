# Brief — Telecom Customer Churn

Last updated: 2026-08-17

> Fictional California telco: phone + internet services to **7,043 customers**. Single **snapshot at the
> end of Q2 2022** (there is no month-by-month history — see the data note in §6). Each customer is
> labelled **Churned / Stayed / Joined** as of that quarter. Goal: understand *who* churns, *why*, and
> *how much revenue* is walking out the door — so retention can target the right people.

## 1. Audience & decision

- **Primary audience:** commercial / customer-retention leadership + a data analyst who acts on it.
- **Decision this report supports:** where to focus retention effort — which customer segments and which
  fixable drivers give the biggest reduction in churned revenue.
- **Decision cadence:** quarterly review (matches the snapshot grain); ad-hoc for retention campaigns.
- **Consumption channel:** Power BI Service (desktop first); a printable exec summary page is a plus.

## 2. Source data & model

- **Semantic model:** thick PBIP — `telecom-churn.SemanticModel` (data imported from the CSVs).
- **Source data (already loaded):**
  - `telecom_customer_churn` — 7,043 rows, one per customer, 38 columns (demographics, location,
    services, charges, status, churn reason).
  - `telecom_zipcode_population` — zip → population (for penetration / per-capita context).
  - `DimDate` — present, but the churn data has **no transaction date** (only `Tenure in Months`); see §6.
- **Grain:** one row = one customer at end of Q2 2022 (a snapshot, not events).
- **Refresh cadence:** static demo dataset — no live refresh.
- **Volume:** 7,043 rows (tiny; performance is not a concern).
- **Sensitive data:** none real (fictional); no sensitivity label required.
- **Model state today:** tables loaded; `_Measures` has only a `_blank` placeholder — **measures still to
  build** (candidate list in §3 / §9).

## 3. KPIs (the executive answer, 5 max)

Apply the 20%-change test — each earns a card only if it moves enough to matter.

| KPI | Measure (to build) | Definition / denominator | Format |
|---|---|---|---|
| Total Customers | `[Total Customers]` | `COUNTROWS(customer)` = 7,043 | #,##0 |
| **Churn Rate** | `[Churn Rate]` | Churned ÷ (Churned + Stayed) — **exclude Joined** (they just arrived). ≈ 26.5% | 0.0% |
| New Customers (this qtr) | `[Joined Customers]` | Status = "Joined" = 454 | #,##0 |
| Churned Revenue (lost) | `[Churned Revenue]` | `SUM(Total Revenue)` filtered to Churned | $#,##0 |
| Monthly Revenue at Risk | `[Churned Monthly Charge]` | `SUM(Monthly Charge)` of Churned (recurring $ lost/month) | $#,##0 |

> Churn Rate is the headline. Decide the denominator once and keep it everywhere: **churned / (churned +
> stayed)**. Reporting churned/total (including Joined) understates it — flag if leadership prefers that.

## 4. Pages & layout (4 pages = the 4 questions)

Each page answers exactly one of the recommended analyses. One insight per visual.

| # | Page | Question it answers | Key visuals |
|---|---|---|---|
| 1 | **Churn Overview** | Where do we stand? How many joined last quarter? | KPI row (§3) · status donut (Churned/Stayed/Joined) · **Churn Category** bar (Competitor / Dissatisfaction / Price / Attitude / Other) · top Churn Reasons table |
| 2 | **Customer Profile** | Churned vs Joined vs Stayed — are they *different*? | Status-segmented comparison: matrix/small-multiples across Contract, Tenure band, Age band, Married, Dependents, Internet Type, Monthly Charge band. Highlight where the three profiles diverge most. |
| 3 | **Churn Drivers** | What drives churn? | **Churn rate by segment** (not raw counts): by Contract, Tenure band, Internet Type, Payment Method, Offer, Premium Tech Support / Online Security. Key-influencers-style ranking; tornado of rate-vs-baseline. |
| 4 | **High-Value at Risk / Retention** | Are we losing high-value customers, and how do we keep them? | Value segmentation (Total Revenue / Monthly Charge deciles) × status · churned-revenue by value tier · **California map** (lat/long or zip) of churn concentration · shortlist table of high-value Month-to-Month churners to target. |

Page size 1280×720. Reading pattern F (analytical). 6–8 data visuals per page max.

## 5. Branding & style

- **Theme:** blueprint default (Segoe UI, accessible). No brand supplied.
- **Status colour convention (keep consistent on every page):** Churned = warm/alert, Stayed = neutral/
  positive, Joined = accent. Use a diverging or categorical set that's CVD-safe — never red/green alone.
- **Logo / font:** none required.

## 6. Constraints & non-goals

- **DATA NOTE — snapshot, not a time series.** There is **no churn-over-time trend** available: no event
  dates, only `Tenure in Months` and the Q2-2022 status label. So:
  - "Customers joined **last quarter**" = `Customer Status = "Joined"` (454). Don't try to build a monthly
    joins/churn line — the data can't support it.
  - `DimDate` has nothing meaningful to join to (no date FK). Either drop it, or repurpose it only if a
    synthetic "signup month = snapshot − tenure" is explicitly wanted (a modelling choice, not a given).
  - Tenure is the closest thing to a time axis — use **tenure bands** for cohort/retention curves.
- **Accessibility:** WCAG AA; meaning never by colour alone (pair status with label/icon).
- **Don't build:** time-trend pages, forecasting, or a predictive churn model (this is descriptive BI, not ML).
- **Deferred (v2):** per-capita penetration using the zip population table; a what-if retention simulator.

## 7. Open questions (answer these first)

- [ ] **Churn Rate denominator** — churned/(churned+stayed) [recommended] or churned/total? Pick one.
- [ ] **"High value"** — define by `Total Revenue` (lifetime to date) or `Monthly Charge` (recurring)? They
      rank customers differently; the retention shortlist depends on it.
- [ ] **Geography** — map by lat/long point density, or aggregate to City / Zip? (Zip enables the
      population join later.)
- [ ] **Joined customers** — include them anywhere besides the "new this quarter" count, or treat as
      out-of-scope for churn/profile comparisons?
- [ ] **DimDate** — drop it, or synthesise a signup-month from tenure for a cohort view?

## 8. References

- Source docs: [`data/telecom_data_dictionary.csv`](data/telecom_data_dictionary.csv) (field definitions),
  [`data/telecom_customer_churn.csv`](data/telecom_customer_churn.csv),
  [`data/telecom_zipcode_population.csv`](data/telecom_zipcode_population.csv).
- Well-known dataset (IBM "Telco customer churn", expanded 7,043-row version) — expect churn ≈ 26.5%.

---

## 9. Starter measures + analysis tips (grounding for the build)

**Measures to seed `_Measures`** (names above; MCP-first if Desktop is open, else TMDL):

```
Total Customers      = COUNTROWS ( telecom_customer_churn )
Churned Customers    = CALCULATE ( [Total Customers], telecom_customer_churn[Customer Status] = "Churned" )
Stayed Customers     = CALCULATE ( [Total Customers], telecom_customer_churn[Customer Status] = "Stayed" )
Joined Customers     = CALCULATE ( [Total Customers], telecom_customer_churn[Customer Status] = "Joined" )
Churn Rate           = DIVIDE ( [Churned Customers], [Churned Customers] + [Stayed Customers] )
Churned Revenue      = CALCULATE ( SUM ( telecom_customer_churn[Total Revenue] ), telecom_customer_churn[Customer Status] = "Churned" )
Churned Monthly Charge = CALCULATE ( SUM ( telecom_customer_churn[Monthly Charge] ), telecom_customer_churn[Customer Status] = "Churned" )
```

**Analysis tips**

- **Show churn *rate*, not churn *count*, when comparing segments.** A big segment has more churners just
  by size; rate reveals the real driver. Every §3-driver visual should plot `[Churn Rate]` by category.
- **Rank drivers against the 26.5% baseline.** A segment matters when its rate sits well above/below the
  overall line — add a constant baseline line so the eye reads the gap. Expect **Month-to-Month**,
  **short tenure**, **Fiber Optic**, and **electronic/mailed payment** to over-index for churn; **two-year
  contracts** and **tech-support/online-security add-ons** to under-index.
- **Let the data explain itself.** `Churn Category` + `Churn Reason` are captured *only for churned*
  customers — they give the qualitative "why" for free; put them on the Overview page.
- **Tenure bands as the retention curve.** Bucket `Tenure in Months` (0–6, 7–12, 13–24, 25–48, 49+) and
  show churn rate falling as tenure rises — the classic "survive the first year" story.
- **Value × risk is the money slide.** Cross value tier (Total Revenue deciles) with status: the story
  isn't "we lose customers", it's "we lose *these high-value* customers, and they're mostly Month-to-Month
  on Fiber — here's the shortlist to call." That's page 4's shortlist table.
- **Guard the `Customer ID` etc.** Set numeric IDs / lat / long / zip to `SummarizeBy = none` and hide keys
  so they never sum by accident.

## After filling this in

Tell Claude **"build the churn report"** — it'll confirm the §7 open questions, seed the §9 measures
(MCP-first if Desktop is open), propose the 4-page layout against `design-system.yaml`, then build.
