# Brief — Demo: Dragonhold Adventurers' Guild (Quest Ledger)

Last updated: 2026-08-22

> A clean end-to-end demo of the workspace: a **synthetic star** flows into this **blank PBIP**, a
> **report** is built on it, and the **Desktop Bridge** renders every page so the agent verifies its own
> work visually. The model is *empty on purpose* until the build runs — step 0 below populates it.
> Upstream dataset brief: [`../../../synthetic-data/projects/quest-ledger/brief.md`](../../../synthetic-data/projects/quest-ledger/brief.md).

## 1. Audience & decision

- **Primary audience:** the Guildmaster + hall captains (executive), and the quartermaster who assigns quests (analyst).
- **Decision this report supports:** where the guild's bounty gold comes from and who earns it — which
  halls/realms, which quest types and danger tiers, and which adventurers to promote or protect.
- **Decision cadence:** monthly guild council; ad-hoc when assigning high-danger quests.
- **Consumption channel:** Power BI Desktop (demo); should read well on a projector.

## 2. Source data & model

- **Semantic model:** thick PBIP — `demo.SemanticModel`, **currently blank**.
- **Source:** the `quest-ledger` synthetic job — CSVs in `synthetic-data/outputs/quest-ledger/latest/`
  (regenerable: `python 03-generate/generate.py projects/quest-ledger/config.yaml`, seed 777).
- **Star (after step 0):**
  - `DimDate` (2024–2026, marked date table; MonthName/DayName/MonthYear sort-by columns)
  - `DimGuildHall` — 6 halls · City · **Realm** (Eldoria / Grimmwald / Sunspire)
  - `DimQuestType` — 8 types · **Danger** (Low / Medium / High / Extreme)
  - `DimAdventurer` — 24 named · **Rank** (Gold / Silver / Bronze / Copper) · Class
  - `FactQuests` — ~40K rows, one per completed quest: `Bounty` (gold), `DaysOnQuest`, FKs to all four dims
  - `_Measures` — seeded by the hand-off: `Total Bounty`, `Quests`, `Avg Bounty`, `Total DaysOnQuest`, `Avg DaysOnQuest`
- **Grain:** one row = one completed quest. **Volume:** ~40K (trivial). **Sensitive data:** none (fictional).
- **Known truths to expect** (the generator pins these — use them to sanity-check visuals):
  Total Bounty = **6,000,000**; Realm Eldoria .40 / Grimmwald .35 / Sunspire .25; Danger Extreme .30 /
  High .35 / Medium .22 / Low .13; Rank Gold .40 / Silver .30 / Bronze .20 / Copper .10; +9% YoY;
  Nov/Dec peak. Top earner: Kaelen Swiftblade. Bread-and-butter quest: Monster Hunt.

## 3. KPIs (5 max)

| KPI | Measure | Context / comparison | Format |
|---|---|---|---|
| Total Bounty | `[Total Bounty]` | vs prior year (`[Bounty PY]`, add) → `[Bounty YoY %]` | #,##0 |
| Quests Completed | `[Quests]` | vs prior year | #,##0 |
| Avg Bounty per Quest | `[Avg Bounty]` | by danger tier | #,##0 |
| Avg Days on Quest | `[Avg DaysOnQuest]` | by quest type | 0.0 |
| Active Adventurers | `[Active Adventurers]` = `DISTINCTCOUNT(FactQuests[AdventurerKey])` (add) | of 24 | #,##0 |

Add during build (MCP-first if Desktop is open): `Bounty PY` (`CALCULATE([Total Bounty], SAMEPERIODLASTYEAR(DimDate[Date]))`),
`Bounty YoY %`, `Active Adventurers`, `Bounty Share` (`DIVIDE([Total Bounty], CALCULATE([Total Bounty], REMOVEFILTERS()))`).

## 4. Pages & layout (3 pages)

