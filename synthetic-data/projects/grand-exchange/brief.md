# Brief — The Grand Exchange (Fantasy MMO Economy)

Last updated: 2026-06-06

> **One-line concept:** A fully-invented fantasy MMO economy. `DimItem` sits at the hub; every item
> has a **rarity**, a **source** (craftable / monster drop / gathered / vendor / quest), an optional
> **recipe** (made from other items — a recursive bill-of-materials), and — for materials — **elemental
> properties** (the Codex of Crystals). Everything trades on **The Grand Exchange** with prices moving
> day by day. The world is invented, but the economics are coherent (price ≈ f(rarity, craft cost,
> drop rate)), which unlocks the headline analytical question: **craft vs. buy**.

---

## 1. Purpose & consumer

- **Purpose:** demo + training fixture, with an emphasis on a **performance / DAX** showcase
  (large fact, time intelligence, many-to-many, recursive BOM).
- **Who/what consumes it:** a Power BI model + people exploring it in training/demos.
- **Realism level:** **business-plausible distributions.** Invented world, but internally consistent —
  prices are driven by rarity, crafting cost and drop rarity rather than pure noise (see §5).

## 2. Datasets & volume

| Entity / table | Rows | Notes |
|---|---|---|
| `DimItem` | ~3,000 | The hub. Every tradeable thing: weapons, armor, consumables, materials, crystals. |
| `DimRarity` | 6 | Common → Uncommon → Rare → Epic → Legendary → Mythic. Carries `DropWeight` + `ColorHex`. |
| `DimSeller` | ~4,000 | Player + NPC traders. (No realm — removed 2026-06-07; see §10.) |
| `DimMonster` | ~400 | Drop sources: name, type, level, region, rarity. |
| `DimRegion` | ~40 | Zones/biomes — gathering nodes + monster habitats. |
| `DimRecipe` | ~900 | Craftable items: skill, level, yield, craft time. Output item → `DimItem`. |
| `DimDate` | ~1,617 | 4 full years (2022–2025) + 2026 YTD through today (2026-06-05), daily. Marked date table. |
| `DimMarketEvent` (optional) | ~90 | "Patch" / seasonal events that shock a category's prices. Scaled with span: ~15 events/year + ~7 YTD. |
| `FactMarketPriceDaily` | ~4.85M | **Primary time-series.** One row per (Item × Day): OHLC + volume + listings. Single global market — one price per item per day. |
| `FactTrade` (optional) | 15–75M | Transaction grain. The stress-test fact — tune the volume knob. |
| `FactDropTable` (bridge) | ~4,000 | Monster ↔ item, with `DropRatePct`. Many-to-many. |
| `FactRecipeIngredient` (BOM bridge) | ~4,500 | Recipe ↔ ingredient item, with `QtyRequired`. **Recursive** (items made from items). |
| `FactItemSource` (bridge) | ~6,000 | Item ↔ acquisition method (an item can have several). |
| `FactCraftBatch` (optional) | ~500k | Actual crafting runs: inputs consumed, yield, success/spoilage. |

## 3. Schema source

- [x] **From scratch** — fully invented world; no real spine. We own every distribution.
- [ ] Match an existing schema.
- [ ] Mimic the shape of a real dataset.

## 4. Fields, types & distributions

**`DimItem`** — the hub
| Field | Type | Domain / pattern | Distribution | Null % |
|---|---|---|---|---|
| ItemKey | int (PK) | surrogate | — | 0 |
| ItemName | string | themed fantasy name | — | 0 |
| ItemCategory | category | {Weapon, Armor, Consumable, Material, Crystal, Reagent, Misc} | weighted | 0 |
| ItemSubtype | category | e.g. {Sword, Potion, Ore, Herb, Essence} | weighted | 0 |
| RarityKey | int (FK) | → DimRarity | rarity weights (commons dominate) | 0 |
| BaseValue | decimal | gold; scales with rarity | right-skewed (log-normal) | 0 |
| StackSize | int | 1 / 20 / 99 | — | 0 |
| IsCraftable | bool | — | ~30% true | 0 |
| IsTradeable | bool | — | ~95% true | 0 |
| Element | category | {Fire, Ice, Lightning, Earth, Water, Wind, Light, Dark, None} | — | null unless Material/Crystal |
| Potency / Density / Volatility | decimal | Codex of Crystals properties (re-flavoured numeric attrs) | — | null unless Crystal |

