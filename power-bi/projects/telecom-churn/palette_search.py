"""Search a futuristic-telecom palette that still survives CVD and greyscale.

Three hard constraints, all measured rather than eyeballed:
  1. WCAG - stayed/churned >= 4.5:1 as text on white, joined >= 3:1 (graphical only)
  2. greyscale - mutual luminance ratio >= 1.3 so status survives a mono printout
  3. colour blindness - pairwise distance in DEUTERANOPIA and PROTANOPIA simulated space,
     because orange-vs-blue (Okabe-Ito) is the safest pair and moving to magenta gives some
     of that up. Vienot 1999 LMS transform.
"""
import itertools

WHITE = "#FFFFFF"


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


# --- Vienot 1999 dichromat simulation (linear RGB -> LMS -> project -> RGB) ---
RGB2LMS = [[0.31399022, 0.63951294, 0.04649755],
           [0.15537241, 0.75789446, 0.08670142],
           [0.01775239, 0.10944209, 0.87256922]]
LMS2RGB = [[5.47221206, -4.6419601, 0.16963708],
           [-1.1252419, 2.29317094, -0.1678952],
           [0.02980165, -0.19318073, 1.16364789]]
# protan / deutan projection matrices in LMS
PROTAN = [[0, 1.05118294, -0.05116099], [0, 1, 0], [0, 0, 1]]
DEUTAN = [[1, 0, 0], [0.9513092, 0, 0.04866992], [0, 0, 1]]


def mul(m, v):
    return [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]


def simulate(h, kind):
    lms = mul(RGB2LMS, linear(srgb(h)))
    lms = mul(PROTAN if kind == "protan" else DEUTAN, lms)
    rgb = mul(LMS2RGB, lms)
    return [max(0.0, min(1.0, x)) for x in rgb]


def dist(h1, h2, kind):
    a, b = simulate(h1, kind), simulate(h2, kind)
    return (sum((a[i] - b[i]) ** 2 for i in range(3))) ** 0.5


CANDIDATES = {
    "stayed": ["#0E7490", "#155E75", "#0F766E", "#075985", "#0C6E8A"],
    "churned": ["#BE185D", "#9D174D", "#A21CAF", "#C2185B", "#B01455"],
    "joined": ["#7C5CE0", "#8B7BF0", "#A78BFA", "#9575F5", "#8A6FE8"],
}
BASELINE = ("#00558F", "#B8480A", "#B673A4")   # the current blue/vermillion/purple

print("baseline (current, with vermillion):")
b_s, b_c, b_j = BASELINE
print("  deutan pair distances: s/c %.3f  c/j %.3f  s/j %.3f"
      % (dist(b_s, b_c, "deutan"), dist(b_c, b_j, "deutan"), dist(b_s, b_j, "deutan")))
print("  protan pair distances: s/c %.3f  c/j %.3f  s/j %.3f"
      % (dist(b_s, b_c, "protan"), dist(b_c, b_j, "protan"), dist(b_s, b_j, "protan")))
print()

best = []
for s, c, j in itertools.product(*CANDIDATES.values()):
    if ratio(s, WHITE) < 4.5 or ratio(c, WHITE) < 4.5 or ratio(j, WHITE) < 3.0:
        continue
    grey = min(ratio(s, c), ratio(c, j), ratio(s, j))
    if grey < 1.3:
        continue
    cvd = min(dist(s, c, "deutan"), dist(c, j, "deutan"), dist(s, j, "deutan"),
              dist(s, c, "protan"), dist(c, j, "protan"), dist(s, j, "protan"))
    best.append((cvd, grey, s, c, j))

best.sort(reverse=True)
print("top candidates (ranked by WORST CVD pair distance):")
print("  %-8s %-6s  stayed    churned   joined" % ("cvd", "grey"))
for cvd, grey, s, c, j in best[:6]:
    print("  %.3f    %.2f    %s   %s   %s" % (cvd, grey, s, c, j))
print()
print("total passing WCAG + greyscale:", len(best))
