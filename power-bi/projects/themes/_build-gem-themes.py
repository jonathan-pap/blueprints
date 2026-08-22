#!/usr/bin/env python3
"""Build the dark-gem set: dark-ruby re-hued into gold, emerald, sapphire, amethyst, onyx.

dark-ruby is the template, not the inspiration. Its 40 visualStyles, its typography and its
whole surface stack are cloned verbatim; only the hue-carrying roles are re-solved. That is
deliberate - the point of a set is that a report can swap between them and change nothing but
its colour.

THE ONE RULE: every re-hued slot keeps dark-ruby's relative luminance, exactly.

Hue rotation alone does not survive contact with human vision - a green at the same HSL
lightness as a red is far brighter, so a naive rotation makes some variants glare and others
sink. So each slot's target is dark-ruby's measured luminance, and HSL lightness is
binary-searched until the new hue hits it (shedding saturation only when a hue cannot reach
the target at full chroma - a saturated blue simply cannot be light). Every variant therefore
inherits dark-ruby's exact contrast behaviour: same ratios against the same surfaces, same
ladder, no re-checking per theme.

WHAT IS NOT CLAIMED. This is a flavour set, not an accessibility set. Each theme is a
near-monochrome ramp, so its series do NOT separate in greyscale or under colour-vision
deficiency - dark-ruby's leading four separate by only 1.14:1 in luminance, and the variants
inherit that by construction. Measured and printed by the audit below rather than papered
over. For a categorical palette that survives a mono printout or CVD, use the era set
(_build-era-themes.py) or okabe-ito.

The gates that ARE enforced, because dark-ruby clears them and a variant that did not would be
a regression: text ink >= 4.5:1 and data fills >= 3:1, against both the page and the panel.

Usage:
    python _build-gem-themes.py            # write all families
    python _build-gem-themes.py --check    # audit only, write nothing
"""
import argparse
import colorsys
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "dark-ruby", "dark-ruby.json")

SCHEMA = ("https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/"
          "Report%20Theme%20JSON%20Schema/reportThemeSchema-2.152.json")

VERSION = "v1.0"

# Surfaces + true neutrals + the red/green semantics are carried over untouched. Everything
# else in the file is hue-bearing and gets re-solved.
KEEP = {
    "#1A1A1A",  # page background
    "#121212",  # outspace (filter pane outer)
    "#1E1E1E",  # tooltip / outspacePane / input box
    "#222222",  # decomposition-tree nodes
    "#2A2A2A",  # visual card background - what most ink actually sits on
    "#333333",  # alternating row
    "#3A3A3A",  # border
    "#F7F3EE",  # foreground ink
    "#CC0000",  # bad / minimum
    "#6FBF73",  # good / maximum
}

# Roles that carry hue. Each is re-solved onto the family's hue at dark-ruby's own luminance.
#   data   - the ten series colours + the primary accent + the table accent
#   tint   - axis labels, gridlines, the tinted filter card: the gem hue at low chroma
#   metal  - header/label ink and the neutral semantic: the second, warmer accent
TINT_ROLES = ["#BC9B9C", "#6B5858", "#2A1A1A"]
METAL_ROLES = ["#CCAA80", "#E6C4A3", "#A68B7A"]
ACCENT_ROLES = ["#990000"]           # tableAccent; #F54651 is dataColors[0], handled with the ramp

GOLD = 35        # the warm metal dark-ruby pairs with its red, reused across the set
PEWTER = 210     # dark-gold needs a cool metal instead, or its ink vanishes into its data

