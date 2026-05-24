"""Generate a library of 5 best-practice Power BI theme JSONs.

Each theme is grounded in a recognized, well-tested color palette and follows the
4-layer color system (data → semantic → fg/bg variants → accents) plus text
classes and clean wildcard visual defaults. Light themes use a white canvas;
the one dark theme flips fg/bg.

Output: projects/themes/<slug>/<slug>-v1.0.json
"""
import json
import os

SCHEMA = "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json"

LIGHT = {
    "background": "#FFFFFF", "page": "#F7F8FA", "neutralBg": "#EEF0F3", "darkBg": "#E2E5EA",
    "foreground": "#1A1C20", "secondary": "#4D5159", "light": "#7A7F88", "tertiary": "#9AA0AA",
    "rule": "#E2E5EA",
}
DARK = {
    "background": "#14161E", "page": "#0F111A", "neutralBg": "#1B1E2A", "darkBg": "#0A0C12",
    "foreground": "#F3F4F8", "secondary": "#D2D5DE", "light": "#A9AEBC", "tertiary": "#8A8FA0",
    "rule": "#2A2E3C",
}

THEMES = {
    "okabe-ito": {
        "name": "Okabe-Ito",
        "mode": "light",
        "data": ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#56B4E9", "#CC79A7", "#F0E442", "#000000"],
        "good": "#009E73", "bad": "#D55E00", "neutral": "#999999",
    },
    "tableau10": {
        "name": "Tableau 10",
        "mode": "light",
        "data": ["#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#76B7B2", "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"],
        "good": "#59A14F", "bad": "#E15759", "neutral": "#BAB0AC",
    },
    "brewer-set2": {
        "name": "ColorBrewer Set2",
        "mode": "light",
        "data": ["#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3"],
        "good": "#66C2A5", "bad": "#FC8D62", "neutral": "#B3B3B3",
    },
    "ibcs-neutral": {
        "name": "IBCS Neutral",
        "mode": "light",
        "data": ["#404040", "#1F6FB2", "#7F7F7F", "#A6A6A6", "#595959", "#BFBFBF", "#8C8C8C", "#D9D9D9"],
        "good": "#2E7D32", "bad": "#C62828", "neutral": "#7F7F7F",
    },
    "viridis": {
        "name": "Viridis (Dark)",
        "mode": "dark",
        "data": ["#FDE725", "#7AD151", "#22A884", "#2A788E", "#414487", "#440154"],
        "good": "#7AD151", "bad": "#FD9A6A", "neutral": "#8A8FA0",
    },
}


def build(spec):
    p = LIGHT if spec["mode"] == "light" else DARK
    data = spec["data"]
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
                }
            },
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
    for slug, spec in THEMES.items():
        out_dir = os.path.join(base, slug)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{slug}-v1.0.json")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(build(spec), f, indent=2)
        print(f"  wrote {slug}/{slug}-v1.0.json  ({spec['mode']}, {len(spec['data'])} data colors)")
    print("done.")


if __name__ == "__main__":
    main()
