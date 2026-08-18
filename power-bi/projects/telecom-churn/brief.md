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
| **Churn Rate** | `[Churn Rate]` | Churned ÷ (Churned + Stayed) — **exclude Joined** (they just arrived). **= 28.4%** (1,869 / 6,589). *Corrected 2026-08-18: this row previously said ≈26.5%, which is the churned/total figure, not this one.* | 0.0% |
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

## 7. Open questions — ANSWERED 2026-08-18

- [x] **Churn Rate denominator** — **churned/(churned+stayed) = 28.4%**. `[Churn Rate of Total]`
      (26.5%) is kept as a footnote on the KPI card so both numbers are visible and neither can be
      quoted by accident. The model measure previously used churned/total; fixed.
- [x] **"High value"** — **both, deliberately**. They rank customers *oppositely* and that
      disagreement is page 4's whole argument: lifetime-revenue Q1 churns **70.7%** while Q5 churns
      13.9%, yet Q5 is where **$1.51M** of the loss sits. Monthly-charge quintiles run the other way
      (Q4 37.0%). Rate finds the leavers; absolute value finds the money.
- [x] **Geography** — **City**, rolled up from zip. Keeps the population join available for v2.
      Shown as a ranked table, not a map: `azureMap` is the only non-deprecated map visual and it
      requires a signed-in Power BI account to render, so a map would have been a blank panel here.
- [x] **Joined customers** — third column on page 2 and the "new this quarter" KPI; **never** in a
      churn denominator. Note they sit entirely in the 0–6 month tenure band by definition.
- [x] **DimDate** — **dropped from the report.** No date FK exists and the brief rules out trend
      pages, so it has nothing to join to.

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

---

## 10. Build record — 2026-08-18

Rebuilt from scratch: the four hash-named pages were removed and replaced, with a new theme and a
layout contract.

### Theme — "Retention Signal (Light)"

Light, not dark: the audience is Power BI Service plus **a printable exec summary** (§1), and dark
themes print badly. `build_theme.py` generates it and **fails the build on any contrast miss**.

That audit earned its keep on the first run. The status triad started as three Okabe-Ito colours,
which are hue-separated but **not luminance-separated** — churned vs joined measured **1.09:1**,
i.e. indistinguishable in greyscale or to some CVD readers. Rebuilt as a deliberate luminance
ladder:

| role | hex | on white | luminance |
|---|---|---|---|
| Stayed | `#00558F` | 7.79:1 | 0.085 |
| Churned | `#B8480A` | 5.29:1 | 0.149 |
| Joined | `#B673A4` | 3.51:1 | 0.249 |

Mutual separation 1.47 / 1.51 / 2.22 — survives a mono printout. One honest trade-off falls out of
this: no colour can be both dark enough for 4.5:1 **text** and light enough to separate from
vermillion by luminance, so **Joined is graphical-only** and never used as a text fill.

SVG measures cannot read the theme, so hex lives in `[Clr *]` measures — one place to re-theme.

### Layout — `design-system.yaml` + `resolve_layout.py`

Every rectangle resolves from a 12×12 grid; region edges snap to 8 so adjacent regions tile with
exact 16px gutters. Nothing is hardcoded at the call site.

### `ProfileAttr` — the disconnected spine

Eight fact columns unioned into one Attribute+Value table with **no relationship**; the `[Attr *]`
measures opt in with `TREATAS`. Without it pages 2 and 3 would each need eight separate visuals,
because a `tableEx` can only group by columns it is given.

Two data-shape traps inside it:

1. Blank `Internet Type` means *no internet service* — labelled **None**, or it renders as an empty row.
2. `Online Security` / `Premium Tech Support` are **blank for those same no-internet customers**, and
   left in they produced three separate rows all describing the identical 1,344-customer cohort at
   8.4%. Filtered out — those add-ons only mean anything to internet subscribers.

### PBIR gotchas hit while building

| Symptom | Cause |
|---|---|
| `sortDefinition` rejected | it is a **sibling of `queryState`**, not inside it |
| `filterConfig` rejected | it belongs at the **root of visual.json**, not inside `visual` |
| TopN filter rejected | not `itemCount`/`topBottom` properties — it is a **subquery in `From`** plus an `In` against it |
| Shape panels invisible | a shape's fill is `objects.fill` with its own `show`; even set explicitly it would not render. Abandoned for headings-on-canvas + each visual carrying its own themed card |
| Two stacked titles on charts | setting container `title.text` renders the custom title **and** the auto-generated name. Headings are textboxes everywhere |
| Data labels unreadable | `labelPosition` Auto flips them *inside* long bars, where secondary ink on vermillion fails. Forced `OutsideEnd` |
| Every screenshot `Unknown pageId` | deleting **all** pages while Desktop is open invalidates its page registry; `reload` does not rebuild it — `powerbi-desktop open` does |
| Table sorted alphabetically | a `tableEx` cannot sort by a column it does not project — use `sortByColumn` on the column instead |

### Audit — `outputs/2026-08-18-telecom-churn-audit.md`

`audit_report.py` runs the §04-review quick checks plus design-system and theme compliance. It
found **44 off-snap coordinates** on its first run: `resolve_layout.py` snaps region *edges*, but a
helper that insets a region (heading strip + gap) reintroduced drift via a 6px gap. Fixed to 8.
Worth keeping precisely because it is *not* redundant with the resolver.

Final: 4 pages, 20 data visuals, 0 off-snap, 0 off-grid, 0 stray hex, `pbir validate` clean.
