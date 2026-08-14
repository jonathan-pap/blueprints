# 01-brief — atomic file index

## Guided planning workflow (plan → spec → approve → build)

- `report-planning-workflow.md` — full lifecycle for a NEW report: Rounds 0–4 (audience → model inventory → page plan → identity/delivery), design-contract gate, locked `projects/<name>/report-spec.md`, approval gate, then build. Use for "plan then build a dashboard"; skip for small edits.

## Wireframes & story (brief → layout skeleton + narrative)

- `wireframes/context.md` — turn a brief into a **data-story arc** + low-fi **page wireframes** before building (text-first, cheap to iterate)
- `wireframes/workflow.md` — the 4-phase flow: story → wireframe → review → handoff
- `wireframes/brief-template.md` — the Wireframe & Story Brief (inputs)
- `wireframes/prompts.md` — copy-paste AI prompts (derive story, wireframe a page, critique)
- `wireframes/notation.md` — ASCII zone/visual notation mapped to the 1280×720 canvas + design-system zones
- `wireframes/handoff.md` — **generate outside here**: portable JSON spec → Claude HTML/SVG mockup, Figma frames (Figma MCP), or any design AI

## Brief-as-file (preferred)

- `brief-template.md` — copy-paste template for `projects/<name>/brief.md`
- `read-project-brief.md` — atomic step: how the agent reads + merges briefs
- `brief-folder-structure.md` — single file vs `brief/` folder; recommended structure

## Chat-fallback intake (when no brief exists)

- `references/report-dev-mindset.md` — stance before building: problem-first, model-first, iterate, format with intent
- `references/vague-prompts.md` — full intake script with anti-patterns
- `references/kpi-selection.md` — 20% change test, picking actionable measures
- `references/layout-patterns.md` — executive / operational / detail layouts with measurements
- `references/limitations.md` — what to tell the user the agent cannot do

## Routing

See `context.md` for the file-first / chat-second pipeline.
