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

Each family builds TWICE.

The FLAVOUR build is the faithful one: a near-monochrome ramp, exactly like dark-ruby. Its
series therefore do NOT separate in greyscale or under colour-vision deficiency - dark-ruby's
leading four separate by only 1.14:1 in luminance, and the variants inherit that by
construction. Measured and printed rather than papered over. Gates: text ink >= 4.5:1 and data
fills >= 3:1 against both surfaces, which is what dark-ruby itself clears.

The A11Y build keeps everything except the thing that cannot survive: an accessible version of
a monochrome theme is not monochrome. Separation for a colour-blind reader has to come from
somewhere, and a single-hue ramp has nowhere to get it. So the gem stays as the LEAD colour and
the rest of the series spread across the hue circle, searched rather than named. It also
replaces dark-ruby's semantics, which do not survive a review - `bad` at 2.44:1 is under the
non-text gate, and red-vs-green is the exact pair both deficiencies collapse. Gates: the
flavour gates PLUS greyscale >= 1.25:1 and CVD >= 0.18 under deuteranopia AND protanopia, with
a 40-degree hue floor so normal vision gets its own separation.

All gates are fatal - a family that misses one is not written.

Usage:
    python _build-gem-themes.py                  # write both builds for every family
    python _build-gem-themes.py --check          # audit only, write nothing
    python _build-gem-themes.py --a11y-only      # skip the flavour builds
    python _build-gem-themes.py --flavour-only   # skip the a11y builds
    python _build-gem-themes.py --only dark-gold # one family
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

# Container corner radius, applied to every radius in the cloned theme (border and
# visualCorners, 11 places). dark-ruby originally shipped 30, which reads as a soft pill on a
# 1280x720 canvas and eats usable area at the corners of small cards. 5 is a crisp panel edge
# that still softens the corner.
CORNER_RADIUS = 6

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

# --------------------------------------------------------------------------- a11y variants
# THE TRADE THE A11Y BUILD MAKES, stated plainly because it cannot be avoided: an accessible
# version of a monochrome theme is not monochrome. Separation for a colour-blind reader has to
# come from somewhere, and in a single-hue ramp there is nowhere for it to come from - which is
# why the flavour set measures 1.14:1 in greyscale and fails CVD outright. So the a11y build
# keeps the gem as the LEAD colour and keeps every surface, ink and type decision, and spreads
# the remaining series across the hue circle. The identity survives in slot 0, the metal ink
# and the black; the monochrome ramp does not.
GREY_MIN = 1.25          # luminance contrast between any two of the gated four
CVD_MIN = 0.18           # RGB distance under simulated deuteranopia AND protanopia
GATED = 4                # how many leading colours the separation gates apply to

# Fills need 3:1 against the CARD (#2A2A2A), which is brighter than the page and therefore sets
# the floor: L >= 0.1695. The era set's dark ladder bottoms out at 0.150 and cannot be reused
# here - its last rung lands at 2.74:1 on this card.
#
# Rungs step by 1.27x rather than exactly 1.25 in (L + 0.05): at 1.25 the measured ratio comes
# out 1.249 and floating point drops it under its own gate.
LADDER_A11Y = {
    # Gated four first, descending - on a dark surface prominence is brightness, so the lead
    # series is the lightest. Then four ungated rungs interleaved through the same band.
    "chromatic": [0.494, 0.378, 0.287, 0.215, 0.430, 0.330, 0.250, 0.190, 0.560, 0.300],
    # Achromatic has only luminance to work with, so it needs a much wider band. Greyscale
    # separation and CVD separation are not the same test and greys are where they come apart:
    # on the chromatic ladder above, four greys measure 0.109 CVD - under the 0.18 gate - even
    # though they are perfectly distinguishable in print. Stretched, they reach 0.278.
    "mono": [0.890, 0.583, 0.351, 0.190, 0.720, 0.460, 0.270, 0.215, 0.800, 0.310],
}

