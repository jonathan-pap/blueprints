# Build a report — the one path (greenfield, multi-page)

> **The single end-to-end pipeline.** Design decisions first, then authoring — one continuous flow,
> no parallel "design room." Two phases: **A. Design** (decide what it looks like + why → a
> `Design Brief:` contract) and **B. Build** (materialize tokens → theme → pages → visuals → gate).
> Each step names the exact file to load. This page is the *sequence*; the linked files are the *detail*.

For a single mechanical edit (add one card, restyle one visual), skip this — use the
[`context.md`](context.md) router directly. This path is for building (or redesigning) a whole report.

---

## Phase A — Design (decide before authoring)

### A0 — Data-first investigation (mandatory)
Inspect the semantic model **before any design decision**.
- **Live model** → Modeling MCP ([`../../03-bind/via-mcp/_index.md`](../../03-bind/via-mcp/_index.md)): list
  tables/columns/measures/relationships; sample rows for cardinality/magnitude; run DAX to confirm a
  measure returns non-flat values.
- **No live connection** → read TMDL ([`semantic-model/find-field-from-tmdl.md`](semantic-model/find-field-from-tmdl.md),
  [`semantic-model/read-measure-definition.md`](semantic-model/read-measure-definition.md)).

Map **each measure + dimension to the analytical question it answers**. A flat line or two-bar chart is
the wrong field/visual, not a styling problem. Missing model work (new measures, sort-by columns,
variance/ratio) is **model-side** → [`../model/_index.md`](../model/_index.md) or [`../../03-bind/_index.md`](../../03-bind/_index.md), not here.

### A1 — Design identity (tone + signature)
Commit a **tone** ([`references/tones.md`](references/tones.md)) and **signature**
([`references/signatures.md`](references/signatures.md)) — the model is in
[`references/design-identity.md`](references/design-identity.md). The tone pins palette/type/density/
borders; the signature is the one recurring move. If the prompt is vague (no audience/purpose/page
count/filter depth), **stop and offer 2–3 named options** first
([`../../01-brief/references/vague-prompts.md`](../../01-brief/references/vague-prompts.md)); recommend
one, record the assumption, proceed. For **brownfield**, capture current + target — the delta is the
redesign ([`references/brownfield.md`](references/brownfield.md)).

### A2 — Archetype per page
Route **each page independently** ([`references/archetypes/_index.md`](references/archetypes/_index.md))
— even one broad request decomposes into pages of different archetypes. Walk that archetype's variant
table using the page's data shape; record `layout_variant` + `variant_rationale`. Multi-page → apply
[`references/composition.md`](references/composition.md) (variant rotation; avoid mono-archetype).

### A3 — Chart selection
Match each question to a visual type via [`add-visual/pick-visual-type.md`](add-visual/pick-visual-type.md)
(the question→chart taxonomy, **cardinality limits**, encoding-accuracy hierarchy, and the canonical
`visualType` names — `columnChart`, not `stackedColumnChart`). One analytical question per visual.

### A4 — Visual configuration
Decide per-visual sort, color strategy, label placement, axis, conditional formatting. Reference
[`references/cards-and-kpis.md`](references/cards-and-kpis.md),
[`references/tables-and-matrices.md`](references/tables-and-matrices.md),
[`references/visual-colors.md`](references/visual-colors.md). Cross-filter etiquette →
[`references/interactivity.md`](references/interactivity.md).

### A5 — Theme decision (DEFAULT: keep the existing theme)
**Use the report's current theme.** The A1 tone is design *direction* — it shapes the brief's
`color_map` (which palette slot maps to which measure); it does **not** authorize a theme. **Never
create, apply, or swap a theme JSON unless the user explicitly asks** for a new/different theme (hard
rule — [`../theme/context.md`](../theme/context.md)). Record `theme.base: existing theme preserved` in
the brief. Only if a swap was explicitly requested: escalate to
[`../theme/create/_index.md`](../theme/create/_index.md), and never replace per-type safeguards with a
blunt `visualStyles["*"]["*"]` ([`../theme/modify/wildcard.md`](../theme/modify/wildcard.md)).

### A6 — Emit the Design Brief contract
Produce the `Design Brief:` YAML — full schema + validation checklist in
[`layout/design-contract.md`](layout/design-contract.md). Must carry
`generated_by: powerbi-report-design-room`, one `pages[]` per page (each with `archetype`,
`layout_variant`, `variant_rationale`, insight `page_title`), a per-page `layout_contract`, and a
`space_budget` with no dead zones. Review it against
[`references/anti-patterns.md`](references/anti-patterns.md) and
[`references/accessibility.md`](references/accessibility.md) **before** authoring — layout gaps,
missing slicers, monochrome charts, raw field names, failed contrast are cheapest to fix on the
contract.

