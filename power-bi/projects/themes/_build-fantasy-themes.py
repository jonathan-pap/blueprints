"""Generate the fantasy / flavor theme family for the Grand Exchange.

Sibling to `_build-theme-library.py` (the accessibility-reference library). Same
4-layer color system + text classes + clean wildcard defaults, but each theme
carries a BESPOKE surface palette (parchment, obsidian, royal navy) instead of
the generic light/dark grays — that's what makes them feel themed. Data colors
are intentionally richer/warmer than the reference set; these are flavor themes,
not accessibility references.

Output: projects/themes/<slug>/<slug>-v1.0.json
"""
import json
import os

SCHEMA = "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json"

# Each spec carries its own surface `palette` (keys mirror the reference
# library's LIGHT/DARK dicts): background = container surface, page = ambient
# canvas, neutralBg/darkBg = deeper surfaces, foreground/secondary/light/
# tertiary = text ink ramp, rule = borders/gridlines.
THEMES = {
    "parchment-ledger": {
        "name": "Parchment Ledger",
        "mode": "light",
        # Aged merchant's ledger: cream parchment canvas, dark sepia ink.
        "palette": {
            "background": "#F7EDD7", "page": "#E9DABA", "neutralBg": "#E0CFA8", "darkBg": "#D4BE8E",
            "foreground": "#3A2A18", "secondary": "#5C4630", "light": "#8A6E4E", "tertiary": "#A88C68",
            "rule": "#C9AE82",
        },
        # gold-leaf, wax-seal crimson, royal blue, forest, copper, plum, teal, umber
        "data": ["#B8860B", "#9E2B25", "#2E5E8C", "#3E7A4F", "#C06A2C", "#6B4A8A", "#2A8A86", "#7A5230"],
        "good": "#3E7A4F", "bad": "#9E2B25", "neutral": "#8A6E4E",
    },
    "emerald-guild": {
        "name": "Emerald Guild",
        "mode": "light",
        # Ranger/druid guild hall: pale moss-green parchment, deep forest ink.
        "palette": {
            "background": "#F2F5EC", "page": "#E4EADB", "neutralBg": "#D7E0C9", "darkBg": "#C6D2B2",
            "foreground": "#1E2C1A", "secondary": "#3C4F33", "light": "#6A7C5C", "tertiary": "#8A9B7B",
            "rule": "#C0CDAC",
        },
        # emerald, bronze, deep teal, gold, oak, berry, sky, plum
        "data": ["#2F7A4F", "#A9772F", "#1F6E6A", "#C9A227", "#7A5A33", "#9C3B5A", "#3E6FA3", "#6B4A8A"],
        "good": "#2F7A4F", "bad": "#9C3B5A", "neutral": "#6A7C5C",
    },
    "dragonhoard": {
        "name": "Dragonhoard (Dark)",
        "mode": "dark",
        # Treasure pile in a dragon's lair: warm obsidian stone, parchment text.
        "palette": {
            "background": "#1C1812", "page": "#15110C", "neutralBg": "#262019", "darkBg": "#100D09",
            "foreground": "#F5ECD8", "secondary": "#D8C9A8", "light": "#A89878", "tertiary": "#897B5E",
            "rule": "#3A3024",
        },
        # molten gold, ember, ruby, emerald, sapphire, amethyst
        "data": ["#E0A100", "#E8662A", "#D1344B", "#2BA56B", "#3E84D6", "#9B5FD0"],
        "good": "#2BA56B", "bad": "#D1344B", "neutral": "#897B5E",
    },
    "royal-arcanum": {
        "name": "Royal Arcanum (Dark)",
        "mode": "dark",
        # Regal treasury vault: deep royal navy/violet, jewel + gold accents.
        "palette": {
            "background": "#181A2E", "page": "#121327", "neutralBg": "#21243F", "darkBg": "#0D0E1D",
            "foreground": "#EDEBFB", "secondary": "#C9C6E8", "light": "#9A97C4", "tertiary": "#7E7BA8",
            "rule": "#33365A",
        },
        # royal gold, arcane violet, sapphire, jade, rose, periwinkle
        "data": ["#E8C24A", "#7B5BD6", "#3E84D6", "#2BA58A", "#D14B7A", "#5B7FE0"],
        "good": "#2BA58A", "bad": "#D14B7A", "neutral": "#7E7BA8",
    },
    "gilded-arcanum": {
        "name": "Gilded Arcanum (Dark)",
        "mode": "dark",
        # "Dark Fantasy UI" — ornate gold line-art on a deep navy-black canvas
        # with an arcane blue glow. Gold text, bright-gold container borders.
        "palette": {
            "background": "#0E1A2E", "page": "#070C16", "neutralBg": "#16243C", "darkBg": "#050810",
            "foreground": "#E7D29A", "secondary": "#C9A24A", "light": "#A6873F", "tertiary": "#7E6634",
            "rule": "#B8923C",
        },
        # gold (hero), arcane blue (the glow), rune teal, copper, amethyst,
        # wax-seal crimson, champagne, antique bronze
        "data": ["#D9B96A", "#4F86CF", "#3FA9A0", "#C9712D", "#9B6FD0", "#C24A4A", "#E7D49A", "#7A6535"],
        "good": "#3FA9A0", "bad": "#C24A4A", "neutral": "#A6873F",
    },
}


def build(spec):
    p = spec["palette"]
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
