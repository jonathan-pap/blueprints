# Schema — The Grand Exchange

Generation contract for [brief.md](brief.md). The generator reads this; the reviewer validates against it.

Galaxy/constellation schema. `DimItem` is the hub. All keys are integer surrogates.

## Scale knobs

| Knob | smoke | full |
|---|---|---|
| `N_ITEMS` | 200 | 3,000 |
| `N_DAYS` | 90 | 1,095 (3 years) |
| `N_SELLERS` | 400 | 4,000 |
| `N_MONSTERS` | 80 | 400 |
| `N_REGIONS` | 12 | 40 |
| `N_RECIPES` | ~0.30 × N_ITEMS | ~0.30 × N_ITEMS |
| `N_TRADES` | 50,000 | 5,000,000 |

`DATE_START = 2023-01-01`, `DATE_END = DATE_START + N_DAYS - 1`.

## Dimensions

### DimRarity (6 rows, hand-built)
| Field | Type | Notes |
|---|---|---|
| RarityKey | int PK | 1..6 |
| RarityName | str | Common, Uncommon, Rare, Epic, Legendary, Mythic |
| RarityRank | int | 1..6 (sortable) |
| DropWeight | int | 50, 25, 14, 7, 3, 1 |
| ValueMultiplier | decimal | 1.0, 2.0, 5.0, 12.0, 40.0, 150.0 |
| ColorHex | str | one per rarity (for conditional fmt demos) |

### DimRegion (~40)
RegionKey int PK, RegionName str, Biome categorical {Forest, Desert, Tundra, Volcanic, Coastal, Swamp, Mountains, Plains}, LevelMin int, LevelMax int.

### DimSeller (~4,000)
SellerKey int PK, SellerName str (themed by SellerType), SellerType cat {Player 80%, NPC 20%}, Realm cat (~8 realms), ReputationTier cat {Bronze, Silver, Gold, Platinum} weighted by `SellerType` (NPCs skew Gold/Platinum).

### DimMonster (~400)
MonsterKey int PK, MonsterName str (themed), MonsterType cat {Beast, Undead, Demon, Elemental, Dragon, Humanoid}, Level int 1–80 (right-skewed low), RegionKey FK→DimRegion, IsElite bool (~12%), IsBoss bool (~3%).

### DimRecipe (~900 at full; ~0.30 × N_ITEMS in smoke)
RecipeKey int PK, OutputItemKey FK→DimItem, CraftingSkill cat {Alchemy, Smithing, Cooking, Enchanting, Tailoring, Engineering}, RequiredLevel int 1–80, YieldQty int 1–10 (right-skewed), CraftTimeSecs int.

### DimDate
Standard date dim: DateKey int yyyymmdd, Date date, Year, Quarter, Month, MonthName, Day, DayOfWeek, DayName, IsWeekend bool, IsoWeek.

### DimMarketEvent (~60)
EventKey int PK, EventName str, EventType cat {Patch, Seasonal, Crisis, Bonanza}, StartDate, EndDate, AffectedCategory FK→ItemCategory (or null = all), PriceShockPct decimal (-0.50…+0.80), DurationDays int. Hand-scripted across the 3-year window.

### DimItem (~3,000 at full, ~200 in smoke) — THE HUB
| Field | Type | Notes |
|---|---|---|
| ItemKey | int PK | 1..N |
| ItemName | str | themed by category + rarity (e.g., "Ember Crystal of Dawn") |
| ItemCategory | cat | {Weapon, Armor, Consumable, Material, Crystal, Reagent, Misc} weights |
| ItemSubtype | cat | depends on category (Sword/Bow/Staff/…; Helm/Chest/…; Potion/Food/…; Ore/Herb/Cloth/…; Essence/Shard/Geode/…) |
| RarityKey | FK | weighted by `DimRarity.DropWeight` (commons dominate) |
| BaseValue | decimal | log-normal, then × RarityMultiplier; floor 1 gold |
| StackSize | int | by category: gear=1, consumables=20, materials=99 |
| IsCraftable | bool | ~30% true (overridden true if the item is a recipe output) |
| IsTradeable | bool | ~95% true |
| Element | cat / null | {Fire, Ice, Lightning, Earth, Water, Wind, Light, Dark, None} — only on Material/Crystal |
| Potency | decimal / null | Codex of Crystals attribute; only on Crystal |
| Density | decimal / null | Crystal only |
| Volatility | decimal / null | Crystal only |
| BomTier | int | 1=raw, 2=refined, 3=component, 4=finished (used to seed recipes top-down) |

