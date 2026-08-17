# Design contract — the `Design Brief:` handoff

> The authoritative handoff from the [design room](../references/design-identity.md) to **authoring**. It specifies
> **what** to build — page intent, design identity, semantic bindings, and a per-page layout contract.
> Authoring computes **how** — exact `pbir` commands, coordinates, theme JSON, validation, screenshots.
>
> This is the blueprint's port of the design-brief contract, expressed in **our** vocabulary: the
> **12×12 grid** and per-type spans from [`design-system.md`](design-system.md) (`design-system.yaml`),
> the detail-gradient [**bands**](detail-gradient.md) (semantic row labels, not geometry), and the
> equal-gap golden rules in [`layout-guidelines.md`](layout-guidelines.md). Placements carry **grid
> regions**, so the contract, the [wireframe spec](../../../01-brief/wireframes/handoff.md), and the
> built report all describe the same geometry.

## Required marker

Every non-trivial brief must begin with:

```yaml
generated_by: powerbi-report-design-room
contract_version: 1
```

The marker distinguishes a design-owned contract from a freeform wireframe. Authoring and the
[validator](../../../04-review/audit/layout-contract-validate.md) both key on it.

## Why the structure

- **`design_identity`** — the Step-1 tone + signature ([tones](../references/tones.md), [signatures](../references/signatures.md)),
  plus brownfield current-state for the redesign delta. Every later choice should visibly serve it.
- **`color_map`** — one palette color per measure. Cards use it as accent; lines as `defaultColor`; bars
  as gradient max. `measure_match` = exact color reuse for the same measure across every visual and page.
