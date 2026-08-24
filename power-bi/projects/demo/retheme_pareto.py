#!/usr/bin/env python3
"""Re-colour the Pareto to match whatever theme the report currently uses.

WHY THIS EXISTS. The pareto-chart recipe bakes its vital/trivial colours in as visual-level
conditional-formatting literals - they have to be literals, because a conditional rule cannot
reference a theme slot. So the theme cascade cannot reach them: swap the report to a dark theme
and the Pareto keeps its light-theme teal and crimson while every other visual changes. That is
not a bug in the recipe, it is the cost of rule-based colour, and the fix is to re-run this
whenever the theme changes.

Reads the active theme from report.json, picks two colours out of its palette, and rewrites the
four colour literals in the Pareto visual.

    python retheme_pareto.py            # follow the report's current theme
    python retheme_pareto.py --show     # print what it would use, change nothing

Colour choice:
  vital   = dataColors[0], the theme's lead - the "vital few" should read as the theme's
            primary, because they are the part of the chart the reader is meant to act on
  trivial = the theme's `bad` slot if it contrasts enough, else the most distant dataColor.
            Measured by CIELAB distance, not picked by eye.
  labels  = the theme's `foreground`, so the cumulative-% callouts stay legible on the
            theme's own surface (the dark themes made them unreadable at the recipe default).
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "demo.Report")
PARETO = os.path.join(REPORT, "definition", "pages", "Quest_Board", "visuals",
                      "questPareto", "visual.json")


def srgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lab(hexv):
    r, g, b = (_lin(c) for c in srgb(hexv))
    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x / 0.95047), f(y), f(z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def dist(a, b):
    la, lb = lab(a), lab(b)
    return sum((la[i] - lb[i]) ** 2 for i in range(3)) ** 0.5


def active_theme():
    rj = json.load(io.open(os.path.join(REPORT, "definition", "report.json"), encoding="utf-8"))
    name = (rj.get("themeCollection", {}).get("customTheme", {}) or {}).get("name")
    if not name:
        sys.exit("report.json has no customTheme; apply a theme first")
    path = os.path.join(REPORT, "StaticResources", "RegisteredResources", name)
    if not os.path.exists(path):
        sys.exit("theme file not found: " + path)
    return name, json.load(io.open(path, encoding="utf-8-sig"))


def pick(theme):
    data = theme.get("dataColors") or []
    if not data:
        sys.exit("theme has no dataColors")
    vital = data[0]
    # The 'bad' slot IS the trivial-many colour, so long as it separates from the lead. The
    # first cut just maximised CIELAB distance, and on the sapphire a11y theme that picked
    # GREEN for the trivial many - the tail you are meant to de-prioritise rendered as the
    # universal colour for "good". Distance is the tie-breaker, never the criterion.
    MIN_SEP = 40.0
    bad = theme.get("bad")
    if bad and dist(bad, vital) >= MIN_SEP:
        trivial = bad
    else:
        candidates = [c for c in data[1:] if c] or [bad or "#CC0000"]
        trivial = max(candidates, key=lambda c: dist(c, vital))
    ink = theme.get("foreground") or "#FFFFFF"
    return vital, trivial, ink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="print the choice, write nothing")
    a = ap.parse_args()

    name, theme = active_theme()
    vital, trivial, ink = pick(theme)
    print("theme:   %s (%s)" % (theme.get("name", "?"), name))
    print("  vital   %s   trivial %s   (CIELAB apart: %.1f)" % (vital, trivial,
                                                                dist(vital, trivial)))
    print("  labels  %s" % ink)
    if a.show:
        return 0

    # Find the colours CURRENTLY in the visual rather than assuming the recipe's defaults.
    # The first cut hardcoded the recipe values, so it worked once and then silently did
    # nothing on every later theme switch - the Pareto kept whichever palette got there first.
    # dataPoint carries the two live values on the GreenLine / RedLine series selectors.
    d = json.load(io.open(PARETO, encoding="utf-8"))
    cur = {}
    for blk in d["visual"]["objects"]["dataPoint"]:
        sel = (blk.get("selector") or {}).get("metadata")
        lit = (((blk.get("properties") or {}).get("fill") or {}).get("solid") or {}) \
            .get("color", {}).get("expr", {}).get("Literal", {}).get("Value")
        if sel in ("select3", "select4") and lit:
            cur[sel] = lit.strip("'")
    old_vital = cur.get("select3", "#0E7490")
    old_trivial = cur.get("select4", "#9D174D")

    src = io.open(PARETO, encoding="utf-8").read()
    before = sorted(set(re.findall(r"#[0-9A-Fa-f]{6}", src)))
    n = src.count(old_vital) + src.count(old_trivial)
    src = src.replace(old_vital, vital).replace(old_trivial, trivial)
    # select2 is the cumulative line itself. The recipe ships it as a hardcoded blue that is
    # not one of its own tokens, so it survives every substitution and clashes with the theme.
    src = src.replace("#2364A6", vital)
    for old_ink in ("#0B1020", "#F7F3EE", "#FFFFFF"):
        if old_ink not in (vital, trivial):
            src = src.replace('"\'%s\'"' % old_ink, '"\'%s\'"' % ink)
    io.open(PARETO, "w", encoding="utf-8", newline="\n").write(src)
    print("  %s -> %s, %s -> %s (%d literals); was %s"
          % (old_vital, vital, old_trivial, trivial, n, before))

    # The cumulative-% callouts sit on a PILL whose fill is a theme slot (ThemeDataColor
    # ColorId 1) while their text is one of the literals above. On a dark theme that pairs
    # light text with a light pill and the numbers vanish - which is exactly what happened.
    # Drop the pill on dark surfaces and let the text sit straight on the chart.
    page_bg = theme.get("background") or "#FFFFFF"
    r, g, b = (_lin(c) for c in srgb(page_bg))
    dark = (0.2126 * r + 0.7152 * g + 0.0722 * b) < 0.18
    d = json.load(io.open(PARETO, encoding="utf-8"))
    for blk in d["visual"]["objects"]["labels"]:
        if (blk.get("selector") or {}).get("metadata") != "select2":
            continue
        props = blk["properties"]
        props["backgroundTransparency"] = {"expr": {"Literal": {"Value": "%dL" % (100 if dark else 30)}}}
        if dark:
            props["color"] = {"solid": {"color": {"expr": {"Literal": {"Value": "'%s'" % ink}}}}}
    io.open(PARETO, "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print("  surface is %s -> callout pill %s" % ("dark" if dark else "light",
                                                  "off" if dark else "kept at 30%"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
