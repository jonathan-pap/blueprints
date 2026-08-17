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

## 2b. LL2 replacement dataset — landed & verified 2026-08-17

`data/space_missions_ll2.csv` — **7,591 rows, 1957-10-04 → 2026-08-16**, the exact same nine
columns, no blank dates. Pulled by `data/fetch_ll2.py` off the free (unauthenticated) tier over
~5½ hours at ~15 requests/hour. **Swapped in 2026-08-17** — see "After the swap" below for the
two defects the swap exposed.

### The finding that matters: the current dataset is materially incomplete

This is not just "more years". Over the **same 1957–2022 window** LL2 has **6,543 rows against
our 4,630 — +1,913, and more in every single year**:

| 1982 | old | LL2 | reality |
|---|---|---|---|
| RVSN USSR | 53 | 108 | USSR flew ~101 orbital launches in 1982 |
| year total | 67 | 129 | world total ~121 |

The old file is missing roughly **half the Soviet launches**. Every "cadence" statement the report
currently makes about the Cold War is therefore understated: the 1980s were the real peak
(~125/yr), not the plateau (~65/yr) the chart shows today. Swapping the data **changes the shape
of the story**, it does not merely extend it.

### Operator attribution is different, and NOT comparable

LL2 credits the **launch service provider**. For 1982 US flights it says US Air Force (15) and
Rockwell International (3); our file spread the same flights across Martin Marietta (4), General
Dynamics (3) and NASA (3). Consequences:

- All-time Top-5 changes from `RVSN USSR · CASC · Arianespace · General Dynamics · VKS RF`
  to `RVSN USSR (2,468) · US Air Force (1,078) · SpaceX (718) · CASC (610) · Roscosmos (343)`.
- **39 operator names are >18 characters** ("Lockheed Space Operations Company",
  "Production Corporation Polyot", …). `PROVIDER` in `fetch_ll2.py` needs extending or the
  Top-5 bar lists become unreadable.
- The `Events` table re-derives itself from the data, so operator debuts will move.

### Everything else the swap breaks

| Thing | Now | After |
|---|---|---|
| Record year | 2021 (157) | **2025 (341)** |
| `valueAxis` / `secEnd` | 0–200 | ~0–360 |
| Event-marker ladder | 110 / 136 / 162 | rescale to the taller axis |
| Partial year | 2022 | **2026** (200 rows to 16 Aug) |
| Success rate | 89.9% | 92.7% |
| `MissionStatus` | 4 values | **3** — LL2 has no "Prelaunch Failure" (measures referencing it return 0, harmless) |
| `DimDate` | `CALENDAR(1957, 2022)` | 1957–2026 |
| `categoryAxis` | 1953.5–2024.5 | ~1953.5–2028.5 |
| `TimelineNodes` `PerRow` | 17 | **18** → axis window and ribbon rect must be re-measured (§5c) |
| Subtitle | "4,630 launches · 1957–2022" | 7,591 · 1957–2026 |

Keep the old file as `space_missions_2022.csv` for reproducibility — the two are **not**
interchangeable at operator level, so any saved analysis built on it should say which it used.

### After the swap — two defects the pull had, and the fixes

**1. The pull included SUBORBITAL flights.** `fetch_ll2.py` filtered on launch *status*
(`status__ids=3,4,7`) but never on orbit, and LL2's `/launch/` endpoint carries suborbital too.
That is `SpaceShipTwo` (67) and `New Shepard` (38) — **105 rows of 7,591** — in a report titled
*Orbital* Launch Cadence. It also put **Virgin Galactic into `Events` as a 2010 operator debut**
with 67 launches, despite it never having flown an orbital mission.

Fixed in the partition, not by re-pulling (a re-pull is ~5½ hours for 1.4% of rows):

```m
#"Removed suborbital" = Table.SelectRows(#"Changed column type",
    each not List.Contains({"SpaceShipTwo", "New Shepard"}, [Rocket]))
```

Nice confirmation that it works: **Blue Origin's debut moves to 2025**, because New Glenn is its
first orbital flight once New Shepard is gone.

**2. A calendar running past the data breaks any "of N years" denominator.** `DimDate` was
extended to 2030 while the facts end 2026 — four empty years. Rank in the node tooltip would have
read *"1st busiest of 74"* when only 70 years have launches, and every year axis gains four empty
slots. `DimDate` now derives its end from the fact table and self-maintains:

