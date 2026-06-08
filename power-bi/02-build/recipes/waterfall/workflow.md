# Workflow — assemble the recipe

Three phases: **intake** (3 questions, preview before generating), **build** (model first, then
visual), **validate** (DAX query + visual reload). Tool path: **MCP first**, paste-able fallback
only when MCP is unavailable.

## Phase 1 — Intake (mandatory)

Do NOT emit any DAX or `visual.json` until these answers are gathered AND the inferred plan is
shown to the user for confirmation.

### Q1 — Steps (free-text, structured)

> List your steps in order. For each: name, type, source measure.
>
> Example:
> ```
> Total Volume    | total | [Trade Quantity]
> NPC Mediated    | drop  | [NPC Volume]
> Player Volume   | total | (derived: Total - NPC)
> Common+Uncommon | drop  | [Low Tier Player Volume]
> Rare+ Player    | total | (derived: Player - Low)
> ```

**Smart-suggest** the total/drop classification: if step name contains `drop`, `loss`, `failed`,
`churn`, `lost` → drop. Else → total. Show the inferred classification in the preview so the
user can correct silent misclassifications.

### Q2 — Stacked composition? (AskUserQuestion, 2 options)

- Yes, some steps split into sub-segments
- No, single-segment per step

If yes → Q2a free-text:

> For each stacked step, list its sub-segments (bottom to top in the stack):
> ```
> Total Volume:
>   NPC   | [NPC Volume]
>   Low   | [Low Tier Player Volume]
>   Rare+ | [Mid+ Tier Player Volume]
> ```

### Q3 — Orientation + label style (AskUserQuestion, 4 chips)

- Vertical + Standard labels (Recommended)
- Vertical + Detailed (rich)
- Horizontal + Standard
- Horizontal + Detailed (rich)

### Preview before generate

After Q1–Q3, show the inferred plan as a table:

| Step | Type | Source | Stacked? |
|---|---|---|---|
| Total Volume | total | `[Trade Quantity]` | NPC + Low + Rare+ |
| NPC Mediated | **drop** | `[NPC Volume]` | — |
| Player Volume | total | derived | Low + Rare+ |
| ... | | | |

**Orientation:** Vertical · **Label style:** Standard · **Variant:** [`vertical-standard`](variants/vertical-standard.md)

Ask "Generate against the model now? (y / adjust)" before any write.

## Phase 2 — Build (ordered file map)

Substitute [tokens](tokens.md) (`<PREFIX>`, `<STEPS_TABLE>`, `<MEASURE_TABLE>`, `<PAGE_ID>`,
`<VISUAL_NAME>`, etc.) into templates before applying.

### If MCP is connected (preferred path)

| # | Action | What | Tool |
|---|---|---|---|
| 1 | **Create** the disconnected steps table | One calculated table; columns inferred from DAX | `mcp__powerbi-modeling-mcp__table_operations` Create |
| 2 | **Refresh** the calculated table | So values populate | `table_operations` RefreshWithXMLA |
| 3 | **Update** columns: `Step` sortByColumn `StepSort`, `StepSort` isHidden | Quick polish | `column_operations` Update |
| 4 | **Batch-create** all measures atomically | Base + 1 helper per source measure + 1 Body per step + Label + Label (rich) + Axis Max + Label Anchor (+ Label Pad if horizontal) (+ Stack measures if stacked) | `measure_operations` Create (single transaction) |
| 5 | **Validate** math with a DAX query | Confirms steps + types are right BEFORE the visual is written | `dax_query_operations` Execute |
| 6 | **PROMPT user to SAVE in Desktop** | Persist model to TMDL on disk so the visual can reference it | (user action) |
| 7 | **Create** the page | `pages.json` may need manual update due to [[pbir-cli-bundled-schema-lag]] | `pbir add page` |
| 8 | **Write** the visual.json | Pick the variant template (vertical-standard etc.) | `Write` (recipe template substitution) |
| 9 | **Reload Desktop** | Visual changes only take effect on file open | (user action) |
| 10 | **Verify** | Math reads right; labels render; colors per tier | (user action) |

### If MCP is unavailable (fallback path)

Same 10 steps, but:
- Steps 1, 3, 4, 5: emit TMDL blocks (steps-table.tmdl, measures.tmdl) for the user to paste into Tabular Editor or directly into the `.SemanticModel/` files **with Desktop closed** (per [[pbi-desktop-clobbers-tmdl]]).
- Step 6: user opens Desktop after pasting model edits.
- Step 7: emit page.json and pages.json updates manually.
- Step 8: emit visual.json as a block; user creates the visual folder and pastes.

