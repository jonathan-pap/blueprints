"""Generate the Spectrum (Light) theme and AUDIT it. Fails the build on any miss.

Direction: futuristic telecom. The palette is fibre and radio spectrum - cyan-teal for a
connected line, deep magenta for a dropped one, electric violet for a new signal - on a cool
near-white canvas. Light rather than dark because the audience is Power BI Service plus a
PRINTABLE exec summary (brief section 1).

Three constraints, all MEASURED rather than eyeballed:
  1. WCAG contrast - 4.5:1 for text, 3:1 for graphical objects
  2. greyscale - mutual luminance ratio >= 1.3, so status survives a mono printout
  3. colour blindness - pairwise separation under simulated deuteranopia AND protanopia
     (Vienot 1999). This one mattered: orange-vs-blue is the safest possible pair, which is
     why Okabe-Ito uses it, so dropping vermillion had to be PROVEN not assumed. Measured
     worst pair here is 0.219 against 0.228 for the vermillion palette - a 4 percent give,
     not a real loss. CVD_MIN sits just under that so a later edit cannot quietly slide the
     palette toward indistinguishable.
"""
import json
import sys

NAME = "Spectrum Light v1.1"
# NOTE: Power BI Desktop caches theme JSON BY FILENAME. Rewriting the same file does not
# take effect - bump the version to force a reload. That is also why the naming convention
# is versioned (where-themes-live.md).
OUT = "telecom-churn.Report/StaticResources/RegisteredResources/Spectrum-Light-v1.1.json"
SCHEMA = ("https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/"
          "Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json")

INK      = "#0B1020"
INK_2    = "#4A5578"
INK_3    = "#6E7A9C"
CANVAS   = "#F1F4FB"
SURFACE  = "#FFFFFF"
RULE     = "#DEE4F2"
STAYED   = "#0E7490"
CHURNED  = "#9D174D"
JOINED   = "#9575F5"
BASELINE = "#334166"

SUPPORT = [STAYED, CHURNED, JOINED, "#2A6F7F", "#7A2E5B", "#4A5578", "#12867F", "#6B4BC2"]
CVD_MIN = 0.18


