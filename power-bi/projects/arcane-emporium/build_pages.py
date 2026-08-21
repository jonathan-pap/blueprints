"""Build the four Arcane Emporium pages.

Page order follows the grains of the star: the chain, then where (shops), then what (items),
then who (patrons). Every rect comes from design-system.yaml via resolve_layout - nothing here
is hand-placed.
"""
import json
import os

from emporiumkit import (BLUE, BRONZE, CRIMSON, FOREST, GOLD, INK, INK2, INK3, IRON, PLUM,
                         RULE, SURFACE, VERD, add_page, axis, bars, col, head_tb, kpi, lit,
                         measure, noframe, page_chrome, proj_c, proj_m, rects, solid, sort_by,
                         stack, table, textbox, ts, vis, write)

FACT, M = "FactSales", "_Measures"


def mref(name):
    return measure(name)


def cref(entity, prop):
    return col(entity, prop)


# ======================================================= PAGE 1 — Overview
d = add_page("Overview", "Emporium Overview")
page_chrome(d, "The Arcane Emporium",
            "Eight shops, three realms, four years of Gold · 25.0M across 99,374 sale "
            "lines, every share pinned by the generator")

k = rects("kpi_hero_plus_4")
kpi(d, "kpiGold", k[0], "Total Gold", "Gold taken", GOLD, "40D",
    units="1000000D", prec="2D")
# NOT [Gold YoY %]: at the all-years grain SAMEPERIODLASTYEAR compares 2023-2026 against
# 2023-2025 and reports +41.6%, which is arithmetic rather than growth. [Gold YoY % Latest]
# always answers "how did the most recent year do".
kpi(d, "kpiYoY", k[1], "Gold YoY % Latest", "Growth, latest year", FOREST, "28D")
kpi(d, "kpiUnits", k[2], "Total Units", "Items sold", INK, "28D", units="1000D", prec="1D")
kpi(d, "kpiTxn", k[3], "Transactions", "Sale lines", INK, "28D", units="1000D", prec="1D")
kpi(d, "kpiAvg", k[4], "Avg Sale", "Gold per sale", INK, "28D")

# ---- the four-year trend -------------------------------------------------
# Columns are the monthly take, the line is the trailing 3-month mean. The Frostfall spike is
# the whole point of the chart, and a spike only reads as a spike against something smooth.
t = rects("overview_trend")[0]
h, c = stack(t, sub=True)
write(d, "trendH", head_tb("trendH", h, "Gold by month, and the trend underneath it",
                           "columns are the month's take · the line is a trailing 3-month "
                           "mean · every Nov–Dec is the Frostfall festival"))
write(d, "trendCombo", vis("trendCombo", "lineClusteredColumnComboChart", c, 200,
    query={"Category": {"projections": [proj_c("DimDate", "MonthYear")]},
           "Y": {"projections": [proj_m("Total Gold")]},
           "Y2": {"projections": [proj_m("Gold 3M Avg")]}},
    objects={"dataPoint": [{"properties": {"fill": solid(IRON)}}],
             "categoryAxis": axis(True, INK3, {"concatenateLabels": lit("false")}),
             "valueAxis": axis(True, INK3, {
                 "secShow": lit("true"), "secShowAxisTitle": lit("false"),
                 "secLabelColor": solid(INK3), "secFontSize": lit("9D")}),
             "lineStyles": [{"properties": {"strokeWidth": lit("3D"),
                                            "lineStyle": lit("'solid'")}}],
             "y1AccentColor": [{"properties": {"fill": solid(GOLD)}}],
             "legend": [{"properties": {"show": lit("false")}}],
             "labels": [{"properties": {"show": lit("false")}}]},
    vco=noframe()))

# ---- the two splits ------------------------------------------------------
s = rects("overview_split")
h, c = stack(s[0])
write(d, "realmH", head_tb("realmH", h, "Gold by realm"))
write(d, "realmBar", sort_by(
    bars("realmBar", c, "DimShop", "Realm", "Total Gold", fill_measure="Realm Colour"),
    mref("Total Gold"), "Descending"))

h, c = stack(s[1])
write(d, "catH", head_tb("catH", h, "Gold by category of ware"))
# vertical: five horizontal bars do not fit a 128px body, and dropping the fifth silently
# is the one thing a category breakdown must never do
write(d, "catBar", sort_by(
    bars("catBar", c, "DimItem", "Category", "Total Gold", fill_measure="Category Colour",
         horizontal=False),
    mref("Total Gold"), "Descending"))

print("page 1 built")

# ======================================================= PAGE 2 — Realms
d = add_page("Realms", "Realms & Shops")
page_chrome(d, "Realms & Shops",
            "Where the Gold comes from · no map, because the realms are invented — a "
            "league table says the same thing without pretending Silverhaven has coordinates")

