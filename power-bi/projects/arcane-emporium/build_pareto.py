"""Add the item Pareto to page 3 from the recipe's own template.

The recipe lives at 02-build/recipes/pareto-chart. Its whole point is that the cumulative line
is a VISUAL calculation - RUNNINGSUM([share], ORDERBY([value], DESC)) - so the model needs no
rank column and no cumulative measure, and the line stays correct even if the reader re-sorts
the axis. Substituting the shipped template rather than hand-writing the JSON keeps that intact:
the formatting selectors key off the queryRef aliases select..select4 in projection order, and
one transposed alias breaks the colour split silently.
"""
import io
import json
import os

from emporiumkit import GOLD, INK, INK3, IRON, PAGES, rects, stack

RECIPE = (r"e:\Workspace-Blueprint\power-bi\02-build\recipes\pareto-chart"
          r"\templates\pareto-combo.visual.json")

hero = rects("items_hero")[0]
_, body = stack(hero, sub=True)

TOKENS = {
    "<VISUAL_NAME_CHART>": "itemPareto",
    "<CHART_X>": str(body["x"]),
    "<CHART_Y>": str(body["y"]),
    "<CHART_Z>": "200",
    "<CHART_WIDTH>": str(body["width"]),
    "<CHART_HEIGHT>": str(body["height"]),
    "<CHART_TAB_ORDER>": "5",
    "<CATEGORY_TABLE>": "DimItem",
    "<CATEGORY_COLUMN>": "Item",
    "<MEASURE_TABLE>": "_Measures",
    "<VALUE_MEASURE>": "Total Gold",
    "<THRESHOLD>": "0.8",
    # not green/red: the split here is "these wares carry the shop" vs "these do not", which is
    # not a good/bad judgement. Forge gold for the vital few, iron for the tail.
    "<VITAL_COLOR>": GOLD,
    "<TRIVIAL_COLOR>": IRON,
    "<VITAL_LABEL_COLOR>": INK,
    "<TRIVIAL_LABEL_COLOR>": INK3,
}

src = io.open(RECIPE, encoding="utf-8").read()
for k, v in TOKENS.items():
    src = src.replace(k, v)
assert "<" not in src.replace("<", "<", 1) or "><" not in src, "unsubstituted token remains"
left = [t for t in TOKENS if t in src]
assert not left, "unsubstituted: %s" % left

obj = json.loads(src)          # proves the substitution produced valid JSON
out = os.path.join(PAGES, "Items", "visuals", "itemPareto")
os.makedirs(out, exist_ok=True)
with io.open(os.path.join(out, "visual.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(obj, f, indent=2)
    f.write("\n")
print("pareto written at %(x)d,%(y)d %(width)dx%(height)d" % body)
