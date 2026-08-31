# Workspace Roadmap

Living doc. What's queued, why, and how big the lift is. Group by theme; sort each group by effort.

Last updated: 2026-08-17

---

## Recently shipped

The layout / design workstream — much of it ported from the Microsoft **skills-for-fabric**
`powerbi-report-design` skill — is done and on `main`:

- **Layout tokens + 12×12 grid.** `projects/<name>/design-system.yaml` (resolution-independent
  regions / bands / spans), `02-build/report/layout/design-system.md` + `layout-guidelines.md`, and the
  drift hook `04-review/hooks/audit-layout-consistency.sh`. The grid runs end-to-end through the design
  contract, the conformance validator, and the wireframe spec.
- **Design-identity room.** `02-build/report/design/` (tone / signature / archetype) +
  `02-build/report/layout/design-contract.md` + `04-review/audit/layout-contract-validate.md`.
- **Wireframes room.** `01-brief/wireframes/` — brief → story → portable spec → Figma / Claude handoff.
- **Redistributable workspace.** Root `.mcp.json` (Power BI Modeling MCP) + `power-bi/setup.ps1`
  bootstrap (pbir CLI, Node, Desktop Bridge). Clone-and-go on Windows with Power BI Desktop.

---

## Queued

_Nothing active right now._

---

## Parked

Decided direction is recorded in Claude's local memory (`parked-workstreams`), outside this repo —
the summary below is the portable version:

- **Cross-blueprint brief chaining** — briefs stay tool-local; chain via a "Downstream / hand-off"
  section rather than a shared engine.
- **Wireframe / screenshot → brief** — image → draft `brief.md` (an intake-layer room, not a new
  blueprint). Raw-screenshot → exact PBIR layout stays out of scope (only viable via Figma MCP data).

---

## How to use this file

- **Add an item** when work is decided but not started.
- **Pull from this file** when picking what's next — sort by current focus, not by section order.
- **Remove an item** when shipped (the commit message is its epitaph); move it briefly under
  "Recently shipped" if it's worth signposting, then let it age out.
- **Promote parked → active** by moving it into "Queued" with an effort estimate.
- Don't list every nice-to-have; only items with a clear "done when".
