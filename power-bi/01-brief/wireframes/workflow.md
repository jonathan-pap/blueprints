# Workflow — brief → story → wireframe → review → handoff

Four phases, each with a **gate** you don't pass until it's satisfied. Draft in text; iterate cheaply;
only build once the wireframe is agreed. Use the prompts in [`prompts.md`](prompts.md) to drive each phase.

## Phase 0 — Gather

Read the brief (`../read-project-brief.md`): **audience, the decision it drives, the questions, KPIs,
constraints**. If there's no brief, fill [`brief-template.md`](brief-template.md) first — you can't
wireframe what you can't state. Note the **canvas**: default 1280×720, 24px margins (see
[`notation.md`](notation.md)).

## Phase 1 — Story (the arc)

Turn the brief into a **narrative**, not a pile of charts.

1. State the **one decision** the report drives ("Which regions to invest in next quarter").
2. List the **audience's questions**, in the order they'd ask them.
3. Pick an **arc pattern** and map questions to pages:
   - **Overview → Analysis → Detail** (most dashboards): summary page → driver pages → row-level detail.
   - **Martini glass**: one guided path, then open exploration.
   - **Drill path**: each page answers "why?" of the previous.
4. Produce an **ordered page list**: `#. Page name — the question it answers — the "so what"`.

> **Gate 1:** every page maps to a real brief question; the sequence tells a story a stranger could follow.

## Phase 2 — Wireframe (each page)

For each page, sketch **zones**, then drop **placeholder visuals** in — low-fi, labels only.

1. Choose a **zone layout** for the page's job (see `../references/layout-patterns.md`):
   header band → KPI row → main chart(s) → detail/table → filter rail.
2. Place **placeholder visuals** using [`notation.md`](notation.md) notation
   (`[KPI: Total Sales]`, `[Bar ▸ Sales by Region]`, `[Slicer: Date]`) — pick chart *intent*, not the
   final visual type yet.
3. Note the **reading order** (Z / F pattern) and the **one hero** per page (the thing the eye hits first).
4. Keep density honest: **4–6 visuals** per analytical page is plenty; a summary page can be fewer + bigger.

> **Gate 2:** each page has one clear hero, a sane reading order, and no zone is empty or crammed.

## Phase 3 — Review (against the brief)

Critique before you commit (prompt C in [`prompts.md`](prompts.md)):

- **Answers?** Does each page answer its brief question — nothing decorative, nothing missing?
- **Flow?** Does the page order match the story arc? Any page that could be cut or merged?
- **Balance?** Over-full pages (split), under-full pages (merge), repeated visuals (consolidate).
- **Feasibility?** Every placeholder maps to a visual the model can feed (cross-check KPIs/fields with the
  brief; if the model's unknown, the [Model Context Brief](../../../briefs/model-context-brief.md)).

> **Gate 3:** the wireframe is something you'd hand a builder and a stakeholder would recognize as "yes, that."

## Phase 4 — Handoff

1. Save **`projects/<name>/story.md`** (arc + ordered page purposes) and **`projects/<name>/wireframe.md`**
   (the page sketches).
2. Map each wireframe's zones/placeholders to **sizes + grid** in
   [`design-system.yaml`](../../02-build/report/layout/design-system.md) — the wireframe zone becomes a
   real position/size token.
3. Enter [`../../02-build/report/`](../../02-build/report/context.md): each placeholder → a real visual
   ([`visual-cookbook.md`](../../02-build/report/references/visual-cookbook.md) picks the type), built to the
   agreed layout. The story keeps page order + purpose honest through the build.

## Optional — a higher-fidelity mockup

The text wireframe is the working artifact. If a stakeholder needs to *see* it, render the same zones as an
HTML/SVG mock (an Artifact) — still no real data. Once built, the **Desktop Bridge**
(`../../03-bind/desktop-bridge.md`) screenshots the real pages to compare against the wireframe.
