"""Build the 4x2 group card grid on Page 2 — Groups.

Each active card: header textbox (name + score + grade + contracts) over a
horizontal bar chart filtered to that group, showing 5 dimension bars.
Each idle card: gray placeholder textbox.

5 active groups present in the data: Mammoet, Nutreco, Kiwa, SHV Holdings, SHV Energy.
3 idle placeholders: Makro, NPM Capital, Corporate.
"""
import json, os

PAGE_DIR = "gddt.Report/definition/pages/02-Groups/visuals"

INK = "#15171C"; INK_2 = "#353841"; INK_3 = "#8F8E87"; INK_4 = "#C9C6BD"
PAPER = "#F7F5EF"; PAPER_2 = "#EBE8DF"; RULE = "#D8D5CC"
BAD = "#A23A2A"; WARN = "#B46C1A"; GOOD = "#2D6948"

# ── helpers ──
def lit(s): return {"expr": {"Literal": {"Value": s}}}
def lit_str(s): return lit(f"'{s}'")
def lit_bool(b): return lit("true" if b else "false")
def lit_num(n): return lit(f"{n}D")
def color(h): return {"solid": {"color": lit_str(h)}}

def write_textbox(name, pos, paragraphs, *, align="left", bg=None, padding=10):
    out_paras = []
    for runs in paragraphs:
        if not runs:
            out_paras.append({"textRuns": [{"value": ""}]}); continue
        tr = []
        for r in runs:
            run = {"value": r["value"]}
            style = r.get("style") or {}
            ts = {}
            for k in ("fontSize","fontFamily","color","letterSpacing"):
                if k in style: ts[k] = style[k]
            if style.get("bold"): ts["fontWeight"] = "bold"
            if style.get("italic"): ts["fontStyle"] = "italic"
            if ts: run["textStyle"] = ts
            tr.append(run)
        out_paras.append({"textRuns": tr, "horizontalTextAlignment": align})

    vco = {
        "title": [{"properties": {"show": lit_bool(False)}}],
        "subTitle": [{"properties": {"show": lit_bool(False)}}],
        "padding": [{"properties": {"top": lit_num(padding), "bottom": lit_num(padding), "left": lit_num(padding), "right": lit_num(padding)}}],
    }
    if bg:
        vco["background"] = [{"properties": {"show": lit_bool(True), "color": color(bg)}}]
    else:
        vco["background"] = [{"properties": {"show": lit_bool(False)}}]
    if bg:
        # subtle border for the card frame
        vco["border"] = [{"properties": {"show": lit_bool(True), "color": color(RULE), "radius": lit_num(0)}}]

    path = f"{PAGE_DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["visual"]["objects"] = {"general": [{"properties": {"paragraphs": out_paras}}]}
    v["visual"]["visualContainerObjects"] = vco
    v["position"]["x"] = pos[0]; v["position"]["y"] = pos[1]
    v["position"]["width"] = pos[2]; v["position"]["height"] = pos[3]
    v["position"]["z"] = pos[4] if len(pos) > 4 else 0
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

def reposition(name, x, y, w, h, z=0):
    path = f"{PAGE_DIR}/{name}/visual.json"
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["position"]["x"] = x; v["position"]["y"] = y
    v["position"]["width"] = w; v["position"]["height"] = h
    v["position"]["z"] = z
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

def add_group_filter(visual_name, group_name):
    """Add visual-level filter pinning to a single group."""
    path = f"{PAGE_DIR}/{visual_name}/visual.json"
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    fc = {
        "filters": [{
            "name": f"Filter_group_{group_name.replace(' ','_')}",
            "type": "Categorical",
            "field": {
                "Column": {
                    "Expression": {"SourceRef": {"Entity": "expected"}},
                    "Property": "group"
                }
            },
            "filter": {
                "Version": 2,
                "From": [{"Name": "e", "Entity": "expected", "Type": 0}],
                "Where": [{
                    "Condition": {
                        "In": {
                            "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "group"}}],
                            "Values": [[{"Literal": {"Value": f"'{group_name}'"}}]]
                        }
                    }
                }]
            },
            "howCreated": "User"
        }]
    }
    v["filterConfig"] = fc
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

def style_bar_chart(visual_name):
    """Minimal styling — hide title, clean background."""
    path = f"{PAGE_DIR}/{visual_name}/visual.json"
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["visual"].setdefault("visualContainerObjects", {})
    v["visual"]["visualContainerObjects"].update({
        "title": [{"properties": {"show": lit_bool(False)}}],
        "background": [{"properties": {"show": lit_bool(False)}}],
        "border": [{"properties": {"show": lit_bool(False)}}],
        "padding": [{"properties": {"top": lit_num(2), "bottom": lit_num(2), "left": lit_num(8), "right": lit_num(8)}}],
    })
    # Hide chart's own legend (we use the dimension labels per bar)
    v["visual"].setdefault("objects", {})
    v["visual"]["objects"]["legend"] = [{"properties": {"show": lit_bool(False)}}]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)

