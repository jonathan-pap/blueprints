"""Generate the space / aerospace theme family.

Sibling to `_build-theme-library.py` (accessibility reference set) and
`_build-fantasy-themes.py` (Grand Exchange flavor set). Same 4-layer color
system, text classes and wildcard defaults, but each theme carries a BESPOKE
surface palette (void indigo, console graphite, cream stock) rather than the
generic light/dark grays.

Built for launch / mission data (see projects/space): the semantic trio maps to
mission outcome — good = Success, bad = Failure, `warn` = Partial Failure. `warn`
is NOT a Power BI theme key, so it is emitted into `dataColors` at a known index
and recorded in each theme's notes.md for conditional-formatting use.

Adds two things the older generators omit, both required by
02-build/theme/create/checklist.md:
  - a `dataTitle` text class
  - container-chrome suppression for textbox / image / shape / actionButton
    (mandatory here because the wildcard turns background + border ON)

Output: projects/themes/<slug>/<slug>-v1.0.json
"""
import json
import os

SCHEMA = "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json"

# palette keys mirror the sibling generators: background = container surface,
# page = ambient canvas, neutralBg/darkBg = deeper surfaces, foreground/
# secondary/light/tertiary = text ink ramp, rule = borders/gridlines.
THEMES = {
    "deep-space": {
        "name": "Deep Space (Dark)",
        "mode": "dark",
        # Long-exposure telescope frame: near-black indigo void, starlight text.
        "palette": {
            "background": "#0F1528", "page": "#070B18", "neutralBg": "#1A2340", "darkBg": "#04070F",
            "foreground": "#E8ECF8", "secondary": "#B9C2DA", "light": "#8892AE", "tertiary": "#6E7896",
            "rule": "#26304F",
        },
        # ion cyan, nebula violet, solar amber, plasma magenta, aurora teal,
        # signal blue, ice, mars rust
        "data": ["#4CC9F0", "#9D7BEA", "#F2A93B", "#E05A8A", "#2DC7A6", "#4F7BE0", "#9FC0E8", "#C96A45"],
        "good": "#2DC7A6", "bad": "#E0555F", "neutral": "#7C87A6", "warn": "#F2A93B",
    },
    "mission-control": {
        "name": "Mission Control (Dark)",
        "mode": "dark",
        # Flight-ops console: graphite panels, phosphor screen text.
        "palette": {
            "background": "#141A18", "page": "#0C0F0E", "neutralBg": "#1E2724", "darkBg": "#070A09",
            "foreground": "#DCE8E2", "secondary": "#B0C0B8", "light": "#82918A", "tertiary": "#6B7A73",
            "rule": "#2A3833",
        },
        # phosphor green, caution amber, CRT cyan, alert red, telemetry blue, tape grey
        "data": ["#4FD98A", "#E8B33C", "#3FC2D6", "#E05C4E", "#5B87D9", "#8A968F"],
        "good": "#4FD98A", "bad": "#E05C4E", "neutral": "#8A968F", "warn": "#E8B33C",
    },
    "starfield-minimal": {
        "name": "Starfield Minimal (Dark)",
        "mode": "dark",
        # Restrained void: silver-forward, one blue accent, color only where it means something.
        "palette": {
            "background": "#111318", "page": "#08090C", "neutralBg": "#1A1D24", "darkBg": "#050609",
            "foreground": "#EDEFF3", "secondary": "#C3C9D4", "light": "#8B93A1", "tertiary": "#6E7787",
            "rule": "#262A33",
        },
        # ion blue, silver, signal amber, slate, pale cyan, indigo slate
        "data": ["#5B9BF5", "#B6BDCA", "#E6A34A", "#6E7787", "#86C6E8", "#566486"],
        "good": "#57B98A", "bad": "#DB5F5F", "neutral": "#6E7787", "warn": "#E6A34A",
    },
    "apollo-retro": {
        "name": "Apollo Retro (Light)",
        "mode": "light",
        # 1960s agency print: cream stock, navy ink, 'worm' orange.
        "palette": {
            "background": "#FFFFFF", "page": "#F4F1EA", "neutralBg": "#EAE5D9", "darkBg": "#DCD5C4",
            # `light` darkened from #6B7280 so dataTitle text clears AA on the cream canvas
            "foreground": "#1C2333", "secondary": "#3E4759", "light": "#656B7A", "tertiary": "#8B919C",
            "rule": "#D8D2C4",
        },
        # worm orange, agency navy, sky blue, gantry grey, module gold, pad green, plum, clay
        # module gold darkened from #C99A2E — 3:1 fill contrast on a white surface
        "data": ["#E0532F", "#21365E", "#3E7CC4", "#6B7280", "#A67C1E", "#3F8A63", "#8C5AA0", "#B0703A"],
        "good": "#3F8A63", "bad": "#C0392B", "neutral": "#6B7280", "warn": "#A67C1E",
    },
}


