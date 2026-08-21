# Brief — Arcane Emporium (Power BI)

> The report half of the job. The **data** brief lives with the generator at
> [`synthetic-data/projects/arcane-emporium/brief.md`](../../../synthetic-data/projects/arcane-emporium/brief.md)
> — read that first for what the numbers are and how they were pinned.

## 1. Audience & decision

A **demo star**: the report exists to show Power BI off, not to run a business. The audience is
whoever is being shown the tool — so the bar is "every page reads at a glance, every number ties
out, and nothing needs a caveat". There is no real decision to support, which changes the design
brief in one important way: **the report has to be interesting to explore**, not merely correct.

## 2. Source data & model

Star schema, built from the generator's CSVs via a single `SourceFolder` M parameter.

| Table | Rows | Notes |
|---|---|---|
| `DimDate` | 1,461 | 2023-01-01 → 2026-12-31, marked as the date table |
| `DimShop` | 8 | Shop → City → Realm (Eldoria / Grimmwald / Sunspire) |
| `DimItem` | 24 | Item → Category (5), config list order is the pareto rank |
| `DimCustomer` | 20 | Customer → CustomerType (Adventurer / Collector / Guild / Noble) |
| `FactSales` | 99,374 | Date × Shop × Item × Customer, Gold + Units |

All four dimensions join the fact **on integer keys, one-to-many, single direction**. The fact
carries a `yyyymmdd` `DateKey` rather than a date, which is why `DimDate` is explicitly marked as
a date table — time intelligence needs `DimDate[Date]`, the relationship needs the key.

### Verified on load

| Check | Expected | Actual |
|---|---|---|
| Fact rows | ~100K | 99,374 |
| Total Gold | 25,000,000 | 25,000,000.76 |
| Realm share | 45 / 30 / 25 | 0.450000 / 0.300000 / 0.250000 |
| Category share | 30 / 25 / 20 / 15 / 10 | ties to 8 dp |
| CustomerType share | 40 / 25 / 20 / 15 | ties to 8 dp |
| YoY growth | +12% | +12.25% / +11.75% / +12.00% |

The 2024 figure runs slightly hot because it is a leap year — 366 days of daily allocation
against 365. Worth knowing before someone points at it in a demo.

## 3. Measures

`_Measures`, a one-row calculated table, holds everything.

- **Core** — Total Gold, Total Units, Transactions, Avg Sale, Avg Item Price, Patrons, Items Sold
- **Time** — Gold PY, Gold YoY, Gold YoY %, Gold YTD, Gold 3M Avg
- **Analysis** — Gold Share of Total

`Total Gold` rather than `Gold`: `FactSales` already has a hidden `[Gold]` column, and a measure
sharing a column's name makes the unqualified reference ambiguous to read even where DAX allows
it. `Gold YoY %` returns **blank** in 2023 rather than 0% — there is no prior year in the data,
and a 0% that means "no comparison" is a lie the reader cannot see.

## 4. Pages & layout

Four pages, one per grain of the star. Geometry from
[`design-system.yaml`](design-system.yaml) — a 12×12 grid, 8px snap, resolved to pixels rather
than hand-placed.

| Page | Question | Shape |
|---|---|---|
| **Overview** | How is the chain doing? | KPI hero + 4, four-year trend with the Frostfall peak, realm and category splits |
| **Realms** | Where does the Gold come from? | Realm panel + shop league table |
| **Items** | What sells? | Pareto of items (flagships vs the long tail) + category strip |
| **Patrons** | Who buys? | Customer-type panels + big-spender table |

Global chrome on every page, inside the header band so no page loses content height: a wordmark
in cols 1–7, and three synced slicers in cols 8–12.

## 5. Branding & style

**Runeforge Dark v1.0**, from the shared library at
[`projects/themes/runeforge/`](../themes/runeforge/) — the fantasy half of the era set, built for
exactly this kind of lore data. Dark because the emporium is a magic shop and the report is a
showpiece; Runeforge **Light** is its twin and shares the same hue angles, so switching modes is
a one-line change to `report.json` and nothing else.

The theme is gated on WCAG contrast, greyscale separation and colour-vision separation
(deuteranopia + protanopia) — see [its notes](../themes/runeforge/notes.md) for the measured
margins.

## 6. Constraints & non-goals

- **No real geography.** The realms are invented, so no map visual — a shop league table carries
  the same information without pretending Silverhaven has coordinates.
