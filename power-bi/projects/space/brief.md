# Brief — Space Missions (single-page launch cadence)

Last updated: 2026-08-16

## 1. Audience & decision

- **Primary audience:** general / enthusiast + analyst. Exploratory, not operational.
- **Decision this report supports:** *"How did orbital launch cadence evolve from 1957 to 2022, and
  who drove each era?"* — a single-screen narrative you scrub through by decade.
- **Decision cadence:** on-demand. Static historical dataset; no refresh loop.
- **Consumption channel:** Power BI Desktop / Service, desktop screen. Not mobile, not print.

## 2. Source data & model

- **Semantic model:** thick PBIP — `example reports.SemanticModel`, import mode.
- **Source:** `projects/space/data/space_missions.csv` — 4,630 rows, one row per launch, 1957-10-04
  to 2022. **This is the only permitted source** (confirmed 2026-08-16). No external lookups, no
  hand-authored fact data.
- **Refresh cadence:** none — one-time load of a static file.
- **Volume:** 4,630 rows. Trivial; no performance concerns.
- **Sensitive data:** none.

### Columns (from `space_missions_data_dictionary.csv`)

| Field | Notes for the build |
|---|---|
| `Company` | 62 distinct. Top: RVSN USSR (1777), CASC (338), Arianespace (293), SpaceX (182). |
| `Location` | Free-text `"Site, Pad, Country"`. Needs splitting if ever used — **not needed for v1**. |
| `Date` | `YYYY-MM-DD`, 1957–2022, **66 distinct years**. The report's spine. |
| `Time` | UTC `HH:MM:SS`. Not used in v1. |
| `Rocket` | Rocket name. Not used in v1. |
| `Mission` | Mission name. Used only in the events tooltip. |
| `RocketStatus` | Active (1010) / Retired (3620). Not used in v1. |
| `Price` | **73% blank (3,365 of 4,630).** See §6 — no cost measure. |
| `MissionStatus` | Success 4162 · Failure 357 · Partial Failure 107 · Prelaunch Failure 4. |

### Three data traps the build must handle

1. **The CSV is mixed-encoding** — *corrected 2026-08-16, an earlier draft of this brief wrongly
   called it latin-1 and prescribed `Encoding=28591`; that would have corrupted the rows that were
   already fine.* 4,623 lines are valid UTF-8, but **7 lines are cp1252** (`Alcântara`, `Maranhão`
   — byte `0xE2`/`0xE3`). Neither encoding reads the whole file: UTF-8 hard-fails on the 7,
   cp1252 mangles the rest (`Pléiades` → `PlÃ©iades`). A default UTF-8 import silently substitutes
   U+FFFD and **loses those characters**.
   **Fix applied:** `data/space_missions_clean.csv` — decoded per line (UTF-8, cp1252 fallback),
   written as clean UTF-8. The model now loads that file with `Encoding=65001`.
   The original M also had `QuoteStyle=QuoteStyle.None` despite quoted comma-bearing fields; the
   rebuilt partition uses `QuoteStyle.Csv`.
2. **`DimDate` is stale scaffold and must be rebuilt.** The existing table was copied from the
   grand-exchange project: it sources
   `synthetic-data/outputs/grand-exchange/latest/DimDate.csv` and filters `DateKey >= 20260101`.
   It covers **none** of 1957–2022. Rebuild it as a generated calendar over the fact date range.
3. **2022 is a partial year.** The dictionary states status is "as of August 2022", and 2022 has 93
   launches vs 157 in 2021. The final column is **not** a real decline — it must be visually
   distinguished (hatched / lower opacity) or the chart tells a lie.

## 3. Measures

No KPI cards — this is a single-chart page by request. The measures exist to drive the one visual.

| Measure | Purpose | Format |
|---|---|---|
| `[Launches]` | `COUNTROWS(Missions)` — the column height. | `#,##0` |
| `[Is Selected Decade]` | Membership test against the disconnected decade table. | `0` |
| `[Column Color]` | Spotlight colour — accent when in selected decade, muted grey otherwise. | text |
| `[Event Label]` | Event text for a year, blank outside the selected decade. | text |
| `[Event Marker]` | Marker Y-position for years that carry an event; blank otherwise. | `#,##0` |

Deliberately **not** built: any measure over `Price` (§6), success-rate measures (v2 — see §6).