def _luminance(hex_color):
    """WCAG relative luminance for a #RRGGBB string."""
    c = hex_color.lstrip("#")
    out = []
    for i in (0, 2, 4):
        v = int(c[i:i + 2], 16) / 255
        out.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    r, g, b = out
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    a, b = _luminance(fg), _luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def audit(slug, spec):
    """Report text pairs below WCAG AA (4.5:1) and data fills below 3:1."""
    p = spec["palette"]
    problems = []
    for role in ("foreground", "secondary", "light"):
        for surface in ("background", "page"):
            r = contrast(p[role], p[surface])
            if r < 4.5:
                problems.append(f"text {role} on {surface}: {r:.2f}:1")
    for i, d in enumerate(spec["data"]):
        r = contrast(d, p["background"])
        if r < 3.0:
            problems.append(f"dataColors[{i}] {d} on surface: {r:.2f}:1")
    for label in ("good", "bad", "neutral", "warn"):
        r = contrast(spec[label], p["background"])
        if r < 3.0:
            problems.append(f"{label} {spec[label]} on surface: {r:.2f}:1")
    for problem in problems:
        print(f"    ! {slug}: {problem}")
    return problems


def build(spec):
    p = spec["palette"]
    data = spec["data"]
    chrome_off = {
        "title": [{"show": False}],
        "background": [{"show": False}],
        "border": [{"show": False}],
        "dropShadow": [{"show": False}],
    }
    return {
        "$schema": SCHEMA,
        "name": spec["name"],
        "dataColors": data,
        "good": spec["good"],
        "neutral": spec["neutral"],
        "bad": spec["bad"],
        "maximum": data[0],
        "center": p["neutralBg"],
        "minimum": spec["bad"],
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
            "callout": {"color": p["foreground"], "fontFace": "Segoe UI", "fontSize": 28},
            "title": {"color": p["foreground"], "fontFace": "Segoe UI Semibold", "fontSize": 12},
            "header": {"color": p["foreground"], "fontFace": "Segoe UI Semibold", "fontSize": 10},
            "label": {"color": p["secondary"], "fontFace": "Segoe UI", "fontSize": 9},
            "dataTitle": {"color": p["light"], "fontFace": "Segoe UI", "fontSize": 10},
        },
        "visualStyles": {
            "*": {
                "*": {
                    "background": [{"show": True, "color": {"solid": {"color": p["background"]}}, "transparency": 0}],
                    "border": [{"show": True, "color": {"solid": {"color": p["rule"]}}, "radius": 5}],
                    "dropShadow": [{"show": False}],
                    "title": [{"show": True, "fontColor": {"solid": {"color": p["foreground"]}},
                               "background": {"solid": {"color": p["background"]}},
                               "fontFamily": "Segoe UI Semibold", "fontSize": 12, "alignment": "left"}],
                    "outspacePane": [{"backgroundColor": {"solid": {"color": p["page"]}},
                                      "foregroundColor": {"solid": {"color": p["foreground"]}},
                                      "transparency": 0, "border": True, "borderColor": {"solid": {"color": p["rule"]}},
                                      "titleSize": 13, "headerSize": 11, "fontFamily": "Segoe UI",
                                      "checkboxAndApplyColor": {"solid": {"color": data[0]}},
                                      "inputBoxColor": {"solid": {"color": p["neutralBg"]}}}],
                    "filterCard": [
                        {"$id": "Applied", "foregroundColor": {"solid": {"color": p["foreground"]}},
                         "backgroundColor": {"solid": {"color": p["neutralBg"]}},
                         "borderColor": {"solid": {"color": p["rule"]}}, "transparency": 0,
                         "inputBoxColor": {"solid": {"color": p["background"]}}, "fontFamily": "Segoe UI"},
                        {"$id": "Available", "foregroundColor": {"solid": {"color": p["secondary"]}},
                         "backgroundColor": {"solid": {"color": p["background"]}},
                         "borderColor": {"solid": {"color": p["rule"]}}, "transparency": 0,
                         "inputBoxColor": {"solid": {"color": p["neutralBg"]}}, "fontFamily": "Segoe UI"},
                    ],
                }
            },
            # container chrome would otherwise wrap these in a card + border
            "textbox": {"*": dict(chrome_off)},
            "image": {"*": dict(chrome_off)},
            "shape": {"*": dict(chrome_off)},
            "actionButton": {"*": dict(chrome_off)},
            "page": {
                "*": {
                    "background": [{"color": {"solid": {"color": p["page"]}}, "transparency": 0}],
                    "outspace": [{"color": {"solid": {"color": p["page"]}}, "transparency": 0}],
                }
            },
        },
    }


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    failures = 0
    for slug, spec in THEMES.items():
        out_dir = os.path.join(base, slug)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{slug}-v1.0.json")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(build(spec), f, indent=2)
        print(f"  wrote {slug}/{slug}-v1.0.json  ({spec['mode']}, {len(spec['data'])} data colors)")
        failures += len(audit(slug, spec))
    print(f"done. contrast issues: {failures}")


if __name__ == "__main__":
    main()
