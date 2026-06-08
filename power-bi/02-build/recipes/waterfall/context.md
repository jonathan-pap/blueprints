# Recipe — Stacked waterfall (DAX-driven funnel/attrition)

> A **DAX-driven waterfall** on a native `lineStackedColumnComboChart` (vertical) or
> `barChart` (horizontal) — a **disconnected steps table** drives a transparent floater plus
> per-step body measures via `SELECTEDVALUE`. Each step renders as totals (start, intermediate,
> end) and drops (subtractions) in a single floating-bar visualization. No native waterfall
> visual — fully controllable colors, labels, and step composition.

## The idea in one line

Power BI's native `waterfallChart` is rigid. Build a waterfall from a **stacked column** plus a
**transparent base** that lifts each colored bar to its floating position — and a **disconnected
steps table** on the category axis that lets every measure use `SELECTEDVALUE(<STEPS>[Step])` to
decide what to emit per step.

## The trick — disconnected steps + SELECTEDVALUE switching

The disconnected `<STEPS_TABLE>` (a calculated `UNION` of `SELECTCOLUMNS` over inline rows) sits
on the chart's Category role. Every measure reads its current step via `SELECTEDVALUE` and
returns the right number — value, drop, BLANK — for *that* step only. Stacked together:

- **`<PREFIX> Base`** — the transparent floater. SWITCH per step: returns 0 for totals, the
  running floor (e.g. the value the drop falls to) for drops. Set `fillTransparency: 100D`.
- **`<PREFIX> Body · <Step>`** — one measure per step, `IF SELECTEDVALUE = "<Step>"` returns the
  body value, else BLANK. One measure per step gives independent **color, label, and visibility
  control per bar**.

That's the engine. Everything else (labels, axis-max, horizontal pad) is variations on the same
idea.

## When to use

- **Funnel / attrition stories** — "X started, Y dropped off, Z completed" with totals + losses.
- **Variance bridges** — "Q1 actual → +Price → -Volume → -Mix → Q4 actual."
- **Composition cascades** — anywhere a flat total benefits from showing where it goes.
- When the native waterfall is too rigid (no per-step color, no rich labels, no totals flagging).

For a *simple* variance bridge with just sign-driven coloring, the native `waterfallChart`
([`../../report/add-visual/waterfall-chart.md`](../../report/add-visual/waterfall-chart.md)) is
enough — this recipe is for full control or multi-tier stories.

## **Interactive — ASK BEFORE GENERATING**

This recipe is interactive. **Before emitting any DAX or visual.json, ask the user 3 questions
(in this order):**

1. **Steps + types + source measures** (free-text) — list each step as:
   ```
   <Step name> | total/drop | <source measure or expression>
   ```
   Example:
   ```
   Sales Pipeline | total | [# Leads]
   Lost in Demo   | drop  | [# Lost Demo]
   Qualified      | total | (derived: Leads - Lost Demo)
   ```
2. **Stacked composition?** (yes / no) — does any step split into sub-segments? If yes,
   ask Q2a: *for each stacked step, list its sub-segments + source measures*.
3. **Orientation + label style?** (4 chips):
   - Vertical + Standard (Recommended)
   - Vertical + Detailed (rich)
   - Horizontal + Standard
   - Horizontal + Detailed (rich)

Smart-suggest the **total/drop** classification in Q1 from step naming (`drop`, `loss`,
`failed`, `churn`, `lost` → drop; else total). Show the inferred plan as a **preview before
generating** so the user can correct silent misclassifications.

See [workflow.md](workflow.md) for the full intake → generate → validate flow.

## Tool priority (MCP first)

Per the workspace rule ([`../../../03-bind/via-mcp/_index.md`](../../../03-bind/via-mcp/_index.md)):

| If… | Then… |
|---|---|
| Power BI MCP connected + Desktop open with the target model | **MCP** for table + measure creation; **`pbir`** for page + visual files; **`dax_query_operations`** to validate immediately |
| MCP not connected but available | Prompt for restart / `connection_operations Connect`; don't silently fall back |
| MCP unavailable (headless, no Desktop, or user opted out) | Emit paste-able TMDL + visual.json blocks (the [templates/](templates/) are designed for this) |

## The six primitives