FAMILIES = {
    "dark-gold": dict(
        name="Dark Gold", hue=42, metal=PEWTER, chroma=1.0, metal_chroma=0.45,
        blurb="Gilt on black - amber and old gold, with cool pewter ink so the text does not "
              "dissolve into the data."),
    "dark-emerald": dict(
        name="Dark Emerald", hue=152, metal=GOLD, chroma=1.0, metal_chroma=1.0,
        blurb="Emerald and gold, the oldest pairing there is - deep green glass over black, "
              "warm gilt lettering."),
    "dark-sapphire": dict(
        name="Dark Sapphire", hue=214, metal=GOLD, chroma=1.0, metal_chroma=1.0,
        blurb="Cold blue fire. The most restrained of the coloured four: blue reads as "
              "recessive, so dense dashboards stay calm."),
    "dark-amethyst": dict(
        name="Dark Amethyst", hue=278, metal=GOLD, chroma=0.92, metal_chroma=1.0,
        blurb="Regal violet - the loudest hue in the set, held back slightly on chroma so it "
              "does not vibrate against the black."),
    "dark-onyx": dict(
        name="Dark Onyx", hue=GOLD, metal=GOLD, chroma=0.0, metal_chroma=1.0,
        blurb="The restrained one. Silver ramp, no hue in the series at all - colour appears "
              "only where it means something (good / bad). For dense or analytical pages."),
}


# --------------------------------------------------------------------------- colour maths
# Lifted from _build-era-themes.py so the two generators agree to the last digit.
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


def hsl_of(h):
    r, g, b = srgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss, ll


def solve(hue, sat, target):
    """Hex at `hue` whose relative luminance is `target`.

    Binary-searches HSL lightness. A saturated blue cannot reach a high luminance, so when the
    hue tops out below target the saturation steps down and the search restarts: the ladder is
    honoured and the hue gives up only as much chroma as it must.
    """
    s = sat
    for _ in range(24):
        if lum_rgb(hsl_rgb(hue, s, 0.995)) >= target:
            lo, hi = 0.0, 0.995
            for _ in range(48):
                mid = (lo + hi) / 2
                if lum_rgb(hsl_rgb(hue, s, mid)) < target:
                    lo = mid
                else:
                    hi = mid
            return hexof(hsl_rgb(hue, s, (lo + hi) / 2))
        s -= 0.04
        if s <= 0:
            break
    return hexof(hsl_rgb(hue, 0, 0.5))


def signed_offset(h, base):
    """Hue delta in (-180, 180]. dark-ruby straddles 0 degrees, so plain subtraction lies."""
    d = (h - base) % 360
    return d - 360 if d > 180 else d


def chroma(hexv):
    """CIELAB C*. Pinning luminance costs chroma in the hues that cannot be both light and
    saturated, and this is the number that says how much - reported so the trade-off is
    visible instead of assumed."""
    r, g, b = linear(srgb(hexv))
    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x / 0.95047), f(y), f(z / 1.08883)
    a_, b_ = 500 * (fx - fy), 200 * (fy - fz)
    return (a_ * a_ + b_ * b_) ** 0.5


# --------------------------------------------------------------------------------- mapping
def build_map(fam, ruby):
    """hex -> hex for one family, preserving every source slot's relative luminance."""
    base_h, _, _ = hsl_of(ruby["dataColors"][0])
    out = {}

    def recolour(src_hex, hue_base, chroma):
        h, s, _ = hsl_of(src_hex)
        hue = hue_base + signed_offset(h, base_h)
        return solve(hue, s * chroma, lum(src_hex))

    for c in ruby["dataColors"] + ACCENT_ROLES + TINT_ROLES:
        out[c.upper()] = recolour(c, fam["hue"], fam["chroma"])

    # The metal is the second accent, not a tint of the first, so it keeps its own hue.
    # metal_chroma exists for dark-gold: at dark-ruby's saturations a blue metal comes out as
    # a bright sky blue rather than the intended pewter, and bright blue lettering over gold
    # data is a different theme than the one being asked for.
    for c in METAL_ROLES:
        h, s, _ = hsl_of(c)
        metal_base_h, _, _ = hsl_of("#CCAA80")
        hue = fam["metal"] + signed_offset(h, metal_base_h)
        out[c.upper()] = solve(hue, s * fam.get("metal_chroma", 1.0), lum(c))

    for c in KEEP:
        out[c.upper()] = c
    return out


def remap(node, cmap):
    if isinstance(node, dict):
        return {k: remap(v, cmap) for k, v in node.items()}
    if isinstance(node, list):
        return [remap(v, cmap) for v in node]
    if isinstance(node, str) and node.startswith("#") and len(node) == 7:
        return cmap.get(node.upper(), node)
    return node