def srgb(h):
    return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def linear(c):
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def lum(h):
    r, g, b = linear(srgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


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


def cvd_dist(h1, h2, kind):
    a, b = simulate(h1, kind), simulate(h2, kind)
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def audit():
    bad = []
    print("  %-28s %9s  %s" % ("check", "value", "min"))

    def row(label, got, need, fmt="%7.2f:1"):
        ok = got >= need
        print(("  %-28s " + fmt + "  %.2f  %s")
              % (label, got, need, "ok" if ok else "*** FAIL ***"))
        if not ok:
            bad.append(label)

    for label, a, b, need in [
        ("text  ink / surface", INK, SURFACE, 4.5),
        ("text  ink / canvas", INK, CANVAS, 4.5),
        ("text  ink2 / surface", INK_2, SURFACE, 4.5),
        ("axis  ink3 / surface", INK_3, SURFACE, 3.0),
        ("text  stayed / surface", STAYED, SURFACE, 4.5),
        ("text  churned / surface", CHURNED, SURFACE, 4.5),
        ("graph joined / surface", JOINED, SURFACE, 3.0),
        ("graph baseline / surface", BASELINE, SURFACE, 3.0),
    ]:
        row(label, ratio(a, b), need)
    print()
    pairs = [("stayed", STAYED, "churned", CHURNED),
             ("churned", CHURNED, "joined", JOINED),
             ("stayed", STAYED, "joined", JOINED)]
    for n1, c1, n2, c2 in pairs:
        row("grey  %s / %s" % (n1, n2), ratio(c1, c2), 1.3)
    print()
    for kind in ("deutan", "protan"):
        for n1, c1, n2, c2 in pairs:
            row("%s %s / %s" % (kind, n1, n2), cvd_dist(c1, c2, kind), CVD_MIN, "%9.3f")
    return bad


def tc(size, colour=INK, face="Segoe UI"):
    return {"fontFace": face, "fontSize": size, "color": colour}


def theme():
    off = [{"show": False}]
    return {
        # $schema FIRST key - enables IDE autocomplete and Desktop validation on import
        # (create/schema-integration.md). Versioned GitHub URL is the authoring form.
        "$schema": SCHEMA,
        "name": NAME,
        "dataColors": SUPPORT,
        "foreground": INK,
        "foregroundNeutralSecondary": INK_2,
        "foregroundNeutralTertiary": INK_3,
        "background": SURFACE,
        "backgroundLight": CANVAS,
        "backgroundNeutral": RULE,
        "tableAccent": STAYED,
        "good": STAYED,
        "neutral": INK_2,
        "bad": CHURNED,
        "maximum": CHURNED,
        "center": INK_3,
        "minimum": STAYED,
        "hyperlink": STAYED,
        "textClasses": {
            "title": tc(16, INK, "Segoe UI Semibold"),
            "header": tc(12, INK, "Segoe UI Semibold"),
            "label": tc(10, INK_2),
            "callout": tc(28, INK, "Segoe UI Semibold"),
            "largeTitle": tc(20, INK, "Segoe UI Semibold"),
            "dataTitle": tc(11, INK_2),
        },
        "visualStyles": {
            "*": {"*": {
                "background": [{"show": True, "color": {"solid": {"color": SURFACE}},
                                "transparency": 0}],
                "border": [{"show": True, "color": {"solid": {"color": RULE}}, "radius": 8}],
                "dropShadow": off,
                "visualHeader": [{"show": False}],
                "title": off,
                "labels": [{"color": {"solid": {"color": INK_2}}, "fontSize": 9}],
                "categoryAxis": [{"labelColor": {"solid": {"color": INK_3}}, "fontSize": 9,
                                  "showAxisTitle": False, "gridlineShow": False}],
                "valueAxis": [{"labelColor": {"solid": {"color": INK_3}}, "fontSize": 9,
                               "showAxisTitle": False, "gridlineShow": True,
                               "gridlineColor": {"solid": {"color": RULE}},
                               "gridlineThickness": 1}],
                "legend": [{"labelColor": {"solid": {"color": INK_2}}, "fontSize": 9,
                            "showTitle": False}],
                "padding": [{"top": 8, "bottom": 8, "left": 10, "right": 10}],
                # filter pane, per the checklist - otherwise it keeps Power BI default grey
                "outspacePane": [{"backgroundColor": {"solid": {"color": CANVAS}},
                                  "foregroundColor": {"solid": {"color": INK}},
                                  "borderColor": {"solid": {"color": RULE}},
                                  "transparency": 0, "titleSize": 12, "headerSize": 10,
                                  "fontFamily": "Segoe UI"}],
                "filterCard": [
                    {"$id": "Applied", "backgroundColor": {"solid": {"color": SURFACE}},
                     "foregroundColor": {"solid": {"color": INK}},
                     "borderColor": {"solid": {"color": RULE}},
                     "transparency": 0, "textSize": 10, "fontFamily": "Segoe UI"},
                    {"$id": "Available", "backgroundColor": {"solid": {"color": SURFACE}},
                     "foregroundColor": {"solid": {"color": INK_2}},
                     "borderColor": {"solid": {"color": RULE}},
                     "transparency": 0, "textSize": 10, "fontFamily": "Segoe UI"},
                ],
            }},
            "page": {"*": {
                "background": [{"color": {"solid": {"color": CANVAS}}, "transparency": 0}],
                "outspace": [{"color": {"solid": {"color": CANVAS}}, "transparency": 0}]}},
            "tableEx": {"*": {
                "grid": [{"gridVertical": False, "gridHorizontal": True,
                          "gridHorizontalColor": {"solid": {"color": RULE}},
                          "outlineWeight": 0, "rowPadding": 4}],
                "columnHeaders": [{"fontColor": {"solid": {"color": INK_2}},
                                   "backColor": {"solid": {"color": SURFACE}},
                                   "fontSize": 9, "outline": "BottomOnly"}],
                "values": [{"fontColor": {"solid": {"color": INK}},
                            "backColorPrimary": {"solid": {"color": SURFACE}},
                            "backColorSecondary": {"solid": {"color": SURFACE}},
                            "fontSize": 10}],
                "total": [{"totals": False}]}},
            "image": {"*": {"border": off, "background": [{"show": False}],
                            "padding": [{"top": 0, "bottom": 0, "left": 0, "right": 0}]}},
            # wildcard padding is right for data visuals but clips a textbox used as a
            # heading - it pushed the text down and forced a scroll indicator. Zero it here.
            "textbox": {"*": {"border": off, "background": [{"show": False}],
                              "padding": [{"top": 0, "bottom": 0, "left": 0, "right": 0}]}},
            "actionButton": {"*": {"border": off, "background": [{"show": False}],
                                   "dropShadow": off}},
            "shape": {"*": {"title": off, "background": [{"show": False}],
                            "border": off, "dropShadow": off}},
        },
    }


if __name__ == "__main__":
    print("auditing %s ...\n" % NAME)
    bad = audit()
    if bad:
        sys.exit("\nBUILD FAILED - %d miss(es): %s" % (len(bad), ", ".join(bad)))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(theme(), f, indent=2)
        f.write("\n")
    print("\nPASS - wrote %s" % OUT)
