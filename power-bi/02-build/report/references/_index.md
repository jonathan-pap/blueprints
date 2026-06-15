# references/ — design best-practices (applied at build time)

> Dataviz judgment + design vocabulary for the build room: how to make a visual *useful*, not just
> present, and how to decide a report's look. The end-to-end process that uses these is
> [`../build-report.md`](../build-report.md).

## Design identity + vocabulary (decide what a report looks like + why)

- `design-identity.md` — the tone + signature + per-page archetype model (start here for greenfield)
- `tones.md` · `signatures.md` — the catalogs (12 tones, 15 signatures)
- `archetypes/_index.md` — per-page router → 5 archetypes (+ layout variants)
- `composition.md` — multi-page composition + variant rotation (avoid mono-archetype)
- `color-palettes.md` — CVD-safe palettes + colour-assignment strategy
- `interactivity.md` — cross-filter etiquette, interaction budget per archetype
- `accessibility.md` · `anti-patterns.md` — pre-ship checks (WCAG; the slop catalog)
- `brownfield.md` — redesign / restyle / theme-swap workflow

## Visual best-practices (how to make each visual useful)

- `cards-and-kpis.md` — the three elements (value/target/gap), display-unit rule, title-vs-label, anti-patterns
- `tables-and-matrices.md` — table vs matrix, subtract-don't-add formatting, strategic CF, the horizontal-scrollbar trap
- `visual-colors.md` — theme tokens over hex, semantic sentiment, WCAG contrast, colorblind-safe pairings

## Sibling design docs (other rooms)

- Layout mechanics → [../layout/layout-guidelines.md](../layout/layout-guidelines.md) + [../layout/detail-gradient.md](../layout/detail-gradient.md)
- Metric selection → [../../../01-brief/references/kpi-selection.md](../../../01-brief/references/kpi-selection.md)
- Report-dev mindset → [../../../01-brief/references/report-dev-mindset.md](../../../01-brief/references/report-dev-mindset.md)
