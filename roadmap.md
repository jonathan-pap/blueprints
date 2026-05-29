# Workspace Roadmap

Living doc. What's queued, why, and how big the lift is. Group by theme; sort each group by effort.

Last updated: 2026-05-27

---

## 1. Power BI — layout consistency (active)

**Driver:** `/sc:analyze` found 7 different slicer sizes, 3 slicer types, and sub-pixel positioning across [power-bi/projects/test](power-bi/projects/test). Root cause: Power BI's theme schema has no `width`/`height`, so the theme-first cascade governs ~80% of consistency (color/font/padding) and **misses the layout axis entirely**. Every `pbir add visual` call is free to pick its own dimensions.

**Architectural lever:** add a 5th cascade level — project-scoped **design tokens** at `projects/<name>/design-system.yaml`. Read before every visual creation; audit hook flags drift.

| # | Effort | Action | Impact |
|---|---|---|---|
| 1.1 | 5 min | Fix [02-build/report/add-visual/slicer.md](power-bi/02-build/report/add-visual/slicer.md) example from `200×80` → `240×40`; add "use `slicer` (dropdown) unless brief specifies list-style" | Removes 80% of new-author drift |
| 1.2 | 5 min | Kill duplicate range table — keep one of [size-visual.md](power-bi/02-build/report/layout/size-visual.md) / [layout-guidelines.md](power-bi/02-build/report/layout/layout-guidelines.md), link the other | Single source of truth |
| 1.3 | 15 min | Snap-to-grid pass on the test project's `ee2fb4ec…` page (cleans 4 sub-pixel slicers) | Immediate cleanup |
| 1.4 | 30 min | Create `projects/test/design-system.yaml` + brief stub that references it | Working example |
| 1.5 | 1 hr | New atomic file `02-build/report/layout/design-system.md` documenting the contract + cascade integration | System-wide pattern |
| 1.6 | 1 hr | New hook `04-review/hooks/audit-layout-consistency.sh` — flag visuals where W/H deviates from project default, non-integer x/y/w/h, off-grid positions | Drift becomes loud not silent |
| 1.7 | 30 min | Decision file `add-visual/slicer-which-type.md` — when to use `slicer` vs `listSlicer` vs `advancedSlicerVisual` | Type drift, not just size drift |

**Done when:** new visuals snap to project tokens by default; audit hook catches any drift; brief stays strategic (no per-visual dimension bloat).

---

## 2. Synthetic-data — scale up + hand-off (grand-exchange ready)

**Driver:** smoke generation passed (0/7 validation failures, [outputs/2026-05-27-grand-exchange-smoke-*](synthetic-data/outputs/)). Two natural follow-ups:

| # | Effort | Action | Impact |
|---|---|---|---|
| 2.1 | 5 min | `pip install pyarrow` so full-scale can write Parquet | Unblocks 2.2 |
| 2.2 | 10 min | Run `python generate.py --scale full` (~3.3M price rows + 5M trades, est. ~3–5 min) | The performance fact dataset |
| 2.3 | 30 min | Power BI hand-off — scaffold `power-bi/projects/grand-exchange/` from the CSVs (galaxy schema, hidden keys, marked date table, BOM hierarchy) | Cross-blueprint demo |
| 2.4 | 1 hr | Build the Sales Overview equivalent: KPI row (Total Sales/Profit %/Trade Count) + market trend + Pareto by item rarity | DAX showcase: time intel, recursive BOM PATH, many-to-many |
| 2.5 | 30 min | Backfill room atomic files now that we have a worked example — `02-schema/distributions.md`, `03-generate/engine-distribution-sampling.md`, `05-review/validate-business-rules.md` | Skeleton fills in from real artefacts |

---

## 3. Cross-blueprint patterns (parked workstreams)

From [memory/parked-workstreams.md](file:///C:/Users/jonathan/.claude/projects/e--Workspace-Blueprint/memory/parked-workstreams.md). Decided direction recorded; not active.

| # | Status | Workstream | Agreed shape if resumed |
|---|---|---|---|
| 3.1 | parked | **Cross-blueprint brief chaining** | Briefs stay tool-local (`<blueprint>/projects/<name>/brief.md`). Chain via hand-off — each brief gets a "Downstream / hand-off" section; the `04-output` hand-off seeds the next tool's brief. Touches both `brief-template.md` files + `synthetic-data/04-output/handoff-to-power-bi.md`. |
| 3.2 | parked (exploring) | **Wireframe / screenshot → brief tool** | Framing A (image → brief) is safe + high-value — drop a wireframe, extract draft `brief.md`, human refines. It's a *room in the intake layer*, NOT a new blueprint. Framing B (image → exact PBIR layout) only viable via Figma MCP structured data, never raw screenshots. Framing C (screenshot of built report → audit/compare) is a useful later QA loop. |

**Design stance:** keep the system a guided workflow, resist a runtime orchestration engine — the strength is "folder is the app, no engine."

---

## 4. Themes — finish the library smoke-test (blocked earlier)

| # | Effort | Action | Impact |
|---|---|---|---|
| 4.1 | 5 min | `pbir theme validate` against all 6 library themes (okabe-ito, tableau10, brewer-set2, ibcs-neutral, viridis, blupulse-v1.1) | Confirm library is valid |
| 4.2 | 5 min | Apply Okabe-Ito to `projects/test` as accessibility default; `pbir validate` the report | Proves library → consumer path |

---

## How to use this file

- **Add an item** when work is decided but not started.
- **Pull from this file** when picking what's next — sort by current focus, not by section order.
- **Remove an item** when shipped (use the commit message as its epitaph).
- **Promote parked → active** by moving it up into a numbered section with effort estimates.
- Don't list every nice-to-have; only items with a clear "done when".