# --------------------------------------------------------------------------------- audit
PAGE = "#1A1A1A"
PANEL = "#2A2A2A"          # nearly all ink actually sits on the card, not the page

# Gridlines are structure, not text - dark-ruby puts them at 2.16:1 on purpose.
INK_ROLES = ["#F7F3EE", "#E6C4A3", "#CCAA80", "#BC9B9C"]


def audit(slug, theme, cmap):
    """Returns (list of failures, list of report lines)."""
    fails, lines = [], []

    for src in INK_ROLES:
        got = cmap[src.upper()]
        rp, rg = ratio(got, PANEL), ratio(got, PAGE)
        ok = rp >= 4.5 and rg >= 4.5
        lines.append("    ink   %-8s panel %5.2f  page %5.2f  %s"
                     % (got, rp, rg, "ok" if ok else "FAIL"))
        if not ok:
            fails.append("%s: ink %s is %.2f:1 on panel / %.2f:1 on page, needs 4.5"
                         % (slug, got, rp, rg))

    worst_fill = 99.0
    for i, c in enumerate(theme["dataColors"]):
        rp, rg = ratio(c, PANEL), ratio(c, PAGE)
        worst_fill = min(worst_fill, rp, rg)
        if min(rp, rg) < 3.0:
            fails.append("%s: dataColors[%d] %s is %.2f:1 on panel / %.2f:1 on page, needs 3.0"
                         % (slug, i, c, rp, rg))
    lines.append("    fills worst against either surface: %.2f:1 (need 3.00)" % worst_fill)

    # Measured, never gated: a single-hue ramp cannot separate without hue.
    lead = theme["dataColors"][:4]
    worst_grey = 99.0
    for i in range(len(lead)):
        for j in range(i + 1, len(lead)):
            lo, hi = sorted([lum(lead[i]), lum(lead[j])])
            worst_grey = min(worst_grey, (hi + 0.05) / (lo + 0.05))
    lines.append("    greyscale separation, leading four: %.2f:1 (reported, not gated)" % worst_grey)

    cs = [chroma(c) for c in theme["dataColors"]]
    lines.append("    chroma C* lead %.1f  mean %.1f (dark-ruby: lead 74.5, mean 40.6)"
                 % (cs[0], sum(cs) / len(cs)))
    return fails, lines


