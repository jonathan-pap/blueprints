"""Validate a generated grand-exchange dataset against schema.md business rules.

Usage: python validate.py [dataset-dir]
   default dir: ../../outputs/grand-exchange/latest
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_DIR = HERE.parent.parent / "outputs" / "grand-exchange" / "latest"

TABLES = ["DimRarity", "DimRegion", "DimSeller", "DimMonster", "DimDate",
          "DimMarketEvent", "DimItem", "DimRecipe", "FactRecipeIngredient",
          "FactDropTable", "FactItemSource", "FactMarketPriceDaily", "FactTrade"]


def load(d: Path) -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    for t in TABLES:
        csv = d / f"{t}.csv"
        pq = d / f"{t}.parquet"
        if pq.exists():
            out[t] = pd.read_parquet(pq)
        elif csv.exists():
            out[t] = pd.read_csv(csv)
        else:
            print(f"MISSING: {t} (looked in {d})")
            sys.exit(2)
    return out


def check(label: str, ok: bool, detail: str = ""):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}{(' :: ' + detail) if detail else ''}")
    return ok


def main():
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    print(f"[validate] dir: {data_dir}\n")
    d = load(data_dir)
    failures = 0

    print("[1] Referential integrity")
    items = set(d["DimItem"]["ItemKey"])
    dates = set(d["DimDate"]["DateKey"])
    sellers = set(d["DimSeller"]["SellerKey"])
    monsters = set(d["DimMonster"]["MonsterKey"])
    rarities = set(d["DimRarity"]["RarityKey"])
    regions = set(d["DimRegion"]["RegionKey"])
    recipes = set(d["DimRecipe"]["RecipeKey"])

    ri_checks = [
        ("DimItem.RarityKey  -> DimRarity", set(d["DimItem"]["RarityKey"]) <= rarities),
        ("DimMonster.RegionKey -> DimRegion", set(d["DimMonster"]["RegionKey"]) <= regions),
        ("DimRecipe.OutputItemKey -> DimItem", set(d["DimRecipe"]["OutputItemKey"]) <= items),
        ("FactRecipeIngredient.RecipeKey -> DimRecipe", set(d["FactRecipeIngredient"]["RecipeKey"]) <= recipes),
        ("FactRecipeIngredient.IngredientItemKey -> DimItem", set(d["FactRecipeIngredient"]["IngredientItemKey"]) <= items),
        ("FactDropTable.MonsterKey -> DimMonster", set(d["FactDropTable"]["MonsterKey"]) <= monsters),
        ("FactDropTable.ItemKey -> DimItem", set(d["FactDropTable"]["ItemKey"]) <= items),
        ("FactItemSource.ItemKey -> DimItem", set(d["FactItemSource"]["ItemKey"]) <= items),
        ("FactMarketPriceDaily.DateKey -> DimDate", set(d["FactMarketPriceDaily"]["DateKey"]) <= dates),
        ("FactMarketPriceDaily.ItemKey -> DimItem", set(d["FactMarketPriceDaily"]["ItemKey"]) <= items),
        ("FactTrade.DateKey -> DimDate", set(d["FactTrade"]["DateKey"]) <= dates),
        ("FactTrade.ItemKey -> DimItem", set(d["FactTrade"]["ItemKey"]) <= items),
        ("FactTrade.SellerKey -> DimSeller", set(d["FactTrade"]["SellerKey"]) <= sellers),
        ("FactTrade.BuyerSellerKey -> DimSeller", set(d["FactTrade"]["BuyerSellerKey"]) <= sellers),
    ]
    for label, ok in ri_checks:
        if not check(label, ok):
            failures += 1

    print("\n[2] OHLC integrity (Low <= Open/Close <= High, all >= 0)")
    fp = d["FactMarketPriceDaily"]
    failures += not check("Low <= Open", (fp["LowPrice"] <= fp["OpenPrice"] + 0.01).all(),
                          f"{(fp['LowPrice'] > fp['OpenPrice'] + 0.01).sum()} violations")
    failures += not check("Low <= Close", (fp["LowPrice"] <= fp["ClosePrice"] + 0.01).all(),
                          f"{(fp['LowPrice'] > fp['ClosePrice'] + 0.01).sum()} violations")
    failures += not check("High >= Open", (fp["HighPrice"] >= fp["OpenPrice"] - 0.01).all(),
                          f"{(fp['HighPrice'] < fp['OpenPrice'] - 0.01).sum()} violations")
    failures += not check("High >= Close", (fp["HighPrice"] >= fp["ClosePrice"] - 0.01).all(),
                          f"{(fp['HighPrice'] < fp['ClosePrice'] - 0.01).sum()} violations")
    failures += not check("All prices >= 0", (fp[["OpenPrice", "ClosePrice", "HighPrice", "LowPrice", "AvgPrice"]] >= 0).all().all())
    failures += not check("Volume >= 0", (fp["Volume"] >= 0).all())
    failures += not check("ListingsCount > 0", (fp["ListingsCount"] > 0).all())

    print("\n[3] BomTier monotonicity (ingredient tier < output tier)")
    bom = d["FactRecipeIngredient"].merge(
        d["DimRecipe"][["RecipeKey", "OutputItemKey"]], on="RecipeKey")
    bom = bom.merge(d["DimItem"][["ItemKey", "BomTier"]].rename(
        columns={"ItemKey": "OutputItemKey", "BomTier": "OutTier"}), on="OutputItemKey")
    bom = bom.merge(d["DimItem"][["ItemKey", "BomTier"]].rename(
        columns={"ItemKey": "IngredientItemKey", "BomTier": "IngTier"}), on="IngredientItemKey")
    violations = bom[bom["IngTier"] >= bom["OutTier"]]
    failures += not check("All ingredient tiers < output tier", len(violations) == 0,
                          f"{len(violations)} violations")

    print("\n[4] Element/Potency nullability")
    di = d["DimItem"]
    failures += not check(
        "Element non-null only on Material/Crystal",
        ((di["Element"].notna()) <= di["ItemCategory"].isin(["Material", "Crystal"])).all(),
        f"{((di['Element'].notna()) & ~di['ItemCategory'].isin(['Material', 'Crystal'])).sum()} violations")
    failures += not check(
        "Potency non-null only on Crystal",
        ((di["Potency"].notna()) <= (di["ItemCategory"] == "Crystal")).all())

    print("\n[5] Primary acquisition (exactly one per item)")
    primary_counts = d["FactItemSource"].groupby("ItemKey")["PrimaryFlag"].sum()
    failures += not check(
        "Exactly 1 primary per item",
        (primary_counts == 1).all(),
        f"{(primary_counts != 1).sum()} items with != 1 primary")

    print("\n[6] Trade pricing math")
    ft = d["FactTrade"]
    diff = (ft["Quantity"] * ft["UnitPrice"] - ft["TotalPrice"]).abs()
    failures += not check("TotalPrice == Quantity * UnitPrice (+/- 0.05)",
                          (diff <= 0.05).all(),
                          f"max diff = {diff.max():.4f}")

    print("\n[7] Recipe cost coherence (loose: AvgPrice within [-50%, +200%] of craft cost)")
    # spot-check: for craftable items, average AvgPrice vs recursive craft cost
    craftable_items = di[di["IsCraftable"]]["ItemKey"]
    avg_by_item = d["FactMarketPriceDaily"].groupby("ItemKey")["AvgPrice"].mean()
    # rebuild anchors (mirror generator logic) — re-import lazily
    sys.path.insert(0, str(HERE))
    from generate import compute_craft_costs
    anchors = compute_craft_costs(d["DimItem"], d["DimRecipe"], d["FactRecipeIngredient"])
    coherent = 0
    incoherent = 0
    for ik in craftable_items:
        if ik not in avg_by_item.index:
            continue
        avg = avg_by_item[ik]
        anchor = anchors[int(ik)]
        ratio = avg / anchor if anchor > 0 else 0
        if 0.5 <= ratio <= 3.0:
            coherent += 1
        else:
            incoherent += 1
    total = coherent + incoherent
    pct = 100.0 * coherent / total if total else 0
    failures += not check(
        f"Craft-vs-buy coherence ({pct:.1f}% within loose band)",
        pct >= 70.0,
        f"{coherent}/{total} craftable items priced within [0.5x, 3.0x] of recursive cost")

    print(f"\n[summary] failures = {failures}")
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
