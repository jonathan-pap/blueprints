"""Game-style coach-mark bubbles for the tutorial: a rounded speech bubble with a tail that
points at the visual being explained.

WHY SVG AND NOT A TEXTBOX

A textbox cannot have a tail, a border radius or a drop shadow, and it cannot mix a small
all-caps step counter with a gold heading and body copy in one block. An `ImageUrl` SVG measure
in an `image` visual can do all of it. Text wrapping comes from `<foreignObject>` holding real
XHTML - the foundation at 02-build/visuals/svg/html-in-svg.md - because raw SVG `<text>` has no
wrapping at all.

WHY TEN MEASURES RATHER THAN ONE

The obvious shape is one function taking (title, body, side) and ten one-line callers. DAX
user-defined functions need compatibility level 1702 and this model is at 1606, so that is out
without raising the model's compat level - a real change with real consequences, not worth it
for a cosmetic win. The boilerplate is therefore generated here, in Python, and each measure
ends up holding its own complete SVG. The generator is the single source of truth; nobody should
hand-edit the measures.

WELL-FORMEDNESS

foreignObject content is XHTML, not loose HTML: single-quoted attributes, self-closed void tags,
and `&` `<` `>` escaped in any body text. Miss one and the whole image fails silently - no error,
just a blank visual.
"""
import io
import json
import os

from emporiumkit import GOLD, INK, INK2, INK3, PAGES, RULE, SURFACE, lit, measure, noframe, vis, write

# Runeforge Dark, but a shade lifted off the page so the bubble reads as floating above it
BODY_FILL = "#221E1A"

STEPS = [
    # id, page, step label, title, body, anchor, tail side, tail offset (0-1).
    # ANCHOR is the edge the tail comes out of: y is the bubble's TOP for a top tail and
    # its BOTTOM for a bottom tail, so growing the bubble to fit its text never drags the
    # tail off the thing it is pointing at. Height is computed, never written by hand.
    ("tut01", "Overview", "Step 1 of 3",
     "The headline numbers",
     "25.00M is the four-year take. The generator was told to hit exactly 25,000,000 and "
     "landed on 25,000,000.76.<br/><br/>Growth reads +12.0% and it is fussier than it looks: "
     "the obvious measure compares 2023-2026 against 2023-2025 and reports +41.6%. That is "
     "arithmetic, not growth. This card always answers <b>how did the most recent year do</b>.",
     {"x": 24, "y": 272, "width": 680}, "top", 0.16),

    ("tut02", "Overview", "Step 2 of 3",
     "Four years, month by month",
     "Columns are each month's take; the gold line is a trailing three-month mean.<br/><br/>"
     "The line exists so the spikes read as spikes rather than as the trend moving. Every "
     "November and December is the <b>Frostfall festival</b>.",
     {"x": 24, "y": 488, "width": 680}, "top", 0.5),

    ("tut03", "Overview", "Step 3 of 3",
     "Two ways to cut the same Gold",
     "Realm on the left, category of ware on the right. Both splits are pinned by the "
     "generator - 45/30/25 and 30/25/20/15/10 - and the model reproduces them to eight "
     "decimal places.<br/><br/>One is horizontal and one vertical for a dull reason: five "
     "horizontal bars did not fit, and Power BI drops the fifth rather than crowd them.",
     {"x": 24, "y": 456, "width": 680}, "bottom", 0.2),

    ("tut04", "Realms", "Step 1 of 2",
     "Every shop, ranked",
     "Bar colour is the realm - Eldoria blue, Grimmwald plum, Sunspire gold.<br/><br/>"
     "<b>Read the realms, not the shops.</b> Within a realm they are near-identical "
     "(3,750,001 / 3,750,000 / 3,749,999) because the generator splits each realm's Gold "
     "evenly across its shops.",
     {"x": 576, "y": 200, "width": 640}, "left", 0.32),

    ("tut05", "Realms", "Step 2 of 2",
     "The shop ledger",
     "Share re-bases to whatever the header slicers have selected. Pick one realm and each of "
     "its shops jumps from 15% to 33%.<br/><br/>It is always a share of what you are looking "
     "at, never a share of the whole four years.",
     {"x": 40, "y": 200, "width": 448}, "right", 0.32),

    ("tut06", "Items", "Step 1 of 2",
     "The vital few",
     "Bars are Gold, the line is the running share. Gold to the 80% mark, iron beyond it: four "
     "wares carry over half the takings.<br/><br/>The line is a <b>visual calculation</b> - "
     "nothing was added to the model. ORDERBY pins accumulation to value-descending, so it "
     "stays correct even if you re-sort the axis.",
     {"x": 24, "y": 488, "width": 744}, "top", 0.28),

    ("tut07", "Items", "Step 2 of 2",
     "Every ware, with its place in the tail",
     "The same twenty-four wares as numbers. Elixir of Vitality alone is 20.2% of everything; "
     "the bottom thirteen together are under twenty.<br/><br/>Avg price is Gold per unit - a "
     "blended price across whatever is filtered, not a list price. There is no price column in "
     "the model.",
     {"x": 24, "y": 464, "width": 744}, "bottom", 0.28),

    ("tut08", "Patrons", "Step 1 of 3",
     "Gold by kind of patron",
     "Four kinds, pinned at 40/25/20/15. Adventurers are the biggest block of Gold and nobles "
     "the smallest - the opposite of the clich&#233;, and entirely deliberate.",
     {"x": 664, "y": 184, "width": 592}, "left", 0.3),

    ("tut09", "Patrons", "Step 2 of 3",
     "Average purse - the odd one",
     "Adventurers have the <b>biggest</b> average purse (284) and nobles the smallest (190).<br/>"
     "<br/>Every patron visits about as often as every other - roughly five thousand times over "
     "four years - so average purse has nothing left to track except the pinned Gold share. An "
     "artefact of the data, not a finding about nobles.",
     {"x": 32, "y": 184, "width": 576}, "right", 0.3),

    ("tut10", "Patrons", "Step 3 of 3",
     "The big spenders",
     "Kaelen Swiftblade alone is 24.1% of everything - more than the whole Noble kind put "
     "together.<br/><br/>The generator ranks big spenders first <b>within</b> each kind, so the "
     "pareto runs inside the type rather than across it.",
     {"x": 560, "y": 416, "width": 696}, "bottom", 0.4),
]

