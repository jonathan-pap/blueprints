# Report Planning Workflow — requirements → locked spec → build

> Adapted from skills-for-fabric (MIT) — see [../ATTRIBUTIONS.md](../ATTRIBUTIONS.md).

A guided lifecycle for **new** reports that goes past discovery into a locked,
approved spec and then implementation:

**Define → Inspect → Spec → Approve → Build → Validate**

Use this for broad "plan then build a report/dashboard" asks. For a small edit to
an existing report, skip this and go straight to `02-build/report/`. For design-only
critique, use `02-build/report/references/` (design-identity + archetypes).

> **Story + wireframes:** the spec's **Narrative** and **Page plan** sections are exactly what the
> [`wireframes/`](wireframes/context.md) room produces — a data-story arc + low-fi page sketches, AI-drafted
> and reviewed before build. Run it during **Spec** and drop its `story.md` / `wireframe.md` into the spec.

## Operating rules

1. **Ask one question at a time**, 3–5 rounds max. One primary question per round;
   a follow-up only if strictly necessary.
2. **Don't re-ask known answers.** If the prompt, `projects/<name>/brief.md`, the
   model, or a prior round already gives audience / page count / scope / delivery /
   design direction, capture it in notes and move on.
3. **Inspect the model before locking scope.** Prefer live inspection via
   `03-bind/via-mcp/` (or `03-bind/via-powershell/` TOM); otherwise read local
   TMDL (`definition/model.tmdl`, `tables/*.tmdl`, `relationships.tmdl`).
4. **Check dependencies explicitly** — don't assume Desktop, MCP, or a generator
   are available (see checklist).
5. **Produce one locked `projects/<name>/report-spec.md`** and **get approval
   before building.**
6. When approved, **build end-to-end**: model changes → PBIR → validate → Desktop
   reload/screenshot → iterate.

## Dependency checklist (capture before build)

| Dependency | Purpose | Required when |
|---|---|---|
| Power BI Desktop | Open/reload PBIP, visual validation | Local preview |
| PBIP/PBIR project | File-based authoring | Generated reports |
| TMDL semantic model | Model persistence + source control | Model edits |
| `powerbi-modeling-mcp` (`03-bind/via-mcp/`) | Inspect + create measures/columns/relationships live | Live model authoring |
| `connect-pbid` TOM (`03-bind/via-powershell/`) | Alternative live model access | When MCP unavailable |
| Desktop Bridge (`03-bind/desktop-bridge.md`) | reload → screenshot loop | Visual validation |

If a dependency is missing, keep planning and mark the affected phase blocked/manual — don't pretend it's available.

## Rounds

**Round 0 — Setup & dependencies.** Identify the semantic model (enumerate local
`.SemanticModel` folders / discoverable models, recommend the best match), check for
existing `.pbip`/`.Report`/`.SemanticModel`, TMDL presence, MCP availability, and
whether a Desktop automation path exists.

**Round 1 — Audience & job.** Who is it for (Exec / Analyst / Operator / External /
Enthusiast) and what job it supports (understand the story / track performance /
find outliers / compare / explore records / recurring review). Capture *Audience,
Primary purpose, Tone, Success criteria*.

**Round 2 — Model inventory & scope.** Inspect the model (facts+grain+keys, dims,
existing measures, likely missing measures/columns/relationships/sort cols, risks:
nulls, inactive relationships, high-cardinality slicers). Infer first-build scope
from the request; only ask a scope question if the boundary is unclear or risky, and
then present choices drawn from the *inspected* model.

**Round 3 — Narrative & page plan.** Route archetype/composition through
`02-build/report/references/archetypes/` + `composition.md`. Surface 2–3 named report
shapes, recommend one, then draft the page list: *Page — archetype — layout variant
(A/B/C) — purpose — visuals — fields/measures — slicers/interactions*. Capture global
vs page slicers, search/prefix slicers for high-cardinality dims, drillthrough/profile
pages, bookmarks/nav.

