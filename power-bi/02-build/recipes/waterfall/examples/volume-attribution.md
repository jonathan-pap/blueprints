# Example — Volume Attribution Funnel (5 steps, mixed totals/drops, stacked variant)

End-to-end build of a 5-step funnel that shows where a market's headline volume actually goes.
Validated 2026-06-04 against a fantasy-MMO economy model.

## The story

> Of total trade volume, how much is meaningful player-to-player on items worth caring about?

Total Volume splits into NPC-mediated trades + player trades. Player trades split further into
Common+Uncommon (low-tier churn) + Rare+ (the "real" market). The funnel reveals: most
headline volume is low-tier player churn; the meaningful market is a small fraction.

## Q1 — Steps (intake)

```
Total Volume    | total | [Trade Quantity]
NPC Mediated    | drop  | [NPC Volume]
Player Volume   | total | (derived: Trade Quantity - NPC Volume)
Common+Uncommon | drop  | [Low Tier Player Volume]
Rare+ Player    | total | (derived: Player Volume - Low Tier Player Volume)
```

Helper measures derived from existing model measures:

```dax
NPC Volume = CALCULATE ( [Trade Quantity], DimSeller[SellerType] = "NPC" )
Low Tier Player Volume = CALCULATE ( [Trade Quantity], DimSeller[SellerType] = "Player", DimRarity[RarityRank] <= 2 )
Mid+ Tier Player Volume = CALCULATE ( [Trade Quantity], DimSeller[SellerType] = "Player", DimRarity[RarityRank] >= 3 )
```

## Q2 — Stacked composition?

**Yes** — both Total Volume (step 1) and Player Volume (step 3) split:

```
Total Volume:
  NPC   | [NPC Volume]
  Low   | [Low Tier Player Volume]
  Rare+ | [Mid+ Tier Player Volume]

Player Volume:
  Low   | [Low Tier Player Volume]
  Rare+ | [Mid+ Tier Player Volume]
```

## Q3 — Orientation + label style

Built FIVE pages to compare variants:
- Vertical Standard
- Vertical Detailed
- Horizontal Standard
- Horizontal Detailed
- Stacked Composition (vertical)

## Tokens

| Token | Value |
|---|---|
| `<PREFIX>` | `Funnel` |
| `<STEPS_TABLE>` | `FunnelSteps` |
| `<MEASURE_TABLE>` | `_Measures` |
| `<DISPLAY_FOLDER>` | `16. Funnel Test` |
| `<FIRST_TOTAL_MEASURE>` | `[Trade Quantity]` |
| `<AXIS_MAX_HEADROOM>` | `1.15` |
| `<AXIS_MAX_ROUND>` | `1000` |
| `<COLOR_TOTAL_START>` | `#1F3A5F` (navy — single Total bar) |
| `<COLOR_TIER_NPC>` | `#CE5A4E` (coral) |
| `<COLOR_TIER_LOW>` | `#E0A030` (warm orange) |
| `<COLOR_TIER_HIGH>` | `#2D6948` (dark green) |

## Generated measures (15 total — 3 helpers + 12 recipe-generated)

```
NPC Volume                                        ← Q1 helper
Low Tier Player Volume                            ← Q1 helper
Mid+ Tier Player Volume                           ← Q1 helper
Funnel Base                                       ← P2 floater
Funnel Body · Total Volume                        ← P2 body
Funnel Body · NPC Mediated                        ← P2 body (drop)
Funnel Body · Player Volume                       ← P2 body
Funnel Body · Common+Uncommon                     ← P2 body (drop)
Funnel Body · Rare+ Player                        ← P2 body (end)
Funnel Label                                      ← P3 simple label
Funnel Label (rich)                               ← P3 rich label
Funnel Axis Max                                   ← P4 axis-max
Funnel Label Anchor                               ← P4 anchor
Funnel Label Pad                                  ← P5 horizontal pad
Stack · Total · NPC                               ← P6 stacked segment
Stack · Total · Low                               ← P6 stacked segment
Stack · Total · Rare+                             ← P6 stacked segment
Stack · Player · Low                              ← P6 stacked segment
Stack · Player · Rare+                            ← P6 stacked segment
```

## Validation values (live from grand-exchange model)

| Step | Base | Body | Bar Top | Standard label | Rich label |
|---|---:|---:|---:|---|---|
| Total Volume | 0 | 526,274 | 526,274 | `526,274` | `526,274 · 100% traded` |
| NPC Mediated | 425,945 | 100,329 | 526,274 | `-100,329` | `-100,329 · 19% NPC take` |
| Player Volume | 0 | 425,945 | 425,945 | `425,945` | `425,945 · 81% player` |
| Common+Uncommon | 68,244 | 357,701 | 425,945 | `-357,701` | `-357,701 · 68% low-tier churn` |
| Rare+ Player | 0 | 68,244 | 68,244 | `68,244` | `68,244 · 13% meaningful` |

Math integrity (T = NPC + Player, Player = Low + Mid+): both return exactly 0. ✓

## Surprise insight from live data

Of 526k total trade volume, **19% is NPC-mediated and 84% of remaining player volume is just
Common+Uncommon churn.** Only **13% of total** (68k units) is genuine player-to-player on
Rare+ items. The "real" market is far smaller than the headline number — exactly the kind of
insight this waterfall pattern exists to surface.

## Stack ordering in the stacked variant

Y projections (bottom-to-top):
```
Funnel Base
Stack · Total · NPC          ← bottom of Step 1 stack
Stack · Total · Low          ← middle of Step 1
Stack · Total · Rare+        ← top of Step 1
Funnel Body · NPC Mediated   ← drop, Step 2
Stack · Player · Low         ← bottom of Step 3 stack
Stack · Player · Rare+       ← top of Step 3
Funnel Body · Common+Uncommon← drop, Step 4
Funnel Body · Rare+ Player   ← end, Step 5
```

NPC at bottom, Low in middle, Rare+ at top — same tier position across Step 1 and Step 3.
The eye traces "the orange band" (Low) shrinking from full-width in Total → smaller in Player
→ gone after the Common+Uncommon drop.

## Mixed labels (recommended for stacked)

- Stack segments → default value labels (each colored slice shows its number)
- Drop bars (NPC Mediated, Common+Uncommon) → dynamic `Funnel Label` for `-` prefix
- End total → default value label
- Funnel Base → suppressed

`labelPosition: 'InsideCenter'` works for large segments but the Rare+ tier (13% of total)
is on the edge of overflowing. Acceptable trade-off; can switch to `OutsideEnd` if too tight.

## Visual.json templates used

- vertical-standard / vertical-detailed → [vertical.visual.json](../templates/vertical.visual.json)
- horizontal-standard / horizontal-detailed → [horizontal.visual.json](../templates/horizontal.visual.json)
- stacked → [stacked.visual.json](../templates/stacked.visual.json)
