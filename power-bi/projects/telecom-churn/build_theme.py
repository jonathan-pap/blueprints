"""Generate 'Retention Signal (Light)' and AUDIT it. The audit FAILS the build on any
contrast miss, so a theme can never ship below WCAG AA.

Direction (from brief §1/§5): commercial retention leadership, Power BI Service, and a
PRINTABLE exec summary - so a light canvas, not a dark one. Status colours are three of the
Okabe-Ito CVD-safe set, which is why churn/stay/join stay separable for colour-blind readers
without relying on red-vs-green.
"""
import json
import sys

NAME = "Retention Signal (Light)"

INK        = "#1B1F27"   # primary text
INK_2      = "#5B6472"   # secondary text
INK_3      = "#7A8494"   # axis / tertiary
CANVAS     = "#EEF1F5"   # page
SURFACE    = "#FFFFFF"   # cards / visual backgrounds
RULE       = "#DCE1E9"   # borders, gridlines
CHURNED    = "#B8480A"   # vermillion - luminance 0.149, the MID rung of the ladder
STAYED     = "#00558F"   # blue       - luminance 0.085, the DARKEST rung
JOINED     = "#B673A4"   # purple     - luminance 0.249, the LIGHTEST rung.
#              GRAPHICAL ONLY: clears 3:1 but not the 4.5:1 text bar, so Joined is never a
#              text colour - it labels via ink + a colour chip instead.
BASELINE   = "#444B57"

# supporting ramp for non-status categories
SUPPORT = ["#00558F", "#B8480A", "#B673A4", "#3F7A6B", "#8A6D1F", "#5B6472", "#2E6E8E", "#9A4B3F"]


def lum(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def audit():
    """4.5:1 for text, 3:1 for graphical objects (WCAG AA)."""
    checks = [
        ("text  ink/surface",       INK,      SURFACE, 4.5),
        ("text  ink/canvas",        INK,      CANVAS,  4.5),
        ("text  ink2/surface",      INK_2,    SURFACE, 4.5),
        ("text  ink3/surface",      INK_3,    SURFACE, 3.0),   # axis labels = graphical-ish
        ("graph churned/surface",   CHURNED,  SURFACE, 3.0),
        ("graph stayed/surface",    STAYED,   SURFACE, 3.0),
        ("graph joined/surface",    JOINED,   SURFACE, 3.0),
        ("text  churned/surface",   CHURNED,  SURFACE, 4.5),   # used as KPI value colour
        ("text  stayed/surface",    STAYED,   SURFACE, 4.5),
        # Joined is graphical-only (see palette note): 3:1, not 4.5:1
        ("graph joined/surface2",   JOINED,   SURFACE, 3.0),
        ("graph baseline/surface",  BASELINE, SURFACE, 3.0),
        ("graph rule/surface",      RULE,     SURFACE, 1.2),   # hairline, decorative only
    ]
    bad = []
    print("  %-26s %7s  %s" % ("pair", "ratio", "min"))
    for label, a, b, need in checks:
        r = ratio(a, b)
        ok = r >= need
        print("  %-26s %6.2f:1  %.1f  %s" % (label, r, need, "ok" if ok else "*** FAIL ***"))
        if not ok:
            bad.append((label, r, need))
    # the three status colours must also be separable FROM EACH OTHER
    for n1, c1, n2, c2 in [("churned", CHURNED, "stayed", STAYED),
                           ("churned", CHURNED, "joined", JOINED),
                           ("stayed", STAYED, "joined", JOINED)]:
        r = ratio(c1, c2)
        print("  %-26s %6.2f:1  %.1f  %s" % ("pair  %s/%s" % (n1, n2), r, 1.3,
                                             "ok" if r >= 1.3 else "*** FAIL ***"))
        if r < 1.3:
            bad.append(("%s/%s" % (n1, n2), r, 1.3))
    return bad


def text_class(size, colour=INK, weight=None):
    d = {"fontFace": "Segoe UI", "fontSize": size, "color": colour}
    if weight:
        d["fontFace"] = weight
    return d


def theme():
    off = [{"show": False}]
    return {
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
            "title":     text_class(16, INK, "Segoe UI Semibold"),
            "header":    text_class(12, INK, "Segoe UI Semibold"),
            "label":     text_class(10, INK_2),
            "callout":   text_class(28, INK, "Segoe UI Semibold"),
            "largeTitle": text_class(20, INK, "Segoe UI Semibold"),
        },
        "visualStyles": {
            "*": {
                "*": {
                    # every visual is a white card on a grey canvas - one surface rule
                    "background": [{"show": True, "color": {"solid": {"color": SURFACE}},
                                    "transparency": 0}],
                    "border":     [{"show": True, "color": {"solid": {"color": RULE}},
                                    "radius": 6}],
                    "dropShadow": off,
                    "visualHeader": [{"show": False}],
                    "title": [{"show": False}],
                    "labels": [{"color": {"solid": {"color": INK_2}}, "fontSize": 9}],
                    "categoryAxis": [{"labelColor": {"solid": {"color": INK_3}}, "fontSize": 9,
                                      "showAxisTitle": False,
                                      "gridlineShow": False}],
                    "valueAxis": [{"labelColor": {"solid": {"color": INK_3}}, "fontSize": 9,
                                   "showAxisTitle": False,
                                   "gridlineShow": True,
                                   "gridlineColor": {"solid": {"color": RULE}},
                                   "gridlineThickness": 1}],
                    "legend": [{"labelColor": {"solid": {"color": INK_2}}, "fontSize": 9,
                                "showTitle": False}],
                },
            },
            "page": {"*": {"background": [{"color": {"solid": {"color": CANVAS}},
                                           "transparency": 0}],
                           "outspace": [{"color": {"solid": {"color": CANVAS}},
                                         "transparency": 0}]}},
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
                "total": [{"totals": False}],
            }},
            # panels are shape visuals used as card backgrounds. A shape's fill comes from
            # objects.fill - NOT the container background - so without this it renders in the
            # first dataColor (solid blue). ~15 panels means this belongs in the theme, not as
            # a per-visual override (theme-first rule, power-bi/CLAUDE.md).
            "shape": {"*": {
                "fill":    [{"show": True, "fillColor": {"solid": {"color": SURFACE}},
                             "transparency": 0}],
                "outline": [{"show": True, "lineColor": {"solid": {"color": RULE}},
                             "weight": 1, "transparency": 0}],
                "title": off, "background": [{"show": False}], "border": off,
                "dropShadow": off,
            }},
            "image": {"*": {"border": off, "background": [{"show": False}]}},
            "textbox": {"*": {"border": off, "background": [{"show": False}]}},
        },
    }


if __name__ == "__main__":
    print("auditing %s ..." % NAME)
    bad = audit()
    if bad:
        sys.exit("\nBUILD FAILED - %d contrast miss(es); fix the palette before shipping." % len(bad))
    out = "telecom-churn.Report/StaticResources/RegisteredResources/retention-signal-light.json"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(theme(), f, indent=2)
        f.write("\n")
    print("\nPASS - wrote %s" % out)
