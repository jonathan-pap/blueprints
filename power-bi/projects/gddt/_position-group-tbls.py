"""Position + filter + style the 5 tableEx cards on Page 2."""
import json, os

PAGE_DIR = "gddt.Report/definition/pages/02-Groups/visuals"

def lit(s): return {"expr": {"Literal": {"Value": s}}}
def lit_str(s): return lit(f"'{s}'")
def lit_bool(b): return lit("true" if b else "false")
def lit_num(n): return lit(f"{n}D")

def reposition(name, x, y, w, h, z=0):
    path = f"{PAGE_DIR}/{name}/visual.json"
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["position"]["x"] = x; v["position"]["y"] = y
    v["position"]["width"] = w; v["position"]["height"] = h
    v["position"]["z"] = z
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

def style_tbl(name):
    path = f"{PAGE_DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["visual"].setdefault("visualContainerObjects", {})
    v["visual"]["visualContainerObjects"].update({
        "title": [{"properties": {"show": lit_bool(False)}}],
        "background": [{"properties": {"show": lit_bool(False)}}],
        "border": [{"properties": {"show": lit_bool(False)}}],
        "padding": [{"properties": {"top": lit_num(2), "bottom": lit_num(2), "left": lit_num(10), "right": lit_num(10)}}],
    })
    # Hide column headers, totals
    v["visual"].setdefault("objects", {})
    v["visual"]["objects"]["columnHeaders"] = [{"properties": {"show": lit_bool(False)}}]
    v["visual"]["objects"]["total"] = [{"properties": {"show": lit_bool(False)}}]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

def filter_to_group(name, group_value):
    path = f"{PAGE_DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["filterConfig"] = {
        "filters": [{
            "name": f"Filter_group_{group_value.replace(' ','_')}",
            "type": "Categorical",
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "expected"}}, "Property": "group"}},
            "filter": {
                "Version": 2,
                "From": [{"Name": "e", "Entity": "expected", "Type": 0}],
                "Where": [{
                    "Condition": {
                        "In": {
                            "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "group"}}],
                            "Values": [[{"Literal": {"Value": f"'{group_value}'"}}]]
                        }
                    }
                }]
            },
            "howCreated": "User"
        }]
    }
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

# Same slot grid as before
CARD_W = 318; CARD_H = 230; HDR_H = 60; BAR_H = CARD_H - HDR_H
GAP = 8; MARGIN_X = 30; CARDS_TOP = 180

def slot_xy(col, row):
    return MARGIN_X + col * (CARD_W + GAP), CARDS_TOP + row * (CARD_H + GAP)

active = [
    ("mammoet",      "Mammoet",      (0,0)),
    ("nutreco",      "Nutreco",      (1,0)),
    ("kiwa",         "Kiwa",         (2,0)),
    ("shv-holdings", "SHV Holdings", (3,0)),
    ("shv-energy",   "SHV Energy",   (0,1)),
]

for slug, group_value, (col, row) in active:
    x, y = slot_xy(col, row)
    bar_y = y + HDR_H
    name = f"card-{slug}-tbl"
    reposition(name, x, bar_y, CARD_W, BAR_H, z=1)
    style_tbl(name)
    filter_to_group(name, group_value)
    print(f"  positioned + filtered {name}")

print("done.")
