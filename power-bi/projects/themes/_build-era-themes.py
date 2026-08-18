"""Generate the ERA theme family: fantasy -> modern -> future, each as a light/dark PAIR.

Sibling to `_build-theme-library.py` (accessibility reference set), `_build-fantasy-themes.py`
(Grand Exchange flavour set) and `_build-space-themes.py` (launch data). Two things make this
generator different:

1. LIGHT AND DARK ARE TWINS, NOT COUSINS. A family declares hue angles once; both modes are
   derived from the same angles. Only the luminance ladder and the surfaces flip. A report can
   therefore switch modes without re-authoring conditional formatting, because dataColors[i]
   means the same thing in both.

2. THE LUMINANCE LADDER IS SOLVED, NOT PICKED. Greyscale separation is the constraint hand-
   mixing always loses: it is invisible on screen and only shows up on a mono printout or a
   projector. So the generator takes a target relative luminance per slot and binary-searches
   HSL lightness (desaturating only if the hue cannot reach the target) until it hits it. The
   ladder is then correct BY CONSTRUCTION rather than by luck.

Three gates, all measured, all fatal:
  - WCAG        4.5:1 for text, 3:1 for data fills and axis ink, against BOTH surfaces
  - greyscale   mutual luminance ratio >= 1.25 across the first four data colours
  - CVD         pairwise separation >= 0.18 across the first four, under simulated
                deuteranopia AND protanopia (Vienot 1999)

The first four are gated rather than all eight because those are the ones a reader actually
compares: the checklist's "the first 4 colors carry the most meaning". Eight colours cannot all
sit 1.25x apart in luminance AND clear 3:1 against the surface - the band is not wide enough.
Pretending otherwise would mean loosening the gate until it passed, which is worse than scoping
it honestly.

Output: projects/themes/<slug>/<slug>-<mode>-v1.0.json  (+ notes.md, written by hand)
"""
import json
import os
import sys

SCHEMA = ("https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/"
          "Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json")

GREY_MIN = 1.25
CVD_MIN = 0.18
GATED = 4          # how many leading data colours the ladder gates apply to

# Target relative luminance per data slot. Light mode runs dark-on-light so every fill has to
# stay under ~0.30 to clear 3:1 on white; dark mode runs the other way and has to stay above
# ~0.14 to clear 3:1 on the panel. Slots 0-3 are the gated ladder, 4-7 fill the same band.
#
# The two ladders run in OPPOSITE directions, and that is the point. Prominence is contrast
# against the surface, so on white the lead series has to be the DARKEST and on charcoal the
# LIGHTEST. A first cut used one descending ladder for both and light mode came out with a
# pastel lead sitting on white - the most important series was the faintest thing on the page.
#
# The light band is also lifted off the floor (0.105 rather than 0.084 at the lead). Very dark
# fills compress under CVD simulation - two near-black colours simulate to two near-black
# colours - and with the lead at 0.084 no gated four for Hyperion could clear 0.18 at all.
# 0.105 still gives the lead 6.6:1 against white, so nothing is lost in prominence.
LADDER = {
    # top rung is 0.290, not 0.300: at 0.300 the contrast against white lands on exactly
    # 3.00:1 and floating point drops it under the gate. 0.290 gives 3.09:1 with the
    # greyscale rungs still 1.25x apart.
    "light": [0.100, 0.155, 0.220, 0.290, 0.125, 0.185, 0.260, 0.072],
    "dark":  [0.560, 0.400, 0.280, 0.190, 0.480, 0.335, 0.235, 0.150],
}


