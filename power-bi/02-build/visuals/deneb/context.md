# Engine — Deneb (Vega / Vega-Lite)

> Declarative custom visuals built on Vega or Vega-Lite. Best for advanced interactive charts that the native visual catalogue can't express.

## When to use Deneb

- Cross-filter + hover + tooltip interactivity matter (Python/R don't have this).
- The chart type doesn't exist in native Power BI (radial, sankey, parallel coordinates, custom bullet).
- You need to compose multiple marks with shared scales.
- You want declarative JSON (versionable, diffable).

## When NOT to use Deneb

- Simple inline graphics in tables → use `../svg/` instead (lighter, no custom visual install).
- Static statistical chart → use `../python/` or `../r/`.

## Quickstart

1. Install the Deneb custom visual in Power BI Desktop (one-time, via AppSource or organizational store).
2. Add a Deneb visual to the page.
3. Bind fields (any role works — Deneb consumes them as `dataset`).
4. Paste a spec (Vega-Lite preferred for simplicity, Vega for advanced).
5. Apply settings from `examples/standard-config.json` (display mode, theme integration).

## Workflow router

- **Pick a dialect** → `vega-vs-vega-lite.md`
- **Minimum spec shape** → `spec-anatomy.md`
- **How Deneb is wired into PBIR** → `pbir-integration.md`
- **Bind Power BI fields into a spec** → `bind-pbi-data.md`
- **Cross-filter integration (selection signals)** → `selection-signals.md`
- **Per chart type** → `charts/_index.md` for bar / line / kpi-card / bullet / trend-with-target / ytd-comparison / ytd-line
- **Inspiration** → `community-examples.md`

## Examples

Spec-only (paste straight into Deneb):

- `examples/spec/vega-lite/bar-chart.json`
- `examples/spec/vega-lite/kpi-card.json`
- `examples/spec/vega-lite/bullet-chart.json` (Vega-Lite version)
- `examples/spec/vega/bar-chart.json` (Vega version for comparison)
- `examples/spec/vega/line-chart.json`

Full visual JSON (drop into `<project>.Report/definition/pages/<page>/visuals/`):

- `examples/visual/bullet-chart.json`
- `examples/visual/kpi-card.json`
- `examples/visual/trend-line.json`
- `examples/visual/ytd-comparison.json`
- `examples/visual/ytd-line-chart.json`

Standard config:

- `examples/standard-config.json` — baseline Deneb config block (theme integration, display mode, tooltip behaviour).

## Rules

- Always start from a known-good spec example, not from scratch.
- Use Power BI theme colors via `{ "expr": "pbiColor(N)" }` rather than hardcoded hex.
- Use Deneb's `selection` signals to integrate with Power BI cross-filter.
- Cap data point count — Deneb renders client-side; large datasets degrade performance.

## Before showing to the user

Run `../../../04-review/reviewers/deneb-review.md` — 10-point validation checklist.