r = rects("realms_body")
h, c = stack(r[0], sub=True)
write(d, "shopH", head_tb("shopH", h, "Every shop, ranked",
                          "bar colour is the realm · Eldoria blue, Grimmwald plum, "
                          "Sunspire gold"))
write(d, "shopBar", sort_by(
    bars("shopBar", c, "DimShop", "Shop", "Total Gold", fill_measure="Realm Colour"),
    mref("Total Gold"), "Descending"))

h, c = stack(r[1], sub=True)
write(d, "leagueH", head_tb("leagueH", h, "The shop ledger",
                            "share re-bases to whatever the header slicers have selected, so "
                            "it always reads as a share of what you are looking at"))
write(d, "leagueTable", sort_by(table("leagueTable", c, [
    proj_c("DimShop", "Shop"),
    proj_c("DimShop", "Realm"),
    proj_c("DimShop", "City"),
    proj_m("Total Gold", "Gold"),
    proj_m("Gold Share of Total", "Share"),
    proj_m("Gold YoY % Latest", "YoY"),
    proj_m("Total Units", "Units"),
    proj_m("Avg Sale", "Avg sale"),
]), mref("Total Gold"), "Descending"))

print("page 2 built")

# ======================================================= PAGE 3 — Items
# The pareto is the recipe at 02-build/recipes/pareto-chart - a sorted combo whose cumulative
# line is built from VISUAL calculations, so the model stays untouched. Written by
# build_pareto.py, which substitutes the recipe's own template rather than reinventing it.
d = add_page("Items", "The Ledger of Wares")
page_chrome(d, "The Ledger of Wares",
            "What actually sells · 24 wares, five categories, and a very long tail")

hero = rects("items_hero")[0]
h, _ = stack(hero, sub=True)
write(d, "paretoH", head_tb("paretoH", h, "The vital few — which wares carry the takings",
                            "bars are Gold, the line is the running share · gold up to the "
                            "80% mark, iron beyond it · sorted by value, and the cumulative "
                            "stays correct even if you re-sort"))

strip = rects("items_strip")[0]
h, c = stack(strip, sub=True)
write(d, "wareH", head_tb("wareH", h, "Every ware, with its place in the tail",
                          "share is of the current selection, not the whole four years"))
write(d, "wareTable", sort_by(table("wareTable", c, [
    proj_c("DimItem", "Item", "Ware"),
    proj_c("DimItem", "Category"),
    proj_m("Total Gold", "Gold"),
    proj_m("Gold Share of Total", "Share"),
    proj_m("Total Units", "Units"),
    proj_m("Avg Item Price", "Avg price"),
    proj_m("Gold YoY % Latest", "YoY"),
]), mref("Total Gold"), "Descending"))

print("page 3 built (pareto added by build_pareto.py)")

# ======================================================= PAGE 4 — Patrons
d = add_page("Patrons", "Patrons")
page_chrome(d, "Patrons of the Emporium",
            "Twenty named buyers in four kinds · adventurers, collectors, guilds and nobles")

p = rects("patrons_two")
h, c = stack(p[0], sub=True)
write(d, "typeH", head_tb("typeH", h, "Gold by kind of patron",
                          "pinned by the generator at 40 / 25 / 20 / 15"))
write(d, "typeBar", sort_by(
    bars("typeBar", c, "DimCustomer", "CustomerType", "Total Gold", colour=BLUE),
    mref("Total Gold"), "Descending"))

h, c = stack(p[1], sub=True)
write(d, "purseH", head_tb("purseH", h, "Average purse by kind",
                           "Gold per sale line · this tracks the pinned Gold share, "
                           "because every patron visits about as often as every other"))
write(d, "purseBar", sort_by(
    bars("purseBar", c, "DimCustomer", "CustomerType", "Avg Sale", colour=VERD),
    mref("Avg Sale"), "Descending"))

b = rects("patrons_body")[0]
h, c = stack(b, sub=True)
write(d, "bigH", head_tb("bigH", h, "The big spenders",
                         "all twenty patrons · the generator ranks big spenders first "
                         "within each kind, so the pareto runs inside the type, not across it"))
write(d, "bigTable", sort_by(table("bigTable", c, [
    proj_c("DimCustomer", "Customer", "Patron"),
    proj_c("DimCustomer", "CustomerType", "Kind"),
    proj_m("Total Gold", "Gold"),
    proj_m("Gold Share of Total", "Share"),
    proj_m("Transactions", "Visits"),
    proj_m("Avg Sale", "Avg purse"),
    proj_m("Total Units", "Units"),
]), mref("Total Gold"), "Descending"))

print("page 4 built")