- **`pages[].layout_contract`** — the geometry handoff, as **grid regions + tokens**. Each placement
  names a grid region `[col_start,row_start,col_end,row_end]` (or a `design-system.yaml` span/template
  token) and a semantic `band`. Authoring resolves regions to pixels via the cell math
  ([layout-guidelines](layout-guidelines.md#grid-12x12)); the audit hook checks the result.
- **`space_budget`** — forces accounting for the whole grid (no dead cells, no bare-card hero).
- Slicer type follows grain: Year/period dropdown or tile for executive/annual; full-date `between` only
  when arbitrary date-range exploration matters and the field renders as Date/DateTime.
- Callouts/context tiles need an `insight_basis` — never a duplicate absolute measure.
- One analytical question per visual.

## Minimal-brief escape hatch

For trivial single-visual asks ("bump this card's font", "add a region slicer"), 3 lines suffice:

```yaml
Design Brief:
  mode: brownfield
  design_identity: { tone: unchanged, signature: unchanged }
  change: "Increase Revenue card value font 28→36pt so it reads as the page hero"
```

The full template below is for a new page, a redesign, or any change touching more than one visual.

## Full template

```yaml
Design Brief:
  generated_by: powerbi-report-design-room
  contract_version: 1
  mode: greenfield                 # greenfield | brownfield
  design_identity:
    tone: <catalog tone, remix, or custom phrase with palette/type/density implications>
    signature: <gallery signature ID/name, remix, or custom one-sentence move>
    # brownfield only:
    # current_tone: <existing report's tone, or "indistinct">
    # current_signature: <existing defining element, or "none">
  color_map:
    - measure: Sales[Revenue]
      color: "#0072B2"
      tint:  "#DEEFFF"
    - measure: Sales[Orders]
      color: "#D55E00"
      tint:  "#FFE8D5"
  pages:
    - name: "Revenue Fell 8% YoY in EMEA"     # descriptive INSIGHT title, not "Overview"
      role: landing                            # landing | detail | drillthrough | tooltip
      archetype: Executive Summary
      layout_variant: A
      variant_rationale: "3 co-equal KPIs + a clear trend and one driver → strip + dual hero."
      page_size: { width: 1280, height: 720 }  # from design-system.yaml meta.page; 1920x1080 for wallboard
      page_background: "#F8F9FA"
      layout_contract:
        # Geometry is the 12×12 grid (design-system.yaml). Each placement carries a grid
        # region [col_start,row_start,col_end,row_end] (1-indexed, END-EXCLUSIVE — [1,1,4,4] = cols 1-3,
        # rows 1-3) OR a design-system.yaml token (defaults.<type> span / layouts.<name> template).
        # `band` is the semantic detail-gradient label on rows (summary/analysis/detail) — story, not geometry.
        placements:
          - id: page_title
            kind: textbox
            band: summary
            region: [1, 1, 13, 2]                     # full-width header row (cols 1-12, row 1)
            text: "Revenue Fell 8% YoY in EMEA"
            purpose: "State the page insight before any chart."
          - id: year_slicer
            kind: slicer
            band: summary
            token: defaults.slicer                    # span [2,1]; authoring anchors it right of the title row
            field_bindings: Date[CalendarYear]
            slicer_type: dropdown
          - id: revenue_card                          # 4-card KPI strip fills layouts.kpi_row_4 (rows 2-3)
            kind: cardVisual
            band: summary
            token: layouts.kpi_row_4                  # this card = region [0]
            region: [1, 2, 4, 4]
            purpose: "What is total revenue, vs last year?"
            field_bindings: Sales[Revenue]
            context: Sales[Revenue YoY %]             # the Δ that earns the card its space
            color_strategy: measure_match
          # ... 3 more cards at regions [4,2,7,4] [7,2,10,4] [10,2,13,4]
          - id: revenue_trend
            kind: lineChart
            band: analysis
            region: [1, 4, 7, 10]                     # left half, analysis band (rows 4-9)
            purpose: "How is revenue trending?"
            field_bindings: { axis: Date[Quarter], values: Sales[Revenue] }
            color_strategy: measure_match
          - id: top_regions
            kind: barChart
            band: analysis
            region: [7, 4, 13, 10]                    # right half, analysis band — gutter aligns with trend
            purpose: "Which regions drive the gap?"
            field_bindings: { category: Region[Name], values: Sales[Revenue YoY %] }
            sort_policy: value_asc                     # most negative first
            color_strategy: gradient
          - id: region_detail
            kind: tableEx
            band: detail
            region: [1, 11, 13, 13]                   # full-width detail band (rows 11-12; row 10 = spacer)
            purpose: "Which regions/products need follow-up?"
            field_bindings: [Region[Name], Product[Name], Sales[Revenue], Sales[Revenue YoY %]]
      space_budget:
        grid: { columns: 12, rows: 12 }               # 144 cells total (from design-system.yaml)
        cells_filled: 132                             # union of every region's cells (row 10 left as a spacer)
        emptiness_pct: 8                              # (144 − filled)/144 → ≤15% analytical / ≤20% executive
        bands_used: [summary, analysis, detail]       # every listed band has ≥1 placement
        largest_region: revenue_trend                 # a chart is the hero, NOT a card (36 cells)
        largest_region_pct: 33                        # of content area below summary; a non-hero region must stay ≤~45%
        balance_rationale: "KPI strip + trend/driver hero + detail row fill the grid; only the row-10 gutter band is empty."
  interaction_pattern:
    drill_targets: [ "Region Detail" ]
    cross_filter_rules: "Filter (default); top_regions → Highlight"
  accessibility:
    alt_text: "every chart gets alt text — headline+trend phrasing"
    contrast: "WCAG AA on every text/background pair; no red-on-red"
  theme:
    base: "existing theme preserved"                 # DEFAULT — keep the report's current theme.
                                                      # Author/swap a theme JSON ONLY if the user
                                                      # explicitly asked. A tone is direction, not a
                                                      # license to build a theme. (build-report.md A5/B8)
    user_overrides: "<what NOT to change if the user has a brand/theme>"
```

## Grid regions + bands

A **placement** assigns one authorable object to a **grid region** — either an explicit
`[col_start,row_start,col_end,row_end]` rectangle or a `design-system.yaml` token (a `defaults.<type>`
span or a `layouts.<name>` template) — plus a semantic **band** label. Authoring resolves the region to
pixels with the [cell math](layout-guidelines.md#grid-12x12) and snaps to 8; it never invents per-visual
dimensions. This keeps the contract aligned with the two-tier enforcement
([`design-system.md`](design-system.md#enforcement-is-two-tier)) — the same `design-system.yaml` grid the
generator reads is the one the audit hook checks.

The **band** is a semantic label on grid rows (the detail gradient — story, not geometry); the **region**
says where. Default bands (tune per `design-system.yaml` `bands`):

| Band | Grid rows | Typical fill |
|---|---|---|
| `summary` | 1–3 | page title (row 1, left-anchored) + slicers (right); KPI/cards with context |
| `analysis` | 4–9 | charts — the hero region(s) |
| `detail` | 10–12 | table/matrix, usually full-width |

A full-height **rail** (e.g. `[1,1,3,13]`) crosses all three bands — grid regions express 2D layouts a
flat zone stack can't.

## Space rules

The contract must account for the **whole grid**, not just avoid overlaps:

- **No reserved-but-unfilled region.** Every band you list has ≥1 placement (`space_budget.bands_used`),
  and no region is declared then left empty. Dead cells read as unfinished — don't reserve grid you
  won't fill; widen a gap instead.
- **No bare single-value `cardVisual` as the largest/dominant region.** Cards encode one number; an
  oversized card starves richer visuals. The hero is the trend / driver / variance / map / table. A
  card-like hero is allowed **only** as a composite KPI treatment (value + Δ/reference + sparkline or
  threshold band) with a `balance_rationale` — see [S9](../references/signatures.md#s9-composite-kpi-focus).
- **Balance the whole page (quantitative check).** Beyond "no empty region": a single **non-hero** data
  region shouldn't exceed **~45%** of the content area (below the summary band) on a page with 4+ data
  visuals — if it does, it's the hero and `balance_rationale` must say why the rest stays readable. Grid
  emptiness (`space_budget.emptiness_pct` = unfilled cells ÷ 144) stays **≤15%** for analytical /
  operational / comparative pages, **≤20%** for executive / narrative (whitespace serving the story). No
  contiguous empty block taller than one band.
- **Every callout/context tile earns its space.** It needs `context:` / `insight_basis` tied to a derived
  value (Δ, variance %, rank shift, gap-to-benchmark, threshold, narrative). If the only available value
  is the same absolute measure plotted next to it, remove it.
- **Summary band reserved.** Exactly one `page_title` textbox (region in row 1) with a non-empty
  **insight** title (not "Overview"/"Dashboard"). Slicers sit right of the title or in a side rail.
  **No data visual's region starts under a slicer** — raising z-order is not a fix
  ([layout golden rules](layout-guidelines.md)).
- **Equal gaps, no overlap, snapped.** Regions share the grid's gutter (16px / 24 on FHD) and margin;
  no two regions overlap; resolved positions/sizes snap to 8. Query real page dims first
  ([page-dimensions](page-dimensions.md)) — the grid re-derives cells per canvas.
- **Perf budget.** Keep data visuals to 6–8 per page where the archetype allows
  ([layout-guidelines](layout-guidelines.md#visual-count-vs-performance)).
- **Date slicer grain.** Year dropdown/tile by default; `between` only for renderable Date/DateTime
  fields where range exploration is the page question.

## Counter-examples to fix before handoff

```yaml
# ✗ Dead grid — the detail band is claimed but nothing fills rows 10-12
space_budget: { bands_used: [summary, analysis], emptiness_pct: 25 }   # >15%, a whole band empty
# Fix: extend the analysis regions down to fill, OR add a real detail table/source-note in rows 10-12.
```

```yaml
# ✗ Card hero — a single number owns the analysis band
- id: total_revenue
  kind: cardVisual
  band: analysis
  region: [1, 4, 7, 10]                    # half the grid on one value
  field_bindings: Sales[Revenue]
space_budget: { largest_region: total_revenue }
# Fix: shrink the card to a summary-band region [1,2,4,4]; give the analysis band to the trend/driver
# that PROVES the headline. Or make it a composite KPI tile (value + Δ + sparkline) and say so in balance_rationale.
```

## Validation checklist

Before handoff, fix any failure (the [04-review validator](../../../04-review/audit/layout-contract-validate.md)
checks the finished report against the same list):

- [ ] `generated_by: powerbi-report-design-room` + `contract_version` present.
- [ ] Every page has `archetype`, `layout_variant`, `variant_rationale`, `page_size`.
- [ ] Every page has exactly one `page_title` placement (row-1 region) with a non-empty **insight** title.
- [ ] Every placement carries a grid `region` (or a resolvable `token`) and a `band`; no two regions overlap.
- [ ] Every listed band has ≥1 placement; `space_budget.emptiness_pct` within tier (≤15% / ≤20%).
- [ ] `largest_region` is not a bare single-value card (composite KPI hero must say so).
- [ ] Every callout/context tile has a derived `context:` / `insight_basis`; none duplicates an adjacent absolute measure.
- [ ] Slicers in the summary band (right of title) or a side rail; no data-visual region starts under a slicer.
- [ ] Equal gutters / equal margins / no overlap / regions snap to 8; page dims queried (grid re-derives per canvas).
- [ ] Every chart/table/map placement has `purpose` + `field_bindings`.
- [ ] Bar/column placements specify `sort_policy`.
- [ ] Every color-bearing measure visual has a `color_strategy` resolvable against `color_map`.
- [ ] Date slicer type matches grain + audience.
- [ ] Field display names are human-readable (no `Count of order_line_id`); rates format as `%`.
- [ ] Multi-page: pages share one tone+signature; archetypes/variants rotate ([composition](../references/composition.md)).

## Related
- [`../build-report.md`](../build-report.md) — Step 6 emits this block
- [design-system.md](design-system.md) · [detail-gradient.md](detail-gradient.md) · [layout-guidelines.md](layout-guidelines.md) — the vocabulary this contract speaks
- [`../../../04-review/audit/layout-contract-validate.md`](../../../04-review/audit/layout-contract-validate.md) — the gate that checks the built report against it
