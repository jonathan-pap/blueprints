# Brief — Quest Ledger (Dragonhold Adventurers' Guild)

**Purpose:** a fresh demo star to populate the blank `power-bi/projects/demo` model end-to-end —
generate → reconcile → hand off → build a report → verify through the Desktop Bridge. Same fantasy world
as Arcane Emporium / Guild Provisioners (Eldoria / Grimmwald / Sunspire) so the demos hang together.

**The data:** the guild's bounty book. One row = one completed quest: which **guild hall** posted it,
the **quest type** (and danger tier), which **adventurer** (and rank/class) completed it, on what
**date**, for how much **Bounty** gold, over how many **DaysOnQuest**. Three years (2024–2026), ~40K
quests, 6M gold, +9% YoY, campaign-season peak.

**Declared story (the shares the engine pins exactly):** Eldoria .40 / Grimmwald .35 / Sunspire .25 ·
danger tier Extreme .30 / High .35 / Medium .22 / Low .13 · adventurer rank Gold .40 / Silver .30 /
Bronze .20 / Copper .10 · pareto leaders inside every pinned group (Monster Hunt is the bread-and-butter
quest; Kaelen Swiftblade the top earner).

- **Config:** [`config.yaml`](config.yaml) (the declaration IS the schema) · seed 777 · PII: none (all fictional).
- **Run:** `python 03-generate/generate.py projects/quest-ledger/config.yaml` →
  `python 05-review/reconcile.py projects/quest-ledger/config.yaml`
- **Output:** `outputs/quest-ledger/latest/` — DimDate, DimGuildHall, DimQuestType, DimAdventurer, FactQuests.

## Hand-off → Power BI (the point of this job)

**Target:** `../power-bi/projects/demo/demo.SemanticModel` (blank PBIP already in place).
**Mode:** TMDL splice — `python 04-output/handoff_to_pbi.py projects/quest-ledger/config.yaml --target ../power-bi/projects/demo`
writes typed import tables (M partitions reading `SourceFolder & "<Table>.csv"`), a `SourceFolder`
parameter pointing at `outputs/quest-ledger/latest/`, fact→dim relationships on the `<Dim>Key` columns,
DimDate marked as the date table, and a `_Measures` table seeded with `Total Bounty` / `Quests` /
`Avg Days on Quest`. Desktop must be **closed** during the splice; first open needs a refresh.

Downstream report brief: `../power-bi/projects/demo/brief.md`.