**Round 4 — Identity, accessibility, delivery.** Pick a tone+signature from
`references/design-identity.md` (+ `tones.md`, `signatures.md`); offer 2–3 concrete
identity options, recommend one. Apply design defaults automatically: WCAG-AA contrast,
no red-on-red, Azure Map over legacy map/filledMap, alt text on every chart, searchable
dropdowns for high-cardinality fields, detailed tables near the page bottom, predictable
interactions. Delivery target for this blueprint is **local PBIP** (Fabric publish is
out of scope here).

## Design contract gate

Before writing the spec, obtain a canonical **layout contract** per the
`02-build/report/layout/design-contract.md` schema — a mechanical `layout_contract`
(canvas, grid.regions, placements, space_audit) for **every** page, not a prose
wireframe. The `04-review/audit/layout-contract-validate.md` checks apply:

- every planned page has a `layout_contract` with `canvas`, `grid.regions`, `placements`, `space_audit` (empty `unplaced_regions`);
- one `page_title` textbox per page with non-empty title;
- slicers in a top-right `filters` region or a justified rail — no data visual under a slicer/header band;
- no bare single-value `cardVisual` as the dominant hero region unless it's an explicit composite-KPI treatment;
- no ellipses / unresolved placeholders.

If the contract fails any check, fix it **before** asking for approval.

## Locked spec output — `projects/<name>/report-spec.md`

One file, two layers: **Markdown** for human sign-off + a fenced **`yaml` layout
contract** that authoring implements. If prose and YAML disagree, fix the file — never
make the author choose. Template:

```markdown
# Report Spec

## Report identity
- Report name / Semantic model / Audience / Primary purpose / Delivery target

## User decisions & constraints
- Scope / Page count / Interactivity / Design direction / Publishing / Tooling /
  Model-edit permissions / Accessibility / Data caveats

## Narrative
- Core story / Audience promise / Key questions answered

## Design identity
- Tone / Signature / Brownfield delta (if redesign)

## Page plan
1. <Page> — archetype — layout variant (A/B/C) + one-line rationale — purpose —
   visuals — fields/measures — slicers/interactions

## Design system summary
- Theme + base palette / color semantics / typography / layout grid+density /
  accessibility commitments

## Model requirements
- Existing measures / new measures / new calc columns / relationship+sort needs

## Layout contract
<paste the exact fenced `yaml` layout_contract — authoritative for implementation>

## Implementation notes
- Model changes / PBIR authoring / validation / Desktop screenshot verification / risks
```

## Approval gate

After writing the spec, ask exactly one approval question — *"Approve this report
spec so I can start building?"* (Approve / revise audience / revise scope / revise
design). **Do not build until approved.**

## Implementation after approval

1. Re-read the approved spec + extract the layout contract; verify per-page contract + space_audit.
2. Connect to the model (`03-bind/via-mcp/` preferred, else TOM).
3. Create/validate measures + calc columns (`02-build/model/`); prefer MCP for mutations.
4. After column/measure changes, trigger a lightweight recalc (XMLA `refreshType=Calculate`) unless a full source refresh is needed.
5. Export/organize TMDL (`database.tmdl`, `model.tmdl`, `relationships.tmdl`, `tables/*.tmdl`).
6. Scaffold PBIR, author per `02-build/report/` (generated PBIR beats hand-editing visual JSON).
7. `pbir validate` after every mutation; validate JSON + `definition.pbir` model pointer.
8. Reload in Desktop (Desktop Bridge) → screenshot → fix visual/slicer/binding/accessibility/layout → iterate.

## Validation standards (report not "done" until)

Required PBIP/PBIR files exist · all JSON parses · `definition.pbir` points at the
expected model · pages/visuals in expected counts · Desktop opens the `.pbip` · reload
succeeds · screenshots capture cover + newly authored pages.

## Anti-patterns

Generated PBIR > hand-edited visual JSON · persist model changes before Desktop reload
· watch DAX filter direction from fact-side flags · high-cardinality slicers need
search/prefix · Desktop validation catches what JSON validation can't.
