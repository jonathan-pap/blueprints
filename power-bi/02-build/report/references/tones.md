# Tone catalog

> A **tone** is the report's feel, expressed as a free-text adjective + short elaboration. This is a
> *calibration set*, not a closed menu — prefer an entry when it fits, otherwise remix two or author a
> custom tone. The point: a tone is a **constraint** that makes every later choice (palette, type,
> density, borders) easier. Tone is not decoration.

Each entry maps the tone to **downstream choices** so picking it actually drives decisions. Those
choices feed two rooms:

- typography + palette + gridline/border treatment → encode in the **theme**
  ([`../../theme/create/typography-roles.md`](../../theme/create/typography-roles.md),
  [`../../theme/create/color-system.md`](../../theme/create/color-system.md))
- density / rhythm → informs the **dimensions**
  ([`../layout/design-system.md`](../layout/design-system.md), [`../layout/layout-guidelines.md`](../layout/layout-guidelines.md))

## Font guardrail (blueprint rule)

Catalog font names are **design direction**. Power BI only reliably renders a built-in set across
Desktop + Service + mobile + embedded. **Prefer Segoe UI, DIN, Georgia, Consolas, Arial, Calibri,
Tahoma, Verdana.** When a tone calls for a font outside that set, name it as direction *and* specify a
built-in fallback — never assume Service matches Desktop. Set fonts via `textClasses` in the theme,
not per-visual, unless a [signature](signatures.md) requires a per-visual numeric font.

## If your tone is one vague word

"Modern" / "professional" / "clean" are ambiguous. Do one of two things:

1. **Pick a catalog entry** — "Editorial Newsroom", "Corporate Cool", "Minimal Restrained" are not ambiguous.
2. **Write a short elaboration** — "modern" → "modern editorial: serif display headings, sans body,
   single amber accent, no chart gridlines."

A custom tone must pin: emotional feel/audience posture · surface/palette direction · typography
direction · density/spacing direction · one concrete downstream implication.

---

## 1. Editorial Newsroom
> Reads like a Sunday business broadsheet. Type leads. One sharp accent. Whitespace generous.

