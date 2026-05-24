"""Editorial restyle for 04-Scoring page (Page 4 mockup)."""
import json, os

PAGE_DIR = "gddt.Report/definition/pages/04-Scoring/visuals"

INK = "#15171C"; INK_2 = "#353841"; INK_3 = "#8F8E87"
PAPER = "#F7F5EF"; PAPER_2 = "#EBE8DF"; RULE = "#D8D5CC"
BAD = "#A23A2A"; WARN = "#B46C1A"; GOOD = "#2D6948"; INFO = "#244E7A"

def lit(s): return {"expr": {"Literal": {"Value": s}}}
def lit_str(s): return lit(f"'{s}'")
def lit_bool(b): return lit("true" if b else "false")
def lit_num(n): return lit(f"{n}D")
def color(h): return {"solid": {"color": lit_str(h)}}

def write_textbox(name, pos, paragraphs, *, align="left", bg=None, padding=8):
    out_paras = []
    for runs in paragraphs:
        if not runs:
            out_paras.append({"textRuns": [{"value": ""}]}); continue
        tr = []
        for r in runs:
            run = {"value": r["value"]}
            style = r.get("style") or {}
            ts = {}
            for k_in, k_out in [("fontSize","fontSize"),("fontFamily","fontFamily"),("color","color"),("letterSpacing","letterSpacing")]:
                if k_in in style: ts[k_out] = style[k_in]
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

    path = f"{PAGE_DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
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
        print(f"  SKIP {name}"); return
    with open(path, "r", encoding="utf-8") as f: v = json.load(f)
    v["position"]["x"] = x; v["position"]["y"] = y
    v["position"]["width"] = w; v["position"]["height"] = h
    v["position"]["z"] = z
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)
    print(f"  moved {name}: {x},{y} {w}x{h}")

# ─── Header
reposition("Title", 0, 0, 1, 1, z=-1)

