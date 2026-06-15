# Colour palettes

> Named, CVD-checked palettes + the assignment strategy that keeps a report visually coherent. This is
> the design-time **catalog**; the build-time mechanics (theme tokens, `dataPoint.fill`, FillRule) live
> in [`../references/visual-colors.md`](../references/visual-colors.md) and
> [`../format/_index.md`](../format/_index.md). Contrast + CVD rules: [accessibility.md](accessibility.md).

## Core principles

1. **Palette family matches data family** — sequential for ordered, diverging for ±, categorical for nominal.
2. **Never rainbow on ordered data** — rainbow has no perceptual order; it misleads.
3. **Colour is never the sole channel** — pair with shape/label/pattern.
4. **Cap categorical at 7–8 hues** — beyond that, indistinguishable.
5. **Restraint beats vibrance** — most of the canvas neutral; colour draws the eye to what matters.
6. **Reserve semantic colours** — green/red/amber carry meaning; don't spend them on decoration.

## Palette-by-data-family decision tree

```text
What type of data?
├── Nominal/categorical (no order)
│   ├── ≤8 → Okabe-Ito or Set2
│   └── >8 → group into "Other"; cap 7–8
├── Ordinal/sequential (low→high)
│   ├── CVD-critical → Cividis or Viridis
│   └── standard → Blues
├── Diverging (± from midpoint)
│   ├── CVD-critical → BrBG
│   └── standard → RdBu
└── Semantic (status/sentiment) → theme good/neutral/bad keys
```

## Sequential (low→high magnitude)

| Name | 5-step ramp | CVD-safe |
|---|---|---|
| **Blues** | `#EFF3FF` `#BDD7E7` `#6BAED6` `#3182BD` `#08519C` | ✅ all |
| **YlOrRd** | `#FFFFB2` `#FECC5C` `#FD8D3C` `#F03B20` `#BD0026` | ⚠️ deutan marginal |
| **Viridis** | `#440154` `#3B528B` `#21908C` `#5DC863` `#FDE725` | ✅ all |
| **Cividis** | `#002051` `#3F5B75` `#8E8E52` `#CBBE2D` `#FDEA45` | ✅ all + greyscale |

## Diverging (± from a midpoint)

| Name | Low → Mid → High | CVD-safe |
|---|---|---|
| **RdBu** | `#B2182B` → `#F7F7F7` → `#2166AC` | ✅ |
| **BrBG** | `#8C510A` → `#F5F5F5` → `#01665E` | ✅ |
| **PiYG** | `#C51B7D` → `#F7F7F7` → `#4D9221` | ⚠️ protan marginal |

## Categorical (nominal)

| Name | Colours | CVD-safe |
|---|---|---|
| **Okabe-Ito** | `#E69F00` `#56B4E9` `#009E73` `#F0E442` `#0072B2` `#D55E00` `#CC79A7` `#000000` | ✅ all |
| **Set2** | `#66C2A5` `#FC8D62` `#8DA0CB` `#E78AC3` `#A6D854` `#FFD92F` `#E5C494` `#B3B3B3` | ✅ |
| **Tableau 10** | `#4E79A7` `#F28E2B` `#E15759` `#76B7B2` `#59A14F` `#EDC948` `#B07AA1` `#FF9DA7` `#9C755F` `#BAB0AC` | ⚠️ deutan clash at 9–10 |

> Set these as the theme `dataColors` array ([`../../theme/modify/colors.md`](../../theme/modify/colors.md)).
> A custom `dataColors` **replaces** the base array — it does not merge.

## Semantic colour rules

| Colour | Meaning | Rule |
|---|---|---|
| Green | good / on-target | favourable status only |
| Red | bad / critical | unfavourable status only |
| Amber | warning | between green and red |
| Grey | neutral / context / benchmark | default for non-highlighted |
| Blue | informational / brand accent | safe default, no semantic load |

Never flip semantics (green=bad) without explicit instruction. Never red+green as the only
differentiator — pair with icon/label. Cultural caveat: some East-Asian finance contexts use red=gain.
Map to theme `good`/`neutral`/`bad` tokens ([`../../theme/modify/sentiment-colors.md`](../../theme/modify/sentiment-colors.md)), not raw hex.

## Colour-assignment strategy (per page)

So visuals are linked when they share a measure and distinct when they don't:

1. **Same measure → same colour.** A card showing "Revenue" in blue → the line trending Revenue is the
   same blue (`dataPoint.defaultColor`). Visual link between card and its trend.
2. **Breakdown of a measure → gradient of that colour.** "Revenue by Region" bars → light→dark gradient
   of that blue (`dataPoint.fill` FillRule). Gradient ties the breakdown to its parent + reinforces sort.
3. **Different measure → different hue.** Next unused `dataColors` slot.
4. **Cards consume palette slots first** in reading order; charts derive from or take the next slot.

> ⚠️ **FillRule gradients must use `Literal` hex stops — `ThemeDataColor` silently renders black inside a
> FillRule.** Compute tint/shade from `dataColors[N]` (blend ~40–60% toward white for the min stop).
> See [`../format/conditional-fmt-color-scale.md`](../format/conditional-fmt-color-scale.md) for the full
> gradient traps. Data labels stay neutral dark (`#252423`), never the accent.

## Highlight pattern

| Element | Treatment |
|---|---|
| Highlighted bar/line | saturated brand/semantic colour |
| Context bars/lines | light grey `#D9D9D9`–`#E0E0E0` |
| Reference line | medium grey `#999999`, 1px dashed |
| Background | white / near-white |

Works across archetypes — see [signatures S5/S6](signatures.md#s5-single-accent-discipline).

## Archetype calibration

| Archetype | Strategy | Colours |
|---|---|---|
| Executive | 3 semantic + 1 brand accent + grey | 5 |
| Operational | RAG + status grey + 1 highlight | 5 |
| Analytical | full categorical (Okabe-Ito/Set2) + sequential for heatmaps | ≤8 |
| Narrative | 1 highlight + grey context | 2–3 |
| Comparative | diverging (RdBu) or paired categorical | 4–6 |

## Related
- [accessibility.md](accessibility.md) — contrast thresholds + CVD simulation · [`../references/visual-colors.md`](../references/visual-colors.md) — build-time tokens
- [`../../theme/create/color-system.md`](../../theme/create/color-system.md) · [`../../theme/modify/colors.md`](../../theme/modify/colors.md) · [`../../theme/modify/sentiment-colors.md`](../../theme/modify/sentiment-colors.md)
- [tones.md](tones.md) (each tone's accent guidance) · [anti-patterns.md](anti-patterns.md#cluster-4--colour-misuse)