| Aspect | Pick |
|---|---|
| Display type | Serif — **Georgia** (PBI-safe) at 28–48pt |
| Body type | Sans — **Segoe UI** at 11–13pt |
| Surface | Cream `#FAF7F0` or off-white `#F8F9FA` |
| Accent | One — black `#0F172A`, or mustard `#D4A30A` for highlight |
| Density | 1.500 (Perfect Fifth) — strong hierarchy |
| Gridlines | Hairline rules between sections; **no chart gridlines** |
| Borders | None on visuals; section dividers only |
| Signature | [S2 display serif headlines](signatures.md#s2-display-serif-headlines) + [S1 tabular numerals](signatures.md#s1-tabular-numerals-throughout) |
| Iconography | Outlined hairline (1px), restrained |
| Domain | Board quarterly review, annual report, financial publication, media analytics |

## 2. Industrial Cockpit
> Dark canvas, instrument-panel feel. High contrast. Color reserved for status, not decoration.

| Aspect | Pick |
|---|---|
| Display type | Geometric sans bold — **Segoe UI Bold** / DIN at 24–36pt |
| Body type | Same family, regular, 10–12pt |
| Surface | Dark navy `#120E2A` or near-black `#0E0E10` |
| Accent | Indigo `#5772D9` + cyan `#8CEEEE` for status; muted purple `#7D77A8` for chrome |
| Density | 1.333 (Perfect Fourth) — density-friendly |
| Gridlines | Dotted, low-opacity `#3A3A4A` |
| Borders | Subtle `#2A2A3A`; prefer background-fill cards for grouping |
| Signature | [S8 status-coded KPI cards](signatures.md#s8-status-coded-kpi-cards), [S5 single-accent](signatures.md#s5-single-accent-discipline) |
| Iconography | Filled, geometric, high contrast |
| Domain | Ops monitoring, NOC/wallboards, infrastructure health |

> Dark mode triggers every formatting trap at once (tables/cards stay white). Carry the dark-mode
> checklist into authoring — see [`../format/`](../format/_index.md) and theme wildcard handling.

## 3. Clinical Calm
> Cool almost-white canvas, teal/sage accents, generous spacing. Healthcare without sterile.

| Aspect | Pick |
|---|---|
| Display type | Humanist sans — **Segoe UI** at 22–32pt |
| Body type | Same, regular, 11pt |
| Surface | Cool blue-white `#F0F9FF` |
| Accent | Teal `#0D9488` + sage `#84CC16`; **reserve red strictly for genuine alerts** |
| Density | 1.250 (Major Third) — gentle |
| Gridlines | Solid, very-low-opacity `#E5E7EB` |
| Borders | 1px hairline `#E5E7EB`, radius 8 |
| Signature | [S5 single-accent](signatures.md#s5-single-accent-discipline) (teal), [S13 duotone icons](signatures.md#s13-duotone-iconography-on-kpi-cards) muted |
| Domain | Patient-safety dashboards, clinical ops, wellness programs |

## 4. FT Pink Financial
> The Financial Times pink-tinted broadsheet. Tabular numerals everywhere. Editorial discipline on financial data.

| Aspect | Pick |
|---|---|
| Display type | Serif — **Georgia** at 28–48pt |
| Body type | Sans — **Segoe UI** with aligned numeric treatment where values must column |
| Surface | Pink-tinged white `#FFF1E5` (FT pink) |
| Accent | Black `#0F172A` for type; one teal/red for variance only |
| Density | 1.500 |
| Gridlines | None on charts; thin rules between sections |
| Signature | [S1 tabular numerals](signatures.md#s1-tabular-numerals-throughout) + [S7 tinted surface](signatures.md#s7-ft-pink-or-any-tinted-surface) |
| Domain | Asset-management reporting, earnings dashboards, market commentary |

## 5. Bauhaus Catalog
> Geometric, modernist, functional. Primary colors used sparingly. Type-as-signal.

| Aspect | Pick |
|---|---|
| Display type | Geometric sans — **DIN** / Segoe UI Bold at 32–48pt; consider all-caps tracking |
| Body type | Same family, 11–13pt |
| Surface | Off-white `#FAFAFA` |
| Accent | One primary — red `#E63946`, blue `#1D3557`, or yellow `#F4D03F` |
| Density | 1.333 |
| Gridlines | None or solid hairline |
| Borders | Strong (2px) where used; otherwise none |
| Signature | [S3 all-caps tracked headlines](signatures.md#s3-all-caps-tracked-headlines) |
| Domain | Design-team dashboards, brand reporting, creative-agency analytics |

## 6. Monospace Terminal
> Developer/quant feel. Monospaced numbers. Ticker-style KPI bars. Color used like syntax highlighting.

| Aspect | Pick |
|---|---|
| Display type | Monospace — **Consolas** at 24–36pt, or sans display + mono numerals |
| Body type | Consolas 11pt, or Segoe UI body with mono numerals |
| Surface | Off-white `#F8F8F2` or near-black `#0E0E10` |
| Accent | Two syntax-token accents — green `#268BD2`-family + amber `#B58900` (Solarized) |
| Density | 1.250 — dense |
| Gridlines | Dotted, monospace-grid feel |
| Signature | [S1 tabular numerals](signatures.md#s1-tabular-numerals-throughout) + monospaced KPI ticker bar |
| Domain | Engineering dashboards, quant trading, observability |

## 7. Industrial Dense (Analyst Workbench)
> Off-white surface, dense data, charcoal type, two-color accent. Built for an hour in the report.

| Aspect | Pick |
|---|---|
| Display type | Sans — **Segoe UI** at 18–26pt |
| Body type | Same, 10–11pt |
| Surface | Off-white `#FAFAFA` |
| Accent | Steel blue `#3B6E91` + burnt orange `#C8742A`; charcoal `#262626` text |
| Density | 1.250 — packed but legible |
| Gridlines | Solid `#E5E5E5` — packed grids need them |
| Borders | 1px `#E0E0E0` — defines cells |
| Signature | [S1 tabular numerals](signatures.md#s1-tabular-numerals-throughout) + [S12 modular grid](signatures.md#s12-modular-grid-with-consistent-gutter) |
| Domain | Financial models, ops analytics, sales-pipeline workbenches, IBCS variance |

## 8. Playful Energetic
> Warm, bright, geometric. Coral and warm accents. Soft shapes. Consumer feel without childish.

| Aspect | Pick |
|---|---|
| Display type | Rounded geometric — **Segoe UI** (rounded fallback) at 28–40pt |
| Body type | Same, 11pt |
| Surface | Warm cream `#FFF7ED` |
| Accent | Coral `#FB7185` + black `#171717`; peach `#FED7AA` for cues |
| Density | 1.333 — friendly |
| Gridlines | None on charts; pill-shaped section labels instead |
| Borders | Rounded (radius 12–16); soft shadow on primary KPI cards OK |
| Signature | [S11 pill-shaped section labels](signatures.md#s11-pill-shaped-section-labels) + [S13 duotone icons](signatures.md#s13-duotone-iconography-on-kpi-cards) |
| Domain | Consumer/retail, lifestyle, hospitality, creator-economy |

## 9. Minimal Restrained
> White canvas, black type, one accent, no chartjunk. Relies entirely on confident hierarchy.

| Aspect | Pick |
|---|---|
| Display type | Sans — **Segoe UI** at 24–48pt |
| Body type | Same, regular, 11pt |
| Surface | True white `#FFFFFF` |
| Accent | One — black `#0F172A` for type + ONE single hue for the highlight |
| Density | 1.500 or 1.618 — hierarchy via size, since color isn't doing the work |
| Gridlines | None |
| Borders | None |
| Signature | [S5 single-accent](signatures.md#s5-single-accent-discipline), [S9 composite KPI focus](signatures.md#s9-composite-kpi-focus), [S10 hairline rules](signatures.md#s10-hairline-rules-instead-of-borders) |
| Domain | Executive landing pages, primary-metric-with-context reports |

## 10. Corporate Cool
> Default for B2B SaaS / enterprise. Cool grey surface, slate type, one tech accent. Restrained, not stark.

| Aspect | Pick |
|---|---|
| Display type | Sans — **Segoe UI Semibold** at 22–32pt |
| Body type | Same, 11pt |
| Surface | Cool grey `#F1F5F9` |
| Accent | Slate `#334155` + cyan `#06B6D4`; slate-300 `#CBD5E1` cues |
| Density | 1.333 |
| Gridlines | Solid `#E2E8F0`, low-opacity |
| Borders | 1px `#E2E8F0`, radius 8 |
| Signature | [S5 single-accent](signatures.md#s5-single-accent-discipline) (cyan) |
| Domain | B2B SaaS metrics, enterprise dashboards, internal tooling |

## 11. Scholarly Calm
> Stone surface, forest-green + soft-red accents, serif headings, no bright colors. Reads like a paper.

| Aspect | Pick |
|---|---|
| Display type | Serif — **Georgia** at 22–32pt |
| Body type | Sans — **Segoe UI** at 11pt |
| Surface | Stone `#F5F5F4` |
| Accent | Forest `#1C5E47` + soft red `#C2615F`; stone-400 `#A8A29E` cues |
| Density | 1.250 — gentle |
| Gridlines | Hairline rules, low-opacity |
| Signature | [S2 display serif](signatures.md#s2-display-serif-headlines) + [S4 caption annotations](signatures.md#s4-caption-style-annotations-under-every-visual) |
| Domain | Research dashboards, academic analytics, policy reporting, public-data viz |

## 12. Brand-Forward (template)
> When the user provides brand guidelines, **treat the brand as the tone.** A template — adapt to the brand.

| Aspect | Pick |
|---|---|
| Display type | Brand display font + **system fallback chain** (always include Segoe UI) |
| Body type | Brand body font + Segoe UI fallback, 11pt |
| Surface | Brand-neutral surface (tinted toward brand if defined) |
| Accent | Primary brand color for main emphasis; secondary for context |
| Density | From brand mood — energetic → 1.5; restrained → 1.25 |
| Gridlines/Borders | Match the brand's rule/container treatment |
| Signature | [S14 brand logos in cards](signatures.md#s14-channelbrand-logos-in-cards), or the brand's most recognizable move |
| Domain | Customer-facing branded dashboards, white-label reports |

---

## Remixing tones

Two tones compose only if the result is coherent:

- **Editorial Newsroom × FT Pink** → serif display + tabular numerals + pink surface. ✓
- **Industrial Cockpit × Bauhaus** → dark canvas + geometric type + primary accent. ✓
- **Playful Energetic × Clinical Calm** → coral + teal? Pick one. ✗

When in doubt, pick ONE and apply it cleanly. A muddied tone reads as no tone at all.

## Default tone by domain (when the user is silent)

If the prompt is specific enough to design but gives no tone, use domain as a recommendation signal —
and **surface it as an assumption in the brief** ("Recommended tone: **Industrial Cockpit**…"). If the
prompt is *vague* (missing audience/purpose/page-count/filter depth), run the
[identity-workflow](../build-report.md) clarification first; offer the domain tone as one option,
not as permission to proceed silently.

| Domain | Default tone |
|---|---|
| Finance / banking / audit | Corporate Cool or Editorial Newsroom |
| Healthcare / clinical | Clinical Calm |
| Operations / NOC | Industrial Cockpit (dark) or Industrial Dense (light) |
| Retail / consumer / lifestyle | Playful Energetic |
| Engineering / observability / quant | Monospace Terminal or Industrial Dense |
| Executive landing / board | Minimal Restrained or Editorial Newsroom |
| B2B SaaS / enterprise | Corporate Cool |
| Research / academic / policy | Scholarly Calm |
| Brand-led (guidelines provided) | Brand-Forward |

## Related
- [signatures.md](signatures.md) — the recurring visual move the tone implies
- [`../../theme/create/typography-roles.md`](../../theme/create/typography-roles.md) · [`../../theme/create/color-system.md`](../../theme/create/color-system.md) — where the tone becomes theme JSON
- [identity-workflow.md](../build-report.md) — Step 1 commits the tone
