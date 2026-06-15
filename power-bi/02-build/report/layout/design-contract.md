# Design contract — the `Design Brief:` handoff

> The authoritative handoff from the [design room](../references/design-identity.md) to **authoring**. It specifies
> **what** to build — page intent, design identity, semantic bindings, and a per-page layout contract.
> Authoring computes **how** — exact `pbir` commands, coordinates, theme JSON, validation, screenshots.
>
> This is the blueprint's port of the design-brief contract, expressed in **our** vocabulary: page sizes
> from [`design-system.md`](design-system.md) (`design-system.yaml`), the 3-zone
> [detail gradient](detail-gradient.md), and the equal-gap golden rules in
> [`layout-guidelines.md`](layout-guidelines.md). It does **not** introduce a parallel 12×12 grid.

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
- **`pages[].layout_contract`** — the geometry handoff, in zones + tokens. Authoring resolves it against
  `design-system.yaml` and the equal-gap math; the audit hook checks the result.
- **`space_budget`** — forces accounting for the whole page (no dead zones, no bare-card hero).
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
        # zones = detail-gradient bands. Each placement names a zone + a design-system.yaml token.
        header_band:
          - id: page_title
            kind: textbox
            text: "Revenue Fell 8% YoY in EMEA"
            purpose: "State the page insight before any chart."
          - id: year_slicer
            kind: slicer
            token: defaults.slicer
            field_bindings: Date[CalendarYear]
            slicer_type: dropdown
        zone1_summary:
          token: layouts.kpi_row_4
          placements:
            - id: revenue_card
              kind: cardVisual
              purpose: "What is total revenue, vs last year?"
              field_bindings: Sales[Revenue]
              context: Sales[Revenue YoY %]          # the Δ that earns the card its space
              color_strategy: measure_match
            # ... remaining cards in the row token
        zone2_analysis:
          placements:
            - id: revenue_trend
              kind: lineChart
              purpose: "How is revenue trending?"
              field_bindings: { axis: Date[Quarter], values: Sales[Revenue] }
              color_strategy: measure_match
            - id: top_regions
              kind: barChart
              purpose: "Which regions drive the gap?"
              field_bindings: { category: Region[Name], values: Sales[Revenue YoY %] }
              sort_policy: value_asc                  # most negative first
              color_strategy: gradient
        zone3_detail:
          placements:
            - id: region_detail
              kind: tableEx
              purpose: "Which regions/products need follow-up?"
              field_bindings: [Region[Name], Product[Name], Sales[Revenue], Sales[Revenue YoY %]]
      space_budget:
        zones_used: [header_band, zone1_summary, zone2_analysis, zone3_detail]
        empty_zones: []                               # MUST be empty — no reserved-but-unfilled zone
        largest_zone: zone2_analysis                  # the hero is analysis, NOT a card
        balance_rationale: "KPI strip + trend/driver hero + detail row fill the canvas; no dead band."
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

## Zones, not a grid

A **placement** assigns one authorable object to one **zone** + (optionally) a `design-system.yaml`
token that fixes its size/position. Authoring resolves the numbers from the token and the
[equal-gap math](layout-guidelines.md#symmetrical-spacing-critical); it never invents per-visual
dimensions. This keeps the contract aligned with the two-tier enforcement
([`design-system.md`](design-system.md#enforcement-is-two-tier)) — the same `design-system.yaml` the
generator reads is the one the audit hook checks.

| Contract zone | Detail-gradient band | Typical fill |
|---|---|---|
| `header_band` | reserved top strip | page title (left anchor) + slicers (right) |
| `zone1_summary` | Zone 1 | KPI/cards (with context), thin |
| `zone2_analysis` | Zone 2 | charts — the hero region |
| `zone3_detail` | Zone 3 | table/matrix, usually full-width |

## Space rules

The contract must account for the **whole page**, not just avoid overlaps:

- **No empty/reserved-but-unfilled zone.** Every zone listed has ≥1 placement, or it isn't listed.
  `space_budget.empty_zones` must be `[]`. (Dead bands read as unfinished.)
- **No bare single-value `cardVisual` as the largest/dominant region.** Cards encode one number; an
  oversized card starves richer visuals. The hero is the trend / driver / variance / map / table. A
  card-like hero is allowed **only** as a composite KPI treatment (value + Δ/reference + sparkline or
  threshold band) with a `balance_rationale` — see [S9](../references/signatures.md#s9-composite-kpi-focus).
- **Every callout/context tile earns its space.** It needs `context:` / `insight_basis` tied to a derived
  value (Δ, variance %, rank shift, gap-to-benchmark, threshold, narrative). If the only available value
  is the same absolute measure plotted next to it, remove it.
- **Header band reserved.** Exactly one `page_title` textbox with a non-empty **insight** title (not
  "Overview"/"Dashboard"). Slicers sit right of the title or in a side rail. **No data visual starts
  under a slicer** — raising z-order is not a fix ([layout golden rules](layout-guidelines.md)).
- **Equal gaps, no overlap, snapped.** All horizontal gaps equal; all vertical gaps equal; equal edge
  margins; positions/sizes on the 8/16px grid. Query real page dims first ([page-dimensions](page-dimensions.md)).
- **Perf budget.** Keep data visuals to 6–8 per page where the archetype allows
  ([layout-guidelines](layout-guidelines.md#visual-count-vs-performance)).
- **Date slicer grain.** Year dropdown/tile by default; `between` only for renderable Date/DateTime
  fields where range exploration is the page question.

## Counter-examples to fix before handoff

```yaml
# ✗ Dead band — a zone is reserved but nothing fills it
space_budget: { zones_used: [header_band, zone1_summary, zone2_analysis], empty_zones: [zone3_detail] }
# Fix: expand zone2 to fill, OR add a real detail table/source-note, OR drop zone3_detail entirely.
```

```yaml
# ✗ Card hero — half the canvas spent on one number
zone2_analysis:
  placements: [ { id: total_revenue, kind: cardVisual, field_bindings: Sales[Revenue] } ]
space_budget: { largest_zone: zone2_analysis }
# Fix: move the card to zone1_summary; give zone2 to the trend/driver that PROVES the headline.
# Or make it a composite KPI tile (value + Δ + sparkline) and say so in balance_rationale.
```

## Validation checklist

Before handoff, fix any failure (the [04-review validator](../../../04-review/audit/layout-contract-validate.md)
checks the finished report against the same list):

- [ ] `generated_by: powerbi-report-design-room` + `contract_version` present.
- [ ] Every page has `archetype`, `layout_variant`, `variant_rationale`, `page_size`.
- [ ] Every page has exactly one `page_title` placement with a non-empty **insight** title.
- [ ] Every listed zone has ≥1 placement; `space_budget.empty_zones` is `[]`.
- [ ] `largest_zone` is not a bare single-value card (composite KPI hero must say so).
- [ ] Every callout/context tile has a derived `context:` / `insight_basis`; none duplicates an adjacent absolute measure.
- [ ] Slicers in `header_band` (right of title) or a side rail; no data visual starts under a slicer.
- [ ] Equal gaps / equal margins / no overlap / snapped to grid; page dims queried.
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