**`DimRarity`**: RarityKey, RarityName, RarityRank (1–6), DropWeight (e.g. 50/25/14/7/3/1),
ValueMultiplier, ColorHex (for conditional formatting demos).

**`DimSeller`**: SellerKey, SellerName, SellerType {Player, NPC}, ReputationTier. *(No realm — removed 2026-06-07; see §10.)*

**`DimMonster`**: MonsterKey, MonsterName, MonsterType, Level, RegionKey (FK), MonsterRarity (elite/boss).

**`DimRecipe`**: RecipeKey, OutputItemKey (FK→DimItem), CraftingSkill {Alchemy, Smithing, Cooking,
Enchanting}, RequiredLevel, YieldQty, CraftTimeSecs.

**`FactMarketPriceDaily`** (grain = item × day) — the time-series spine
| Field | Type | Domain / pattern | Null % |
|---|---|---|---|
| DateKey | int (FK) | → DimDate | 0 |
| ItemKey | int (FK) | → DimItem | 0 |
| OpenPrice / ClosePrice / HighPrice / LowPrice | decimal | ≥ 0, OHLC consistent (Low ≤ Open/Close ≤ High) | 0 |
| AvgPrice | decimal | ≥ 0 | 0 |
| Volume | int | units traded that day | 0 |
| ListingsCount | int | active listings | 0 |

**`FactTrade`** (optional, grain = one trade): TradeKey, DateKey, ItemKey, SellerKey, BuyerKey,
Quantity, UnitPrice, TotalPrice. *(No realm — removed 2026-06-07.)*

**`FactDropTable`** (bridge): MonsterKey, ItemKey, DropRatePct (0–100), MinQty, MaxQty.

**`FactRecipeIngredient`** (BOM bridge): RecipeKey, IngredientItemKey (FK→DimItem), QtyRequired.

**`FactItemSource`** (bridge): ItemKey, AcquisitionMethod {Crafted, MonsterDrop, Gathered, Vendor,
QuestReward, Treasure}, PrimaryFlag.

## 5. Constraints & relationships

- **Keys:** surrogate PKs on every dim; bridges carry composite keys.
- **Relationships (galaxy / constellation schema, `DimItem` at the centre):**
  - `FactMarketPriceDaily` → `DimItem`, `DimDate`. Single global market — no realm dimension.
  - `FactTrade` → `DimItem`, `DimDate`, `DimSeller`, + Buyer as a **role-playing** seller relationship.
  - `FactDropTable`: `DimMonster` ↔ `DimItem` (**many-to-many** via the bridge).
  - `FactRecipeIngredient`: `DimRecipe` ↔ `DimItem` (**recursive BOM** — an item is both a recipe output
    *and* an ingredient in other recipes; supports a parent-child / `PATH` cost roll-up).
  - `FactItemSource`: `DimItem` ↔ acquisition method (**many-to-many**).
  - `DimMonster` → `DimRegion`; `DimRecipe[OutputItemKey]` → `DimItem`.
- **Economic business rules (the coherence layer — what makes it more than noise):**
  - `BaseValue` scales with rarity (`ValueMultiplier`); Mythic ≫ Common.
  - For craftable items: implied craft cost = Σ(ingredient AvgPrice × QtyRequired) ÷ YieldQty;
    market price should orbit craft cost × (1 + margin) + noise → enables **craft-vs-buy** analysis.
  - For drop items: price rises as `DropRatePct` falls and monster level rises.
  - OHLC integrity: `LowPrice ≤ Open/Close ≤ HighPrice`; `Volume`, `ListingsCount` ≥ 0.
  - Materials/Crystals only carry Element/Potency/etc.; finished gear does not.
- **Temporal:** 4 full years (2022–2025) + 2026 YTD daily — `2022-01-01` through today (`2026-06-05`),
  ~1,617 days. Long enough for **YoY comparisons across 4 prior years** (Trade Value PY/YoY %, the
  YoY variance recipe, rolling 30D), a multi-year **base trend** + **weekly seasonality** (weekend
  demand spikes) + a bounded random walk, plus scripted **market events** (`DimMarketEvent`) that
  pump or crash a category for a window — event-annotated time-series demos that span multiple
  patches per year.