- **No forecasting.** The data has a known synthetic trend; projecting it would be circular.
- **Nothing that needs a Fabric sign-in.** The demo has to run from a local `.pbip`.

## 7. Build record

- **2026-08-21** — model built live through the Power BI Modeling MCP (Desktop was open;
  editing TMDL on disk would have been clobbered by the next Desktop save). Tables, relationships,
  date-table marking and measures created, full refresh, figures verified against the generator
  config.
- **2026-08-21** — four pages built from `design-system.yaml` via `build_pages.py`; the item
  Pareto substituted from the recipe's own template by `build_pareto.py`. Theme registered,
  `pbir validate` clean, every page screenshotted.

### Three things the first render caught

**The headline KPI was wrong.** `Gold YoY %` read **+41.6%** with all four years selected —
SAMEPERIODLASTYEAR was comparing 2023–2026 against 2023–2025, which is arithmetic, not a growth
rate. Added `Gold YoY % Latest`, which always answers "how did the most recent year do" whatever
the grain: +12.0% at the all-years grain, and identical to the old measure at a single year.
The tables' YoY columns had the same bug and now use the same measure.

**A caption claimed the opposite of its chart.** The average-purse subtitle said "nobles buy
rarely and expensively, adventurers often and cheaply". The chart shows adventurers with the
*highest* average purse (284) and nobles the lowest (190) — because every patron visits about
as often as every other, so average purse just tracks the pinned Gold share. Caption corrected.
Written narrative has to be checked against the render, not against what feels true.

**A dead column.** "Wares bought" was 24 for all twenty patrons across four years — every
patron has bought everything. Replaced with Units, which has real spread.

### Two Desktop-bridge behaviours worth knowing

- **`hasUnsavedChanges` does not track MCP model edits.** After creating measures over XMLA the
  bridge still reported `false` while the live model and the on-disk TMDL differed by three
  measures. Do not trust the flag as a "safe to reload" signal.
- **`reload` reloads the REPORT, not the MODEL.** New PBIR pages appear; new TMDL measures do
  not. A card bound to a measure that only exists on disk renders an error tile. Model changes
  need a real file re-open — or, as here, the same change applied live through the MCP.

## 8. The bookmark tour — 2026-08-21

Five stops driven by a `bookmarkNavigator` across the bottom of every page. Script and the
presenter's live-click moments: [`tour.md`](tour.md). Built by [`build_tour.py`](build_tour.py).

The bookmarks **navigate only** — `suppressData` and `suppressDisplay` are both set, so they
restore the page and nothing else. A tour that resets the slicers fights the person giving it,
and staged-filter bookmarks could not be verified here anyway: the bridge reloads and
screenshots but cannot click, so a wrong slicer state would look perfect in every screenshot and
fail live. The two moments that want a filter are written into `tour.md` as live clicks instead.

### The tour cost every page a grid row

A `bookmarkNavigator` **clips its tile labels below about 48px** — at 32px the tiles draw and the
text is cut through the middle. So the bar could not live in the 24px page margin; it took row 12
(y 656..704) and every content band now stops at row 12 instead of row 13.

That knocked on: the Overview's category chart had five bars in the resulting 128px body, and
Power BI drops the fifth rather than crowd them. Fixed by making that chart **vertical** — five
columns fit a short wide panel comfortably — which let the trend chart keep its four rows. It
needs them: at three rows Power BI drops the month labels entirely, and the Frostfall story
depends on seeing which months are the spikes.

### Two PBIR findings

- **A `bookmarkNavigator` needs a `query` block.** Omit `query: {}` and the visual writes,
  validates and reloads cleanly, then draws nothing — no error, no placeholder, just empty space.
  Found by generating one with `pbir add visual` and diffing it against mine.
- **It is fussy about `objects`.** A version carrying `layout` / `text` / `fill` / `outline` /
  `shape` also rendered nothing, at every height tried. With an empty `objects` block it renders
  immediately, so it ships unstyled and inherits from the theme — which is the workspace's
  theme-first rule regardless.
- **`pbir bookmarks new` does not exist in pbir 0.9.25.** The room's `create-bookmark.md`
  documents it; the CLI has only `list / rename / data / display / current-page / visuals / json`.
  Bookmarks have to be hand-authored. `explorationState.sections` is required by the schema even
  for a navigate-only bookmark — an empty `visualContainers` map satisfies it.

### A data characteristic worth knowing before demoing page 2

