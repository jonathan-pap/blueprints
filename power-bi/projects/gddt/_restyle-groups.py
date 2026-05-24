"""Editorial restyle for 02-Groups page (matches the Page 2 mockup)."""
import json, os

PAGE_DIR = "gddt.Report/definition/pages/02-Groups/visuals"

INK = "#15171C"; INK_2 = "#353841"; INK_3 = "#8F8E87"
PAPER = "#F7F5EF"; PAPER_2 = "#EBE8DF"
BAD = "#A23A2A"; INFO = "#244E7A"

def lit(s): return {"expr": {"Literal": {"Value": s}}}
def lit_str(s): return lit(f"'{s}'")
def lit_bool(b): return lit("true" if b else "false")
def lit_num(n): return lit(f"{n}D")
def color(h): return {"solid": {"color": lit_str(h)}}

def write_textbox(name, pos, paragraphs, *, align="left", bg=None, padding=8):
    out_paras = []
    for runs in paragraphs:
        if not runs:
            out_paras.append({"textRuns": [{"value": ""}]})
            continue
        tr = []
        for r in runs:
            run = {"value": r["value"]}
            style = r.get("style") or {}
            ts = {}
            if "fontSize" in style: ts["fontSize"] = style["fontSize"]
            if "fontFamily" in style: ts["fontFamily"] = style["fontFamily"]
            if "color" in style: ts["color"] = style["color"]
            if style.get("bold"): ts["fontWeight"] = "bold"
            if style.get("italic"): ts["fontStyle"] = "italic"
            if "letterSpacing" in style: ts["letterSpacing"] = style["letterSpacing"]
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

    path = f"{PAGE_DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f:
        v = json.load(f)
    v["visual"]["objects"] = {"general": [{"properties": {"paragraphs": out_paras}}]}
    v["visual"]["visualContainerObjects"] = vco
    v["position"]["x"] = pos[0]; v["position"]["y"] = pos[1]
    v["position"]["width"] = pos[2]; v["position"]["height"] = pos[3]
    v["position"]["z"] = pos[4] if len(pos) > 4 else 0
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)
    print(f"  wrote {name}: {pos[0]},{pos[1]} {pos[2]}x{pos[3]}")

def reposition(name, x, y, w, h, z=0):
    path = f"{PAGE_DIR}/{name}/visual.json"
    if not os.path.exists(path):
        print(f"  SKIP {name}")
        return
    with open(path, "r", encoding="utf-8") as f:
        v = json.load(f)
    v["position"]["x"] = x; v["position"]["y"] = y
    v["position"]["width"] = w; v["position"]["height"] = h
    v["position"]["z"] = z
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)
    print(f"  moved {name}: {x},{y} {w}x{h}")

# ─── Header
reposition("Title", 0, 0, 1, 1, z=-1)

write_textbox("g-hdr-eyebrow", (30, 20, 600, 20),
    [[{"value": "PAGE 2  ·  GROUPS", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3, "letterSpacing": "0.18em"}}]],
)
write_textbox("g-hdr-title", (30, 38, 800, 60),
    [[
        {"value": "Group ", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK}},
        {"value": "performance", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK_2, "italic": True}},
    ]],
)
write_textbox("g-hdr-meta", (920, 30, 380, 50),
    [
        [{"value": "ranked  ·  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "by health", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}}],
        [{"value": "active  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "5", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}},
         {"value": "  ·  idle  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "3", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}}],
    ],
    align="right",
)

# ─── Filter bar
write_textbox("g-filter-bar", (30, 110, 1260, 44),
    [[
        {"value": "FILTERS    ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#FFFFFF", "letterSpacing": "0.15em"}},
        {"value": "[year 2026]    [view all groups]    [sort health desc]    [show idle yes]", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": "#FFFFFF"}},
    ]],
    bg=INK, padding=12,
)

# ─── Main scorecard (reposition existing)
reposition("group-scorecards", 30, 180, 1260, 460)

# ─── Section label
write_textbox("g-sec-where", (30, 660, 1260, 24),
    [[
        {"value": "WHERE THE GAP IS, BY FREQUENCY", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_2, "letterSpacing": "0.18em"}},
        {"value": "                                                                                                                                    same data, different lens  ·  v0 is monthly-only", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}},
    ]],
)

# ─── Status by frequency + overdue per group
reposition("freq-status", 30, 690, 800, 280)
reposition("group-overdue", 850, 690, 440, 280)

# ─── Footnote
write_textbox("g-footnote", (30, 990, 1260, 80),
    [
        [{"value": "V0 note: ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
         {"value": "all contracts currently registered as monthly. Frequency-driven cadence (Q/H/Y) is a v1 refinement. Once applied, January should spike as Y+H+Q+M periods converge there.", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK_2}}],
    ],
    bg=PAPER_2, padding=14,
)

print("done.")