# --------------------------------------------------------------------------------- build
def build(slug, fam, ruby, write):
    cmap = build_map(fam, ruby)
    theme = remap(ruby, cmap)
    theme["name"] = fam["name"]

    # dark-ruby ships without a $schema; the variants do not repeat that. Rebuilt as an
    # ordered dict so $schema lands first, which is what gives Desktop and editors their
    # validation and autocomplete.
    ordered = {"$schema": SCHEMA}
    ordered.update({k: v for k, v in theme.items() if k != "$schema"})

    fails, lines = audit(slug, ordered, cmap)
    print("  %s (%s)" % (slug, fam["name"]))
    for line in lines:
        print(line)
    print("    palette " + " ".join(ordered["dataColors"]))

    if fails:
        for f in fails:
            print("    FAIL " + f)
        return fails

    if write:
        folder = os.path.join(HERE, slug)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "%s-%s.json" % (slug, VERSION))
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(ordered, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        write_notes(folder, slug, fam, ordered, cmap)
        print("    wrote %s" % os.path.relpath(path, HERE))
    return []


def write_notes(folder, slug, fam, theme, cmap):
    d = theme["dataColors"]
    rows = "\n".join(
        "| %d | `%s` | %5.2f:1 | %5.2f:1 |" % (i, c, ratio(c, PANEL), ratio(c, PAGE))
        for i, c in enumerate(d))
    ink = "\n".join(
        "| %s | `%s` | %5.2f:1 |" % (lbl, cmap[src.upper()], ratio(cmap[src.upper()], PANEL))
        for lbl, src in [("foreground", "#F7F3EE"), ("label", "#E6C4A3"),
                         ("header / axis line", "#CCAA80"), ("axis + legend label", "#BC9B9C"),
                         ("gridline", "#6B5858")])
    lead = d[:4]
    worst_grey = min(
        (max(lum(lead[i]), lum(lead[j])) + 0.05) / (min(lum(lead[i]), lum(lead[j])) + 0.05)
        for i in range(len(lead)) for j in range(i + 1, len(lead)))

    body = """# {name}

{blurb}

Generated by [`../_build-gem-themes.py`](../_build-gem-themes.py) from
[`../dark-ruby/dark-ruby.json`](../dark-ruby/dark-ruby.json). Do not hand-edit - re-run the
generator.

## What was kept and what changed

Everything structural is dark-ruby's: all 40 `visualStyles`, the DM Sans / Segoe UI type stack,
the surface stack (`#1A1A1A` page, `#2A2A2A` card, `#3A3A3A` border), the white ink, and the
`good` / `bad` semantics. Only the hue-bearing roles were re-solved.

Each re-hued slot **keeps dark-ruby's relative luminance exactly**. Rotating hue alone would not
survive contact with vision - a green at the same HSL lightness as a red is far brighter - so
lightness is binary-searched per slot until the new hue matches the original's luminance,
shedding chroma only where a hue cannot reach the target. The practical result: this theme has
the same contrast behaviour as dark-ruby, ratio for ratio.

## Palette

Data hue {hue} degrees, metal (header + label ink) {metal} degrees.

| # | Colour | vs card `#2A2A2A` | vs page `#1A1A1A` |
|---|---|---|---|
{rows}

## Ink

| Role | Colour | vs card |
|---|---|---|
{ink}

The gridline is deliberately low-contrast - it is structure, not text, and dark-ruby sets it at
2.16:1 for the same reason.

## What this theme is not

**A categorical palette.** It is a near-monochrome ramp, so the series separate by lightness and
hue-family only. Greyscale separation across the leading four is **{grey:.2f}:1** - print this on
a mono printer, or view it with deuteranopia, and the series will not be reliably tellable apart.
dark-ruby measures 1.14:1 on the same test; the ramp is the design, not a defect.

Use it where colour is atmosphere and the series are distinguished by position or label - KPI
rows, ranked bars, a single-series trend. For a palette that has to survive a mono printout or
colour-vision deficiency, use [`../runeforge/`](../runeforge/), [`../meridian/`](../meridian/) or
[`../okabe-ito/`](../okabe-ito/).

{semantic}

## Apply it

```bash
pbir theme serialize {slug}-{version}.json -o /tmp/{slug}.Theme
pbir theme build /tmp/{slug}.Theme -o "<project>.Report" -f --clean
```
""".format(name=fam["name"], blurb=fam["blurb"], hue=fam["hue"], metal=fam["metal"],
           rows=rows, ink=ink, grey=worst_grey, slug=slug, version=VERSION,
           semantic=semantic_note(slug))

    with io.open(os.path.join(folder, "notes.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)


def semantic_note(slug):
    if slug == "dark-emerald":
        return ("**One caveat specific to this theme.** `good` is `#6FBF73`, a green, and the\n"
                "series are also green. On a page that uses conditional formatting for good/bad,\n"
                "bind the semantic colours to something the series cannot be confused with, or\n"
                "pick another family. The clash is inherited from dark-ruby's own structure,\n"
                "where `bad` is red and so are the series.")
    if slug == "dark-onyx":
        return ("Because the series carry no hue at all, `good` and `bad` are the only colour on\n"
                "the page. That is the point of this variant - it makes a status read as status.")
    return ""


# --------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="audit only, write nothing")
    ap.add_argument("--only", help="build a single family by slug")
    args = ap.parse_args()

    ruby = json.load(io.open(TEMPLATE, encoding="utf-8-sig"))
    print("template: dark-ruby, %d visualStyles, %d dataColors"
          % (len(ruby["visualStyles"]), len(ruby["dataColors"])))

    all_fails = []
    for slug, fam in FAMILIES.items():
        if args.only and slug != args.only:
            continue
        all_fails += build(slug, fam, ruby, write=not args.check)

    if all_fails:
        print("\n%d gate failure(s) - nothing written for the failing families." % len(all_fails))
        return 1
    print("\nall families pass: ink >= 4.5:1 and fills >= 3:1 against both surfaces")
    return 0


if __name__ == "__main__":
    sys.exit(main())
