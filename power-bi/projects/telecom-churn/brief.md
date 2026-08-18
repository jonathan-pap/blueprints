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

### Theme — "Spectrum Light v1.2"

Futuristic telecom: fibre and radio spectrum. Cyan-teal for a connected line, deep magenta for a
dropped one, electric violet for a new signal, on a cool near-white canvas. Light rather than dark
because the audience is Power BI Service plus a **printable exec summary** (§1).

| role | hex | on white | luminance |
|---|---|---|---|
| Stayed | `#0E7490` | 5.36:1 | 0.106 |
| Churned | `#9D174D` | 7.88:1 | 0.072 |
| Joined | `#9575F5` | 3.42:1 | 0.271 |

`build_theme.py` generates it and **fails the build on any miss** across three constraint families:
WCAG contrast, greyscale separation (1.47 / 2.31 / 1.57 — status survives a mono printout), and
**simulated colour blindness** (Viénot 1999, deuteranopia + protanopia).

That third check exists because the first palette used Okabe-Ito vermillion, and orange-vs-blue is
the safest possible pair — which is exactly *why* Okabe-Ito uses it. Moving to magenta therefore
had to be proven rather than assumed:

```
vermillion palette   worst CVD pair distance  0.228
spectrum palette     worst CVD pair distance  0.219
```

A 4 percent give, not a real loss. `CVD_MIN = 0.18` now guards it so a later edit cannot quietly
slide the palette toward indistinguishable.

An earlier version of this theme also failed its own audit before shipping: three Okabe-Ito colours
were hue-separated but **not luminance-separated** (churned vs joined measured 1.09:1, identical in
greyscale). Fixed by making the three a deliberate luminance ladder.

SVG measures cannot read the theme, so hex lives in `[Clr *]` measures — one place to re-theme.

### Following the theme room (corrected 2026-08-18)

The first cut of this theme was authored ad-hoc and skipped `02-build/theme/`. Re-done against
`create/checklist.md`, which caught six real gaps:

| Gap | Fix |
|---|---|
| No `$schema` | added as the **first key** (versioned GitHub URL) — without it you author blind |
| `textClasses` missing `dataTitle` | added |
| Wildcard missing `padding` | added — then **zeroed for `textbox`/`image`**, because it clipped heading textboxes and forced scroll indicators |
| No filter-pane styling | `outspacePane` + `filterCard` (Applied/Available) added |
| No `actionButton` chrome override | added |
| Unversioned filename, `name:` out of sync | `Spectrum-Light-v1.1.json` with matching `name:` per `where-themes-live.md` |

Validated with **`pbir theme validate`** (passes), and audited with **`pbir color list`** — 14 distinct
colours, all palette members plus the one measure-driven fill.

> **Power BI Desktop will not pick up an edit to a theme file in place.** Rewriting the same file
> has no effect however many times you reload — the padding fix above appeared to do nothing until
> the version moved v1.0 → v1.1. What actually forces the re-import is the theme's internal `name:`
> field: on import Desktop **re-registers the theme under a filename it derives from `name:`**,
> sanitised and uniquified — `"Spectrum Light v1.2"` came back as
> `Spectrum_Light_v1.2053488466004665725.json`, rewriting `report.json` and leaving a duplicate
> file behind. Bump the filename and `name:` together (which is exactly what the room's naming
> convention asks for), then repoint `report.json` at the intended filename — the registration
> holds across reloads after that.

> `audit/compliance.md` documents `pbir audit theme`, which **does not exist in pbir 0.9.25** (there
> is no `audit` command group at all). `pbir color list` plus `audit_report.py` cover the same ground.

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

Final: 4 pages, 0 off-snap, 0 off-grid, 0 stray hex, `pbir validate` clean.

## 11. Global chrome + the missing-rows bug — 2026-08-18 (second pass)

Three things were missing and one was silently wrong.

### Global chrome — legend + synced slicers on every page

`header` split into `header_title` (cols 1–7) and `header_filters` (cols 8–12), both **inside** the
existing title band — so the chrome cost no content height on any page.

- **Legend**: a `Status Legend` SVG measure in an `image` visual, right-aligned. Static content, but
  the swatch colours come from the `[Clr *]` measures, so a re-theme recolours it. `viewBox` is
  authored at exactly the container size (504×24) so the image maps 1:1 instead of letterboxing.
- **Slicers**: Contract · Internet · Tenure Band, classic dropdowns, `syncGroup` on all four pages
  so a selection carries across. Three is the cap the room sets.

