"""One-shot script to rebuild 01-Summary page layout in editorial style.
Run from gddt project dir: python _restyle-summary.py"""
import json, os

PAGE_DIR = "gddt.Report/definition/pages/01-Summary/visuals"

# ── color palette (editorial paper/ink) ────────────────────────────────────
INK      = "#15171C"
INK_2    = "#353841"
INK_3    = "#8F8E87"
PAPER    = "#F7F5EF"
PAPER_2  = "#EBE8DF"
RULE     = "#D8D5CC"
GOOD     = "#2D6948"
BAD      = "#A23A2A"
WARN     = "#B46C1A"

def lit(s):
    return {"expr": {"Literal": {"Value": s}}}

def lit_str(s):
    # Power BI Literal.Value for strings is wrapped in single quotes; numbers/bools not
    return lit(f"'{s}'")

def lit_bool(b):
    return lit("true" if b else "false")

def lit_num(n):
    return lit(f"{n}D")

def hex_color(h):
    return {"solid": {"color": lit_str(h)}}

def build_container(title=False, bg=None, border=False, padding=8, shadow=False):
    """visualContainerObjects with sensible defaults: hide title, optional bg, no border/shadow."""
    out = {
        "title": [{"properties": {"show": lit_bool(title)}}],
        "subTitle": [{"properties": {"show": lit_bool(False)}}],
        "border": [{"properties": {"show": lit_bool(border)}}],
        "dropShadow": [{"properties": {"show": lit_bool(shadow)}}],
        "padding": [{"properties": {
            "top": lit_num(padding), "bottom": lit_num(padding),
            "left": lit_num(padding), "right": lit_num(padding),
        }}],
    }
    if bg is not None:
        out["background"] = [{"properties": {
            "show": lit_bool(True),
            "color": hex_color(bg),
        }}]
    else:
        out["background"] = [{"properties": {"show": lit_bool(False)}}]
    return out

def textbox(text_runs_per_paragraph, *, align="left", bg=None, padding=8):
    """
    text_runs_per_paragraph: list of paragraphs, each paragraph is a list of text-runs.
    Each text-run = dict with 'value' and 'style' keys.
    style: {'fontSize': '10pt', 'fontFamily': 'Segoe UI', 'color': '#hex', 'bold': True, 'italic': False}
    """
    paragraphs = []
    for runs in text_runs_per_paragraph:
        if not runs:
            paragraphs.append({"textRuns": [{"value": ""}]})
            continue
        text_runs = []
        for r in runs:
            tr = {"value": r["value"]}
            style = r.get("style") or {}
            text_style = {}
            if "fontSize" in style: text_style["fontSize"] = style["fontSize"]
            if "fontFamily" in style: text_style["fontFamily"] = style["fontFamily"]
            if "color" in style: text_style["color"] = style["color"]
            if style.get("bold"): text_style["fontWeight"] = "bold"
            if style.get("italic"): text_style["fontStyle"] = "italic"
            if "letterSpacing" in style: text_style["letterSpacing"] = style["letterSpacing"]
            if text_style:
                tr["textStyle"] = text_style
            text_runs.append(tr)
        paragraphs.append({
            "textRuns": text_runs,
            "horizontalTextAlignment": align,
        })
    objects = {"general": [{"properties": {"paragraphs": paragraphs}}]}
    return objects

def write_textbox(name, pos, text_runs_per_paragraph, *, align="left", bg=None, padding=8):
    path = f"{PAGE_DIR}/{name}/visual.json"
    visual = {
        "name": name,
        "visual": {
            "visualType": "textbox",
            "query": {"queryState": {}},
            "objects": textbox(text_runs_per_paragraph, align=align, bg=bg, padding=padding),
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": build_container(title=False, bg=bg, padding=padding),
        },
        "position": {"x": pos[0], "y": pos[1], "z": pos.get("z", 0) if isinstance(pos, dict) else pos[4] if len(pos)>4 else 0, "width": pos[2], "height": pos[3], "tabOrder": 0},
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"
    }
    # Fix z handling for tuple style
    visual["position"]["z"] = pos[4] if len(pos) > 4 else 0
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(visual, f, indent=2)
    print(f"  wrote {name}: {pos[0]},{pos[1]} {pos[2]}x{pos[3]}")

def reposition(name, x, y, w, h, z=0):
    path = f"{PAGE_DIR}/{name}/visual.json"
    if not os.path.exists(path):
        print(f"  SKIP {name} (not found)")
        return
    with open(path, "r", encoding="utf-8") as f:
        v = json.load(f)
    v["position"]["x"] = x
    v["position"]["y"] = y
    v["position"]["width"] = w
    v["position"]["height"] = h
    v["position"]["z"] = z
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)
    print(f"  moved {name}: {x},{y} {w}x{h} z={z}")

# ─────────────────────────────────────────────────────────────────────────────
# Header row
# ─────────────────────────────────────────────────────────────────────────────

# Hide the default Title visual (we control the header ourselves)
reposition("Title", 0, 0, 1, 1, z=-1)