TAIL = 18          # how far the tail sticks out
R = 14             # corner radius
PAD = 22           # inner padding for the text block
TOUR_TOP = 656     # the tour row - no bubble may overlap it


def wrapped_height(body, width):
    """Estimate the rendered height of the XHTML block.

    foreignObject clips silently, so this errs generous. Segoe UI at 13px averages ~6.2px a
    character - a first cut used 2.05 and every bubble lost its last line, which on step 2 was
    the words "the Frostfall festival", i.e. the entire point of the step. Paragraphs split on
    <br/><br/>, 20px a line, 14px between paragraphs, plus 16px of slack.
    """
    per_line = max(20, int(width / 6.2))
    import re
    plain = re.sub("<[^>]+>", "", body.replace("<br/><br/>", "\n\n").replace("<br/>", "\n"))
    h = 0
    for para in plain.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        lines = max(1, -(-len(para) // per_line))
        h += lines * 20 + 14
    return h + 20 + 5 + 21 + 9 + 16   # step label + gap + title + gap + slack


def bubble_rect(anchor, side, body, title):
    w = anchor["width"]
    _, _, iw, _ = 0, 0, w - 2 * PAD - (TAIL if side in ("left", "right") else 0), 0
    inner_h = wrapped_height(body, iw) + (24 if len(title) > 30 else 0)
    h = inner_h + 2 * PAD + TAIL
    y = anchor["y"] if side in ("top", "left", "right") else anchor["y"] - h
    if side in ("left", "right"):
        y = anchor["y"]
    if y + h > TOUR_TOP - 8:
        y = TOUR_TOP - 8 - h
    return {"x": anchor["x"], "y": max(136, y), "width": w, "height": h}



def path(w, h, side, off):
    """One path for the whole bubble - body and tail together, so there is no seam to hide."""
    if side == "top":
        t, b, l, r = TAIL, h, 0, w
        tip = l + off * (r - l)
        head = ["M %d %d" % (l + R, t),
                "L %d %d" % (tip - TAIL, t), "L %d %d" % (tip, 0), "L %d %d" % (tip + TAIL, t)]
    elif side == "bottom":
        t, b, l, r = 0, h - TAIL, 0, w
        tip = l + off * (r - l)
        head = ["M %d %d" % (l + R, t)]
    elif side == "left":
        t, b, l, r = 0, h, TAIL, w
        tip = t + off * (b - t)
        head = ["M %d %d" % (l + R, t)]
    else:  # right
        t, b, l, r = 0, h, 0, w - TAIL
        tip = t + off * (b - t)
        head = ["M %d %d" % (l + R, t)]

    p = list(head)
    p.append("L %d %d" % (r - R, t))
    p.append("A %d %d 0 0 1 %d %d" % (R, R, r, t + R))
    if side == "right":
        p.append("L %d %d" % (r, tip - TAIL))
        p.append("L %d %d" % (r + TAIL, tip))
        p.append("L %d %d" % (r, tip + TAIL))
    p.append("L %d %d" % (r, b - R))
    p.append("A %d %d 0 0 1 %d %d" % (R, R, r - R, b))
    if side == "bottom":
        p.append("L %d %d" % (tip + TAIL, b))
        p.append("L %d %d" % (tip, b + TAIL))
        p.append("L %d %d" % (tip - TAIL, b))
    p.append("L %d %d" % (l + R, b))
    p.append("A %d %d 0 0 1 %d %d" % (R, R, l, b - R))
    if side == "left":
        p.append("L %d %d" % (l, tip + TAIL))
        p.append("L %d %d" % (l - TAIL, tip))
        p.append("L %d %d" % (l, tip - TAIL))
    p.append("L %d %d" % (l, t + R))
    p.append("A %d %d 0 0 1 %d %d" % (R, R, l + R, t))
    p.append("Z")
    return " ".join(p)


def inner(w, h, side):
    """Text box inside the body, inset from whichever edge carries the tail."""
    x, y, iw, ih = PAD, PAD, w - 2 * PAD, h - 2 * PAD
    if side == "top":
        y += TAIL; ih -= TAIL
    elif side == "bottom":
        ih -= TAIL
    elif side == "left":
        x += TAIL; iw -= TAIL
    else:
        iw -= TAIL
    return x, y, iw, ih


def svg(step, title, body, rect, side, off):
    w, h = rect["width"], rect["height"]
    ix, iy, iw, ih = inner(w, h, side)
    d = path(w, h, side, off)
    css = ("font-family:Segoe UI,Segoe,sans-serif;color:%s;font-size:13px;line-height:1.5"
           % INK2)
    return (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d'>" % (w, h)
        + "<defs><filter id='s' x='-20%' y='-20%' width='140%' height='140%'>"
          "<feDropShadow dx='0' dy='3' stdDeviation='6' flood-color='#000' "
          "flood-opacity='0.55'/></filter></defs>"
        + "<path d='%s' fill='%s' stroke='%s' stroke-width='2' filter='url(#s)'/>"
          % (d, BODY_FILL, GOLD)
        + "<foreignObject x='%d' y='%d' width='%d' height='%d'>" % (ix, iy, iw, ih)
        + "<div xmlns='http://www.w3.org/1999/xhtml' style='%s'>" % css
        + "<div style='color:%s;font-size:10px;letter-spacing:0.16em;"
          "text-transform:uppercase;margin-bottom:5px'>%s</div>" % (INK3, step)
        + "<div style='color:%s;font-size:17px;font-weight:600;line-height:1.25;"
          "margin-bottom:9px'>%s</div>" % (GOLD, title)
        + "<div>%s</div>" % body
        + "</div></foreignObject></svg>"
    )


def esc(s):
    """Escape bare ampersands WITHOUT touching entities that are already there.

    A blunt s.replace("&", "&amp;") turned `clich&#233;` into `clich&amp;#233;`, which renders
    as the literal text `clich&#233;`. Any text carrying a numeric entity would hit this.
    """
    import re
    s = re.sub(r"&(?!#?\w+;)", "&amp;", s)
    return s.replace("'", "&#39;")


MEASURES, RECTS = {}, {}
for sid, page, step, title, body, anchor, side, off in STEPS:
    rect = bubble_rect(anchor, side, body, title)
    RECTS[sid] = rect
    MEASURES["Bubble " + sid[3:]] = svg(esc(step), esc(title), esc(body), rect, side, off)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_bubbles.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(MEASURES, indent=1, ensure_ascii=False))
    print("wrote %d bubble measures to _bubbles.json" % len(MEASURES))
    for sid, page, step, title, body, anchor, side, off in STEPS:
        r = RECTS[sid]
        print("  %s %-7s %4d,%4d %4dx%-4d bottom=%d"
              % (sid, side, r["x"], r["y"], r["width"], r["height"],
                 r["y"] + r["height"]))

    # swap the caption textboxes for image visuals bound to the bubble measures
    for sid, page, step, title, body, anchor, side, off in STEPS:
        rect = RECTS[sid]
        name = "cap" + sid
        v = vis(name, "image", rect, 980,
                objects={"image": [{"properties": {
                    "sourceType": lit("'imageData'"), "transparency": lit("0D"),
                    "effects": lit("false"), "fit": lit("'Fit'"),
                    "sourceField": {"expr": measure("Bubble " + sid[3:])}}}]},
                vco=noframe())
        v["isHidden"] = True
        write(os.path.join(PAGES, page), name, v)
    print("  %d caption visuals swapped to bubbles" % len(STEPS))