write_textbox("s-hdr-eyebrow", (30, 20, 600, 20),
    [[{"value": "PAGE 4  ·  SCORING", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3, "letterSpacing": "0.18em"}}]],
)
write_textbox("s-hdr-title", (30, 38, 800, 60),
    [[
        {"value": "Group ", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK}},
        {"value": "health", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK_2, "italic": True}},
        {"value": " score", "style": {"fontSize": "32pt", "fontFamily": "Georgia", "color": INK}},
    ]],
)
write_textbox("s-hdr-meta", (920, 30, 380, 50),
    [
        [{"value": "formula  ·  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "5 dimensions", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}}],
        [{"value": "weights  ·  ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_3}},
         {"value": "tunable", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK, "bold": True}}],
    ],
    align="right",
)

# ─── Filter bar
write_textbox("s-filter-bar", (30, 110, 1260, 44),
    [[
        {"value": "FILTERS    ", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#FFFFFF", "letterSpacing": "0.15em"}},
        {"value": "[year 2026]    [as of today]    [scoring weighted composite]", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": "#FFFFFF"}},
    ]],
    bg=INK, padding=12,
)

# ─── HOW THE SCORE WORKS
write_textbox("s-sec-how", (30, 170, 1260, 24),
    [[
        {"value": "HOW THE SCORE WORKS", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_2, "letterSpacing": "0.18em"}},
        {"value": "                                                                                                                            five dimensions  ·  weighted composite  ·  0–100  ·  A–F grade", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}},
    ]],
)

# ─── Formula box (black, large)
# Existing formula-box textbox already exists — restyle it
write_textbox("formula-box", (30, 200, 1260, 80),
    [
        [{"value": "COMPOSITE HEALTH SCORE  ·  0–100", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#A6A39B", "letterSpacing": "0.18em"}}],
        [{"value": "", "style": {"fontSize": "4pt"}}],
        [
            {"value": "score = ", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#C4D8C8"}},
            {"value": "0.25", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#F4A987"}},
            {"value": " × reliability + ", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": PAPER}},
            {"value": "0.15", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#F4A987"}},
            {"value": " × punctuality + ", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": PAPER}},
            {"value": "0.25", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#F4A987"}},
            {"value": " × quality + ", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": PAPER}},
            {"value": "0.10", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#F4A987"}},
            {"value": " × recovery + ", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": PAPER}},
            {"value": "0.15", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#F4A987"}},
            {"value": " × discipline − ", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": PAPER}},
            {"value": "0.10", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": "#F4A987"}},
            {"value": " × overdue_share", "style": {"fontSize": "16pt", "fontFamily": "Consolas", "color": PAPER}},
        ],
    ],
    bg=INK, padding=22,
)

# ─── Two-panel: Dimensions + Grade bands
write_textbox("s-dimensions-panel", (30, 300, 620, 220),
    [
        [{"value": "Dimensions", "style": {"fontSize": "16pt", "fontFamily": "Georgia", "color": INK}}],
        [{"value": "each measured 0–100  ·  latest-wins active deliveries", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}}],
        [{"value": "", "style": {"fontSize": "6pt"}}],
        [
            {"value": "Reliability  ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
            {"value": "25%  ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INFO}},
            {"value": "delivered / expected-by-today  ·  did the source show up?", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "Punctuality  ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
            {"value": "15%  ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INFO}},
            {"value": "on-time / delivered  ·  did they meet the window?", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "Quality  ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
            {"value": "25%  ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INFO}},
            {"value": "gold / delivered  ·  was the data usable?", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "Recovery  ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
            {"value": "10%  ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INFO}},
            {"value": "re-ingested / first-failures  ·  do they fix what breaks?", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "Discipline  ", "style": {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": INK, "bold": True}},
            {"value": "15%  ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INFO}},
            {"value": "1 − scope-quar / delivered  ·  contract respect", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
    ],
    bg=PAPER, padding=16,
)

write_textbox("s-grade-panel", (670, 300, 620, 220),
    [
        [{"value": "Grade bands", "style": {"fontSize": "16pt", "fontFamily": "Georgia", "color": INK}}],
        [{"value": "colour mapping for cards and tables", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}}],
        [{"value": "", "style": {"fontSize": "6pt"}}],
        [
            {"value": "  A  ", "style": {"fontSize": "13pt", "fontFamily": "Georgia", "color": PAPER, "bold": True}},
            {"value": "   90+      ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
            {"value": "excellent  ·  low intervention", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "  B  ", "style": {"fontSize": "13pt", "fontFamily": "Georgia", "color": GOOD, "bold": True}},
            {"value": "   75–89    ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
            {"value": "acceptable", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "  C  ", "style": {"fontSize": "13pt", "fontFamily": "Georgia", "color": WARN, "bold": True}},
            {"value": "   60–74    ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
            {"value": "monitor  ·  watch trend", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "  D  ", "style": {"fontSize": "13pt", "fontFamily": "Georgia", "color": WARN, "bold": True}},
            {"value": "   40–59    ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
            {"value": "underperforming", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
        [
            {"value": "  F  ", "style": {"fontSize": "13pt", "fontFamily": "Georgia", "color": BAD, "bold": True}},
            {"value": "   < 40     ", "style": {"fontSize": "10pt", "fontFamily": "Consolas", "color": INK}},
            {"value": "critical  ·  escalate", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3}},
        ],
    ],
    bg=PAPER, padding=16,
)

# ─── LEADERBOARD section
write_textbox("s-sec-leader", (30, 540, 1260, 24),
    [[
        {"value": "LEADERBOARD", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_2, "letterSpacing": "0.18em"}},
        {"value": "                                                                                                                                                ranked descending  ·  sparkline  ·  score over 4 weeks", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}},
    ]],
)

# Reposition existing leaderboard tableEx — full width
reposition("leaderboard", 30, 570, 1260, 270)

# ─── WHY EACH GROUP SCORES section
write_textbox("s-sec-why", (30, 860, 1260, 24),
    [[
        {"value": "WHY EACH GROUP SCORES WHAT IT DOES", "style": {"fontSize": "9pt", "fontFamily": "Consolas", "color": INK_2, "letterSpacing": "0.18em"}},
        {"value": "                                                                                                                              dimension-by-dimension  ·  top 3 by health", "style": {"fontSize": "10pt", "fontFamily": "Segoe UI", "color": INK_3, "italic": True}},
    ]],
)

# Reposition existing dimensions-ref (score components) + score-trend
reposition("dimensions-ref", 30, 890, 800, 240)
reposition("score-trend", 850, 890, 440, 240)

print("done.")
