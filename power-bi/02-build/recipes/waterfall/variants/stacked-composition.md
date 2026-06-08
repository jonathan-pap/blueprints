# Variant — Stacked Composition

Some steps split into sub-segments. The headline bar shows the composition that the drops
will reveal. Tier-coherent coloring (same color per tier across stack and drop) makes the
funnel read as "where did each tier go."

Currently supported in **vertical** orientation. (Horizontal stacked composition is possible
but adds visual.json complexity — defer to a future iteration.)

## Visual

Template: [../templates/stacked.visual.json](../templates/stacked.visual.json).

## Required measures

- P1: [steps disconnected table](../primitives/steps-table.md)
- P2: `<PREFIX> Base` + one `<PREFIX> Body · <Step>` per **non-stacked** step
- P3: `<PREFIX> Label`
- P4: `<PREFIX> Axis Max` (Anchor optional — labels here are mostly default values)
- **P6: [`<PREFIX> Stack · <Step> · <Segment>`](../primitives/stacked-segments.md) — one per stacked step's sub-segment**

For each stacked step, the simple `<PREFIX> Body · <Step>` measure is **replaced** by the
sub-segment measures. For other steps, keep the original body.

## Y projection order — tier coherence

Order matters. For tier-coherent reading, keep the same tier at the same relative position
across stacked steps. Example for a 5-step funnel with stacking on steps 1 and 3:

```
Funnel Base                          (transparent floater)
Stack · Total · NPC                  (bottom of step 1 stack)
Stack · Total · Low                  (middle of step 1)
Stack · Total · Rare+                (top of step 1)
Funnel Body · NPC Mediated           (drop, step 2)
Stack · Player · Low                 (bottom of step 3 stack)
Stack · Player · Rare+               (top of step 3)
Funnel Body · Common+Uncommon        (drop, step 4)
Funnel Body · Rare+ Player           (end total, step 5)
```

## Tier-coherent colors

Same color per tier wherever it appears (in stack AND in drop):

| Tier | Color |
|---|---|
| NPC | `<COLOR_TIER_NPC>` |
| Low | `<COLOR_TIER_LOW>` |
| Rare+ | `<COLOR_TIER_HIGH>` |

Apply via `dataPoint` selectors on each measure's metadata. The eye traces a tier across the
chart and the drops visually correspond to specific tier slices in the totals.

## Label pattern — mixed

The richest information density:
- **Stack segments**: default value labels (each colored slice shows its own value)
- **Drop bars**: dynamic `<PREFIX> Label` so they show signed values with `-` prefix
- **End total**: default value label
- **Funnel Base**: suppressed via `enableValueDataLabel: false`

```json
"labels": [
  { "properties": { "show": true, "labelPosition": "'InsideCenter'", "fontSize": "9D",
                    "enableValueDataLabel": true } },
  { "properties": { "enableValueDataLabel": false },
    "selector": { "metadata": "<PREFIX> Base" } },
  { "properties": { "dynamicLabelValue": "<PREFIX> Label" },
    "selector": { "data": [wildcard], "metadata": "<PREFIX> Body · <DROP_STEP>", ... } }
  // ... one dynamic-label entry per drop body
]
```

## Caveat — small segment labels

When a tier's share is very small (< 5% of total), the `InsideCenter` label may overflow or
collide with neighbors. Options:
- Drop `labelPosition` to `'OutsideEnd'` so small labels float above
- Reduce `fontSize` to `8D`
- Accept the limitation and let the user hide specific labels in Desktop

There's no clean PBIR-level solution.

## When to choose this

- The headline total is meaningful as the **sum of categories** the audience already thinks in
  (e.g. revenue by product line, leads by channel, attrition by reason).
- The composition is **stable across the funnel** (the categories don't change as steps
  progress, just shrink/disappear).
- You can afford the extra measures (one per sub-segment per stacked step).

## Sample read

For a 5-step funnel with Step 1 stacked into 3 tiers and Step 3 stacked into 2:

```
        ╔══════════╗
        ║  Rare+   ║ 68
        ╠══════════╣
        ║  Low     ║ 358    ←  Step 1: Total = NPC + Low + Rare+ = 526
        ╠══════════╣
        ║  NPC     ║ 100
        ╚══════════╝
        Total Volume

                ┃┃ -100   ←  Step 2: NPC drop
                ┃┃
        Mediated

         ╔══════════╗
         ║  Rare+   ║ 68
         ╠══════════╣
         ║  Low     ║ 358    ←  Step 3: Player = Low + Rare+ = 426
         ╚══════════╝
         Player Volume

   ┃┃ -358            ←  Step 4: Low-tier drop
   ┃┃
   Common+Uncommon

   ║║  68             ←  Step 5: Rare+ Player = 68
   ║║
   Rare+ Player
```
