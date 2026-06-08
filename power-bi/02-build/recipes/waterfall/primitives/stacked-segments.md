# P6 — Stacked sub-segments

**Stacked composition variant only.** When a step's total is meaningful as the **sum of
sub-segments** (e.g. "Total Volume = NPC + Common+Uncommon + Rare+"), each sub-segment becomes
its own measure stacked at that step. Sub-segment measures use the same `IF + SELECTEDVALUE`
pattern as the simple body measures (P2) but read one tier from one step.

## When to use

Stack a step when the **composition tells a story** that a single body doesn't:
- A funnel's headline total split by acquisition channel.
- A revenue bridge's opening bar split by product line.
- An attrition cascade's "at risk" stage split by reason.

If the user answered Q2 = yes, ask Q2a for each stacked step's sub-segments.

## The DAX

For each stacked step, one measure per sub-segment:

```dax
<PREFIX> Stack · <Step> · <Segment> =
    IF (
        SELECTEDVALUE ( <STEPS_TABLE>[Step] ) = "<Step name>",
        [<source measure for this segment>]
    )
```

Example (from the volume-attribution example — Total Volume split into NPC, Low, Rare+):

```dax
Stack · Total · NPC   = IF ( SELECTEDVALUE ( FunnelSteps[Step] ) = "Total Volume", [NPC Volume] )
Stack · Total · Low   = IF ( SELECTEDVALUE ( FunnelSteps[Step] ) = "Total Volume", [Low Tier Player Volume] )
Stack · Total · Rare+ = IF ( SELECTEDVALUE ( FunnelSteps[Step] ) = "Total Volume", [Mid+ Tier Player Volume] )
```

The simple body measure (`<PREFIX> Body · Total Volume` from P2) is **replaced** by these
sub-segments for the stacked step. For non-stacked steps, the original `Body · Step` measure
stays.

## Y projection order

The Y order defines the visual stacking, bottom-to-top within each step. Plan it explicitly:

```
Funnel Base                          (transparent floater - bottom)
Stack · Total · NPC                  (bottom of Total bar)
Stack · Total · Low                  (middle of Total bar)
Stack · Total · Rare+                (top of Total bar)
Funnel Body · NPC Mediated           (drop on step 2)
Stack · Player · Low                 (bottom of Player bar - step 3)
Stack · Player · Rare+               (top of Player bar)
Funnel Body · Common+Uncommon        (drop on step 4)
Funnel Body · Rare+ Player           (end total on step 5)
```

This makes the SAME tier (NPC, Low, Rare+) appear consistently positioned across steps.

## Tier-coherent colors

The recipe's strong recommendation: use **one color per tier** wherever that tier appears.

| Tier | Stack on totals | Drop bar |
|---|---|---|
| NPC | `<COLOR_TIER_NPC>` (e.g. `#CE5A4E`) | Same color |
| Low | `<COLOR_TIER_LOW>` (e.g. `#E0A030`) | Same color |
| Rare+ | `<COLOR_TIER_HIGH>` (e.g. `#2D6948`) | Same color |

This reads as "where did the orange go" across the funnel — the eye traces a tier from its
stack appearance through its drop and out of the picture. Different colors per occurrence
break that visual story.

## Labels — composition vs total

Stacked composition opens up a fourth label pattern (in addition to the standard / detailed /
default-only options):

**Mixed (recommended for stacked):**
- **Stack segments** (Stack · Total · *, Stack · Player · *): default value labels — each
  colored slice shows its own numeric value.
- **Drop bars** (Funnel Body · NPC Mediated, Funnel Body · Common+Uncommon): dynamic
  `<PREFIX> Label` so they keep the `-` prefix.
- **End total** (Funnel Body · Rare+ Player): default value label.
- **Funnel Base** (floater): suppressed.

```json
"labels": [
  { "properties": { "show": { ... true ... },
      "labelPosition": { ... 'InsideCenter' ... },
      "fontSize": { ... '9D' ... },
      "enableValueDataLabel": { ... true ... } } },
  { "properties": { "enableValueDataLabel": { ... false ... } },
    "selector": { "metadata": "_Measures.<PREFIX> Base" } },
  { "properties": { "dynamicLabelValue": { ... <PREFIX> Label ... } },
    "selector": { "data": [{ ... wildcard ... }],
      "metadata": "_Measures.<PREFIX> Body · <Drop Step>", "highlightMatching": 1 } }
  /* ... one dynamic-label entry per drop body ... */
]
```

## Caveat — small segments

`labelPosition: 'InsideCenter'` reads cleanly on large segments but can overflow when a tier's
share is small (e.g. <5% of total). Options:
- Drop to `'OutsideEnd'` so small-segment labels float above the bar.
- Reduce `fontSize` to `8D` or `7D` (cramped but readable).
- Accept the limitation and let the user manually overflow-rule the small ones in Desktop.

There's no clean solution within native PBI label rendering — the trade-off between in-bar
readability and small-segment fit is real.

## Validation

After creating, sanity-check that sub-segments sum to the parent step:

```dax
EVALUATE
SUMMARIZECOLUMNS (
    <STEPS_TABLE>[Step], <STEPS_TABLE>[StepSort],
    "Stack Total", COALESCE ( [Stack · Total · NPC], 0 )
                 + COALESCE ( [Stack · Total · Low], 0 )
                 + COALESCE ( [Stack · Total · Rare+], 0 ),
    "Step 1 Total", IF ( <STEPS_TABLE>[Step] = "<Step 1>", [<step 1 source>] )
)
ORDER BY [StepSort]
```

Expected: `Stack Total` equals `Step 1 Total` on Step 1 only (both BLANK on other steps,
because the sub-segments are gated to Step 1 only). If they differ, the sub-segment list
doesn't sum to the step's headline total — the user missed a segment in Q2a.

## Next

Apply the [stacked-composition variant](../variants/stacked-composition.md) — uses
[templates/stacked.visual.json](../templates/stacked.visual.json).