```dax
VAR _maxY = YEAR ( MAX ( space_missions[Date] ) )
RETURN ADDCOLUMNS ( CALENDAR ( DATE ( 1957, 1, 1 ), DATE ( _maxY, 12, 31 ) ), … )
```

**Operator names.** 36 names ran over 20 characters ("Lockheed Space Operations Company",
"Production Corporation Polyot") and would have swamped the Top-5 bars and the event labels.
Short forms are applied to the CSV **and** added to `PROVIDER` in `fetch_ll2.py`, so a re-pull
produces identical names. The rename script carries a **collision guard**: a target that already
exists under a different source name aborts the run. That mattered — the obvious shortening of
"Northrop Grumman Space Systems" is "Northrop", which already exists separately, and the counts
would have silently fused.

### The partial-year test must be DERIVED, not named

Four measures hardcoded `_y = 2022` — correct for the old file (which ended 29 Jul 2022) and
**silently wrong the moment the data changed**: LL2 has 2022 complete (06 Jan – 30 Dec, 189
launches) and **2026** partial (to 16 Aug). `Column Color` was painting 2022 in the muted
"partial" fill and 2026 as if it were finished; both tooltips labelled the wrong year; the
all-time narrative read "Across 1957–2022". All four now derive it:

```dax
VAR _lastDate = CALCULATE ( MAX ( space_missions[Date] ),
                            REMOVEFILTERS ( DimDate ), REMOVEFILTERS ( TimelineNodes ) )
VAR _partial  = _y = YEAR ( _lastDate ) && _lastDate < DATE ( YEAR ( _lastDate ), 12, 31 )
```

### ⚠️ MCP model edits do not survive on their own — verify them on DISK

The suborbital filter was applied through MCP, confirmed live (7,486 rows), and **still ended up
missing from both disk and git**. Desktop re-read the model from disk and discarded it, and a
`grep` that appeared to confirm it in the commit was actually matching `SiteCountry` on the same
lines. The partition's *description* persisted while its *expression* reverted — a partial revert
that is very easy to miss.

**The rule this earns:** after any MCP model change and save, `grep the TMDL on disk for a string
unique to the change` before claiming it is done. A live-model query is not evidence — it only
proves Desktop's memory, which is the thing that keeps getting rolled back. Where Desktop can be
closed, edit the TMDL directly instead; that is the documented order and it does not race.

### Desktop strips `$schema` from `definition.pbism` on every save

Not intermittent — **every single save**, 11 times across this build. It is the only error
`pbir validate` reports when it happens:

```text
space.SemanticModel/definition.pbism  SCHEMA_ERROR  (root): '$schema' is a required property
```

Restore the first key and revalidate; nothing else is affected:

```json
"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json"
```

Treat a lone `SCHEMA_ERROR` on `definition.pbism` as expected after a save, not as a new problem.

### Final state, verified

| | value |
|---|---|
| Fact rows | 7,486 (7,591 − 105 suborbital) |
| Range | 1957–2026, 70 years, no empty tail |
| Busiest year | 2025, **332** |
| `Events` | 21 rows, longest `EventShort` 18 chars |
| Longest operator name | 20 chars |
| `valueAxis` / `secEnd` | 0–380 |
| Event-marker ladder | 209 / 258 / 307 |
| `categoryAxis` | 1953.5–2028.5 |
| `TimelineNodes` `PerRow` | 18 (auto-rebalanced), scatter axis window −1.4 … 18.4 |
| Ribbon rect | **unchanged** at 55/173/1175×520 — re-measured, still lands within 0.1–0.3 of a column on all four bands |

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

**Resolved — and the earlier conclusion here was wrong.** This section previously claimed Power BI
culls by horizontal proximity and that adjacent years could never both be labelled. That was a
misread. The real cause: **the stagger was added on top of `[Launches]`, so a fall in launches
cancelled the tier gap.**

| | 1957 | 1958 | 1959 | gap 58→59 |
|---|---|---|---|---|
| `[Launches] + 14 + tier*20` | 3+14+0 = 17 | 28+14+20 = 62 | 20+14+40 = 74 | **12 — culled** |
| Fixed ladder `MAX([Launches]+14, 110+tier*26)` | 110 | 136 | 162 | **26 — renders** |

The tell was a **cross-filter**: filtering to one operator flattens the columns, which accidentally
evens out the tiers — and three labels appeared. Same categories, same widths, same pitch. So it was
never horizontal proximity.

