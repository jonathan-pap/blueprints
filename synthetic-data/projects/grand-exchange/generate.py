"""Grand Exchange — fantasy MMO economy generator.

Reads contract from schema.md (this file IS the implementation of that contract).
Honors the seed in seed.txt. Two scales: 'smoke' (default, fast) and 'full' (multi-million rows).

Usage:
    python generate.py                 # smoke
    python generate.py --scale full    # full
    python generate.py --out ../../outputs/2026-05-27-grand-exchange   # custom out prefix
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_OUT_DIR = HERE.parent.parent / "outputs"
JOB = "grand-exchange"


# ──────────────────────────────────────────────────────────────────────────────
# Scale config
# ──────────────────────────────────────────────────────────────────────────────
SCALES = {
    "smoke": dict(
        N_ITEMS=200, N_DAYS=90, N_SELLERS=400, N_MONSTERS=80,
        N_REGIONS=12, N_TRADES=50_000, N_EVENTS=12,
    ),
    "full": dict(
        N_ITEMS=3_000, N_DAYS=1_095, N_SELLERS=4_000, N_MONSTERS=400,
        N_REGIONS=40, N_TRADES=5_000_000, N_EVENTS=60,
    ),
}
DATE_START = date(2023, 1, 1)


# ──────────────────────────────────────────────────────────────────────────────
# Themed name pools (generic fantasy — no game IP)
# ──────────────────────────────────────────────────────────────────────────────
PREFIXES = ["Ember", "Frost", "Storm", "Shadow", "Sun", "Moon", "Iron", "Mithril",
            "Obsidian", "Crystal", "Verdant", "Hollow", "Ancient", "Cursed", "Blessed",
            "Twilight", "Dawn", "Dusk", "Wyrm", "Drake", "Phoenix", "Spectral"]
SUFFIXES_OF = ["of Dawn", "of Embers", "of Tides", "of the Void", "of Whispers",
               "of Valor", "of Ruin", "of Stars", "of the Forge", "of the Wild",
               "of Echoes", "of Lightning", "of Frost", "of Flame", "of Glass"]
WEAPON_TYPES = ["Sword", "Bow", "Staff", "Dagger", "Axe", "Spear", "Mace", "Wand", "Crossbow", "Glaive"]
ARMOR_TYPES = ["Helm", "Chestplate", "Gauntlets", "Greaves", "Boots", "Cloak", "Robe", "Pauldrons"]
CONSUMABLE_TYPES = ["Potion", "Elixir", "Tonic", "Draught", "Food", "Scroll"]
MATERIAL_TYPES = ["Ore", "Ingot", "Bar", "Plank", "Cloth", "Leather", "Herb", "Bone", "Hide"]
CRYSTAL_TYPES = ["Crystal", "Shard", "Geode", "Essence", "Prism", "Sliver"]
REAGENT_TYPES = ["Powder", "Extract", "Resin", "Ash", "Tincture"]
MISC_TYPES = ["Trinket", "Charm", "Token", "Relic", "Fragment"]

SUBTYPE_BY_CATEGORY = {
    "Weapon": WEAPON_TYPES, "Armor": ARMOR_TYPES, "Consumable": CONSUMABLE_TYPES,
    "Material": MATERIAL_TYPES, "Crystal": CRYSTAL_TYPES, "Reagent": REAGENT_TYPES,
    "Misc": MISC_TYPES,
}

ELEMENTS = ["Fire", "Ice", "Lightning", "Earth", "Water", "Wind", "Light", "Dark"]
BIOMES = ["Forest", "Desert", "Tundra", "Volcanic", "Coastal", "Swamp", "Mountains", "Plains"]
MONSTER_TYPES = ["Beast", "Undead", "Demon", "Elemental", "Dragon", "Humanoid"]
MONSTER_NAMES = ["Wraith", "Ghoul", "Direwolf", "Ogre", "Lich", "Wyrm", "Drake", "Imp",
                 "Golem", "Hydra", "Specter", "Basilisk", "Manticore", "Banshee", "Troll", "Harpy"]
CRAFT_SKILLS = ["Alchemy", "Smithing", "Cooking", "Enchanting", "Tailoring", "Engineering"]
REALMS = ["Aurelia", "Mythos", "Veridian", "Stormhaven", "Ashfall", "Eldoria", "Tenebris", "Solaris"]
REP_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]
PLAYER_NAMES = ["Aria", "Bjorn", "Caelum", "Drust", "Eira", "Faelyn", "Gorm", "Hesper",
                "Idra", "Joren", "Kael", "Lyra", "Myrra", "Nyx", "Oryn", "Pell", "Quill",
                "Ronan", "Sable", "Thane", "Ulric", "Vex", "Wren", "Xara", "Yorick", "Zane"]
NPC_TITLES = ["Merchant", "Trader", "Quartermaster", "Vendor", "Broker"]


# ──────────────────────────────────────────────────────────────────────────────
# Dim builders
# ──────────────────────────────────────────────────────────────────────────────
def build_dim_rarity() -> pd.DataFrame:
    return pd.DataFrame({
        "RarityKey": range(1, 7),
        "RarityName": ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic"],
        "RarityRank": range(1, 7),
        "DropWeight": [50, 25, 14, 7, 3, 1],
        "ValueMultiplier": [1.0, 2.0, 5.0, 12.0, 40.0, 150.0],
        "ColorHex": ["#9E9E9E", "#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#F44336"],
    })


def build_dim_region(rng: np.random.Generator, n: int) -> pd.DataFrame:
    biomes = rng.choice(BIOMES, n)
    level_min = rng.integers(1, 60, n)
    level_max = np.minimum(level_min + rng.integers(10, 25, n), 80)
    return pd.DataFrame({
        "RegionKey": range(1, n + 1),
        "RegionName": [f"{b} of {PREFIXES[i % len(PREFIXES)]}" for i, b in enumerate(biomes)],
        "Biome": biomes, "LevelMin": level_min, "LevelMax": level_max,
    })


def build_dim_seller(rng: np.random.Generator, n: int) -> pd.DataFrame:
    types = rng.choice(["Player", "NPC"], n, p=[0.80, 0.20])
    realms = rng.choice(REALMS, n)
    names = []
    for i, t in enumerate(types):
        if t == "Player":
            base = PLAYER_NAMES[i % len(PLAYER_NAMES)]
            names.append(f"{base}{rng.integers(1, 9999)}")
        else:
            names.append(f"{rng.choice(NPC_TITLES)} {PLAYER_NAMES[i % len(PLAYER_NAMES)]}")
    rep = np.where(
        types == "NPC",
        rng.choice(REP_TIERS, n, p=[0.05, 0.15, 0.50, 0.30]),
        rng.choice(REP_TIERS, n, p=[0.35, 0.35, 0.25, 0.05]),
    )
    return pd.DataFrame({
        "SellerKey": range(1, n + 1), "SellerName": names,
        "SellerType": types, "Realm": realms, "ReputationTier": rep,
    })


def build_dim_monster(rng: np.random.Generator, n: int, n_regions: int) -> pd.DataFrame:
    types = rng.choice(MONSTER_TYPES, n)
    # right-skewed levels (most monsters are low-level fodder)
    levels = np.clip(rng.gamma(2.0, 8.0, n).astype(int) + 1, 1, 80)
    base_names = rng.choice(MONSTER_NAMES, n)
    prefixes = rng.choice(PREFIXES, n)
    return pd.DataFrame({
        "MonsterKey": range(1, n + 1),
        "MonsterName": [f"{p} {b}" for p, b in zip(prefixes, base_names)],
        "MonsterType": types, "Level": levels,
        "RegionKey": rng.integers(1, n_regions + 1, n),
        "IsElite": rng.random(n) < 0.12,
        "IsBoss": rng.random(n) < 0.03,
    })


def build_dim_date(n_days: int) -> pd.DataFrame:
    dates = pd.date_range(DATE_START, periods=n_days, freq="D")
    return pd.DataFrame({
        "DateKey": dates.strftime("%Y%m%d").astype(int),
        "Date": dates.date,
        "Year": dates.year, "Quarter": dates.quarter, "Month": dates.month,
        "MonthName": dates.month_name(), "Day": dates.day,
        "DayOfWeek": dates.dayofweek + 1,
        "DayName": dates.day_name(),
        "IsWeekend": dates.dayofweek >= 5,
        "IsoWeek": dates.isocalendar().week.values,
    })


def build_dim_market_event(rng: np.random.Generator, n: int, n_days: int,
                           categories: list[str]) -> pd.DataFrame:
    event_types = rng.choice(["Patch", "Seasonal", "Crisis", "Bonanza"], n,
                             p=[0.30, 0.35, 0.20, 0.15])
    start_offsets = np.sort(rng.integers(0, max(1, n_days - 14), n))
    durations = rng.integers(3, 21, n)
    # Crisis = price down, Bonanza = price up, Patch/Seasonal = mixed
    shocks = np.where(event_types == "Crisis", -np.abs(rng.normal(0.30, 0.10, n)),
                      np.where(event_types == "Bonanza", np.abs(rng.normal(0.40, 0.15, n)),
                               rng.normal(0.0, 0.20, n))).clip(-0.50, 0.80)
    affected = rng.choice(categories + [None], n,
                          p=[0.95 / len(categories)] * len(categories) + [0.05])
    starts = [DATE_START + timedelta(days=int(o)) for o in start_offsets]
    ends = [s + timedelta(days=int(d) - 1) for s, d in zip(starts, durations)]
    return pd.DataFrame({
        "EventKey": range(1, n + 1),
        "EventName": [f"{t}: {PREFIXES[i % len(PREFIXES)]} {SUFFIXES_OF[i % len(SUFFIXES_OF)]}"
                      for i, t in enumerate(event_types)],
        "EventType": event_types,
        "StartDate": starts, "EndDate": ends,
        "AffectedCategory": affected,
        "PriceShockPct": np.round(shocks, 4),
        "DurationDays": durations,
    })


def build_dim_item(rng: np.random.Generator, n: int, dim_rarity: pd.DataFrame) -> pd.DataFrame:
    categories = ["Weapon", "Armor", "Consumable", "Material", "Crystal", "Reagent", "Misc"]
    cat_weights = np.array([0.15, 0.15, 0.20, 0.25, 0.10, 0.10, 0.05])
    cats = rng.choice(categories, n, p=cat_weights)
    subtypes = np.array([rng.choice(SUBTYPE_BY_CATEGORY[c]) for c in cats])

    # rarity by drop weight
    rarity_weights = dim_rarity["DropWeight"].values / dim_rarity["DropWeight"].sum()
    rarity_keys = rng.choice(dim_rarity["RarityKey"].values, n, p=rarity_weights)
    rarity_mult = dim_rarity.set_index("RarityKey").loc[rarity_keys, "ValueMultiplier"].values

    # log-normal base value × rarity multiplier
    base = np.exp(rng.normal(3.0, 1.2, n))  # mean ~20 gold
    base_value = np.maximum(1.0, np.round(base * rarity_mult, 2))

    # names
    prefixes = rng.choice(PREFIXES, n)
    suffixes_use_of = rng.random(n) < 0.45
    names = []
    for i in range(n):
        suff = f" {rng.choice(SUFFIXES_OF)}" if suffixes_use_of[i] else ""
        names.append(f"{prefixes[i]} {subtypes[i]}{suff}")

    stack_size = np.where(np.isin(cats, ["Weapon", "Armor"]), 1,
                          np.where(np.isin(cats, ["Consumable"]), 20, 99))

    is_tradeable = rng.random(n) < 0.95
    is_craftable_seed = rng.random(n) < 0.30  # may be promoted later by recipe assignment

    # element only on Material/Crystal
    element = np.where(np.isin(cats, ["Material", "Crystal"]),
                       rng.choice(ELEMENTS, n), None)
    # Crystal-only attributes
    potency = np.where(cats == "Crystal", np.round(rng.uniform(1, 100, n), 2), np.nan)
    density = np.where(cats == "Crystal", np.round(rng.uniform(0.5, 10, n), 2), np.nan)
    volatility = np.where(cats == "Crystal", np.round(rng.uniform(0, 1, n), 3), np.nan)

    # BomTier: raw materials tier 1, refined tier 2, components tier 3, finished tier 4
    # heuristic by category
    tier = np.where(cats == "Material", rng.choice([1, 2], n, p=[0.65, 0.35]),
            np.where(cats == "Crystal", rng.choice([1, 2], n, p=[0.50, 0.50]),
             np.where(cats == "Reagent", rng.choice([2, 3], n, p=[0.60, 0.40]),
              np.where(cats == "Consumable", rng.choice([3, 4], n, p=[0.30, 0.70]),
               np.where(np.isin(cats, ["Weapon", "Armor"]), 4,
                rng.choice([2, 3], n, p=[0.5, 0.5]))))))  # Misc

    return pd.DataFrame({
        "ItemKey": range(1, n + 1), "ItemName": names,
        "ItemCategory": cats, "ItemSubtype": subtypes,
        "RarityKey": rarity_keys, "BaseValue": base_value,
        "StackSize": stack_size, "IsCraftable": is_craftable_seed,
        "IsTradeable": is_tradeable, "Element": element,
        "Potency": potency, "Density": density, "Volatility": volatility,
        "BomTier": tier,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Bridges / recipes
# ──────────────────────────────────────────────────────────────────────────────
def build_recipes_and_bom(rng: np.random.Generator, dim_item: pd.DataFrame):
    """Pick craftable outputs (tier ≥ 2), assign 2–5 ingredients each from strictly lower tiers."""
    # eligible outputs = any item with BomTier >= 2
    eligible = dim_item[dim_item["BomTier"] >= 2].copy()
    n_recipes = max(10, int(0.30 * len(dim_item)))
    if len(eligible) < n_recipes:
        n_recipes = len(eligible)
    chosen = eligible.sample(n=n_recipes, random_state=int(rng.integers(0, 2**31)))

    recipe_keys = np.arange(1, n_recipes + 1)
    output_keys = chosen["ItemKey"].values
    skills = rng.choice(CRAFT_SKILLS, n_recipes)
    levels = np.clip(rng.gamma(3.0, 8.0, n_recipes).astype(int) + 1, 1, 80)
    yield_qty = np.maximum(1, rng.choice([1, 1, 1, 2, 3, 5, 10], n_recipes,
                                          p=[0.40, 0.20, 0.10, 0.15, 0.08, 0.05, 0.02]))
    craft_time = rng.integers(5, 600, n_recipes)
    dim_recipe = pd.DataFrame({
        "RecipeKey": recipe_keys, "OutputItemKey": output_keys,
        "CraftingSkill": skills, "RequiredLevel": levels,
        "YieldQty": yield_qty, "CraftTimeSecs": craft_time,
    })

    # ingredients: each recipe consumes 2-5 ingredients from items at strictly lower BomTier
    bom_rows = []
    item_by_tier = {t: dim_item[dim_item["BomTier"] == t]["ItemKey"].values for t in [1, 2, 3]}
    output_tier = dim_item.set_index("ItemKey").loc[output_keys, "BomTier"].values
    for rk, out_tier in zip(recipe_keys, output_tier):
        candidates = np.concatenate([item_by_tier[t] for t in range(1, out_tier)
                                     if t in item_by_tier and len(item_by_tier[t])])
        if len(candidates) == 0:
            continue
        n_ing = int(rng.integers(2, min(6, len(candidates) + 1)))
        ingredients = rng.choice(candidates, n_ing, replace=False)
        qtys = rng.integers(1, 11, n_ing)
        for ing, qty in zip(ingredients, qtys):
            bom_rows.append((rk, int(ing), int(qty)))
    fact_bom = pd.DataFrame(bom_rows, columns=["RecipeKey", "IngredientItemKey", "QtyRequired"])

    # promote items that are recipe outputs to IsCraftable=True
    craftable_outputs = set(int(k) for k in output_keys)
    dim_item.loc[dim_item["ItemKey"].isin(craftable_outputs), "IsCraftable"] = True
    return dim_recipe, fact_bom


def build_fact_drop_table(rng: np.random.Generator, dim_monster: pd.DataFrame,
                          dim_item: pd.DataFrame) -> pd.DataFrame:
    """Each monster drops 5–15 items; rarer items more likely from higher-level monsters."""
    rows = []
    item_keys = dim_item["ItemKey"].values
    item_rarity = dim_item["RarityKey"].values  # 1..6
    for mk, level in zip(dim_monster["MonsterKey"].values, dim_monster["Level"].values):
        n_drops = int(rng.integers(5, 16))
        # weight: higher level → more chance of rare items
        rarity_pref = np.clip((item_rarity - 1) * (level / 80.0), 0.1, 5.0)
        weights = 1.0 / (1.0 + rarity_pref)
        weights = weights / weights.sum()
        chosen = rng.choice(item_keys, size=min(n_drops, len(item_keys)),
                            replace=False, p=weights)
        for ik in chosen:
            rarity = int(dim_item.loc[dim_item["ItemKey"] == ik, "RarityKey"].iloc[0])
            drop_rate = max(0.1, rng.beta(2.0, 2.0 + rarity * 1.5) * 100)
            min_q = int(rng.integers(1, 4))
            max_q = min_q + int(rng.integers(0, 10))
            rows.append((int(mk), int(ik), round(drop_rate, 2), min_q, max_q))
    return pd.DataFrame(rows, columns=["MonsterKey", "ItemKey", "DropRatePct", "MinQty", "MaxQty"])


def build_fact_item_source(rng: np.random.Generator, dim_item: pd.DataFrame) -> pd.DataFrame:
    """Each item has 1–3 sources, exactly one PrimaryFlag=True."""
    rows = []
    methods_by_cat = {
        "Weapon": ["Crafted", "MonsterDrop", "QuestReward", "Treasure"],
        "Armor": ["Crafted", "MonsterDrop", "QuestReward", "Treasure"],
        "Consumable": ["Crafted", "Vendor", "QuestReward"],
        "Material": ["Gathered", "MonsterDrop", "Vendor"],
        "Crystal": ["Gathered", "MonsterDrop", "Treasure"],
        "Reagent": ["Gathered", "Vendor"],
        "Misc": ["QuestReward", "Treasure", "Vendor"],
    }
    for ik, cat in zip(dim_item["ItemKey"].values, dim_item["ItemCategory"].values):
        candidates = methods_by_cat.get(cat, ["Vendor"])
        n_sources = int(rng.integers(1, min(4, len(candidates) + 1)))
        chosen = list(rng.choice(candidates, n_sources, replace=False))
        primary_idx = int(rng.integers(0, n_sources))
        for i, m in enumerate(chosen):
            rows.append((int(ik), m, i == primary_idx))
    return pd.DataFrame(rows, columns=["ItemKey", "AcquisitionMethod", "PrimaryFlag"])


# ──────────────────────────────────────────────────────────────────────────────
# Recursive craft cost roll-up (memoized)
# ──────────────────────────────────────────────────────────────────────────────
def compute_craft_costs(dim_item: pd.DataFrame, dim_recipe: pd.DataFrame,
                        fact_bom: pd.DataFrame) -> dict[int, float]:
    """Returns {ItemKey: anchor_cost}. For non-craftable items = BaseValue. For craftable items =
    max(BaseValue, recursive_ingredient_cost / YieldQty)."""
    base_value = dict(zip(dim_item["ItemKey"].astype(int), dim_item["BaseValue"].astype(float)))
    recipe_of = dict(zip(dim_recipe["OutputItemKey"].astype(int),
                          zip(dim_recipe["RecipeKey"].astype(int),
                              dim_recipe["YieldQty"].astype(int))))
    bom_by_recipe: dict[int, list[tuple[int, int]]] = {}
    for _, r in fact_bom.iterrows():
        bom_by_recipe.setdefault(int(r["RecipeKey"]), []).append(
            (int(r["IngredientItemKey"]), int(r["QtyRequired"])))

    memo: dict[int, float] = {}
    visiting: set[int] = set()

    def cost(item_key: int) -> float:
        if item_key in memo:
            return memo[item_key]
        if item_key in visiting:
            return base_value[item_key]  # cycle guard — shouldn't happen with BomTier rule
        if item_key not in recipe_of:
            memo[item_key] = base_value[item_key]
            return memo[item_key]
        visiting.add(item_key)
        recipe_key, yield_qty = recipe_of[item_key]
        ing_cost = sum(cost(ing) * qty for ing, qty in bom_by_recipe.get(recipe_key, []))
        c = max(base_value[item_key], ing_cost / max(1, yield_qty))
        memo[item_key] = c
        visiting.discard(item_key)
        return c

    for ik in dim_item["ItemKey"].astype(int):
        cost(ik)
    return memo


# ──────────────────────────────────────────────────────────────────────────────
# FactMarketPriceDaily — the spine
# ──────────────────────────────────────────────────────────────────────────────
def build_fact_market_price(rng: np.random.Generator, dim_item: pd.DataFrame,
                             dim_date: pd.DataFrame, anchors: dict[int, float],
                             dim_event: pd.DataFrame) -> pd.DataFrame:
    n_items = len(dim_item)
    n_days = len(dim_date)
    item_keys = dim_item["ItemKey"].values
    date_keys = dim_date["DateKey"].values
    is_weekend = dim_date["IsWeekend"].values
    cats = dim_item["ItemCategory"].values
    rarities = dim_item["RarityKey"].values

    # vectorized per-item anchor
    anchor_arr = np.array([anchors[int(k)] for k in item_keys])

    # event matrix: shock multiplier per (day, category)
    event_mult = np.ones((n_days, n_items))
    dates_arr = pd.Series(dim_date["Date"].values)
    for _, ev in dim_event.iterrows():
        start, end = ev["StartDate"], ev["EndDate"]
        mask_day = (dates_arr >= start) & (dates_arr <= end)
        affected = ev["AffectedCategory"]
        if affected is None or (isinstance(affected, float) and np.isnan(affected)):
            mask_item = np.ones(n_items, bool)
        else:
            mask_item = cats == affected
        if mask_day.any() and mask_item.any():
            event_mult[np.ix_(mask_day.values, mask_item)] *= (1.0 + ev["PriceShockPct"])

    # seasonality: weekend boost on Consumable/Material
    seasonal_boost = np.where(np.isin(cats, ["Consumable", "Material"]), 0.10, 0.02)
    seasonal_mult = np.outer(np.where(is_weekend, 1.0, 0.0), seasonal_boost) + 1.0

    # gentle trend over 3-year span (±10%)
    trend = 1.0 + np.linspace(-0.05, 0.05, n_days) + rng.normal(0, 0.01, n_days)
    trend_mult = np.broadcast_to(trend[:, None], (n_days, n_items))

    # AR(1) random walk per item
    sigma = anchor_arr * 0.04
    walks = np.zeros((n_days, n_items))
    walks[0] = rng.normal(0, sigma, n_items)
    for t in range(1, n_days):
        walks[t] = 0.85 * walks[t - 1] + rng.normal(0, sigma, n_items)

    # close price
    close = (anchor_arr * trend_mult * seasonal_mult * event_mult + walks).clip(min=0.1)
    open_p = np.vstack([anchor_arr[None, :], close[:-1]])
    high = np.maximum(open_p, close) * (1.0 + np.abs(rng.normal(0, 0.03, close.shape)))
    low = np.minimum(open_p, close) * (1.0 - np.abs(rng.normal(0, 0.03, close.shape)))
    low = np.clip(low, 0.01, None)
    avg = (open_p + close + high + low) / 4.0

    # volume: higher for common items, weekend boost on Consumable/Material
    base_lambda = (7 - rarities) * 50  # commons = ~300, mythics = ~50
    weekend_boost_vol = np.outer(np.where(is_weekend, 1.4, 1.0),
                                 np.where(np.isin(cats, ["Consumable", "Material"]), 1.0, 0.7))
    lam_vol = base_lambda * weekend_boost_vol
    volume = rng.poisson(lam_vol).astype(int)
    listings = (rng.poisson(np.clip(base_lambda * 0.2, 1, None), (n_days, n_items)) + 1).astype(int)

    # tile and stack
    date_grid = np.repeat(date_keys, n_items)
    item_grid = np.tile(item_keys, n_days)
    return pd.DataFrame({
        "DateKey": date_grid, "ItemKey": item_grid,
        "OpenPrice": np.round(open_p.flatten(), 2),
        "ClosePrice": np.round(close.flatten(), 2),
        "HighPrice": np.round(high.flatten(), 2),
        "LowPrice": np.round(low.flatten(), 2),
        "AvgPrice": np.round(avg.flatten(), 2),
        "Volume": volume.flatten(),
        "ListingsCount": listings.flatten(),
    })


# ──────────────────────────────────────────────────────────────────────────────
# FactTrade — sampled from price snapshot
# ──────────────────────────────────────────────────────────────────────────────
def build_fact_trade(rng: np.random.Generator, fact_price: pd.DataFrame,
                     dim_seller: pd.DataFrame, n_trades: int) -> pd.DataFrame:
    seller_keys = dim_seller["SellerKey"].values
    # weighted by volume so popular items see more trades
    weights = fact_price["Volume"].astype(float).values + 1.0
    weights = weights / weights.sum()
    idx = rng.choice(len(fact_price), size=n_trades, p=weights)
    chosen = fact_price.iloc[idx].reset_index(drop=True)
    qty = rng.integers(1, 21, n_trades)
    unit_price = np.round(chosen["AvgPrice"].values * rng.normal(1.0, 0.05, n_trades).clip(0.5, 1.5), 2)
    unit_price = np.clip(unit_price, 0.01, None)
    sellers = rng.choice(seller_keys, n_trades)
    buyers = rng.choice(seller_keys, n_trades)
    return pd.DataFrame({
        "TradeKey": range(1, n_trades + 1),
        "DateKey": chosen["DateKey"].values,
        "ItemKey": chosen["ItemKey"].values,
        "SellerKey": sellers, "BuyerSellerKey": buyers,
        "Quantity": qty, "UnitPrice": unit_price,
        "TotalPrice": np.round(qty * unit_price, 2),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ──────────────────────────────────────────────────────────────────────────────
def write_table(df: pd.DataFrame, out_dir: Path, name: str, big_to_parquet: bool, manifest: dict):
    if big_to_parquet:
        try:
            path = out_dir / f"{name}.parquet"
            df.to_parquet(path, index=False)
            manifest["tables"][name] = {"rows": int(len(df)), "file": path.name}
            print(f"  [ok] {name:30s} {len(df):>10,} rows -> {path.name}")
            return
        except Exception as e:
            print(f"  ! parquet failed ({e}); falling back to CSV")
    path = out_dir / f"{name}.csv"
    df.to_csv(path, index=False)
    manifest["tables"][name] = {"rows": int(len(df)), "file": path.name}
    print(f"  [ok] {name:30s} {len(df):>10,} rows -> {path.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=list(SCALES), default="smoke")
    ap.add_argument("--out", default=None, help="override output dir (default: outputs/<job>/latest)")
    ap.add_argument("--archive", action="store_true",
                    help="also snapshot this run to outputs/<job>/runs/<date>-<scale>/")
    args = ap.parse_args()

    cfg = SCALES[args.scale]
    seed = int((HERE / "seed.txt").read_text().strip())
    rng = np.random.default_rng(seed)
    print(f"[grand-exchange] scale={args.scale}  seed={seed}  cfg={cfg}")

    job_dir = DEFAULT_OUT_DIR / JOB
    out_dir = Path(args.out) if args.out else (job_dir / "latest")
    # clean latest/ so stale tables from a previous scale don't linger
    if out_dir.exists():
        for old in list(out_dir.glob("*.csv")) + list(out_dir.glob("*.parquet")) + list(out_dir.glob("_manifest.json")):
            old.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[grand-exchange] writing to: {out_dir}\n")

    # 1. dims (parents first)
    print("[1/6] dims")
    dim_rarity = build_dim_rarity()
    dim_region = build_dim_region(rng, cfg["N_REGIONS"])
    dim_seller = build_dim_seller(rng, cfg["N_SELLERS"])
    dim_monster = build_dim_monster(rng, cfg["N_MONSTERS"], cfg["N_REGIONS"])
    dim_date = build_dim_date(cfg["N_DAYS"])
    dim_item = build_dim_item(rng, cfg["N_ITEMS"], dim_rarity)

    categories = list(dim_item["ItemCategory"].unique())
    dim_event = build_dim_market_event(rng, cfg["N_EVENTS"], cfg["N_DAYS"], categories)

    # 2. recipes + BOM (modifies dim_item.IsCraftable)
    print("[2/6] recipes + BOM bridge")
    dim_recipe, fact_bom = build_recipes_and_bom(rng, dim_item)

    # 3. drop table + item-source bridges
    print("[3/6] drop table + item-source bridges")
    fact_drop = build_fact_drop_table(rng, dim_monster, dim_item)
    fact_item_src = build_fact_item_source(rng, dim_item)

    # 4. recursive craft cost roll-up → anchors
    print("[4/6] recursive craft cost roll-up")
    anchors = compute_craft_costs(dim_item, dim_recipe, fact_bom)

    # 5. price spine
    print(f"[5/6] FactMarketPriceDaily ({cfg['N_ITEMS']:,} items × {cfg['N_DAYS']:,} days = {cfg['N_ITEMS'] * cfg['N_DAYS']:,} rows)")
    fact_price = build_fact_market_price(rng, dim_item, dim_date, anchors, dim_event)

    # 6. trades (sampled from price)
    print(f"[6/6] FactTrade (~{cfg['N_TRADES']:,} rows)")
    fact_trade = build_fact_trade(rng, fact_price, dim_seller, cfg["N_TRADES"])

    # write
    print("\n[write]")
    big = args.scale == "full"
    manifest = {
        "job": JOB, "scale": args.scale, "seed": seed,
        "generated": date.today().isoformat(),
        "date_start": DATE_START.isoformat(),
        "date_end": (DATE_START + timedelta(days=cfg["N_DAYS"] - 1)).isoformat(),
        "config": cfg, "tables": {},
    }
    write_table(dim_rarity, out_dir, "DimRarity", False, manifest)
    write_table(dim_region, out_dir, "DimRegion", False, manifest)
    write_table(dim_seller, out_dir, "DimSeller", False, manifest)
    write_table(dim_monster, out_dir, "DimMonster", False, manifest)
    write_table(dim_date, out_dir, "DimDate", False, manifest)
    write_table(dim_event, out_dir, "DimMarketEvent", False, manifest)
    write_table(dim_item, out_dir, "DimItem", False, manifest)
    write_table(dim_recipe, out_dir, "DimRecipe", False, manifest)
    write_table(fact_bom, out_dir, "FactRecipeIngredient", False, manifest)
    write_table(fact_drop, out_dir, "FactDropTable", False, manifest)
    write_table(fact_item_src, out_dir, "FactItemSource", False, manifest)
    write_table(fact_price, out_dir, "FactMarketPriceDaily", big, manifest)
    write_table(fact_trade, out_dir, "FactTrade", big, manifest)

    (out_dir / "_manifest.json").write_text(json.dumps(manifest, indent=2, default=str))
    print(f"  [ok] {'_manifest.json':30s} {'(seed/scale/rows)':>17}")

    if args.archive:
        run_dir = job_dir / "runs" / f"{date.today():%Y-%m-%d}-{args.scale}"
        run_dir.mkdir(parents=True, exist_ok=True)
        for f in out_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, run_dir / f.name)
        print(f"\n[archive] snapshot -> {run_dir}")

    print(f"\n[done] {args.scale} generation complete -> {out_dir}")


if __name__ == "__main__":
    main()