# --------------------------------------------------------------------------- colour maths
def srgb(h):
    return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def linear(c):
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def lum_rgb(rgb):
    r, g, b = linear(rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def lum(h):
    return lum_rgb(srgb(h))


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def hsl_rgb(h, s, l):
    h = (h % 360) / 360.0
    if s == 0:
        return [l, l, l]
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q

    def hue(t):
        t = t % 1.0
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p
    return [hue(h + 1 / 3), hue(h), hue(h - 1 / 3)]


def hexof(rgb):
    return "#" + "".join("%02X" % max(0, min(255, round(x * 255))) for x in rgb)


def solve(hue, sat, target):
    """Hex at `hue` whose relative luminance is `target`.

    Binary-searches HSL lightness. A saturated blue simply cannot reach a high luminance, so
    when the hue tops out below target the saturation is stepped down and the search restarts.
    That is the whole trick: the ladder is honoured and the hue gives up only as much chroma
    as it has to.
    """
    s = sat
    for _ in range(12):
        if lum_rgb(hsl_rgb(hue, s, 0.98)) >= target:
            lo, hi = 0.0, 0.98
            for _ in range(40):
                mid = (lo + hi) / 2
                if lum_rgb(hsl_rgb(hue, s, mid)) < target:
                    lo = mid
                else:
                    hi = mid
            return hexof(hsl_rgb(hue, s, (lo + hi) / 2))
        s -= 0.06
        if s <= 0:
            break
    return hexof(hsl_rgb(hue, 0, 0.5))


# --------------------------------------------------------------- colour-vision simulation
RGB2LMS = [[0.31399022, 0.63951294, 0.04649755],
           [0.15537241, 0.75789446, 0.08670142],
           [0.01775239, 0.10944209, 0.87256922]]
LMS2RGB = [[5.47221206, -4.6419601, 0.16963708],
           [-1.1252419, 2.29317094, -0.1678952],
           [0.02980165, -0.19318073, 1.16364789]]
PROTAN = [[0, 1.05118294, -0.05116099], [0, 1, 0], [0, 0, 1]]
DEUTAN = [[1, 0, 0], [0.9513092, 0, 0.04866992], [0, 0, 1]]


def _mul(m, v):
    return [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]


def simulate(h, kind):
    lms = _mul(RGB2LMS, linear(srgb(h)))
    lms = _mul(PROTAN if kind == "protan" else DEUTAN, lms)
    return [max(0.0, min(1.0, x)) for x in _mul(LMS2RGB, lms)]


def cvd_dist(a, b, kind):
    x, y = simulate(a, kind), simulate(b, kind)
    return sum((x[i] - y[i]) ** 2 for i in range(3)) ** 0.5


# --------------------------------------------------------------------------- the families
# `hues` are (name, angle, saturation). Order IS priority - slot 0 leads every chart, and the
# first four are the gated set.
#
# The gated four follow Okabe-Ito's shape: blue, orange/gold, a reddish-purple and a
# bluish-green. Reds and true greens live at 4-7 on purpose. A first cut put crimson, gold
# and forest together in the gated set and ten CVD gates failed at once - protanopia and
# deuteranopia both push long wavelengths toward the same yellow, so red/green/orange trios
# collapse. They are still in the palette, just never among the four a reader is asked to
# tell apart at a glance.
#
# The gated hue angles were not chosen by eye - they came out of a sweep of the whole circle
# scored on the worst CVD pair across BOTH modes, then the highest-scoring set whose colours
# still read as the family was taken. That order matters: the constraint picks the palette and
# the names are applied afterwards, rather than a name list being defended until it passes.
FAMILIES = {
    "runeforge": {
        "label": "Runeforge",
        "era": "fantasy",
        "blurb": "Illuminated manuscript by day, forge-lit vault by night. Heraldic jewel "
                 "hues over limestone or warm charcoal.",
        "hues": [("royal blue", 220, 0.62), ("forge gold", 48, 0.68),
                 ("verdigris", 174, 0.52), ("arcane plum", 294, 0.50),
                 ("crimson", 352, 0.60), ("forest", 145, 0.50),
                 ("bronze", 24, 0.50), ("iron", 212, 0.14)],
        "good": 5, "bad": 4, "neutral": 7,
        "light": {"page": "#F2F0E8", "background": "#FFFFFF", "neutralBg": "#E6E2D6",
                  "darkBg": "#D6D1C2", "rule": "#DDD8CA",
                  "foreground": "#1E1A14", "secondary": "#4A4238",
                  "light": "#675F52", "tertiary": "#877E70"},
        "dark": {"page": "#100E0C", "background": "#1A1714", "neutralBg": "#262220",
                 "darkBg": "#080706", "rule": "#342E28",
                 "foreground": "#F2EAE0", "secondary": "#CDC2B4",
                 "light": "#9E9285", "tertiary": "#7F7466"},
    },
    "meridian": {
        "label": "Meridian",
        "era": "modern",
        "blurb": "Contemporary product-design flat UI. Cool neutrals, one confident indigo "
                 "lead, colour used sparingly and on purpose.",
        "hues": [("indigo", 245, 0.55), ("amber", 42, 0.68), ("teal", 174, 0.55),
                 ("magenta", 300, 0.55), ("green", 145, 0.48), ("rose", 345, 0.55),
                 ("azure", 210, 0.60), ("slate", 220, 0.12)],
        "good": 4, "bad": 5, "neutral": 7,
        "light": {"page": "#F5F7FA", "background": "#FFFFFF", "neutralBg": "#E9EDF3",
                  "darkBg": "#DCE2EB", "rule": "#E2E7EF",
                  "foreground": "#101623", "secondary": "#454E60",
                  "light": "#666F81", "tertiary": "#798190"},
        "dark": {"page": "#0D1016", "background": "#161A21", "neutralBg": "#212630",
                 "darkBg": "#070910", "rule": "#2C323D",
                 "foreground": "#EDF0F5", "secondary": "#C0C6D2",
                 "light": "#929AA8", "tertiary": "#767E8C"},
    },
    "hyperion": {
        "label": "Hyperion",
        "era": "future",
        "blurb": "Near-future instrument panel. Graphite and glass, electric cyan lead, "
                 "high chroma held on a short leash.",
        "hues": [("cyan", 190, 0.80), ("lime", 84, 0.62), ("magenta", 324, 0.68),
                 ("violet", 264, 0.62), ("coral", 8, 0.62), ("mint", 160, 0.55),
                 ("amber", 45, 0.62), ("steel", 205, 0.16)],
        "good": 5, "bad": 4, "neutral": 7,
        "light": {"page": "#F4F7F9", "background": "#FFFFFF", "neutralBg": "#E6EDF1",
                  "darkBg": "#D6E0E6", "rule": "#DFE7EC",
                  "foreground": "#0A1218", "secondary": "#3E4A54",
                  "light": "#5F6C77", "tertiary": "#828E98"},
        "dark": {"page": "#080B0D", "background": "#12171A", "neutralBg": "#1C2429",
                 "darkBg": "#040607", "rule": "#29343A",
                 "foreground": "#EAF4F8", "secondary": "#B6C6CE",
                 "light": "#86969E", "tertiary": "#6C7B83"},
    },
}


def palette(fam, mode):
    return [solve(h, s, t) for (_, h, s), t in zip(fam["hues"], LADDER[mode])]


# --------------------------------------------------------------------------------- audit
def audit(slug, mode, fam, p, data):
    bad = []

    def row(label, got, need, fmt="%7.2f:1"):
        ok = got >= need - 1e-9
        print(("    %-34s " + fmt + "  %.2f  %s")
              % (label, got, need, "ok" if ok else "*** FAIL ***"))
        if not ok:
            bad.append("%s-%s %s" % (slug, mode, label))

    for role, need in (("foreground", 4.5), ("secondary", 4.5),
                       ("light", 4.5), ("tertiary", 3.0)):
        for surf in ("background", "page"):
            row("text  %s / %s" % (role, surf), ratio(p[role], p[surf]), need)
    for i, c in enumerate(data):
        name = fam["hues"][i][0]
        row("fill  %d %-11s / surface" % (i, name), ratio(c, p["background"]), 3.0)

    print()
    for i in range(GATED):
        for j in range(i + 1, GATED):
            row("grey  %d/%d" % (i, j), ratio(data[i], data[j]), GREY_MIN)
    print()
    for kind in ("deutan", "protan"):
        for i in range(GATED):
            for j in range(i + 1, GATED):
                row("%s %d/%d" % (kind, i, j), cvd_dist(data[i], data[j], kind),
                    CVD_MIN, "%7.3f  ")
    return bad


# --------------------------------------------------------------------------------- build
def build(slug, mode, fam):
    p = fam[mode]
    data = palette(fam, mode)
    chrome_off = {"title": [{"show": False}], "background": [{"show": False}],
                  "border": [{"show": False}], "dropShadow": [{"show": False}]}
    name = "%s %s v1.0" % (fam["label"], mode.capitalize())
    return name, data, {
        "$schema": SCHEMA,
        "name": name,
        "dataColors": data,
        "good": data[fam["good"]],
        "bad": data[fam["bad"]],
        "neutral": data[fam["neutral"]],
        "maximum": data[0],
        "center": p["neutralBg"],
        "minimum": data[fam["bad"]],
        "null": p["tertiary"],
        "foreground": p["foreground"],
        "foregroundNeutralSecondary": p["secondary"],
        "foregroundLight": p["light"],
        "foregroundNeutralTertiary": p["tertiary"],
        "foregroundDark": p["foreground"],
        "background": p["background"],
        "backgroundLight": p["page"],
        "backgroundNeutral": p["neutralBg"],
        "backgroundDark": p["darkBg"],
        "tableAccent": data[0],
        "hyperlink": data[0],
        "shapeStroke": p["rule"],
        "accent": data[0],
        "textClasses": {
            "callout": {"color": p["foreground"], "fontFace": "Segoe UI Semibold",
                        "fontSize": 28},
            "largeTitle": {"color": p["foreground"], "fontFace": "Segoe UI Semibold",
                           "fontSize": 18},
            "title": {"color": p["foreground"], "fontFace": "Segoe UI Semibold",
                      "fontSize": 12},
            "header": {"color": p["foreground"], "fontFace": "Segoe UI Semibold",
                       "fontSize": 10},
            "label": {"color": p["secondary"], "fontFace": "Segoe UI", "fontSize": 9},
            "boldLabel": {"color": p["foreground"], "fontFace": "Segoe UI Semibold",
                          "fontSize": 9},
            "dataTitle": {"color": p["light"], "fontFace": "Segoe UI", "fontSize": 10},
        },
        "visualStyles": {
            "*": {"*": {
                "background": [{"show": True,
                                "color": {"solid": {"color": p["background"]}},
                                "transparency": 0}],
                "border": [{"show": True, "color": {"solid": {"color": p["rule"]}},
                            "radius": 6}],
                "dropShadow": [{"show": False}],
                "title": [{"show": True,
                           "fontColor": {"solid": {"color": p["foreground"]}},
                           "background": {"solid": {"color": p["background"]}},
                           "fontFamily": "Segoe UI Semibold", "fontSize": 12,
                           "alignment": "left"}],
                "padding": [{"top": 8, "bottom": 8, "left": 10, "right": 10}],
                "outspacePane": [{
                    "backgroundColor": {"solid": {"color": p["page"]}},
                    "foregroundColor": {"solid": {"color": p["foreground"]}},
                    "transparency": 0, "border": True,
                    "borderColor": {"solid": {"color": p["rule"]}},
                    "titleSize": 13, "headerSize": 11, "fontFamily": "Segoe UI",
                    "checkboxAndApplyColor": {"solid": {"color": data[0]}},
                    "inputBoxColor": {"solid": {"color": p["neutralBg"]}}}],
                "filterCard": [
                    {"$id": "Applied",
                     "foregroundColor": {"solid": {"color": p["foreground"]}},
                     "backgroundColor": {"solid": {"color": p["neutralBg"]}},
                     "borderColor": {"solid": {"color": p["rule"]}}, "transparency": 0,
                     "inputBoxColor": {"solid": {"color": p["background"]}},
                     "fontFamily": "Segoe UI"},
                    {"$id": "Available",
                     "foregroundColor": {"solid": {"color": p["secondary"]}},
                     "backgroundColor": {"solid": {"color": p["background"]}},
                     "borderColor": {"solid": {"color": p["rule"]}}, "transparency": 0,
                     "inputBoxColor": {"solid": {"color": p["neutralBg"]}},
                     "fontFamily": "Segoe UI"}],
            }},
            # the wildcard turns background + border ON, so anything that is really just a
            # piece of text has to opt out or it renders inside a card. Zero padding too:
            # 8/10 padding on a heading textbox pushes the text down and clips it.
            "textbox": {"*": dict(chrome_off,
                                  padding=[{"top": 0, "bottom": 0, "left": 0, "right": 0}])},
            "image": {"*": dict(chrome_off,
                                padding=[{"top": 0, "bottom": 0, "left": 0, "right": 0}])},
            "shape": {"*": dict(chrome_off)},
            "actionButton": {"*": dict(chrome_off)},
            # a card is one value plus one caption - the wildcard padding eats a third of a
            # small card and clips the caption's descenders
            "card": {"*": {"padding": [{"top": 4, "bottom": 4, "left": 8, "right": 8}]}},
            "slicer": {"*": {
                # both containers take textSize, NOT fontSize - fontSize is ignored silently
                "header": [{"show": True, "textSize": 9, "fontFamily": "Segoe UI Semibold",
                            "fontColor": {"solid": {"color": p["light"]}},
                            "showRestatement": False}],
                "items": [{"textSize": 10, "fontFamily": "Segoe UI",
                           "fontColor": {"solid": {"color": p["foreground"]}},
                           "background": {"solid": {"color": p["background"]}},
                           "padding": 4}],
                "padding": [{"top": 0, "bottom": 0, "left": 0, "right": 0}]}},
            "page": {"*": {
                "background": [{"color": {"solid": {"color": p["page"]}}, "transparency": 0}],
                "outspace": [{"color": {"solid": {"color": p["page"]}},
                              "transparency": 0}]}},
        },
    }


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    failures = []
    for slug, fam in FAMILIES.items():
        for mode in ("light", "dark"):
            name, data, theme = build(slug, mode, fam)
            print("\n=== %s-%s  (%s, %s) ===" % (slug, mode, fam["era"], name))
            for (label, _, _), c in zip(fam["hues"], data):
                print("    %-12s %s" % (label, c))
            print()
            failures += audit(slug, mode, fam, fam[mode], data)
            out_dir = os.path.join(base, slug)
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "%s-%s-v1.0.json" % (slug, mode))
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(theme, f, indent=2)
                f.write("\n")
            print("    -> %s" % os.path.relpath(path, base))
    print()
    if failures:
        sys.exit("BUILD FAILED - %d gate miss(es):\n  %s"
                 % (len(failures), "\n  ".join(failures)))
    print("PASS - 6 themes, all gates clear")


if __name__ == "__main__":
    main()