## 4. Pages & layout

**One page. One chart. 1280 × 720.** Theme handles all colour — no per-visual hex.

```text
┌──────────────────────────────────────────────────────────────────────┐
│  ORBITAL LAUNCH CADENCE            4,630 launches · 1957–2022        │  title textbox
│                                                                      │
│  [1950s][1960s][1970s][1980s][1990s][2000s][2010s][2020s]           │  8 decade toggles
│                                                                      │
│   160 │                                          ▐                   │
│       │                                          ▐ ▐                 │
│   120 │      ░░░░░░░░                          ▐▐▐▐▐                 │
│       │    ░░░░░░░░░░░░░░                     ▐▐▐▐▐▐▐                │
│    80 │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▐▐▐▐▐▐▐▐░              │  column chart
│    40 │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▐▐▐▐▐▐▐▐▐░              │
│     0 └──────────────────────────────────────────────────────        │
│        1957      ▲            ▲         ▲    1990s selected  ▲2022⁺  │
│                  └─ event markers, labelled only in selection        │
└──────────────────────────────────────────────────────────────────────┘
```

- **Toggles = 8 buttons, not 7** (1950s, 1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020s). A tile
  slicer over a **disconnected** decade table, styled as chiclets. Multi-select allowed.
- **Chart = clustered column, NOT a line chart.** The spotlight works by binding `dataPoint.fill`
  per point; a line chart has one continuous stroke and cannot colour individual years. This is the
  one place the original idea has to bend — the interaction requires columns.
- **X axis = every year, 1957–2022** (66 columns). All 66 stay visible at all times; the decade
  selection only ever changes *colour*, never what is shown. That is the whole point of the pattern.
- **Event markers** ride on the same visual as a second series (line-and-column combo), so "one
  chart" still holds. Labels render only for the selected decade — typically 1–3 at a time.
- **2022 column** gets a distinct treatment plus a `⁺ partial year` axis note.

## 5. The interaction — reuse an existing recipe

You were right that this exists. Use
[`02-build/recipes/disconnected-selection-emphasis/`](../../02-build/recipes/disconnected-selection-emphasis/context.md),
specifically the [**category-spotlight**](../../02-build/recipes/disconnected-selection-emphasis/variants/category-spotlight.md)
variant — a disconnected slicer drives a *colour property* rather than a filter.

| Primitive | Applied here |
|---|---|
| P1 selection table | `Decades` — `VALUES` over a derived decade column, **no relationship** |
| P2 harvest | `[Is Selected Decade]` membership test, plus `[Band Start]` / `[Band End]` boundaries |
| P3 band | **included** (added 2026-08-16) — background highlight behind the selected decade |
| P4 conditional series | `[Event Label]` / `[Event Marker]` gated by the selection |
| P5 self-filter wiring | slicer self-filter; chart keeps its own axis scope |

### P3 — the background band

Two `xAxisReferenceLine` entries at `[Band Start]` / `[Band End]`, both shading `'before'`: the end
line tints everything before it at 88% transparency, the start line re-shades everything before *it*
opaque in the card colour `#0F1528`, erasing the pre-band area. Both lines are themselves invisible
(`transparency: 100`) — only their shading shows.

Three constraints this imposes, all learned the hard way:

1. **X-axis reference lines need a `Scalar` (continuous) axis.** `DimDate[Year]` is Int64 so it can
   be scalar, but switching axis type has two side effects: the axis auto-ranges **from 0** unless
   pinned (which collapses all 66 years into a sliver), and numeric labels gain thousand separators.
   Fixes: `categoryAxis.start = 1956.5` / `.end = 2022.5`, and `formatString: 0` on `DimDate[Year]`.
2. **The band cannot represent a non-contiguous selection.** `MIN`/`MAX` collapse the selection to
   its edges, so 1970s + 2010s would tint the unselected 1980s–2000s between them. `[Band Start]` /
   `[Band End]` therefore carry a contiguity guard — `(_max - _min) = (_n - 1) * 10` — and return
   blank when the selection has gaps. The band disappears; the per-column spotlight still marks the
   right decades. Single or adjacent decades get the band; gapped selections don't.
3. **Band edges sit at ±0.5 of a category** so the boundary columns are fully covered. `[Band End]`
   is additionally capped at the last year with data, so the final decade's band doesn't run into
   the empty axis headroom reserved for labels.