# ── layout: 4 cols × 2 rows on a 1320-wide page ──
CARD_W = 318
CARD_H = 230
HDR_H = 60
BAR_H = CARD_H - HDR_H
GAP = 8
MARGIN_X = 30
CARDS_TOP = 180  # below the existing filter bar at y=110-154

# Hide existing scorecards (we're replacing it with the grid)
reposition("group-scorecards", 0, 0, 1, 1, z=-1)

# Move freq + overdue down to make room
reposition("freq-status", 30, 690, 800, 280)
reposition("group-overdue", 850, 690, 440, 280)

# Card slot positions
def slot_xy(col, row):
    x = MARGIN_X + col * (CARD_W + GAP)
    y = CARDS_TOP + row * (CARD_H + GAP)
    return x, y

# ── ACTIVE group card data ──
active = [
    # (slug, display_name, group_filter_value, contracts, expected_count, score, grade)
    ("mammoet",      "Mammoet",      "Mammoet",        6,  72, 42, "D"),
    ("nutreco",      "Nutreco",      "Nutreco",       31, 372, 39, "F"),
    ("kiwa",         "Kiwa",         "Kiwa",          31, 372, 36, "F"),
    ("shv-holdings", "SHV Holdings", "SHV Holdings",  30, 360, 31, "F"),
    ("shv-energy",   "SHV Energy",   "SHV Energy",     6,  72,  0, "F"),
]

grade_color_map = {"A": GOOD, "B": GOOD, "C": WARN, "D": WARN, "F": BAD}

positions = [(0,0),(1,0),(2,0),(3,0),(0,1)]  # row1: 4 cards, row2: 1 card + 3 idle

for (slug, name, group_filter, contracts, expected, score, grade), (col, row) in zip(active, positions):
    x, y = slot_xy(col, row)

    # Header textbox
    grade_color = grade_color_map.get(grade, INK_3)
    write_textbox(
        f"card-{slug}-hdr",
        (x, y, CARD_W, HDR_H, 2),
        [
            [
                {"value": name, "style": {"fontSize": "16pt", "fontFamily": "Georgia", "color": INK}},
                {"value": "                          ", "style": {"fontSize": "10pt"}},
                {"value": str(score), "style": {"fontSize": "26pt", "fontFamily": "Georgia", "color": INK, "bold": True}},
                {"value": "  ", "style": {"fontSize": "10pt"}},
                {"value": f" {grade} ", "style": {"fontSize": "11pt", "fontFamily": "Georgia", "color": PAPER, "bold": True}},
            ],
            [
                {"value": f"{contracts} contracts  ·  {expected} expected", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
            ],
        ],
        bg=PAPER, padding=12,
    )

    # Position bar chart underneath
    bar_y = y + HDR_H
    reposition(f"card-{slug}-bars", x, bar_y, CARD_W, BAR_H, z=1)
    style_bar_chart(f"card-{slug}-bars")
    add_group_filter(f"card-{slug}-bars", group_filter)

# ── IDLE group placeholders ──
idle = [
    ("makro",    "Makro",       "no contracts assigned"),
    ("npm",      "NPM Capital", "no contracts assigned"),
    ("corporate","Corporate",   "no contracts assigned"),
]
idle_positions = [(1,1),(2,1),(3,1)]

for (slug, name, sub), (col, row) in zip(idle, idle_positions):
    x, y = slot_xy(col, row)
    write_textbox(
        f"card-{slug}-idle",
        (x, y, CARD_W, CARD_H, 2),
        [
            [
                {"value": name, "style": {"fontSize": "16pt", "fontFamily": "Georgia", "color": INK_3}},
                {"value": "                          ", "style": {"fontSize": "10pt"}},
                {"value": "—", "style": {"fontSize": "26pt", "fontFamily": "Georgia", "color": INK_4}},
            ],
            [{"value": sub, "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}}],
            [{"value": "", "style": {"fontSize": "12pt"}}],
            [{"value": "Idle group  ·  awaiting onboarding.", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}}],
        ],
        bg=PAPER, padding=12,
    )

# Resize page if needed — content runs to y=180+2*(230+8)=656, then freq table to 970
# Current page is 1100 tall — plenty of room.

# Update the section label position for "WHERE THE GAP IS"
reposition("g-sec-where", 30, 670, 1260, 24)
reposition("freq-status", 30, 700, 800, 290)
reposition("group-overdue", 850, 700, 440, 290)
reposition("g-footnote", 30, 1010, 1260, 70)

print("done — 5 active cards + 3 idle placeholders built")