**Fix: pin the tiers to a fixed ladder** (110 / 136 / 162), lifted above the column only when the
column is taller. Separation is then guaranteed regardless of column height, and the error bar
stretches to connect each marker back to its column. Verified: 1957/58/59 all render together.

Two lessons worth keeping: a stagger measured from a *variable* baseline isn't a stagger; and when
a rendering behaviour changes under cross-filter, the cause is geometry, not a hard visual limit.

The narrative still names the decade's debuts (`[Decade Takeaway]` → "First launches: …", three most
significant by `EventWeight` plus `+N more`). That is now belt-and-braces rather than the only
channel, and it still earns its place when a decade has more debuts than markers.

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

## 5c. Mission Timeline page — serpentine (added 2026-08-16)

A second page, requested after v1 shipped. **This supersedes the "don't build: extra pages"
line in §6** — recorded here rather than silently deleted, because the reasoning in §6 (one
page, one story) still holds for everything else.

One node per calendar year 1957–2022, laid out **boustrophedon**: row 0 left→right, row 1
right→left, and so on, with the bands joined by U-turn arcs. Power BI has no wrapping axis,
so this is a **hybrid**: the connector is SVG, the nodes are a real chart.

| Layer | Visual | Why |
|---|---|---|
| Backdrop | `image` ← `[Nebula Backdrop]` | page scenery |
| Ribbon | `image` ← `[Timeline Ribbon]` | the bands + U-turns — SVG can draw them, no native visual can |
| Nodes | `scatterChart` | **real** points: tooltips, hover, cross-filter. Not a picture |

`TimelineNodes` is a calculated table (one row per year) carrying `NodeRow`/`NodeCol`;
`[Node X]`/`[Node Y]` read them, `[Node Size]` = launches, `[Node Color]` paints milestone
years amber via a `dataViewWildcard` selector. `TimelineNodes[Year] → DimDate[Year]` (1:*)
so a node click filters through the existing date path; `Decades` stays disconnected.

### The alignment problem, and how it was solved

Power BI **insets a chart's plot area** inside its container by an amount that depends on the
axis labels, the data labels **and the bubble size** — so an image sized to the same rectangle
does *not* line up. Final measured values:

| | scatter container | ribbon = actual plot rect |
|---|---|---|
| x / width | 40 / 1200 | **55 / 1175** |
| y / height | 150 / 560 | **173 / 520** |

The ribbon image is positioned to the **plot rect**, not the container. Do not "tidy" the two
visuals onto the same rectangle — that is the bug, not the fix.

### Gotchas found building the timeline

1. **The plot rect depends on `bubbleSize`.** This cost the most time. Alignment was measured
   with big bubbles (`-5`), then the bubbles were shrunk to `-18` — which shrank the inset and
   moved every node outward, while the ribbon stayed pinned. The symptom was subtle and
   misleading: the band appeared to *start one column inboard*, so the left U-turn looked like
   it joined 1989→1992 instead of 1990→1991. **Align the ribbon LAST**, after the bubble size
   and the layout are settled, and re-check after any change to either.
2. **`powerbi-desktop reload` does NOT re-read the semantic model.** Editing a measure in TMDL
   on disk and reloading leaves the *live* model on the old definition — verified by evaluating
   `[Timeline Ribbon]` through MCP and getting the previous SVG back while the file on disk said
   otherwise. This is the same failure class as the `formatStringDefinition` one. **Measure
   edits go through MCP**; the disk is not the source of truth while Desktop is open. A silent
   disk↔live divergence is also dangerous in the other direction — the next Ctrl+S writes the
   live model over your file.
3. **Locale decimal separator will silently corrupt the path data.** `FORMAT(x,"0.0")` on a
   European locale emits `1110,6`, which is invalid SVG that fails *without an error* — the
   image just doesn't draw. Every coordinate goes through `FORMAT(ROUND(x,0),"0")`.
4. **`bubbleSize` is roughly exponential.** `-35` → invisible specks, `40` → one solid mass of
   overlapping circles, `-18` → correct.
5. **The viewBox aspect does not affect positions.** Everything the SVG draws is a fraction of
   `_W`/`_H`, and `preserveAspectRatio='none'` stretches those fractions onto the rect — so
   `1200 × 430` in a `1175 × 520` box still lands correctly. Only the **arc radii** feel the
   aspect (`_rx` is a constant, so it renders as `46 × 1175/1200 ≈ 45` page units). Changing
   `_W`/`_H` to "match" the rect is therefore cosmetic, not a fix.