**Customer Status is deliberately not a slicer.** It is the comparison axis the whole report is
built on: filtering it blanks two of the three columns in the profile matrix, collapses the waffle,
and makes the tornado compare a segment against a baseline that no longer exists. Status is
communicated by the legend instead; the slicers are attributes you would hold constant *while*
comparing statuses. Say the word if you want it as a slicer anyway.

### The profile matrix was missing 5 of its 29 rows

`Attr Share`'s `SWITCH` covered 6 of the 8 attributes in `ProfileAttr`. An unmatched `SWITCH`
returns BLANK, and a `tableEx` drops rows whose measures are all blank — so **Online security, Tech
support and Internet = None were absent with no error anywhere**. Not truncation, not a filter: rows
that were never drawn.

Two of them turned out to be among the strongest signals in the report:

| row | churners | stayers | divergence |
|---|---|---|---|
| Online security: No | 78.2% | 38.4% | **+39.8pp** |
| Tech support: No | 77.4% | 38.2% | **+39.2pp** |

Only `Attr Churn Rate` and `Attr Segment Customers` had the full 8 branches, which is why the
tornado on page 3 showed "Online security: No" while page 2 did not.

> **Rule:** when a disconnected spine drives a `SWITCH`, every value of the spine needs a branch.
> A missing one is invisible — it removes the row rather than erroring.

### The matrix was also scrolling

29 rows in one full-width table rendered 13. Split into two half-width tables (`profile_body_2`),
with one-line panel headings and the reading rule moved up to the page subtitle to buy the last two
rows. Both halves now show every row with nothing below the fold.

### Unlabelled bars on page 3

`Internet Type`, `Online Security` and `Premium Tech Support` are an **empty string, not BLANK**, for
the 1,526 customers with no internet — so three small multiples drew a nameless bar at 8.4%. Added a
calculated `[Internet]` column that labels that cohort `None` (slicer and category axis both bind
there), and excluded the not-applicable blank from the two add-on charts.

### The audit earned its keep again

It flagged 12 off-snap coordinates in the new chrome: 160px slicers left a 12px gap. 152px leaves 24,
which is a multiple of 8. It also flagged the three slicer origins as off-grid — correctly, since
they tile *inside* one region. Rather than whitelist the numbers, `churnkit.chrome_rects()` is now
the single source and `audit_report.py` imports it, so builder and auditor cannot drift.

### Theme v1.2 — slicer chrome

Added a `slicer` block to the theme (`header` + `items` + `selection`), so slicer styling lives in
the theme rather than on each visual. Both containers take `textSize`, **not** `fontSize` —
`fontSize` is silently ignored. Filename bumped v1.1 → v1.2 to force a re-import.

> **Correction (found in section 13):** the mechanism is not the filename. On import Desktop **re-registers the theme under a name it derives from the JSON's internal `name:` field**, sanitised and uniquified — `"Spectrum Light v1.2"` came back as `Spectrum_Light_v1.2053488466004665725.json`, with `report.json` and a duplicate file rewritten to match. So it is the internal `name:` that has to change, and the convention of keeping filename and `name:` in step is what makes bumping either one work. After repointing `report.json` at the intended filename the registration held across reloads.

Per `02-build/theme/where-themes-live.md`, `build_theme.py` now also writes the theme to the shared
library at `projects/themes/spectrum-light/`, so it is reusable outside this report.

## 12. Page 4 quintile panels — 2026-08-18 (third pass)

Compared against the reference design. Two problems: the panels were the wrong *form*, and one
of them was measuring the wrong population.

### 452 of the 454 Joined customers were sitting in Q1

`Revenue Quintile` cut its thresholds over `ALL(telecom_customer_churn)` — all 7,043, Joined
included. Joined customers are two months old, so nearly every one of them landed in the lowest
lifetime-revenue quintile:

| quintile | customers | churn base (churned + stayed) | rate |
|---|---|---|---|
| Q1 | 1,409 | **957** | 70.7% |
| Q2–Q5 | ~1,408 each | ~1,408 each | 13.9–30.5% |

`[Churn Rate]` excludes Joined from numerator *and* denominator, so Q1's bar was drawn from a base
a third smaller than every other bar on the chart — it was not a quintile.

Both quintile columns now rank within the **churn base**. Joined still receive a quintile so nothing
breaks; they just no longer move the boundaries. Bases came out at 1,317–1,322 across all five.

