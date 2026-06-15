# Signatures

> A **signature** is the *one* defining visual move every page of a report shares — what a user
> remembers after closing it. Commit to exactly one: pick from the gallery, remix an entry, or author
> a fresh one. A signature must be **specific** (not "good typography" but "tabular-numeral KPI values
> in cards"), **recurring** (on every relevant page, not one hero), and **tone-coherent**
> ([`tones.md`](tones.md)).

Each entry names the **mechanic** — the concrete theme or per-visual change that delivers it. Theme-level
moves live in [`../../theme/`](../../theme/context.md); per-visual moves in
[`../format/override-property.md`](../format/override-property.md) and the
[`../format/conditional-fmt-*`](../format/_index.md) files.

**Font guardrail:** font names here are direction. Prefer Power BI-safe families (Segoe UI, DIN,
Georgia, Consolas, Arial, Calibri, Tahoma, Verdana) or give a fallback — see [`tones.md`](tones.md#font-guardrail-blueprint-rule).

---

## Typographic signatures

### S1. Tabular numerals throughout
> Every number — KPI values, axis labels, table cells, data labels — uses aligned (monospaced-digit)
> figures. Columns of numbers line up; the eye reads patterns instantly.

**When:** Editorial, FT-style financial, scholarly, anything quantitatively comparative.
**Mechanic:** Power BI exposes no reliable theme-level tabular-figure control. Treat as design intent:
prefer fonts whose digits align; if they don't, set **Consolas** on KPI-card/table numeric values
only (per-visual `value.fontFamily`), keep labels in the body family. Verify on a test page with two
magnitude columns.

### S2. Display serif headlines
> Page titles + section headers in a display serif (**Georgia**); body + chart text in a sans. The
> serif/sans contrast is the signature.

**When:** Editorial, Scholarly, FT-style.
**Mechanic (theme `textClasses`):** `title.fontFace` → Georgia · `largeTitle.fontFace` → Georgia
(visual titles) · `label.fontFace` → Segoe UI (labels stay legible) · `callout.fontFace` → Segoe UI
Bold (KPI values readable). Set in [`../../theme/create/typography-roles.md`](../../theme/create/typography-roles.md).

### S3. All-caps tracked headlines
> Page titles in ALL CAPS with extra letter-spacing. Reads deliberate, editorial, Bauhaus. Don't track
> body — only the headline.

**When:** Bauhaus, Industrial, Brand-forward.
**Mechanic:** Power BI exposes no reliable per-class `letter-spacing` — do **not** promise exact
tracking. Author headings/section labels as uppercase text; approximate the tracked look with
spacing/layout. Don't track lowercase runs.

### S4. Caption-style annotations under every visual
> Every chart carries a small caption (8–9pt) below it stating the takeaway. The caption is the
> headline; the chart is the evidence.

**When:** Narrative Story, Scholarly, Editorial.
**Mechanic:** per-visual `subTitle.show: true`, `text` = a hand-authored takeaway, 9pt, fontColor
`#6B7280`. For a data-driven takeaway use a [thin-report measure](../calculations/thin-report-measure.md)
bound to the subtitle.

---

## Chromatic signatures

### S5. Single-accent discipline
> One saturated accent used throughout; everything else greyscale. The eye goes straight to whatever
> wears the accent.

**When:** Minimal Restrained, Executive landing, primary-metric-with-context.
**Mechanic (theme `dataColors`):** `[0]` = the accent; `[1..7]` = greyscale ramp (`#9CA3AF`, `#6B7280`,
`#4B5563`, `#374151`, `#1F2937`, `#111827`, `#0F172A`). Primary KPI in accent; supporting cards
`#374151`; each chart's hero series in accent, others grey. See [`../format/conditional-fmt-rule.md`](../format/conditional-fmt-rule.md).

### S6. Highlight-and-grey
> All bars/lines muted grey EXCEPT the one highlighted (top performer, current period, selection). The
> highlight is the entire story.

**When:** Comparative Benchmark, Operational Monitor, "rank by X" pages.
**Mechanic:** per-visual `dataPoint.fill` with a scope/identity selector on the highlighted category →
accent; theme `dataColors[0]` = `#BDBDBD`. Mind the selector trap — see [`../schema-patterns/selectors.md`](../schema-patterns/selectors.md).

### S7. FT pink (or any tinted) surface
> Page background is a tinted surface (FT pink `#FFF1E5`, cream `#FAF7F0`, mint `#F0FDF4`) — not white,
> not grey. The tint is the signature.

**When:** Editorial Newsroom, FT Pink, Scholarly Calm.
**Mechanic:** `page.json → objects.background.color` to the tint with low transparency; keep visual
containers white `#FFFFFF` to layer. See [`../page/set-page-wallpaper.md`](../page/set-page-wallpaper.md).
Note: page `background` supports only `color`/`image`/`transparency` (no `show`).

### S8. Status-coded KPI cards
> Every KPI card's accent bar (or tint) reflects status — green good, amber warning, red bad. The board
> reads as traffic lights at a glance.

**When:** Operational Monitor, Executive Summary with status.
**Mechanic:** per-card `accentBar.color` driven by a status measure via conditional formatting; card
backgrounds stay neutral. See [`../format/conditional-fmt-rule.md`](../format/conditional-fmt-rule.md)
and [`../references/cards-and-kpis.md`](../references/cards-and-kpis.md).

---

## Structural signatures

### S9. Composite KPI focus
> The primary metric + its context is emphasized **without** wasting a hero region on a bare number.
> Eye lands on the metric, then sees why it matters.

**When:** Executive Summary, landing pages, single-question reports.
**Mechanic:** a compact-but-prominent card/tile with value + delta/reference + sparkline or threshold
band + a nearby explanation chart. Supporting cards 28–36pt. **Never let a bare single-measure
`cardVisual` occupy the largest region** — that belongs to the trend/driver/variance visual. Enforced
by [`../layout/design-contract.md`](../layout/design-contract.md) space rules.

### S10. Hairline rules instead of borders
> No borders on any visual. Section breaks marked by 1px hairline rules. Whitespace + rules carry
> structure; containers are invisible.

**When:** Editorial Newsroom, Scholarly Calm, Minimal Restrained.
**Mechanic:** per-visual `border.show: false`; `background.show: false` on chart visuals (white-on-white);
section dividers = 1px-tall **shape** rectangles `#E5E7EB` (not textboxes — textboxes render ~24px tall
regardless of height; use a shape — see [`../add-visual/shape.md`](../add-visual/shape.md)).

### S11. Pill-shaped section labels
> Section headers wrapped in rounded-end pills. Every section ("KPIs", "Trends", "Top Performers") gets
> one. Reads warm, modern, energetic.

**When:** Playful Energetic, consumer-facing, brand-forward.
**Mechanic:** textbox/shape with `background.color` (warm tint), `border.radius: 24`, h-padding 16,
top-left of each section.

### S12. Modular grid with consistent gutter
> Every visual snaps to a strict grid with a single gutter (16 or 24px). No off-grid elements. The
> signature is the regularity itself.

**When:** Industrial Dense, Bauhaus, analyst workbench.
**Mechanic:** the brief sets the gutter; [`../layout/design-system.md`](../layout/design-system.md)
(`design-system.yaml`) encodes it and [`audit-layout-consistency.sh`](../../../04-review/hooks/) enforces
it — off-grid/sub-pixel positions are flagged. This signature is *free* if you follow the layout golden rules.

---

## Iconographic signatures

### S13. Duotone iconography on KPI cards
> Every KPI card carries a duotone icon (filled silhouette + accent overlay) left of the value. A
> consistent visual family.

**When:** Playful Energetic, Corporate Cool with personality, B2B SaaS.
**Mechanic:** registered PNGs (one per metric) at 32px via `StaticResources/RegisteredResources/`; keep
sizing/style consistent across the row. See [`../add-visual/image.md`](../add-visual/image.md).

### S14. Channel/brand logos in cards
> One KPI card per channel/platform/region/competitor, each carrying that entity's logo. The logo IS
> the card's identity.

**When:** Multi-platform marketing, competitor benchmarking, multi-region ops.
**Mechanic:** one registered PNG per entity; cards in a row, logo 32–40px top-left, value centered,
label below.

### S15. Status icons in tables
> Every row carries a status-icon column (✓ / ! / ✗ or custom glyphs). The table reads as a status board.

**When:** Operational Monitor, compliance, project tracking.
**Mechanic:** conditional-formatting icon rule on a status measure — built-in icon set or registered
custom PNGs. See [`../format/conditional-fmt-svg-icon.md`](../format/conditional-fmt-svg-icon.md) and
[`../references/tables-and-matrices.md`](../references/tables-and-matrices.md).

---

## Composing tone + signature

The signature should *emerge from* the tone. Quick coherence checks:

| If tone is… | Don't pick | Do pick |
|---|---|---|
| Editorial Newsroom | S11 pills, S13 duotone | S2 serif, S1 tabular, S10 hairline |
| Industrial Cockpit | S2 serif, S11 pills | S5 single-accent, S8 status cards, S15 status icons |
| Playful Energetic | S10 hairline, S5 monochrome | S11 pills, S13 duotone, S14 logos |
| Minimal Restrained | S13 duotone, S11 pills | S5 single-accent, S9 composite KPI, S10 hairline |
| FT Pink Financial | S11 pills, S13 duotone | S1 tabular, S2 serif, S7 tinted surface |
| Monospace Terminal | S2 serif, S11 pills | S1 tabular, S5 single-accent, S15 status icons |
| Industrial Dense | S11 pills, S9 (too sparse) | S1 tabular, S12 modular grid, S15 status icons |
| Clinical Calm | S5 with red (red = alerts only) | S5 teal/sage, S10 hairline, S13 muted duotone |

When tone and signature feel disconnected the signature wins visually — but reads as accidental. Pick
one the tone naturally supports.

## Authoring a fresh signature

If none fit, author one. A good signature: (1) one sentence describes it, (2) it's theme/VCO-authorable,
(3) it recurs across pages, (4) it's tone-coherent. Record it in the brief's
`design_identity.signature` field with that one-sentence pattern.

## Related
- [tones.md](tones.md) — the tone the signature must serve
- [`../layout/design-contract.md`](../layout/design-contract.md) — where `design_identity.signature` is recorded + checked
- [archetypes/_index.md](archetypes/_index.md) — the per-page layout the signature decorates