# dark-ruby's own semantics do not survive an accessibility review, so the a11y build replaces
# them rather than inheriting them:
#   bad  #CC0000 sits at 2.44:1 on the card - under the 3:1 non-text gate
#   good #6FBF73 is a true green, and red-vs-green is the exact pair both common deficiencies
#         collapse. Okabe-Ito's answer is orange-vs-bluish-green; this keeps a red hue for
#         normal vision but pushes green to a bluish-green so the pair still separates.
A11Y_SEMANTIC = {"bad": (8, 0.72, 0.215), "good": (168, 0.60, 0.360)}   # hue, sat, luminance

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


# --------------------------------------------------------------- colour-vision simulation
# Viénot, Brettel & Mollon 1999, same transform as _build-era-themes.py.
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


def dist(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def cvd_score(sims, idx):
    """Worst pairwise separation across BOTH deficiencies among the given slots."""
    worst = 99.0
    for i in range(len(idx)):
        for j in range(i + 1, len(idx)):
            for k in (0, 1):
                worst = min(worst, dist(sims[idx[i]][k], sims[idx[j]][k]))
    return worst


# --------------------------------------------------------------------- a11y palette search
HUE_STEP = 3
SATS = (0.45, 0.60, 0.75)

# Minimum hue angle between any two of the gated four.
#
# The CVD and greyscale metrics do not enforce this and cannot: a light gold and a dark gold
# separate perfectly on both, because both tests reward the luminance gap. The first run of this
# search duly put two golds in dark-gold's gated four and two greens in dark-emerald's. Both
# passed every gate and both looked like one colour at two brightnesses, which is not a
# categorical palette. Normal vision needs its own constraint.
HUE_SEP_MIN = 40


def _candidates(target):
    """Every (hex, simulated-pair) reachable at one ladder rung."""
    out = []
    for hue in range(0, 360, HUE_STEP):
        for s in SATS:
            h = solve(hue, s, target)
            out.append((h, (simulate(h, "deutan"), simulate(h, "protan")), hue))
    return out


def a11y_palette(fam):
    """Slot 0 is the gem. Slots 1-3 are SEARCHED, not named.

    The constraint picks the colours and the names are applied afterwards - the era generator
    learned that the hard way, with a hand-picked crimson/gold/forest trio that collapsed under
    both deficiencies at once. Greedy farthest-point insertion followed by coordinate ascent,
    scored on the worst CVD pair across deuteranopia and protanopia.
    """
    ladder = LADDER_A11Y["mono" if fam["chroma"] == 0.0 else "chromatic"]

    if fam["chroma"] == 0.0:
        # No hue to search over. Luminance is the whole palette.
        return [solve(0, 0.0, t) for t in ladder]

    lead = solve(fam["hue"], 0.68, ladder[0])
    chosen = [(lead, (simulate(lead, "deutan"), simulate(lead, "protan")), fam["hue"])]

    pools = [_candidates(ladder[i]) for i in range(1, GATED)]

    def best_for(slot, others):
        best, best_s = None, -1.0
        for cand in pools[slot]:
            if min(abs(signed_offset(cand[2], o[2])) for o in others) < HUE_SEP_MIN:
                continue                      # too close in plain hue - see HUE_SEP_MIN
            s = min(min(dist(cand[1][k], o[1][k]) for k in (0, 1)) for o in others)
            # keep normal-vision separation too: two colours that only differ under
            # simulation would be a strange thing to ship
            s = min(s, min(dist(srgb(cand[0]), srgb(o[0])) for o in others))
            if s > best_s:
                best, best_s = cand, s
        return best

    for slot in range(len(pools)):                       # greedy seed
        chosen.append(best_for(slot, chosen))
    for _ in range(8):                                   # coordinate ascent
        moved = False
        for slot in range(len(pools)):
            others = [c for i, c in enumerate(chosen) if i != slot + 1]
            cand = best_for(slot, others)
            if cand[0] != chosen[slot + 1][0]:
                chosen[slot + 1] = cand
                moved = True
        if not moved:
            break

    # Slots 4-7 are not gated - a reader is not asked to tell eight series apart at a glance -
    # but they should still spread rather than clump. Plain-vision distance is enough here.
    tail = []
    for i in range(GATED, 8):
        pool = _candidates(ladder[i])
        picked = max(pool, key=lambda c: min(dist(srgb(c[0]), srgb(o[0]))
                                             for o in chosen + tail))
        tail.append(picked)
    return [c[0] for c in chosen + tail]


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


def set_radius(node):
    """Rewrite every corner radius in the cloned theme. Radius is a theme concern - doing it
    per visual would be the override anti-pattern the format room warns about."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "radius" and isinstance(v, (int, float)):
                node[k] = CORNER_RADIUS
            else:
                set_radius(v)
    elif isinstance(node, list):
        for v in node:
            set_radius(v)
    return node


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


# ---------------------------------------------------------------------------- a11y build
def a11y_map(fam, ruby):
    """Flavour map, then the parts an accessibility review will not let stand."""
    cmap = build_map(fam, ruby)
    pal = a11y_palette(fam)

    for src, new in zip(ruby["dataColors"], pal):
        cmap[src.upper()] = new

    # #F54651 IS dataColors[0], but it also appears nine more times as the primary accent -
    # selection outlines, KPI callouts, slicer chrome. It has to move with the lead.
    cmap["#F54651"] = pal[0]

    for key, (hue, sat, target) in A11Y_SEMANTIC.items():
        cmap[{"bad": "#CC0000", "good": "#6FBF73"}[key].upper()] = solve(hue, sat, target)

    # tableAccent #990000 measures 1.61:1 on the card. Lifted to the fill floor, on the lead's
    # own hue so it still reads as part of the theme.
    h, s, _ = hsl_of(pal[0])
    cmap["#990000"] = solve(h, min(0.75, s + 0.1), 0.215)
    return cmap, pal


def a11y_audit(slug, theme, cmap, pal):
    fails, lines = [], []

    for src in INK_ROLES:
        got = cmap[src.upper()]
        rp, rg = ratio(got, PANEL), ratio(got, PAGE)
        if rp < 4.5 or rg < 4.5:
            fails.append("%s: ink %s is %.2f:1 card / %.2f:1 page, needs 4.5" % (slug, got, rp, rg))

    worst_fill = 99.0
    for i, c in enumerate(theme["dataColors"]):
        rp, rg = ratio(c, PANEL), ratio(c, PAGE)
        worst_fill = min(worst_fill, rp, rg)
        if min(rp, rg) < 3.0:
            fails.append("%s: dataColors[%d] %s is %.2f:1 card / %.2f:1 page, needs 3.0"
                         % (slug, i, c, rp, rg))
    for key in ("bad", "good", "tableAccent"):
        c = theme[key]
        if ratio(c, PANEL) < 3.0:
            fails.append("%s: %s %s is %.2f:1 on card, needs 3.0" % (slug, key, c, ratio(c, PANEL)))

    gated = pal[:GATED]
    worst_grey = min((max(lum(gated[i]), lum(gated[j])) + 0.05)
                     / (min(lum(gated[i]), lum(gated[j])) + 0.05)
                     for i in range(GATED) for j in range(i + 1, GATED))
    if worst_grey < GREY_MIN:
        fails.append("%s: greyscale separation %.2f among the leading %d, needs %.2f"
                     % (slug, worst_grey, GATED, GREY_MIN))

    sims = [(simulate(c, "deutan"), simulate(c, "protan")) for c in gated]
    worst_cvd = cvd_score(sims, list(range(GATED)))
    if worst_cvd < CVD_MIN:
        fails.append("%s: CVD separation %.3f among the leading %d, needs %.2f"
                     % (slug, worst_cvd, GATED, CVD_MIN))

    sem = cvd_score([(simulate(theme["bad"], "deutan"), simulate(theme["bad"], "protan")),
                     (simulate(theme["good"], "deutan"), simulate(theme["good"], "protan"))],
                    [0, 1])
    if sem < CVD_MIN:
        fails.append("%s: good/bad separate by only %.3f under CVD, needs %.2f"
                     % (slug, sem, CVD_MIN))

    lines.append("    fills worst against either surface: %.2f:1 (need 3.00)" % worst_fill)
    lines.append("    greyscale, leading %d: %.2f:1 (need %.2f)" % (GATED, worst_grey, GREY_MIN))
    lines.append("    CVD, leading %d:       %.3f  (need %.2f, deuteranopia AND protanopia)"
                 % (GATED, worst_cvd, CVD_MIN))
    lines.append("    CVD, good vs bad:     %.3f  (%s / %s)" % (sem, theme["bad"], theme["good"]))
    return fails, lines


def build_a11y(slug, fam, ruby, write):
    cmap, pal = a11y_map(fam, ruby)
    theme = set_radius(remap(ruby, cmap))
    theme["name"] = fam["name"] + " A11y"

    ordered = {"$schema": SCHEMA}
    ordered.update({k: v for k, v in theme.items() if k != "$schema"})

    fails, lines = a11y_audit(slug, ordered, cmap, pal)
    print("  %s-a11y (%s)" % (slug, ordered["name"]))
    for line in lines:
        print(line)
    print("    gated  " + " ".join(pal[:GATED]))
    print("    rest   " + " ".join(pal[GATED:]))

    if fails:
        for f in fails:
            print("    FAIL " + f)
        return fails

    if write:
        folder = os.path.join(HERE, slug)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "%s-a11y-%s.json" % (slug, VERSION))
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(ordered, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        write_a11y_notes(folder, slug, fam, ordered, cmap, pal)
        print("    wrote %s" % os.path.relpath(path, HERE))
    return []


# --------------------------------------------------------------------------------- build
def build(slug, fam, ruby, write):
    cmap = build_map(fam, ruby)
    theme = set_radius(remap(ruby, cmap))
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


def write_a11y_notes(folder, slug, fam, theme, cmap, pal):
    rows = "\n".join(
        "| %d%s | `%s` | %5.2f:1 | %5.2f:1 |"
        % (i, " *" if i < GATED else "", c, ratio(c, PANEL), ratio(c, PAGE))
        for i, c in enumerate(theme["dataColors"]))

    gated = pal[:GATED]
    grey_rows = "\n".join(
        "| `%s` vs `%s` | %.2f:1 | %.3f | %.3f |"
        % (gated[i], gated[j],
           (max(lum(gated[i]), lum(gated[j])) + 0.05) / (min(lum(gated[i]), lum(gated[j])) + 0.05),
           dist(simulate(gated[i], "deutan"), simulate(gated[j], "deutan")),
           dist(simulate(gated[i], "protan"), simulate(gated[j], "protan")))
        for i in range(GATED) for j in range(i + 1, GATED))

    mono = fam["chroma"] == 0.0
    body = """# {name} A11y

The accessibility build of [{base}](notes.md). Same theme - same black, same card, same DM Sans,
same 40 `visualStyles`, same {gem} lead - with a palette that a colour-blind reader and a mono
printer can both take apart.

Generated by [`../_build-gem-themes.py`](../_build-gem-themes.py) (`--a11y`). Do not hand-edit.

## What it gives up, and why it has to

**An accessible version of a monochrome theme is not monochrome.** That is not a shortcut, it is
the whole problem: separation for a colour-blind reader has to come from somewhere, and in a
single-hue ramp there is nowhere for it to come from. {base} measures **1.14:1** in greyscale
across its leading four and fails the CVD gate outright.

So slot 0 stays {gem} - it leads every chart, and with the metal ink and the black surface it is
where the theme's identity actually lives - and slots 1-3 are {how}.

{searched}

## Palette

Rows marked `*` are the gated four: the colours a reader is asked to tell apart at a glance.
Slots 4-9 are not gated, because nobody distinguishes ten series by colour.

| # | Colour | vs card `#2A2A2A` | vs page `#1A1A1A` |
|---|---|---|---|
{rows}

## Measured separation, gated four

Every pair, both deficiencies, Vienot-Brettel-Mollon 1999. Gates: greyscale >= {gmin}:1,
CVD >= {cmin} under **both** conditions. The build fails rather than writing a palette that misses.

| Pair | Greyscale | Deuteranopia | Protanopia |
|---|---|---|---|
{grey_rows}

## Semantics were replaced, not inherited

dark-ruby's `good` / `bad` do not survive a review:

- `bad` was `#CC0000` at **2.44:1** on the card - under the 3:1 non-text gate. Now `{bad}`
  at {badr:.2f}:1.
- `good` was `#6FBF73`, a true green. Red-versus-green is the exact pair both common
  deficiencies collapse. Now `{good}` - a bluish-green, which is Okabe-Ito's answer: it keeps a
  red hue for normal vision while still separating under simulation. Measured **{sem:.3f}**
  against `bad`.
- `tableAccent` was `#990000` at 1.61:1. Now `{ta}` at {tar:.2f}:1, on the lead's hue.

## What is still not gated

Gridlines stay low-contrast ({gridr:.2f}:1). WCAG's non-text rule covers meaningful graphics, and
a gridline is scaffolding - lifting it to 3:1 makes every chart noisier for every reader, which is
a worse outcome than leaving it quiet. If you need heavier gridlines for a specific audience, that
is a per-report override rather than a theme change.

Text still sits at {inkmin:.2f}:1 or better against the card, inherited unchanged from dark-ruby.

## Apply it

```bash
pbir theme serialize {slug}-a11y-{version}.json -o /tmp/{slug}-a11y.Theme
pbir theme build /tmp/{slug}-a11y.Theme -o "<project>.Report" -f --clean
```
""".format(
        name=fam["name"], base=fam["name"], gem=slug.replace("dark-", ""),
        how=("stretched across a much wider luminance band" if mono
             else "searched across the hue circle"),
        searched=("**Luminance is the entire palette here.** With no hue to work with, the ramp\n"
                  "is spread from `{lo}` to `{hi}` instead of the tight band the coloured\n"
                  "families use. On their ladder four greys measure 0.109 under CVD - below the\n"
                  "gate - even though they are perfectly readable in print. Stretched, they clear\n"
                  "it at 0.278.".format(lo=pal[GATED - 1], hi=pal[0]) if mono else
                  "**The hues were searched, not named.** A greedy farthest-point pass followed\n"
                  "by coordinate ascent over the whole circle, scored on the worst CVD pair across\n"
                  "both deficiencies, with a 40-degree floor on plain hue so normal vision gets\n"
                  "its own separation. That last constraint was not in the first run, and it\n"
                  "showed: the search put a light gold and a dark gold in dark-gold's gated four\n"
                  "and two greens in dark-emerald's. Both passed every metric - the luminance gap\n"
                  "satisfies greyscale and CVD alike - and both read as one colour at two\n"
                  "brightnesses.\n\n"
                  "The constraint picks the colours and the names are applied afterwards. Hand-\n"
                  "picking a set and defending it is how you end up with crimson, gold and forest\n"
                  "in the same gated four, which collapses under both conditions at once."),
        rows=rows, grey_rows=grey_rows, gmin=GREY_MIN, cmin=CVD_MIN,
        bad=theme["bad"], badr=ratio(theme["bad"], PANEL),
        good=theme["good"],
        sem=dist(simulate(theme["bad"], "deutan"), simulate(theme["good"], "deutan")),
        ta=theme["tableAccent"], tar=ratio(theme["tableAccent"], PANEL),
        gridr=ratio(cmap["#6B5858"], PANEL),
        inkmin=min(ratio(cmap[s.upper()], PANEL) for s in INK_ROLES),
        slug=slug, version=VERSION)

    with io.open(os.path.join(folder, "notes-a11y.md"), "w", encoding="utf-8", newline="\n") as fh:
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
    ap.add_argument("--flavour-only", action="store_true", help="skip the a11y builds")
    ap.add_argument("--a11y-only", action="store_true", help="skip the flavour builds")
    args = ap.parse_args()

    ruby = json.load(io.open(TEMPLATE, encoding="utf-8-sig"))
    print("template: dark-ruby, %d visualStyles, %d dataColors"
          % (len(ruby["visualStyles"]), len(ruby["dataColors"])))

    all_fails = []
    for slug, fam in FAMILIES.items():
        if args.only and slug != args.only:
            continue
        if not args.a11y_only:
            all_fails += build(slug, fam, ruby, write=not args.check)
        if not args.flavour_only:
            all_fails += build_a11y(slug, fam, ruby, write=not args.check)

    if all_fails:
        print("\n%d gate failure(s) - nothing written for the failing families." % len(all_fails))
        return 1
    print("\nflavour builds: ink >= 4.5:1, fills >= 3:1, against both surfaces")
    print("a11y builds:    the above PLUS greyscale >= %.2f:1 and CVD >= %.2f under both"
          % (GREY_MIN, CVD_MIN))
    return 0


if __name__ == "__main__":
    sys.exit(main())