### Event markers — connector + text label

Added 2026-08-16, following
[`recipes/actual-vs-target-variance`](../../02-build/recipes/actual-vs-target-variance/primitives/error-bar-variance-connector.md).

`[Event Marker]` floats 12 units **above** the column top; `[Event Stem Base]` sits at the column
top. A native **error bar** between them draws the connector, so each event year reads as a pin:
column → amber stem → dot → text.

Four mechanics that are easy to get wrong:

1. **Error bars need TWO `objects.error` entries.** A *style* block (`barColor`, `barWidth`,
   `markerShow`) keyed by `metadata`, plus a *range* block (the measure bounds) keyed by
   `dataViewWildcard`. `pbir visuals error-bars add` writes only the range block — the stem then
   renders as an uncontrollable hairline.
2. **Per-series data labels use `showSeries`, not `show`.** `labels.show` is the visual-level master
   switch and must be `true`, then `showSeries` turns each series on/off. Setting only `show` on a
   series selector silently does nothing.
3. **`labelPosition` is series-type-specific** — `'Above'` for the line/marker series;
   `'OutsideEnd'` is column-only and is ignored on a line.
4. **Text in a numeric data label comes from a dynamic format string.** `[Event Marker]` is numeric;
   its `formatStringDefinition` returns the event text wrapped in **literal double quotes**
   (`"""" & _txt & """"`), which the label renders as words. Outside the selected decade it returns
   an empty literal (`""""""`) so the label vanishes but the marker stays. Requires
   `compatibilityLevel >= 1601` (model is 1606), and a measure may **not** carry both `formatString`
   and `formatStringDefinition` — the server rejects it outright.

Axis consequence: the label needs vertical room, so `valueAxis` runs 0–200 (**both** primary and
`secEnd`, or the markers detach from the columns) and `categoryAxis` spans 1953.5–2024.5 so labels
on the first and last decades aren't clipped by the plot edge.

### Label collision — what works and what doesn't (tested 2026-08-16)

Three consecutive event years (1957, 1958, 1959) can't all show a label. Three things were tried:

| Change | Result |
|---|---|
| Extend `categoryAxis` left (1956.5 → 1953.5) | Helped the **1957** label, which was genuinely clipped by the plot edge. Keep it. |
| **Stagger marker heights** — `[Launches] + 14 + _tier * 20`, `_tier = MOD(rank-1, 3)` over event years | Keep it. Adjacent event years sit at three different heights, so the surviving labels no longer overlap each other. |
| Shorten the label — lead with the most notable event (`Record` if present) + `"+N"` | Keep it. A 3-event year produced a ~250px label; now ~130px. |
| Widen the stagger (step 20 → 28, axis → 230) | **Reverted — no effect.** 1958 still dropped, and the taller axis visibly compressed the columns. |

**Conclusion: Power BI culls line-series data labels by horizontal proximity alone — vertical
separation does not buy you a label back.**

Tested further: suppressing the 1959 label did **not** make 1958 appear, so it is not a
"two per cluster" quota either. **Two *directly adjacent* event years can never both be labelled** —
the category pitch is ~17px and the shortest label ("NASA") is ~50px, so the earlier year's label
occupies its neighbour's slot and the neighbour is dropped regardless of width, height or tier.
1957 beats 1958 every time.

Consequence: **the chart cannot surface every debut, so the narrative does.** `[Decade Takeaway]`
now ends with "First launches: …" naming the decade's three most significant operator debuts by
`EventWeight` plus a `+N more` remainder. NASA (1958, weight 203) is invisible on the chart by
construction and appears there instead. Don't spend more time fighting the labels — the ceiling is
in the visual, and the narrative is the right home for what doesn't fit.

### The narrative is a `tableEx`, not a card

`cardVisual` renders its subtitle in a fixed-height header and leaves the body empty, so a long
sentence truncates ("…succeeded. First lau…") while most of the card sits unused. The narrative is
therefore a **`tableEx`** bound to `[Decade Takeaway]` with `wordWrap: true`, header blanked the same
way as the tooltip (`displayName " "` + header painted into the background), `grid` off and
`stylePreset: 'None'`. It wraps and uses the full area. The decade heading rides the visual title
as a measure (`[Decade Scope Label]`).