## Bridges / facts

### FactDropTable (~4,000)
MonsterKey FK, ItemKey FK, DropRatePct decimal (0–100, right-skewed low), MinQty int, MaxQty int. Many-to-many. Higher monster level → rarer items more likely in the drop.

### FactRecipeIngredient (~4,500)
RecipeKey FK, IngredientItemKey FK→DimItem, QtyRequired int (1–10). **Recursive BOM** — an item can be an ingredient in higher-tier recipes. Tier rule: an item at `BomTier=k` may only consume ingredients with `BomTier < k`.

### FactItemSource (~6,000)
ItemKey FK, AcquisitionMethod cat {Crafted, MonsterDrop, Gathered, Vendor, QuestReward, Treasure}, PrimaryFlag bool (exactly one primary per item).

### FactMarketPriceDaily (~3.3 M at full)
DateKey FK, ItemKey FK, OpenPrice, ClosePrice, HighPrice, LowPrice, AvgPrice, Volume, ListingsCount.

**Price model per item** (where coherence lives):
- `anchor = BaseValue × RarityMultiplier × craft_cost_factor`
  - `craft_cost_factor = max(1.0, recursive_craft_cost / BaseValue)` if craftable, else 1.0
- Daily walk: `price[t] = anchor × trend(t) × seasonality(t) × event_shock(t) × random_walk(t)`
  - `trend`: gentle ±10% across 3 years
  - `seasonality`: weekly — weekend +5–15% demand spike on Consumables/Materials, others flat
  - `event_shock`: `DimMarketEvent` rows pump/crash a category for their window
  - `random_walk`: AR(1) `walk[t] = 0.85 × walk[t-1] + N(0, σ)` with `σ = anchor × 0.04`
- OHLC: `Open = price[t-1]`, `Close = price[t]`; sample High/Low around `[Open, Close]` with extra noise. **Invariant:** `LowPrice ≤ Open/Close ≤ HighPrice`.
- `Volume`: ~ Poisson(λ) where λ inversely scales with rarity; weekend boost.
- `ListingsCount`: ~ Poisson(λ_listings); always > 0 if tradeable.

### FactTrade (~5 M at full, sampled ~50 k at smoke)
TradeKey int PK, DateKey FK, ItemKey FK, SellerKey FK→DimSeller, BuyerSellerKey FK→DimSeller (role-playing), Quantity int, UnitPrice decimal, TotalPrice decimal. `UnitPrice` sampled around that day's `AvgPrice` ± noise; `TotalPrice = Quantity × UnitPrice`.

## Business rules (enforced post-generation, checked by 05-review)

1. **Referential integrity** — every FK resolves.
2. **OHLC integrity** — `Low ≤ Open ≤ High`, `Low ≤ Close ≤ High`, all ≥ 0.
3. **`BomTier` monotonic** — recipe ingredients have strictly lower tier than output.
4. **Element/Potency nullability** — non-null only on Material (Element) / Crystal (Element + Potency + Density + Volatility).
5. **Primary acquisition** — exactly one `PrimaryFlag = true` per `ItemKey` in `FactItemSource`.
6. **Trade pricing** — `TotalPrice ≈ Quantity × UnitPrice` (tolerance 0.01).
7. **Recipe cost coherence** — for craftable items: `AvgPrice` should orbit `recursive_craft_cost × (1 + margin)`, margin in [-0.30, +1.00] (loose — gives the craft-vs-buy analysis its tension).

## Outputs

- Dims + bridges → CSV (`outputs/<date>-grand-exchange-<table>.csv`)
- `FactMarketPriceDaily`, `FactTrade` → **Parquet** at `full` scale; CSV at `smoke`
- Power BI hand-off: drop CSVs into `../power-bi/projects/grand-exchange/` (see [04-output/handoff-to-power-bi.md](../../../04-output/handoff-to-power-bi.md))