write_textbox("hdr-eyebrow", (30, 20, 600, 20),
    [[{"value": "PAGE 1  ·  SUMMARY", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3, "letterSpacing": "0.18em"}}]],
)

write_textbox("hdr-title", (30, 38, 700, 60),
    [[
        {"value": "Where ", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK}},
        {"value": "is my", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK_2, "italic": True}},
        {"value": " data?", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK}},
    ]],
)

write_textbox("hdr-meta", (920, 24, 380, 70),
    [
        [{"value": "reporting year  ·  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "2026", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}}],
        [{"value": "groups  ·  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "5 active", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}},
         {"value": "  ·  3 idle", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}}],
        [{"value": "contracts  ·  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "104", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}}],
    ],
    align="right",
)

# Filter bar (black) — span full width, slicer overlaid on top
write_textbox("filter-bar", (30, 110, 1260, 44),
    [[{"value": "FILTERS    ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#FFFFFF", "letterSpacing": "0.15em"}}]],
    bg=INK, padding=12,
)
reposition("slicer-year", 130, 116, 200, 32, z=2)

# ─────────────────────────────────────────────────────────────────────────────
# Hero block
# ─────────────────────────────────────────────────────────────────────────────

write_textbox("hero-narrative", (30, 170, 830, 150),
    [
        [{"value": "AT A GLANCE  ·  PERIOD 2026", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#A6A39B", "letterSpacing": "0.18em"}}],
        [{"value": "", "style": {"fontSize": "4pt"}}],  # spacer
        [
            {"value": "Of ", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER}},
            {"value": "312", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER, "bold": True}},
            {"value": " files due so far, ", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER}},
            {"value": "252", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": "#ED8D80", "bold": True}},
            {"value": " haven't arrived.", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER}},
        ],
        [
            {"value": "The ", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER}},
            {"value": "62", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": "#7AB494", "bold": True}},
            {"value": " that did mostly reached gold — ", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER}},
            {"value": "59", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": "#7AB494", "bold": True}},
            {"value": " of them.", "style": {"fontSize": "18pt", "fontFamily": "Georgia", "color": PAPER}},
        ],
        [{"value": "", "style": {"fontSize": "6pt"}}],
        [{"value": "934 files have deadlines later this year — not yet a concern.   |   1 schema failure  ·  10 DQ issues  ·  0 late  ·  0 quarantine", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#A6A39B"}}],
    ],
    bg=INK, padding=24,
)

write_textbox("hero-verdict", (870, 170, 420, 150),
    [
        [{"value": "GROUP VERDICT", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3, "letterSpacing": "0.18em"}}],
        [{"value": "", "style": {"fontSize": "2pt"}}],
        [{"value": "5 of 5", "style": {"fontSize": "44pt", "fontFamily": "Georgia", "color": BAD, "bold": True}}],
        [{"value": "active groups under 35% delivery pace.", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK_2}}],
        [{"value": "SHV Energy at 0% needs escalation.", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK_2, "bold": True}}],
    ],
    bg=PAPER, padding=22,
)

# ─────────────────────────────────────────────────────────────────────────────
# KPI band — reposition 5 cards
# ─────────────────────────────────────────────────────────────────────────────

kpi_y = 340
kpi_h = 110
kpi_w = 246
gap = 6
for i, name in enumerate(["card-expected", "card-due", "card-delivered", "card-overdue", "card-gold"]):
    x = 30 + i * (kpi_w + gap)
    reposition(name, x, kpi_y, kpi_w, kpi_h)

# ─────────────────────────────────────────────────────────────────────────────
# Section labels + monthly chart
# ─────────────────────────────────────────────────────────────────────────────

write_textbox("sec-monthly", (30, 470, 1260, 24),
    [[
        {"value": "MONTHLY DELIVERY  ·  PERIOD VIEW", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_2, "letterSpacing": "0.18em"}},
        {"value": "                                                                                                each bar = 104 expected  ·  stacked by current state", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}},
    ]],
)

reposition("monthly-trend", 30, 500, 1260, 240)

# ─────────────────────────────────────────────────────────────────────────────
# Section label + two-panel split
# ─────────────────────────────────────────────────────────────────────────────

write_textbox("sec-where", (30, 760, 1260, 24),
    [[
        {"value": "WHERE TO LOOK", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_2, "letterSpacing": "0.18em"}},
        {"value": "                                                                                                                                                                     left  ·  groups       right  ·  what to chase today", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}},
    ]],
)

reposition("groups-table", 30, 790, 620, 380)
reposition("overdue-table", 670, 790, 620, 380)

# ─────────────────────────────────────────────────────────────────────────────
# Footnote
# ─────────────────────────────────────────────────────────────────────────────

write_textbox("footnote", (30, 1190, 1260, 60),
    [
        [{"value": "How to read this page:  ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
         {"value": "Due by today", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
         {"value": " = deadline ≤ today.   ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK_2}},
         {"value": "Overdue", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
         {"value": " = past deadline, no delivery.   ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK_2}},
         {"value": "In Window", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
         {"value": " = period started, deadline future, no delivery yet.", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK_2}}],
    ],
    bg=PAPER_2, padding=14,
)

print("\ndone.")