| # | Page | Question | Key visuals |
|---|---|---|---|
| 1 | **Guild Overview** | How is the guild doing, and where does the gold come from? | KPI row (§3) · monthly Bounty trend line (3 yrs, YoY visible) · Bounty by **Realm** (bar) · Bounty by **Danger** tier (bar, ordered Low→Extreme) |
| 2 | **Quest Board** | Which quests pay, and how long do they take? | Bounty by **QuestType** (pareto bar) · Avg Bounty vs Avg Days scatter (one dot per quest type, sized by Quests) · matrix Realm × Danger (Bounty) · slicer: Year |
| 3 | **Adventurer Roster** | Who earns the gold, and is rank earning its keep? | Bounty by **Rank** (bar) · top-10 adventurers (bar, with Rank colour) · table: Adventurer · Rank · Class · Quests · Total Bounty · Avg Days · slicers: Realm, Rank |

Page size 1280×720. Use the project `design-system.yaml` (copy from `02-build/report/layout/design-system-default.yaml`)
— 12×12 grid, summary/analysis/detail bands. 6–8 data visuals per page max. One insight title per page.

## 5. Branding & style

- **Theme:** reuse the workspace **Spectrum-Light** theme (`projects/themes/spectrum-light/`) — light, accessible.
- **Semantic colours (consistent everywhere):** Realm — Eldoria blue, Grimmwald slate, Sunspire amber.
  Danger is an ordered scale (sequential ramp Low→Extreme), never a random categorical.
- **Font / logo:** defaults; no logo.

## 6. Constraints & non-goals

- **Step 0 is mandatory and Desktop must be CLOSED for it** (the TMDL splice would be clobbered by an open Desktop).
- First open of the model needs a **Refresh** to load the CSVs (do it via the Modeling MCP `RefreshWithXMLA` once
  Desktop is up, or Home ▸ Refresh).
- **Accessibility:** WCAG AA; Danger tier also labelled, never colour-only.
- **Don't build:** drill-through pages, bookmarks, RLS — keep the demo flat and fast.
- **Deferred:** a "quest-type danger vs payout" what-if parameter.

## 7. Build sequence (the agent follows this when told "build the demo")

0. **Hand-off** (Desktop closed):
   `cd synthetic-data && python 04-output/handoff_to_pbi.py projects/quest-ledger/config.yaml --target ../power-bi/projects/demo`
   — splices tables, relationships, `SourceFolder`, `_Measures`. Then `pbir model "projects/demo/demo.Report" -d` to confirm.
1. **Activate the bridge (build-report.md B9a):** set `desktop_bridge: true` in `03-bind/via-powershell/hooks/config.yaml`;
   preflight `powerbi-desktop --version` (fallback `npx -y @microsoft/powerbi-desktop-bridge-cli`); then
   `powerbi-desktop open projects/demo/demo.pbip --timeout 120` and `status --wait-seconds 60` until
   `bridgeStatus: connected` — note the pid + page ids.
2. **Load data:** connect the Modeling MCP to the Desktop instance → `RefreshWithXMLA` (Full). Verify
   `[Total Bounty]` = 6,000,000 via a DAX query before touching visuals.
3. **Add the §3 measures** via MCP. Save in Desktop (persists to TMDL).
4. **Build pages 1→3** with `pbir`, theme applied, **reload + screenshot after each page** through the bridge;
   fix what the render shows before moving on.
5. **Review:** `pbir validate`, then `04-review/audit/layout-contract-validate.md` against this brief.

## 8. Open questions

- [ ] Scatter on page 2: per quest type (8 dots) or per adventurer (24 dots)? Default: quest type.
- [ ] Page 3 "top-10" by Total Bounty or by Avg Bounty (rewarding efficiency)? Default: Total.
- [ ] Keep `DaysOnQuest` as a KPI, or demote to page-2 context only?

## 9. References

- Dataset brief + config: `synthetic-data/projects/quest-ledger/`
- Hand-off mechanics: `synthetic-data/04-output/handoff-to-power-bi.md` (+ `handoff_to_pbi.py`)
- Bridge loop: `03-bind/desktop-bridge.md` · MCP-first rule: `02-build/context.md`
- Sibling demos in the same world: `projects/arcane-emporium/`, `synthetic-data/projects/guild-provisioners/`
