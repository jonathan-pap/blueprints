# Layout-contract conformance

> Check a **built report against its approved `Design Brief:`** — did authoring implement the contract?
> This is a *conformance* gate (build vs. spec), distinct from [`visual-design.md`](visual-design.md)
> (generic design quality) and the hard [`audit-layout-consistency.sh`](../hooks/) hook (off-token sizes,
> off-grid positions). Run all three for a design-led report.

## When to run

After a report built from a [design contract](../../02-build/report/layout/design-contract.md) — at
handoff, and again after any layout edit. Skip for trivial single-visual brownfield changes (the
minimal-brief escape hatch).

## Inputs

1. The approved `Design Brief:` (from `01-brief/` or the conversation — the source of truth).
2. The built `<project>.Report/definition/` PBIR.
3. `pbir` CLI for inventory: `pbir preview-pages`, `pbir preview-visuals`, `pbir preview-filters`
   (or read `pages.json` + each `visual.json`).

## Conformance checks

Walk each, marking **Pass / Warn / Fail**. A Fail means the build diverged from the approved contract —
fix the report (not the brief) unless the brief itself was wrong.

### Provenance & coverage
- [ ] Brief begins with `generated_by: powerbi-report-design-room` + `contract_version`.
- [ ] Every `pages[]` entry in the brief exists in `pages.json`, and vice-versa (no extra/missing pages).
- [ ] Each built page's visual set matches its `layout_contract` placements (no orphan visuals, none dropped).

### Per-page structure
- [ ] Exactly one `page_title` textbox per page, text = the brief's **insight** title (not "Overview"/"Dashboard").
- [ ] Every contract zone has its placements built; `space_budget.empty_zones` is `[]` and no built zone is empty.
- [ ] `largest_zone` in the build is not a bare single-value `cardVisual` (composite KPI hero must carry value + Δ/spark/threshold).
- [ ] Slicers sit in the header band (right of title) or a side rail; **no data visual starts under a slicer region**.
- [ ] Data-visual count per page within the [perf budget](../../02-build/report/layout/layout-guidelines.md#visual-count-vs-performance) (6–8 where the archetype allows).

### Bindings & encoding
- [ ] Every chart/table/map has the `field_bindings` the contract names — verify against canonical model names ([`../../02-build/report/bind/find-canonical-name.md`](../../02-build/report/bind/find-canonical-name.md)).
- [ ] `color_strategy` honored: `measure_match` measures use the same `color_map` color on every visual + page; gradients run tint→base.
- [ ] Bar/column visuals sorted per `sort_policy` (not left alphabetical).
- [ ] Every callout/context tile shows its derived `context`/`insight_basis` — none duplicates an adjacent absolute measure.
- [ ] Display names human-readable (no `Count of order_line_id`); rates format as `%`, not `0.53`.

### Layout hygiene (defer to the hook, spot-check here)
- [ ] Equal horizontal gaps, equal vertical gaps, equal margins, no overlap, snapped to grid — the
      [`audit-layout-consistency.sh`](../hooks/) hook is authoritative; confirm it ran clean.
- [ ] Date slicer grain matches the contract (Year dropdown/tile vs full-date `between`).

### Identity propagation
- [ ] The **tone** shows up in concrete choices (fonts, surface, gridline/border treatment) — not the
      default look. Cross-check the theme against [`../../02-build/report/references/tones.md`](../../02-build/report/references/tones.md).
- [ ] The **signature** recurs on every relevant page (the one move from the brief is actually present).
- [ ] Multi-page: all pages share one tone+signature; archetypes/variants rotated per [composition](../../02-build/report/references/composition.md).

### Accessibility — walk [`design/accessibility.md`](../../02-build/report/references/accessibility.md) testing checklist
- [ ] Alt text (insight-driven, not "chart") on every non-decorative visual; DAX alt text where the insight is filter-dependent.
- [ ] WCAG AA contrast on every text/background pair (body ≥4.5:1, large ≥3:1, non-text ≥3:1).
- [ ] No meaning by colour alone — paired with icon/arrow/label. CVD simulation passes.
- [ ] Tab order matches reading order; keyboard-only navigation works; targets ≥24×24px.
- [ ] Modern visual types only (`cardVisual`/`tableEx`/`pivotTable`/`azureMap`), no legacy `card`/`table`/`matrix`/`map`/`filledMap`.

### Anti-pattern detection — run [`design/anti-patterns.md`](../../02-build/report/references/anti-patterns.md) heuristics
- [ ] No `strong-warn` triggers unresolved: dual axis · bar baseline ≠ 0 · contrast <4.5:1.
- [ ] `warn` triggers reviewed: >8 hues · >6 cards · pie/donut >5 · >12 visuals · empty alt text · ops page without freshness timestamp.

## Output

Write a conformance audit to `../../outputs/` alongside the design-quality audit:

```
2026-06-10-<project>-contract-conformance.md
```

Record per check: Pass / Warn / Fail + the offending page/visual ID + the fix. A clean run = the build
faithfully implements the approved design. Pair with [`visual-design.md`](visual-design.md) for the
subjective quality pass.

## Related
- [`../../02-build/report/layout/design-contract.md`](../../02-build/report/layout/design-contract.md) — the contract this validates against
- [visual-design.md](visual-design.md) — generic design quality (run alongside) · [pbir-validate.md](pbir-validate.md) — structural PBIR validity
- [`../hooks/`](../hooks/) — `audit-layout-consistency.sh` (hard layout gate)