## 6. Reproducibility

- **Seed:** yes — fix one (default `42`). Critical here, since the *entire* dataset is generated:
  same seed + same config = identical data, prices and trades.

## 7. Privacy / PII

- **Fully synthetic.** No real records, no real PII anywhere — invented world end to end.

## 8. Output target

- **Format(s):** CSV per dimension/bridge; **Parquet** for the multi-million-row facts
  (`FactMarketPriceDaily`, `FactTrade`) since CSV gets unwieldy at that size.
- **Destination:** `outputs/` → handed off to a Power BI project (`../power-bi/projects/grand-exchange/`).
- Build as a clean galaxy schema: hidden keys, display folders, marked date table, bridges hidden.

## 9. Decisions (resolved 2026-05-27; time-span extended 2026-06-05)

- [x] **Market fact grain:** BOTH — `FactMarketPriceDaily` (daily OHLC snapshot) for charts/time-intel + a sampled `FactTrade` for volume/flow analysis.
- [x] **Volume target:** two-knob scale.
  - **smoke** — 200 items × 90 days (most-recent window: `2026-03-09` → `2026-06-05`) = ~18 k snapshot rows, ~50 k trades. Default for iteration.
  - **full** — 3,000 items × 1,617 days (`2022-01-01` → `2026-06-05`) = **~4.85 M snapshot rows**, **~7.5 M trades**. The performance fact.
- [x] **Time span:** 4 full years + 2026 YTD daily (`2022-01-01` → `2026-06-05`, ~1,617 days); no intraday.
- [x] **Craft-batch layer:** SKIP `FactCraftBatch` for v1 — BOM bridge is enough. Add later if manufacturing analytics requested.
- [x] **Sellers:** BOTH player + NPC. Track buyer too (`BuyerSellerKey` on `FactTrade`, role-playing relationship to `DimSeller`).
- [x] **Market events:** INCLUDE `DimMarketEvent` (~90 rows, scripted shocks scaled with the extended span). Huge analytical payoff for ~90 rows.
- [x] **Theme set:** GENERIC fantasy-MMO flavour (no specific game IP) — themed name pools per category.
- [x] **BOM depth:** 3 tiers (raw → refined → component → finished). Meaningful recursion for `PATH` cost roll-up without combinatorial blow-up.

## 10. Realm — explored, then removed (decided 2026-06-07)

**Decision: there is no realm dimension. The exchange is a single global market.** Realms are
purely a player-connection grouping — everyone trades on *one* shared exchange, so there is
exactly one price per item per day and nothing meaningful to slice "market by realm." Realm was
removed from the model entirely (no `DimRealm`, no `RealmKey` on `DimSeller`/`FactTrade`, no
per-realm price fact, no Arbitrage measures).

**Why it was explored first (and what we learned).** A realm slicer was originally requested for
the market + trade visuals. Four iterations established that it doesn't fit this world:

| Attempt | What | Outcome |
| --- | --- | --- |
| 1–2 | Extract `DimRealm`; put `RealmKey` on `DimSeller` + `FactTrade`. | Realm worked as a *trade/seller* grouping, but the **market candle is exchange-wide** — a realm slicer has no price path to it (you never join fact→fact; conform via shared dims only). |
| 3 | Re-grain the single `FactMarketPriceDaily` to (Item, Realm, Date). | Reverted — 38.8 M rows, and every SUM-based candle measure inflated 8×. |
| 4 | Separate `FactMarketPriceDailyByRealm` fact (~2.34 M) with faction-tilted per-realm price divergence + Arbitrage measures. | Built and validated, then **removed** — per-realm *divergent* prices only make sense if realms are separate markets. They aren't: one shared exchange = one price. The divergence modelled a world we don't have. |

**The takeaway (kept for posterity):** realm/seller can only meaningfully filter **trades** (who
traded), never the **market price** (which is global). Filtering market by realm is not a modelling
gap — it's semantically empty under "one shared exchange." If a true multi-server world is ever
wanted, that's a separate `FactMarketPriceDailyByRealm` with genuinely independent per-server
prices — a deliberate re-introduction, not a default.