6. **`pbir pages rename` renames the folder only.** It left `page.json`'s `name` and the
   `pages.json` entry as the original hash (`1ea4852a6657b623`) while the folder became
   `Mission_Timeline`. Aligned by hand to match `Launch_Cadence`, where all three agree.
7. **MCP model edits are live-only until Ctrl+S.** Order matters: save the model first, then
   edit report JSON, then reload. (The reverse also bites: edit report JSON first and a later
   Ctrl+S rewrites `pages.json` from Desktop's copy, deleting the new page.)

### Measuring alignment from a screenshot

**Do not calibrate against the page canvas.** The nebula's own fill (`#070B18`) is nearly
identical to Desktop's chrome, so the canvas edges cannot be detected reliably — and the
screenshot scale *changes between captures* when the window or the Filters pane resizes
(observed 3330px wide, then 2968px). Calibrate against the **ribbon** instead: its rect is
known in page units and its bands sit at known fractions of it, which gives the raw-px ↔
page-unit mapping for free. Then convert node centres and invert the pinned axis window.
`solve_plot.py` (in this folder) does this. Detect the dotted bands as *thin* horizontal features
(brighter than the pixels 9px above **and** below) — a colour match alone picks up nebula
gradients and stars.

### When the LL2 data lands

`_rows` is fixed at 4 and `PerRow` is derived, so the table rebalances itself — 1957–2026 gives
`PerRow = 18`, not 17. The **pinned axis window does not follow**. Update together:
`categoryAxis` end `17.4` → `18.4`, and re-measure the plot rect.

## 5d. Node Tooltip page (added 2026-08-16)

A canvas tooltip on the timeline nodes — `Node_Tooltip`, 340 × 320, `type: "Tooltip"`, one
`tableEx` bound to `[Timeline Tooltip]` with the column header painted out. Same shape as the
existing `Year Tooltip`; the scatter points at it through `visualContainerObjects.visualTooltip`
(`type: 'Canvas'`, `section: 'Node_Tooltip'`).

```text
2021

Launches        157 · +38 vs 2020
Rank            1st busiest of 66
Success         143 of 157 (91.1%)
Failures        11
Operators       23 · most CASC (48)
Rockets         51 · most Falcon 9 Block 5 (31)
Launched from   10 countries · most USA (57)
Debuts          GK LS, Firefly

• Record year — 157 launches
```

### New data points, and one new dimension

`Rank`, the year-on-year delta, and `Debuts` (operators whose **first launch anywhere** was that
year) are new. So is `Launched from`, which comes from a column the brief had written off:

**`space_missions[SiteCountry]`** — the last comma-segment of `Location`. 22 distinct values
covering all 4,630 rows; only 11 rows need normalising (`New Mexico` → USA,
`Pacific Missile Range Facility` → USA, `Gran Canaria` → Spain, `Shahrud Missile Test Site` →
Iran) and the three sea ranges fold into `Sea launch` because they genuinely have no country.

> **It is the launch-site country, not the operator's nationality.** Kazakhstan's 719 is Baikonur
> flying Soviet/Russian missions; France's 318 is mostly Kourou flying ESA/Arianespace. Always
> label it "launched from". A visual that reads it as "who launched" is simply wrong.

### Gotchas found building the tooltip

1. **`ALL()` will not take two tables** (`Multiple table arguments are not allowed`). The hovered
   node filters `TimelineNodes`, which filters `DimDate`, so every "across all years" figure —
   rank, prior year, an operator's first-ever launch — has to clear **both**. It has to be
   `REMOVEFILTERS ( DimDate ), REMOVEFILTERS ( TimelineNodes )` per `CALCULATE`. Clearing only
   `DimDate` leaves the calculation pinned to the hovered year and every rank comes out as 1st.
2. **Never put literal words inside `FORMAT`.** `FORMAT ( x, "+#,##0;-#,##0;no change" )`
   rendered as **`no chang`** — letters in a format string are read as specifiers and the `e` was
   eaten as an exponent marker. It fails silently. Build the words with `&` outside `FORMAT`.
3. **Tabs (`UNICHAR(9)`) collapse to a single space in a `tableEx` cell**, so label/value columns
   cannot be aligned this way. Each line has to read as a phrase instead — hence
   "10 countries · most USA (57)" rather than a bare "10". True of the older `Year Tooltip` too.
4. **`TOPN` ties return several rows** and `CONCATENATEX` glues them into one string. Every
   top-N carries a name tiebreaker.

### Verifying a tooltip page without hovering

The bridge cannot hover, and the page renders **empty** on its own (the measure returns `BLANK()`
with no year in context — correct behaviour). To check layout, add a temporary page filter, then
remove it:

```json
"filterConfig": { "filters": [ { "name": "tmpYearProbe",
  "field": { "Column": { "Expression": { "SourceRef": { "Entity": "TimelineNodes" } },
                         "Property": "Year" } },
  "type": "Categorical",
  "filter": { "Version": 2, "From": [ { "Name": "t", "Entity": "TimelineNodes", "Type": 0 } ],
    "Where": [ { "Condition": { "In": {
      "Expressions": [ { "Column": { "Expression": { "SourceRef": { "Source": "t" } },
                                     "Property": "Year" } } ],
      "Values": [ [ { "Literal": { "Value": "1969L" } } ] ] } } } ] },
  "howCreated": "User" } ] }
```

**Do not read the colours off that screenshot.** Desktop renders a Tooltip-type page dimmed in
the canvas — text measured `#4F5465`, i.e. `#E8ECF8` at ~30% alpha, about 2.3:1, which looks like
an accessibility failure and is not one. The identical `tableEx` on `Launch_Cadence` samples
exactly `#E8ECF8`. Check contrast on a normal page, never on the tooltip preview.

## 5e. Milestones page — vertical timeline (added 2026-08-17)

A tall vertical timeline of the 15 **event years**: a centre spine, one node per year, and the
operator names alternating left/right on leader lines with an end dot. Third use of the same
hybrid — SVG for what nothing native can draw, a real `scatterChart` for the nodes so hover and
the canvas tooltip still work.

| Layer | Visual | Why |
|---|---|---|
| Backdrop | `image` ← `[Nebula Backdrop]` | page scenery |
| Spine | `image` ← `[MS Spine]` | band, leader lines, end dots, names as `<tspan>` stacks |
| Nodes | `scatterChart` | **real** points: hover, tooltip, cross-filter |

`[MS Idx]` returns the 0-based position of a year **among event years only, blank otherwise** —
that blank is what makes the scatter draw 15 points from a 70-row table, without a filter.
`[MS X]` is a constant 0 (every node on the spine) and `[MS Y]` is `-Idx`, so the earliest year
is at the top. Sides alternate on index parity inside `[MS Spine]`.

### A page taller than the canvas

`1280 × 1500` with **`displayOption: "FitToWidth"`**. `FitToPage` would shrink the whole page to
fit the viewport, which is not what a long timeline wants; `FitToWidth` scales to the width and
scrolls vertically.

### Gotchas found building it

1. **The image visual letterboxes by default.** `[Nebula Backdrop]` is a 16:9 SVG; in a
   1280 × 1500 container it rendered centred at 1280 × 720 with dark bands above and below — a
   hard seam across the page. The SVG's own `preserveAspectRatio='xMidYMid slice'` does **not**
   govern this; the *visual* does. Set `image.fit` to **`'Fill'`** (cover, preserving aspect):
   `"fit": { "expr": { "Literal": { "Value": "'Fill'" } } }`. Valid values are `Fit`, `Fill`,
   `Stretch`, `Normal`. Report-side only — no need to touch the shared measure.
2. **Removing the `Size` binding resets the bubble scale.** Dropping `Size` gives the uniform
   circles this design wants, but the same `bubbleSize` that looked right *with* a size field
   (`-22`) renders as specks without one. `25` is correct here. Re-check the size whenever the
   `Size` well changes, not just when the layout does.
3. **Same plot-area inset as every other page** — container `y 150 / h 1290`, actual plot rect
   **`y 173 / h 1249`**. Consistent with `Mission_Timeline` (23 top, 17 bottom), so that inset
   looks like a constant for a hidden-axis scatter at this page scale rather than something to
   re-derive from scratch each time.

The year sits *beside* each node rather than inside it: a scatter cannot centre a data label in
its bubble, and putting the text in the SVG would either hide it behind the node or block hover.
Baking the circles into the SVG would allow it, at the cost of the tooltip.

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