## Phase 3 — Validate

DAX query after Step 4 (math check):

```dax
EVALUATE
SUMMARIZECOLUMNS (
    <STEPS_TABLE>[Step],
    <STEPS_TABLE>[StepSort],
    "Base", [<PREFIX> Base],
    "Body", COALESCE ( <one Body per step, COALESCE-chained> ),
    "BarTop", [<PREFIX> Base] + COALESCE ( <Body chain> ),
    "Label", [<PREFIX> Label]
)
ORDER BY [StepSort]
```

Expected: every step's `BarTop` matches the prior step's running total (for drops) or its own
value (for totals). Labels are signed correctly for drops.

After Desktop reload — visual checks:
- Floater (`<PREFIX> Base`) is invisible (transparent fill); drops appear floating between
  their start and the running floor.
- Each step's body has its expected color (drop palette vs total palette, or tier-coherent
  for stacked).
- Labels render (vertical: at bar tops via Y2 anchor; horizontal: at right edge via stacked
  Anchor with `labelPosition: 'InsideBase'`).
- For horizontal: all bars appear the same total length (Pad fills to AxisMax).

## Why this order

- **Disconnected table before measures.** Every measure references `SELECTEDVALUE(<STEPS_TABLE>[Step])` — the table must exist first.
- **Measures before the visual.** The visual binds them; if any is missing, the visual is broken at load.
- **Save before visual.** The `pbir` CLI and direct `visual.json` edits operate on disk; if the model isn't persisted, the visual references measures that don't exist on disk.
- **DAX validation before visual build.** Catches step-classification errors (a drop misclassified as a total) before they bake into the visual's colors and labels.

## Gotchas

- **showSeries trap on the Label Anchor.** The Anchor (or any series carrying `dynamicLabelValue`) must NOT have a `showSeries: false` entry in `labels[]`. Apply it to every OTHER series. See [primitives/label-measures.md](primitives/label-measures.md) and [[pbi-labels-showseries-trap]].
- **TMDL multi-line measure indent.** Bodies of multi-line measures (Base, Label, Label (rich), Label Pad) MUST sit one tab deeper than `formatString:`/`displayFolder:`/`lineageTag:` or Desktop reports `"syntax for 'formatString' is incorrect"`. Only matters on the **fallback path** (paste-able TMDL); the MCP path serializes correctly on its own. Use [templates/waterfall-measures.tmdl](templates/waterfall-measures.tmdl) verbatim — it's pre-indented. See [[tmdl-multiline-measures]].
- **Calculated tables can't have columns pre-declared.** Don't include a `columns` array in the table-create payload — the MCP rejects it. Columns are inferred from the DAX. Update column metadata (sortByColumn, isHidden) in a follow-up `column_operations` call.
- **`SELECTCOLUMNS` over inline rows uses positional refs.** The DAX `SELECTCOLUMNS({(...)}, "Step", [Value1], "StepSort", [Value2])` form uses `[Value1]`/`[Value2]` — `Value1`, `Value2` etc. are the auto-named columns of an inline row constructor.
- **Save before visual build.** Otherwise `pbir` and direct writes operate against a stale TMDL — the visual references measures that don't exist on disk yet.
- **`pbir add page` may fail schema validation** with a pagesMetadata 1.0.0 / 1.1.0 mismatch (see [[pbir-cli-bundled-schema-lag]]). The page folder still gets created — manually update `pages.json` to register it in `pageOrder` and set `activePageName`.
- **Horizontal needs the Pad measure.** Without `<PREFIX> Label Pad` stacked between the bodies and the Anchor, the Anchor's `labelPosition: 'InsideBase'` won't align right-edge across bars of different visible totals.

## Adapt for a variant

- [vertical-standard](variants/vertical-standard.md) — default; Y2 anchor binds `<PREFIX> Label`
- [vertical-detailed](variants/vertical-detailed.md) — Y2 anchor binds `<PREFIX> Label (rich)`
- [horizontal-standard](variants/horizontal-standard.md) — `barChart` + Pad + Anchor in Y; anchor binds `<PREFIX> Label`
- [horizontal-detailed](variants/horizontal-detailed.md) — same shape; anchor binds `<PREFIX> Label (rich)`
- [stacked-composition](variants/stacked-composition.md) — adds P6 `Stack · <Step> · <Segment>` measures + extra Y series; labels become per-segment defaults + dynamic on drops
