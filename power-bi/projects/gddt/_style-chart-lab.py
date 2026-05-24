"""Style the 05-Chart-Lab page experiments."""
import json

DIR = "gddt.Report/definition/pages/05-Chart-Lab/visuals"

def lit(s): return {"expr": {"Literal": {"Value": s}}}
def lit_str(s): return lit(f"'{s}'")
def lit_bool(b): return lit("true" if b else "false")
def lit_num(n): return lit(f"{n}D")
def color(h): return {"solid": {"color": lit_str(h)}}

def write_textbox(name, paragraphs, *, bg=None, padding=12):
    """paragraphs = list of (text, style) pairs OR list of [run,run,...]"""
    out_paras = []
    for p in paragraphs:
        if isinstance(p, tuple):
            text, style = p
            runs = [{"value": text, "textStyle": style}] if style else [{"value": text}]
        else:
            runs = []
            for run_text, run_style in p:
                tr = {"value": run_text}
                if run_style: tr["textStyle"] = run_style
                runs.append(tr)
        out_paras.append({"textRuns": runs, "horizontalTextAlignment": "left"})
    objects = {"general": [{"properties": {"paragraphs": out_paras}}]}

    vco = {
        "title": [{"properties": {"show": lit_bool(False)}}],
        "subTitle": [{"properties": {"show": lit_bool(False)}}],
        "padding": [{"properties": {"top": lit_num(padding), "bottom": lit_num(padding), "left": lit_num(padding), "right": lit_num(padding)}}],
    }
    if bg:
        vco["background"] = [{"properties": {"show": lit_bool(True), "color": color(bg)}}]
    else:
        vco["background"] = [{"properties": {"show": lit_bool(False)}}]

    path = f"{DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f:
        v = json.load(f)
    v["visual"]["objects"] = objects
    v["visual"]["visualContainerObjects"] = vco
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)
    print(f"  styled {name}")

def write_shape(name, fill_color):
    path = f"{DIR}/{name}/visual.json"
    with open(path, "r", encoding="utf-8") as f:
        v = json.load(f)
    v["visual"]["objects"] = {
        "shape": [{"properties": {"tileShape": lit_str("rectangle")}}],
        "fill": [{"properties": {"show": lit_bool(True), "fillColor": color(fill_color), "transparency": lit_num(0)}}],
        "border": [{"properties": {"show": lit_bool(False)}}]
    }
    v["visual"]["visualContainerObjects"] = {
        "title": [{"properties": {"show": lit_bool(False)}}],
        "background": [{"properties": {"show": lit_bool(False)}}],
        "border": [{"properties": {"show": lit_bool(False)}}],
    }
    v["position"]["z"] = 5
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(v, f, indent=2)
    print(f"  styled shape {name}")

# Header
write_textbox("lab-header", [
    [("CHART LAB  ·  TODAY-MARKER EXPERIMENTS", {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#8F8E87", "letterSpacing": "0.18em"})],
    [("Same data, two ways to mark TODAY on the X-axis", {"fontSize": "18pt", "fontFamily": "Georgia", "color": "#15171C"})],
])

# Today label for second chart
write_textbox("today-label-2", [
    [("TODAY", {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#F7F5EF", "fontWeight": "bold", "letterSpacing": "0.1em"})]
], bg="#15171C", padding=4)
# Move it up + center
with open(f"{DIR}/today-label-2/visual.json", "r", encoding="utf-8") as f: v = json.load(f)
v["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["horizontalTextAlignment"] = "center"
v["position"]["z"] = 6
with open(f"{DIR}/today-label-2/visual.json", "w", encoding="utf-8", newline="\n") as f: json.dump(v, f, indent=2)

# Shape line for second chart
write_shape("today-line-2", "#15171C")

# Notes panel
write_textbox("lab-notes", [
    [("HOW EACH WORKS", {"fontSize": "9pt", "fontFamily": "Consolas", "color": "#353841", "letterSpacing": "0.18em"})],
    [
        ("Combo chart (top)", {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": "#15171C", "fontWeight": "bold"}),
        (" — uses 'lineStackedColumnComboChart'. The line series is a DAX measure that returns the bar height ONLY when YearMonth = current. Renders as a single peaked point. Data-driven: auto-moves every month.", {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": "#353841"}),
    ],
    [
        ("Shape overlay (bottom)", {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": "#15171C", "fontWeight": "bold"}),
        (" — thin rectangle shape positioned manually between Apr and May. Pixel-perfect line + label. Static: needs manual repositioning each month, OR a periodic script to recompute x-coordinate.", {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": "#353841"}),
    ],
    [
        ("Verdict so far: ", {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": "#15171C", "fontWeight": "bold"}),
        ("the combo chart's line series gives an automatic marker but reads as a 'spike' not a 'divider'. The shape gives the cleaner mockup look but needs maintenance. A third option — switching the X axis to a continuous date type — would unlock the analytics-pane constant line and beat both. Worth testing if these don't satisfy.", {"fontSize": "11pt", "fontFamily": "Segoe UI", "color": "#353841"}),
    ],
], bg="#EBE8DF", padding=14)

print("done.")
