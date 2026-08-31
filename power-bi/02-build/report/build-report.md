# Build a report — the one path (greenfield, multi-page)

> The single end-to-end sequence: **A. Design** (decide → a `Design Brief:` contract) then **B. Build**
> (tokens → theme → pages → visuals → gate). One line per step = *what to do* + *the file to load*.
> Elaboration per step: [`build-report-detail.md`](build-report-detail.md) (same headings).
> Single mechanical edits skip this — use the [`context.md`](context.md) router.

## Phase A — Design (decide before authoring)

- **A0 Data-first investigation (mandatory)** — inspect the model before any design decision: live → [`../../03-bind/via-mcp/_index.md`](../../03-bind/via-mcp/_index.md); no connection → [`semantic-model/find-field-from-tmdl.md`](semantic-model/find-field-from-tmdl.md). Map every measure/dimension to the question it answers; missing model work is model-side ([`../model/_index.md`](../model/_index.md)).
- **A1 Design identity** — commit a tone ([`references/tones.md`](references/tones.md)) + signature ([`references/signatures.md`](references/signatures.md)); vague prompt → offer 2–3 options first ([`../../01-brief/references/vague-prompts.md`](../../01-brief/references/vague-prompts.md)); brownfield → [`references/brownfield.md`](references/brownfield.md).
- **A2 Archetype per page** — route each page ([`references/archetypes/_index.md`](references/archetypes/_index.md)); record `layout_variant` + rationale; multi-page → rotate ([`references/composition.md`](references/composition.md)).
- **A3 Chart selection** — one question per visual; canonical `visualType` names ([`add-visual/pick-visual-type.md`](add-visual/pick-visual-type.md)).
- **A4 Visual configuration** — sort, color strategy, labels, axes ([`references/cards-and-kpis.md`](references/cards-and-kpis.md), [`references/tables-and-matrices.md`](references/tables-and-matrices.md), [`references/visual-colors.md`](references/visual-colors.md), [`references/interactivity.md`](references/interactivity.md)).
- **A5 Theme decision — DEFAULT keep the existing theme.** Tone is direction, not a licence to build a theme; swap only on explicit ask ([`../theme/context.md`](../theme/context.md)).
- **A6 Emit the `Design Brief:` contract** — grid regions + bands per page, `space_budget`, `color_map` ([`layout/design-contract.md`](layout/design-contract.md)); review against [`references/anti-patterns.md`](references/anti-patterns.md) + [`references/accessibility.md`](references/accessibility.md) before authoring.

## Phase B — Build (implement the contract)

- **B7 Materialize `projects/<name>/design-system.yaml`** (do not skip) — copy [`layout/design-system-default.yaml`](layout/design-system-default.yaml) if absent; it's what authoring reads and the layout hook audits ([`layout/design-system.md`](layout/design-system.md)).
- **B8 Theme** — only if A5 sanctioned a change ([`../theme/create/_index.md`](../theme/create/_index.md)); theme-first: repeated per-visual overrides move up into the theme.
- **B9 Pages** — add each page with a title ([`page/add-page.md`](page/add-page.md)). The `pbir` CLI writes the pages manifest; verify the page names match the brief with `pbir ls`.
- **B9a Activate the render loop (Desktop Bridge)** — when `desktop_bridge: true` in [`../../03-bind/via-powershell/hooks/config.yaml`](../../03-bind/via-powershell/hooks/config.yaml): open Desktop with live reload so each visual change appears on-screen without reopening the file. Preflight the bridge CLI (`powerbi-desktop --version`, fallback `npx -y @microsoft/powerbi-desktop-bridge-cli`); then `open <pbip>` → build visuals → `reload` + `screenshot` to verify each page before moving to the next ([`../../03-bind/desktop-bridge.md`](../../03-bind/desktop-bridge.md)). Save every visual in Desktop before reloading (the file on disk wins). Can't connect → close/reopen loop; never build without renders.
- **B10 Per page: place visuals per the brief** — for each visual in the design contract, resolve size and position from the **12×12 grid** in [`projects/<name>/design-system.yaml`](layout/design-system.md) — spans for size, regions for placement ([`layout/layout-guidelines.md`](layout/layout-guidelines.md)); a hand-picked dimension is an override and belongs in the yaml `overrides:` block. Bind each visual to the correct measure/dimension from the model ([`bind/find-canonical-name.md`](bind/find-canonical-name.md) first — do NOT guess field names). Apply only the formatting the brief specifies; everything else cascades from the theme ([`add-visual/_index.md`](add-visual/_index.md) for patterns per chart type). The `pbir` CLI tools automate this; scripted builds import [`tools/pbirkit.py`](tools/pbirkit.py) for bulk operations ([`validate/validate.md`](validate/validate.md) explains validation).
- **B11 Validate — two layers, and the second is the one that catches real defects.** *Schema* (`pbir validate` — whole-report, ~2s: run it per finished page or straight after a hand edit, never per template-driven write; real vs cosmetic per [`../../04-review/audit/pbir-validate.md`](../../04-review/audit/pbir-validate.md)) proves the JSON is well-formed — it has never caught a wrong-looking report. *Intent* is [`../../04-review/hooks/lint-report-traps.sh --page <name>`](../../04-review/hooks/lint-report-traps.sh), run **per page while you're still on it**: inverted sorts, stacked titles, scrolling bars ([`validate/build-traps.md`](validate/build-traps.md)). Catching a trap on the page you just built costs one edit; catching it at B12 costs a rebuild.
- **B12 Gate against the contract** — [`../../04-review/audit/layout-contract-validate.md`](../../04-review/audit/layout-contract-validate.md) + [`../../04-review/hooks/audit-layout-consistency.sh`](../../04-review/hooks/audit-layout-consistency.sh); finish with `screenshot-all --settle 1500` (bridge) or close/reopen Desktop. Rendered pixels are the final truth.

## Gotchas (check before handoff)

Tone never propagated · white-on-white page background · redundant callouts without an `insight_basis` ·
full-date `between` slicer on an annual page · raw field names · rates shown as 0.53 · monochrome bars ·
unprompted theme build · missing `design-system.yaml` · **unrecorded layout override** (hand-picked
dimensions, not in `overrides:`) · **built blind** (bridge on, no renders / CLI not on
PATH) · **reload clobbered unsaved MCP edits**. Each is explained in [`build-report-detail.md#gotchas-check-each-before-handoff`](build-report-detail.md#gotchas-check-each-before-handoff).

## Related

[`context.md`](context.md) (the router this is the "build a full report" branch of) · [`references/design-identity.md`](references/design-identity.md) · [`layout/design-contract.md`](layout/design-contract.md) · [`../../01-brief/_index.md`](../../01-brief/_index.md)