**Final form: one name per marker.** The label shows the `EventShort` of the year's **earliest**
event by `Events[EventDate]` — nothing joined, no `"+N"`. Both of those were tried and rejected:
joining made multi-event years two to three times wider than their neighbours, which is precisely
what got them culled. A single name puts every marker in the same width class (~90–110px), so a
3-event year is no longer the odd one out.

`Events[EventDate]` exists for this: the real first-launch date for a debut, 31 Dec for a record.
That makes the pick deterministic and sensible — 1958 resolves to **US Air Force** (17 Aug) ahead of
NASA (11 Oct) and the year's failure-rate record. Full detail stays in the canvas tooltip.

### ⚠️ `reload` does not re-read `formatStringDefinition`

Editing a `formatStringDefinition` in the TMDL on disk and running `powerbi-desktop reload` leaves
the **old** format string live — verified by `measure_operations Get`, which still returned the
previous expression after a successful reload. Every other model property reloads normally.

**Change a dynamic format string via the MCP, not via disk + reload.** Mirror it to TMDL afterwards
for persistence, but don't expect the reload to apply it. This is a strong candidate for some of the
earlier "the edit didn't take" episodes in this build.

### Tooltip page — hiding the column header

`columnHeaders.show = false` **does not work** on `tableEx` (tried; header still rendered with its
sort arrow). What works is a belt-and-braces pair:

1. set each projection's `displayName` to `" "` — the header renders the field's display name, so a
   blank name renders nothing; and
2. paint `columnHeaders.fontColor` and `.backColor` to the page background.

Page is `300 × 360` with the table at `284 × 344`; at the original 280 × 230 the event list
overflowed into a scrollbar.

> **Verifying interactivity:** a *page filter* on `Decades[DecadeLabel]` narrows the slicer's items
> but does **not** select one, so it does not trigger the spotlight/band/labels. Only a real slicer
> click does. Don't mistake a filtered-but-unselected slicer for a broken build.

Two build notes carried from the recipe docs, both silent-failure traps:

- The measure-bound `dataPoint.fill` **must** carry a `dataViewWildcard` selector or every column
  renders the same colour and nothing appears to highlight. Use
  `pbir visuals cf … --measure …` rather than hand-writing the JSON — the CLI gets it right.
- With nothing selected, `[Column Color]` must fall back to "all normal", not "all dimmed".

## 5b. Decade detail panel (added 2026-08-16)

A briefing band below the chart, modelled on a decade-summary layout: narrative → KPIs with
vs-prior-decade deltas → two Top-5 lists. Chart shrinks to h300; panel occupies y472–688.

| Zone | Visual | Content |
|---|---|---|
| Narrative | `card` | Dynamic title `[Decade Scope Label]`; sentence `[Decade Takeaway]` on the **subTitle** (it wraps and accepts a measure) |
| KPIs ×4 | `card` | `[Sel Launches]`, `[Sel Success %]`, `[Sel Operators]`, `[Sel Rockets]`, each with its `[Delta …]` text on the subTitle |
| Top 5 ×2 | `barChart` | Company / Rocket by `[Sel Launches]`, TopN=5 visual filter |

### The architectural point

`Decades` is **disconnected**, so these visuals get no filtering for free. Every panel measure opts
in explicitly with `CALCULATE ( …, TREATAS ( VALUES ( Decades[Decade] ), DimDate[Decade] ) )`, and
falls back to the all-time total when nothing is selected. The recipe's "selection ≠ filtering"
invariant is intact — the panel *chooses* to be filtered; the chart still isn't.

Deltas use `[Prv Decade]`, which is blank unless **exactly one** decade is selected — a delta against
a multi-decade span has no clean meaning, so the deltas simply hide. Success rate is compared in
**percentage points**, not as a percentage of a percentage.

### Gotchas found building it

1. **`cardVisual` (the new card) rendered no value at all** here, with or without formatting
   overrides. The classic **`card`** (role `Values`, objects `labels` + `categoryLabels`) works.
2. **Never replace a `visualContainerObjects.title` properties dict wholesale** — it drops the
   `text` set by `pbir add visual -t`, and the visual silently reverts to its auto-generated name
   (`"Sel Launches by Company"`). Set `text` explicitly whenever you touch that object.
3. A card needs ~104px height for title + subtitle + a 19pt value; at 100px/24pt the number clips.