Q1 reads 61.2%, not 70.7%. Still the highest — the cheapest customers really do churn most — but now
it is comparable to the bars beside it.

> The reference's numbers (40.5% down to 18.2%) do not reproduce under either basis, so its
> quintiles were cut some third way. Ours is documented in the column description; if you know what
> the original did, it is a one-line change.

### The form was wrong too

A bar chart can show the rate but not the money beside it — and the money is the whole argument of
the page: **Q5 churns least and still loses the most, $1.44M**. Each panel is now a table:

`Quintile · SVG track bar · churn rate · money lost`

- **Sorted Q5 first.** The reader wants the most valuable customers at the top, not the cheapest.
- **Fixed 0–70% domain** rather than per-panel autoscale, so a bar in the revenue panel and one in
  the charge panel mean the same length. (The reference scales each panel to its own max, which
  makes its 41.8% bar look longer than its 40.5% one.)
- **A tick marks the 28.4% baseline**, so above/below average is readable without relying on colour;
  fill colour then reinforces it rather than carrying it alone.
- Footnote under each panel carrying the interpretation.

### The charge panel is not monotonic, and that is real

The peak is **Q4 at 36.9%, not Q5 at 32.5%** — the very highest bills skew to long-tenure fibre
contracts, which are sticky. The subtitle used to claim "premium plans churn most"; it now says what
the data says.

### Sizing a table against its rendered row height

At `rowPadding 4` / 10pt a row is ~35px, so five rows plus a header overflowed a 176px table and
Power BI drew a **scroll track with nothing to scroll to** — which reads as hidden data. At
`rowPadding 1` / 9pt a row is ~26px and it fits with slack. Same trap then hit the 32px footnote.
Measure the rendered row, do not guess it.

## 13. Tooltips — 2026-08-18 (fourth pass)

Every visual carrying an SVG measure was showing its raw `data:image/svg+xml;utf8,<svg …>`
string in the default tooltip. A report-page tooltip **replaces** the default outright, which
kills that and buys room for context no cell could hold.

### Four pages, not one

A tooltip only helps if its measures mean something in the context being hovered, and the four
contexts in this report do not share a vocabulary:

| page | reaches | why it is separate |
|---|---|---|
| `ttSegment` | 6 driver small multiples, both quintile tables, churn by city | plain fact context — `[Churn Rate]` and friends resolve |
| `ttAttr` | tornado, both halves of the profile matrix | ProfileAttr context — only the `[Attr *]` family resolves; plain `[Churn Rate]` is blank |
| `ttReason` | churn-category bar, reason table | reason rows are churned-only, so a churn rate would read **100% on every row** |
| `ttCustomer` | retention shortlist | one customer — shows the risk score *and which rules produced it* |

A tooltip built for the wrong context is worse than no tooltip: it renders a confident number
that is either blank or circular.

### A tooltip page cannot echo what you hovered

There is no built-in "current value" token, so `[TT Segment Label]` reads whichever dimension
is single-valued in the hover context and names it — `Contract · Month-to-Month`,
`Lifetime revenue · Q5 — highest`, `San Diego`. Order is most-specific-first: Churn Reason
beats Churn Category, because a reason row filters both.

`[Attr Label]` needed the same guard — with nothing in context its concatenation returned a
bare `": "`. It now falls back to `Hover one segment`.

### The customer tooltip shows its working

`[Risk Score]` is a transparent rule set, not a model, so `[TT Customer Why]` spells out which
rules fired: *"Score from: month-to-month +30, under 6 months tenure +25, fibre +15, no online
security +10, no tech support +10, bank withdrawal +10."* A score with no explanation invites
exactly the "is this AI?" question the brief rules out of scope.

### Theme v1.3 — card padding

The wildcard `padding` of 8/8/10/10 is right for a chart and wrong for a card: it ate 16px of a
64px tooltip card and clipped the caption descenders. `card` now takes 4/4/8/8. This is the
third time the wildcard padding has had to be overridden per visual type (`textbox`, `image`,
now `card`) — the pattern is that the checklist's wildcard suits *data* visuals, and anything
whose whole job is a line of text needs it relaxed.

### Sizing, again

The tooltip footers clipped their second line at 24px and drew a scroll indicator — the same
"there is more below" lie as the page-2 and page-4 tables. They get 40px. All tooltip geometry
is on the 8px snap, but the **region-edge** half of the audit now skips tooltip pages: a
320×240 popup is not on the 12×12 page grid, and grading it against one is cargo cult.
