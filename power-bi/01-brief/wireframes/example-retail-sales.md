# Example — Wireframe & Story Brief: Retail Sales

> A **filled example** of [`brief-template.md`](brief-template.md), to show what "good" looks like before
> you draft a story + wireframe. Built from a **provided model diagram** (a Sales star — see §6); the model
> doesn't need to exist yet — describing it is enough to brief the wireframe. Feeds prompts **A→E** in
> [`prompts.md`](prompts.md).

## 1. The decision (why this report exists)

- **The one decision it drives:** where to focus next quarter to grow retail sales — which stores, product
  categories, and customer segments to push, and where reported sales are being helped/hurt by FX.
- **Who decides / who reads:** commercial leadership + regional store managers; medium data-literacy.
- **When / where used:** monthly business review on a boardroom screen; self-serve on laptops between reviews.

## 2. The questions (in order)

1. Are we hitting the **sales target** overall, and up or down **vs last year**?
2. Which **stores / regions** are driving or dragging the number?
3. Which **product categories / products** are growing or declining?
4. Who are the **top customers / segments**, and is the mix healthy (not over-concentrated)?
5. Is **currency (FX)** flattering or hurting reported sales?
6. Where exactly to act — **which store × product** combinations?

## 3. Key numbers (KPIs / headline measures)

- **Headline KPIs:** Total Sales (reporting currency), Sales vs Target, YoY %, # Transactions (or Units).
- **Supporting:** Sales by Store/Region, Sales by Product Category, Sales by Customer Segment, Sales trend
  (monthly), FX impact (reported − constant-currency).
- **Comparisons / context:** vs Target, vs PY, constant-currency vs reported.

## 4. Story arc

- **Preferred arc:** Overview → Analysis → Detail.
- **Approx page count:** 4.
- **Must-have pages:**
  1. **Executive Summary** — Q1 (are we on plan, where's the gap).
  2. **Stores & Regions** — Q2.
  3. **Products & Customers** — Q3 + Q4.
  4. **Sales Detail** — Q6 (store × product × date, drill-through target). *(FX / Q5 shown as a strip on the summary.)*
- **Entry point:** Executive Summary.

## 5. Layout constraints

- **Canvas:** 1280×720 (16:9). **Device:** desktop primary; a phone layout for the summary later.
- **Navigation:** page tabs; **drill-through** from Stores/Products into Sales Detail.
- **Must-fit elements:** company logo, **currency selector**, global **date slicer**, last-refresh stamp.
- **Branding/tone:** TBD — neutral corporate; decide in `../../02-build/report/references/` before build.
- **Filters:** global rail — Date, Region/Store, Product Category, Reporting Currency.

## 6. Data reality (the provided model)

_Provided as a schema diagram — a **Sales star**. Illustrative; not a live model yet._

- **Fact:** `Sales` — grain: **one row per sales line** *(the optional `Orders`/`OrderRows` variant would make
  it one row per order line — pick one before build).*
- **Dimensions:** `Customers` (name, segment), `Products` (category, name), `Stores` (name, region),
  `Dates` (calendar — the date table), `CurrencyExchanges` (rate per currency × date, for reporting-currency
  conversion).
- **Assumed measures:** `Total Sales` (SUM of a sales-amount column, converted via CurrencyExchanges),
  `Quantity`/`Units`, `# Transactions`.
- **Grain / range:** daily; assume ~2–3 years for YoY.
- **⚠ Gaps:** **no cost/margin** in the schema → *Margin %* can't be built until a Cost measure exists;
  **no target table** → *vs Target* needs a Target added (a disconnected table or a measure). Flag both now.

## 7. Output & review

- **Fidelity:** text wireframe + an **HTML/SVG mockup** ([`handoff.md`](handoff.md)) for sign-off.
- **Who signs off:** commercial lead + one store manager.
- **Definition of done:** every page answers one of the §2 questions; the two data gaps (margin, target) are
  resolved or explicitly deferred; wireframe signed off before any PBIR is written.

---

### Next (run the room on this brief)

1. **Prompt A** → story arc + ordered page list (should land the 4 pages above).
2. **Prompt B** per page → ASCII wireframe (e.g. Exec Summary: KPI row → hero *Sales vs Target by Region*
   bar → *Sales trend* line → FX strip → detail table).
3. **Prompt C** → critique vs this brief (does each page answer its question? are the margin/target gaps
   handled?).
4. **Prompt E** → the portable JSON spec → **Claude HTML mockup** or **Figma frames** via
   [`handoff.md`](handoff.md).