1. [Steps disconnected table](primitives/steps-table.md) — `UNION` of `SELECTCOLUMNS` calculated table; columns `Step` + `StepSort` (sortByColumn). (P1)
2. [Floater + body measures](primitives/floater-body-measures.md) — `<PREFIX> Base` + per-step `<PREFIX> Body · <Step>`. The engine. (P2)
3. [Label measures](primitives/label-measures.md) — `<PREFIX> Label` (signed simple) and `<PREFIX> Label (rich)` (value + share + context word). (P3)
4. [Axis max + label anchor](primitives/axis-anchor.md) — `<PREFIX> Axis Max` (dynamic value-axis end) and `<PREFIX> Label Anchor` (the label carrier; Y2 vertical, Y stack-last horizontal). (P4)
5. [Horizontal label pad](primitives/horizontal-label-pad.md) — `<PREFIX> Label Pad` (transparent right-edge filler) — **horizontal only**. (P5)
6. [Stacked sub-segments](primitives/stacked-segments.md) — `<PREFIX> Stack · <Step> · <Segment>` measures for stacked composition steps. (P6, optional)

## Variants

| Variant | What changes |
|---|---|
| [Vertical Standard](variants/vertical-standard.md) | `lineStackedColumnComboChart` + Y2 anchor + `<PREFIX> Label` |
| [Vertical Detailed](variants/vertical-detailed.md) | same shape, anchor bound to `<PREFIX> Label (rich)` |
| [Horizontal Standard](variants/horizontal-standard.md) | `barChart` + stacked Pad + Anchor + `<PREFIX> Label` |
| [Horizontal Detailed](variants/horizontal-detailed.md) | same shape, anchor bound to `<PREFIX> Label (rich)` |
| [Stacked composition](variants/stacked-composition.md) | adds P6 sub-segment measures for selected steps |

## Build it

- Ordered file map + intake + validation → [workflow.md](workflow.md)
- Token reference → [tokens.md](tokens.md)
- Reusable templates → [templates/](templates/) — `waterfall-steps-table.tmdl`, `waterfall-measures.tmdl`, `vertical.visual.json`, `horizontal.visual.json`, `stacked.visual.json`
- Worked end-to-end → [examples/volume-attribution.md](examples/volume-attribution.md) (5-step funnel, mixed totals/drops, stacked composition variant)

## Critical gotcha — the showSeries trap

`showSeries: false` on the same series that carries `dynamicLabelValue` (i.e. the Label Anchor)
**silently suppresses the label.** Apply it to every OTHER series — never to the carrier.

See [primitives/label-measures.md](primitives/label-measures.md) and the memory entry
[[pbi-labels-showseries-trap]] (saved 2026-06-04 after this exact bug bit twice in one session).

## Critical gotcha — TMDL multi-line measure indent

Multi-line measure bodies (`VAR…RETURN…SWITCH(…)`) MUST be indented **one tab deeper** than the
trailing `formatString:` / `displayFolder:` / `lineageTag:` lines. Same indent collides, and the
parser reports "The syntax for 'formatString' is incorrect" on Desktop open.

The [templates/waterfall-measures.tmdl](templates/waterfall-measures.tmdl) is pre-indented
correctly — paste verbatim and only fill `<TOKENS>`. See memory entry
[[tmdl-multiline-measures]] (saved 2026-06-04 after this bit the first recipe-driven build).

## Provenance

Recipe pattern derived from an internal pipeline-attrition project (file-delivery funnel,
gddt) and validated 2026-06-04 against a fantasy-MMO market-volume funnel
(grand-exchange — Volume Attribution Funnel). Both proved the same plumbing across radically
different domains.

## Related atomic docs

- `../../report/add-visual/waterfall-chart.md` — the native waterfall (when this recipe is overkill)
- `../../visuals/svg/per-chart/waterfall.md` — inline SVG waterfall (when a per-row micro-chart is wanted instead)
- `../../report/format/conditional-fmt-rule.md` — measure-driven color, if `<PREFIX> Body Color` is used
- `../../model/dax/disconnected-tables.md` — the broader disconnected-table family this recipe is one instance of
- `../disconnected-selection-emphasis/context.md` — pairs well if the recipe is driven by a what-if step picker