---

## Phase B — Build (implement the contract)

> The contract is the spec; authoring computes the **how** (exact `pbir` commands, coordinates, theme
> JSON, validation). Don't free-author — every visual traces to a contract placement.

### B7 — Materialize `projects/<name>/design-system.yaml`  ← do not skip
The contract speaks in zones + tokens; the **dimensions** live in the project's
`design-system.yaml` ([`layout/design-system.md`](layout/design-system.md)). **If the project has none,
copy the starter** [`layout/design-system-default.yaml`](layout/design-system-default.yaml) to
`projects/<name>/design-system.yaml` and set `meta.page`, `meta.theme`, and any layout tokens to match
the contract. This is the file Claude reads before every `pbir add visual` **and** the file
[`../../04-review/hooks/audit-layout-consistency.sh`](../../04-review/hooks/audit-layout-consistency.sh)
checks — a project without it cannot be layout-audited and visual sizes will drift.

### B8 — Theme (only if A5 sanctioned a change)
**By default, do nothing here — the report already has a theme; keep it.** Only when the user
*explicitly* asked for a new/swapped theme: author it
([`../theme/create/_index.md`](../theme/create/_index.md)) — it lands in
`<project>.Report/StaticResources/RegisteredResources/<Theme>.json`, referenced from `report.json`
([`../theme/where-themes-live.md`](../theme/where-themes-live.md)); add a `$schema` line
([`../theme/create/schema-integration.md`](../theme/create/schema-integration.md)). **Theme-first:**
push any repeated per-visual override up into the theme; don't scatter formatting on individual visuals.

### B9 — Pages
Create pages ([`page/add-page.md`](page/add-page.md)). **Mind the schema-lag write block** — if
`pages.json` is at `pagesMetadata/1.1.0`, `pbir add page`/`add visual` refuse to write; pin to `1.0.0`
first ([`../../04-review/audit/pbir-validate.md`](../../04-review/audit/pbir-validate.md)). Reference
pages by **display name**, keep names unique, verify with `pbir ls`.

### B10 — Per page: tokens → visuals → format
For each contract page: read the `design-system.yaml` tokens for sizes/positions, then add + bind each
visual ([`add-visual/_index.md`](add-visual/_index.md); bulk via `pbir add visual --from-json`).
Bindings reference **real** fields — run [`bind/find-canonical-name.md`](bind/find-canonical-name.md)
first. Place on the canvas with the zones model
([`layout/detail-gradient.md`](layout/detail-gradient.md)) + equal-gap golden rules
([`layout/layout-guidelines.md`](layout/layout-guidelines.md)); snap to the 8-grid. Then titles/format.

### B11 — Validate
`pbir validate` after every mutation ([`validate/validate.md`](validate/validate.md)). Interpret
real-vs-cosmetic against [`../../04-review/audit/pbir-validate.md`](../../04-review/audit/pbir-validate.md).

### B12 — Gate against the contract
Check the finished report against the brief
([`../../04-review/audit/layout-contract-validate.md`](../../04-review/audit/layout-contract-validate.md))
and run the layout audit
([`../../04-review/hooks/audit-layout-consistency.sh`](../../04-review/hooks/audit-layout-consistency.sh)).
Fix drift before declaring done. Desktop is the final visual truth (edit TMDL/PBIR with Desktop closed).

---

## Gotchas (check each before handoff)
- **Tone declared but never propagated** — same fonts/palette/borders as every other report. Walk the
  tone's downstream column.
- **Page background** — an intentional surface; avoid white canvas + white containers.
- **Redundant callouts** — a tile repeating an absolute measure already in the adjacent chart is noise.
  Needs a derived `insight_basis` (Δ, variance %, rank, threshold, narrative) or delete it.
- **Temporal slicer grain** — annual/executive pages → a Year dropdown/tile, not a full-date `between`.
- **Raw field names** — set human-readable display names everywhere.
- **Percentage formatting** — a rate stored as 0.53 must display "53%".
- **Monochrome bars** — single-measure bars render one color; specify per-category/gradient in the brief.
- **Unprompted theme build** — authoring/swapping a theme JSON when the user only picked a tone. Tone is
  *direction*; keep the existing theme unless a theme change was **explicitly** requested (A5/B8).
- **Missing `design-system.yaml`** — B7 skipped → the report can't be layout-audited and sizes drift.

## Related
- [`context.md`](context.md) — the intent router (this path is its "build a full report" branch)
- [`references/design-identity.md`](references/design-identity.md) — the tone/signature/archetype model
- [`layout/design-contract.md`](layout/design-contract.md) — the Phase-A output Phase B implements
- [`../../01-brief/_index.md`](../../01-brief/_index.md) — the requirements that feed A0–A1
