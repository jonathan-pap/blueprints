# Wireframes & story — turn a brief into a layout skeleton + narrative

> The planning step **between the brief and the build**: take what the report must answer and produce
> (1) a **data-story arc** — the sequence of questions the report walks a reader through — and
> (2) low-fidelity **page wireframes** — zone layouts with placeholder visuals. Text-first, so the AI
> can draft and iterate them fast, and cheap to change *before* any PBIR is written.

## When to enter

- You have a brief (or a rough ask) and want to **agree the shape + flow before building**.
- A stakeholder asks "what will it look like / how does it tell the story?" — wireframe it, don't build it.
- Part of the [report-planning workflow](../report-planning-workflow.md) **Spec** phase: story + wireframes
  are the visual half of the locked spec.

For a small edit to an existing report, skip this. For pixel design (tone, color, type), that's the
**design-identity** references in [`../../02-build/report/references/`](../../02-build/report/references/) —
wireframes are deliberately *low-fi* (boxes + labels, no styling).

## The flow (4 phases)

```
Brief ─▶ 1. STORY ─▶ 2. WIREFRAME ─▶ 3. REVIEW ─▶ 4. HANDOFF ─▶ 02-build
        arc + page   low-fi zones    vs the       story.md +
        sequence     per page        brief        wireframe.md
```

1. **Story** — from the brief, derive the one decision the report drives, the audience's questions, and a
   narrative arc (overview → analysis → detail → action). Output: an ordered page list, each with a purpose.
2. **Wireframe** — sketch each page as **zones** (header / KPI row / main / detail / filter) filled with
   **placeholder visuals** (`[KPI: Total Sales]`, `[Bar ▸ Sales by Region]`). No colors, no real data.
3. **Review** — check every page against the brief: does it answer a real question? Is the arc coherent?
   Is each page balanced (not over/under-full)? Cut, merge, resequence.
4. **Handoff** — save `story.md` + `wireframe.md` to `projects/<name>/`; map each wireframe's zones to
   [`design-system.yaml`](../../02-build/report/layout/design-system.md) sizes/zones, and enter `02-build`.

## Files in this room

- [`workflow.md`](workflow.md) — the flow in detail, with the gate at each phase
- [`brief-template.md`](brief-template.md) — the **Wireframe & Story Brief** (fill this; extends the report brief)
- [`prompts.md`](prompts.md) — copy-paste AI prompts: derive the story, wireframe a page, critique it
- [`notation.md`](notation.md) — how to render a text wireframe (ASCII grid + zone/visual notation) that maps
  to the 1280×720 canvas and the design-system zones
- [`handoff.md`](handoff.md) — **generate it outside here**: the portable JSON spec + how to turn it into a
  Claude HTML/SVG mockup, **Figma** frames (via a Figma MCP), or hand it to any design AI
- **Worked example** — a **filled** Wireframe & Story Brief (retail Sales star) lives in the briefs hub:
  [`../../../briefs/examples/power-bi-wireframe-retail-sales.md`](../../../briefs/examples/power-bi-wireframe-retail-sales.md)

## How it connects

| Upstream | This room | Downstream |
|---|---|---|
| `../brief-template.md` (audience, KPIs, questions) | story arc + page wireframes | `../../02-build/report/layout/design-system.md` (zones→sizes) → `../../02-build/report/` (build) |
| `../references/kpi-selection.md`, `layout-patterns.md` | which KPIs land where | `../../02-build/report/references/visual-cookbook.md` (pick the real visual per placeholder) |

## Output

`projects/<name>/story.md` (the narrative arc) and `projects/<name>/wireframe.md` (the page sketches).
Both are inputs the build reads — the wireframe's placeholder visuals become real visuals; the story keeps
page order + purpose honest.
