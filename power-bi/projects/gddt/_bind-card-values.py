"""Bind live measure values into the Group card headers.

Strips the hardcoded text from card-{group}-hdr (now only shows the group name),
then adds three measure-bound card visuals per group:
  - card-{group}-score  → [Score]   (big number)
  - card-{group}-grade  → [Grade]   (A-F chip)
  - card-{group}-meta   → [Card Meta] (contracts · expected)
"""
import json, os

PAGE_DIR = "gddt.Report/definition/pages/02-Groups/visuals"

active = [
    ("mammoet",      "Mammoet",      (0, 0)),
    ("nutreco",      "Nutreco",      (1, 0)),
    ("kiwa",         "Kiwa",         (2, 0)),
    ("shv-holdings", "SHV Holdings", (3, 0)),
    ("shv-energy",   "SHV Energy",   (0, 1)),
]

CARD_W = 318; CARD_H = 230; HDR_H = 60
GAP = 8; MARGIN_X = 30; CARDS_TOP = 180

def slot_xy(col, row):
    return MARGIN_X + col * (CARD_W + GAP), CARDS_TOP + row * (CARD_H + GAP)

def lit(s): return {"expr": {"Literal": {"Value": s}}}
def lit_str(s): return lit(f"'{s}'")
def lit_bool(b): return lit("true" if b else "false")
def lit_num(n): return lit(f"{n}D")

def write_json(path, v):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

def measure_field(prop):
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Entity": "_Measures"}},
            "Property": prop,
        }
    }

def group_filter(group_value):
    return {
        "filters": [{
            "name": f"Filter_group_{group_value.replace(' ', '_')}",
            "type": "Categorical",
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "expected"}}, "Property": "group"}},
            "filter": {
                "Version": 2,
                "From": [{"Name": "e", "Entity": "expected", "Type": 0}],
                "Where": [{
                    "Condition": {
                        "In": {
                            "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "group"}}],
                            "Values": [[{"Literal": {"Value": f"'{group_value}'"}}]],
                        }
                    }
                }],
            },
            "howCreated": "User",
        }]
    }

def strip_header_textbox(slug, group_name, x, y):
    """Reduce header textbox to just the group name on the left, no hardcoded values."""
    path = f"{PAGE_DIR}/card-{slug}-hdr/visual.json"
    with open(path, "r", encoding="utf-8") as f:
        v = json.load(f)
    # Replace paragraphs with just the group name
    v["visual"]["objects"]["general"] = [{
        "properties": {
            "paragraphs": [{
                "textRuns": [{
                    "value": group_name,
                    "textStyle": {
                        "fontSize": "16pt",
                        "fontFamily": "Georgia",
                        "color": "#15171C",
                    },
                }],
                "horizontalTextAlignment": "left",
            }]
        }
    }]
    write_json(path, v)

def card_visual(name, measure_prop, x, y, w, h, *, value_font=26, value_color="#15171C",
                value_bold=True, value_family="Georgia", value_align="left",
                bg_color=None, group_value=None, z=3):
    """Generic single-measure card visual."""
    value_props = {
        "fontSize": lit_num(value_font),
        "color": {"solid": {"color": lit_str(value_color)}},
        "fontFamily": lit_str(value_family),
        "bold": lit_bool(value_bold),
        "horizontalAlignment": lit_str(value_align),
    }

    vc_objects = {
        "title": [{"properties": {"show": lit_bool(False)}}],
        "background": [{"properties": {"show": lit_bool(False)}}],
        "border": [{"properties": {"show": lit_bool(False)}}],
        "padding": [{"properties": {
            "top": lit_num(0), "bottom": lit_num(0),
            "left": lit_num(0), "right": lit_num(0),
        }}],
    }
    if bg_color:
        vc_objects["background"] = [{"properties": {
            "show": lit_bool(True),
            "color": {"solid": {"color": lit_str(bg_color)}},
        }}]

    v = {
        "name": name,
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [{
                            "queryRef": f"_Measures.{measure_prop}",
                            "field": measure_field(measure_prop),
                            "nativeQueryRef": measure_prop,
                        }]
                    }
                }
            },
            "objects": {
                "labels": [{"properties": value_props}],
                "categoryLabels": [{"properties": {"show": lit_bool(False)}}],
            },
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": vc_objects,
        },
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": 0},
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
    }
    if group_value:
        v["filterConfig"] = group_filter(group_value)

    path = f"{PAGE_DIR}/{name}/visual.json"
    write_json(path, v)

for slug, group_value, (col, row) in active:
    x, y = slot_xy(col, row)
    # 1) Strip header textbox
    strip_header_textbox(slug, group_value, x, y)

    # 2) Score card — top right, big number
    card_visual(
        f"card-{slug}-score",
        "Score",
        x=x + 170, y=y + 4, w=80, h=42,
        value_font=24, value_bold=True, value_align="right",
        group_value=group_value, z=3,
    )

    # 3) Grade chip — far right, dark badge
    card_visual(
        f"card-{slug}-grade",
        "Grade",
        x=x + 260, y=y + 12, w=42, h=28,
        value_font=14, value_bold=True, value_align="center",
        value_color="#F7F5EF", bg_color="#15171C",
        group_value=group_value, z=4,
    )

    # 4) Meta line — second row, small Consolas-like
    card_visual(
        f"card-{slug}-meta",
        "Card Meta",
        x=x + 12, y=y + 36, w=240, h=20,
        value_font=9, value_bold=False, value_align="left",
        value_color="#8F8E87", value_family="Consolas",
        group_value=group_value, z=3,
    )

    print(f"  bound card values for {slug}")

print("done.")