## 6. Constraints & non-goals

- **No `Price` measure.** 73% of rows have no price. Any cost KPI would silently describe the 27%
  that do — worst case a "total programme cost" that is off by a factor of four. Excluded from v1.
- **Events must be derived from the CSV** (confirmed 2026-08-16). No hand-curated milestone table,
  which means no "Apollo 11" / "Challenger" style annotations — the data does not flag them. See §7
  for what *is* derivable.
- **Accessibility:** the dim/highlight contrast must stay ≥ 3:1 against the card surface. Theme
  colours already pass; do not substitute custom hex.
- **Page size:** 1280 × 720.
- **Don't build:** extra pages, KPI card row, a company breakdown page, maps from `Location`.
- **Deferred to v2:** success-rate-by-era (the `MissionStatus` split is the obvious second story —
  Success 89.9% overall but 1958 ran 71.4% failures); `RocketStatus` active/retired framing.

## 7. Derived events — what the data can actually justify

All computed from `space_missions.csv` alone, verified 2026-08-16.

**A. First launch of each major operator** (companies with ≥ 50 launches) — 16 events, spread
roughly 2 per decade, which is why this works: the selected decade shows 1–3 labels, never a wall.

| Year | Operator | Total launches |
|---|---|---|
| 1957 | RVSN USSR | 1,777 |
| 1958 | US Air Force · NASA | 161 · 203 |
| 1959 | General Dynamics | 251 |
| 1965 | Martin Marietta | 114 |
| 1969 | CASC | 338 |
| 1970 | Roscosmos | 69 |
| 1975 | MHI | 87 |
| 1979 | ISRO | 82 |
| 1984 | Arianespace | 293 |
| 1989 | Boeing | 136 |
| 1990 | Northrop · Lockheed | 89 · 79 |
| 1992 | VKS RF | 216 |
| 2006 | SpaceX · ULA | 182 · 151 |

**B. Record years** — 4 more events, all defensible from the data:

- **1957-10-04** — first launch in the dataset (Sputnik-1, RVSN USSR)
- **1971** — busiest year of the Cold War era (119 launches)
- **2021** — all-time record (157 launches)
- **1958** — worst failure rate (71.4% of 28 launches; also the highest failure count, 20)

That is ~20 markers over 66 years. The ≥ 50-launch threshold in (A) is the tuning knob — lower it to
add more operators, raise it to thin the chart out.

## 8. Branding & style

- **Theme:** **Deep Space (Dark)** — `projects/themes/deep-space/deep-space-v1.0.json`, already
  applied to this report and validated 2026-08-16.
- **Spotlight colour:** `dataColors[0]` ion cyan `#4CC9F0`. **Dimmed colour:** `neutral` `#7C87A6`.
- **Event markers:** `dataColors[2]` solar amber `#F2A93B` — the palette's designated signal colour.
- **Font:** Segoe UI / Segoe UI Semibold (theme default).
- Per the theme cascade rule: colours come from the theme, not per-visual hex. The one sanctioned
  exception is the `[Column Color]` measure, which must return literal hex by design.

## 9. Open questions

- [ ] **Multi-select or single-select decades?** Spec above allows multi (ctrl+click two decades to
      compare). Single-select is cleaner to read but loses comparison. *Assumed: multi.*
- [ ] **What happens with nothing selected?** *Assumed: all 66 columns at full colour* (a neutral
      "whole history" resting state) rather than all dimmed.
- [ ] **Is the ≥ 50-launch threshold for operator debuts right?** 16 events. Dropping to ≥ 30 adds
      roughly 6 more, mostly 1990s–2000s.
- [ ] **Should the 2022 partial year be shown-but-marked, or excluded entirely?** *Assumed: shown,
      visually distinguished* — cutting it hides the record 2021→2022 context.

## 10. Build order (once this is locked)

1. Rebuild `DimDate` over 1957–2022 (§2 trap 2), load `Missions` with `Encoding=28591` (trap 1).
2. Add the derived `Decade` column + disconnected `Decades` selection table (recipe P1).
3. Add the derived `Events` calculated table from §7 (A + B).
4. Add the five measures from §3 (recipe P2).
5. Build the page: title textbox, tile slicer, combo chart (recipe P4 + P5).
6. `pbir validate` + visual verify against the theme checklist.