Within a realm the shops are near-identical — 3,750,001 / 3,750,000 / 3,749,999 — because the
generator splits each realm's Gold evenly across its shops. The **realm** split is pinned and
meaningful; the **shop** split is not. Flagged in `tour.md` so nobody zooms in on it live.

## 9. The tutorial — 2026-08-21

Ten spotlight steps, driven by a second navigator on the right of the tour row. Each hides every
other data visual on the page and reveals a caption. Built by
[`build_tutorial.py`](build_tutorial.py); narrative in [`tour.md`](tour.md).

### PBIR findings

- **`display.mode` accepts only `"hidden"`.** `visible`, `shown`, `show`, `default`, `normal`,
  `active` and `expanded` are all rejected by the schema. Visibility is expressed by **omission**
  — a bookmark lists what to hide and everything unmentioned is shown.
- **A navigator lists every bookmark in the report** unless it is pointed at a group. Grouping
  them in `bookmarks.json` is not enough on its own; the visual needs
  `objects.bookmarks.bookmarkGroup`. Without it the bar showed all fifteen tiles truncated to
  four characters.
- **`objects.bookmarks.bookmarkGroup` is safe** even though a fuller objects block
  (layout/text/fill/outline/shape) kills the navigator outright. It is not "no objects at all",
  it is a specific bad property in that set.
- **Bookmark groups nest as `{name, displayName, children:[...]}`** in `bookmarks.json` and
  validate cleanly.

### The bug the preview caught

The first cut hid `tutorBar` along with everything else, stranding the reader mid-step — no way
to advance, no way to `Show all`, and the page tour cannot rescue them because those bookmarks
carry `suppressDisplay`. Found by applying a step's state to the page files and screenshotting
(`preview_step.py` in the scratchpad), which is the only verification available: the bridge
reloads and screenshots but cannot click, so the bookmarks' restore behaviour stays unproven.

## 10. Coach-mark bubbles — 2026-08-21

The tutorial captions became game-style speech bubbles with a tail pointing at the graph. Ten SVG
`ImageUrl` measures generated by [`build_bubbles.py`](build_bubbles.py), rendered in `image`
visuals. Wrapped text via `<foreignObject>` + XHTML (the foundation at
`02-build/visuals/svg/html-in-svg.md`) — raw SVG `<text>` has no word wrap.

Body and tail are **one path**, so there is no seam to hide. All four tail directions
(top / bottom / left / right) were rendered and checked.

### Three things that bite

- **`<foreignObject>` clips silently.** No scroll, no error — the last line just vanishes. The
  first cut estimated text width at ~2.05px a character; Segoe UI at 13px is nearer **6.2**, so
  every bubble lost its final line. Step 2 lost the words "the Frostfall festival", which was the
  entire point of that step. The generator now computes each bubble's height from its own text
  and adds slack.
- **Escaping `&` blindly corrupts entities.** `s.replace("&", "&amp;")` turned `clich&#233;` into
  `clich&amp;#233;`, which renders as literal `clich&#233;`. The escaper now skips anything that
  is already an entity.
- **DAX user-defined functions need compatibility level 1702**; this model is 1606. One
  `BubbleSVG(title, body, side)` function would have collapsed ten measures into one, but raising
  a model's compat level is a real change with real consequences and not worth it for a cosmetic
  win. The boilerplate is generated in Python instead.

### On dimming rather than hiding

Still hiding, for the reason in section 9: z-order is static in PBIR, so a scrim needs every
focusable visual duplicated at a high z. If the dim look is wanted, an SVG `image` overlay is the
mechanism — proven here — but the duplicate-visual cost stands.

### The clobber, and what it cost

`Bubble 01` went missing between writing it and reopening. The sequence: the generator wrote all
ten measures to `_Measures.tmdl` on disk, but only nine had also been created in the live model
over XMLA. Desktop was open the whole time, so its next save wrote its own nine back over the
file — and the tenth was gone, silently, with no error anywhere. The give-away on inspection was
that the surviving blocks carried `displayFolder: Tutorial` and real GUID `lineageTag`s: Desktop's
serialisation, not the generator's.

This is exactly the rule in `02-build/context.md` — **Desktop must be closed before editing TMDL
on disk** — and the mitigation used everywhere else in this build (make the same change through
the MCP so memory and disk agree) was simply skipped for that one measure. Recovered by creating
it live; all ten now resolve.

The wider lesson for this project: while Desktop is open, **the live model is the source of truth
and disk is a copy it overwrites**. Write to TMDL only for things that are also going through the
MCP, or close Desktop first.

