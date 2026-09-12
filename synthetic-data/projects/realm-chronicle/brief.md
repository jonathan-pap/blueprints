# Brief — Realm Chronicle

One world, four ledgers. This merges the two fantasy strands the workspace already has — the
adventurers' guild (quests, ranks, bounties) and the grand exchange (items, gold, trading posts) —
into a single RPG universe where **monsters slain, quests taken, loot dropped and goods traded all
share the same dimensions**. Four years of it (2023-2026).

## 1. Purpose & consumer

A demo dataset rich enough to carry a multi-page Power BI report without inventing extra tables:
guild rivalry, player leaderboards, field-vs-boss combat, quest economics, and a loot-driven market.
Consumer: the `power-bi/` blueprint (report build), and anyone wanting a star with four conformed facts.

## 2. Datasets & volume

| Table | Grain | Cross-product | Rows after sparsity |
|---|---|---|---|
| `FactMonsterKills` | Date × Adventurer × Monster | 2.80M | ~195k |
| `FactQuests` | Date × Adventurer × Quest | 1.75M | ~105k |
| `FactLootDrops` | Date × Monster × Item | 2.24M | ~67k |
| `FactMarketTrades` | Date × Item × Realm | 561k | ~309k |
| 6 dimensions | — | — | 1461 + 60 + 32 + 48 + 20 + 8 |

Every fact's cross-product stays in the low millions, per the engine's scaling note
(`03-generate/engine-share-allocation.md`).

## 3. Schema source

Declared, not hand-written: `config.yaml` in this folder, run through the room engine
(`03-generate/generate.py`). Grammar: `02-schema/config-schema.md`.

## 4. Fields, types & distributions

**Dimensions** (explicit members throughout, so every row reads as a name rather than a key):

- **Date** — calendar, 2023-01-01 → 2026-12-31, day grain.
- **Adventurer** (60) — `Guild` (10), `Class` (6), `Rank` (Copper/Bronze/Silver/Gold). Guild is an
  attribute here, not a separate grain dimension: a player belongs to exactly one guild, so
  Guild × Adventurer in a grain would create ~600 combinations where only 60 are real. Roll up by
  `Guild`, drill down to `Adventurer` — the report the request asks for, with an honest model.
- **Monster** (32) — `Kind` (**Field / Elite / Boss**), `Family` (Beast, Undead, Dragon, Elemental,
  Demon, Construct), `Tier` 1-5, `Habitat`.
- **Quest** (20) — `QuestType` (Hunt/Escort/Gather/Delve/Raid), `Danger` (Low→Extreme), `RankRequired`.
- **Item** (48) — `Category` (Weapon/Armour/Potion/Reagent/Trophy), `Rarity`
  (Common→Legendary), `Slot`.
- **Realm** (8) — `Terrain`, `ThreatBand`. The market's trading posts.

**Declared marginals** (the story the engine rakes to):

- Combat is mostly rank-and-file: **Field .82 / Elite .15 / Boss .03** of all kills.
- Loot skews common: **Common .55 → Legendary .015**.
- Bounty rises with danger: **Low .12 / Medium .28 / High .36 / Extreme .24**.
- Guild share of kills is deliberately uneven (Ironpact leads at .155, Hollow Crown trails at .045)
  so leaderboards have a shape.
- Growth: kills +12%/yr, bounty +9%/yr, market +15%/yr — the realm is getting busier.
- **Party wipes are allocated, not derived** (9,000 total; Elite .40 / Boss .38 / Field .22, and a
  guild split that deliberately *differs* from the kill split). Deriving them per row as
  `floor(slain / n)` collapsed to zero on low-volume rows — the smallest guild showed one wipe per
  18,000 kills against the leader's one per 329. Declared, it rakes cleanly and says something
  better: Gilded Fang wipes every ~142 kills, Emberwatch every ~373. Recklessness, not volume.

## 5. Constraints & relationships

Conformed dimensions do the joining: Adventurer links kills↔quests, Monster links kills↔loot,
Item links loot↔market. That chain is the point — **a boss dies, an item drops, the item trades** —
and it means a report can follow gold from the dungeon to the exchange.

**Known limitation (engine v1):** shares are 1-D per key, so *cross* marginals aren't controlled.
Loot rarity and monster kind are each exact on their own, but "bosses drop the legendaries" is not
enforced — a Legendary can drop from a Field monster. Fixing it properly means cross-share support
in the engine (`engine-share-allocation.md` → Extending), not a hack in this config.

## 6. Reproducibility

Seed `20260912`, recorded in `seed.txt` and `_manifest.json`. Same seed + same config = same data.

## 7. Privacy / PII

None. Every name is invented fantasy; no faker providers, no real-world people, places or records.

## 8. Output target

`synthetic-data/outputs/realm-chronicle/latest/` (stable path for the Power BI hand-off).
Not yet spliced into a semantic model — that's `04-output/handoff_to_pbi.py` when a report project exists.

## 9. Open questions

- Should Adventurer carry a `JoinedDate` for cohort analysis? Left out to keep the dim flat.
- Boss kills at .03 of 2.4M is ~72k boss slayings over four years — generous for "boss" semantics.
  Lower it if bosses should feel rarer.
