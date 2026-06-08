# P3 — Label measures

Two label measures: `<PREFIX> Label` (simple signed value) and `<PREFIX> Label (rich)` (value +
share + context word). The variant chooses which one is bound to the carrier (the Y2 anchor for
vertical, the stacked anchor for horizontal).

## `<PREFIX> Label` — simple, signed

One number per step. Drops get a `-` prefix; totals don't.

```dax
<PREFIX> Label =
VAR <Source1> = [<source step 1>]
VAR <Source2> = [<source step 2>]
-- ...
RETURN
    SWITCH (
        SELECTEDVALUE ( <STEPS_TABLE>[Step] ),
        "<Step 1 (total)>", FORMAT ( <RunningTotalAtStep1>, "#,0" ),
        "<Step 2 (drop)>",  "-" & FORMAT ( <Source2>, "#,0" ),
        "<Step 3 (total)>", FORMAT ( <RunningTotalAtStep3>, "#,0" ),
        -- ...
        BLANK ()
    )
```

For totals: format the **running cumulative value** at that step. For drops: prefix `-` and
format the **drop magnitude**.

## `<PREFIX> Label (rich)` — value + share + word

A storytelling label. Each step shows value + share-of-total + a contextual phrase:

```dax
<PREFIX> Label (rich) =
VAR T = [<first total source>]   -- the headline total for share calculation
VAR <Source2> = [<source step 2>]
-- ...
RETURN
    SWITCH (
        SELECTEDVALUE ( <STEPS_TABLE>[Step] ),
        "<Step 1 (total)>",
            FORMAT ( T, "#,0" ) & " · 100% <context phrase 1>",
        "<Step 2 (drop)>",
            "-" & FORMAT ( <Source2>, "#,0" ) & " · "
            & FORMAT ( DIVIDE ( <Source2>, T ), "0%" ) & " <context phrase 2>",
        -- ...
        BLANK ()
    )
```

Example rendered output (from the volume-attribution example):

| Step | Rich label |
|---|---|
| Total Volume | `526,274 · 100% traded` |
| NPC Mediated | `-100,329 · 19% NPC take` |
| Player Volume | `425,945 · 81% player` |
| Common+Uncommon | `-357,701 · 68% low-tier churn` |
| Rare+ Player | `68,244 · 13% meaningful` |

The context phrases are user-provided (during the intake). Default to the step name if the
user doesn't supply phrases — but rich labels are much more impactful with explicit phrases.

## The showSeries trap — CRITICAL

The label is rendered by a **carrier series** — the Y2 anchor (vertical) or the stacked
Anchor (horizontal). The `dynamicLabelValue` binding in `labels[]` targets that series via
`selector.metadata`. **DO NOT** apply `showSeries: false` to the carrier in `labels[]` — it
silently suppresses the label rendering chain, even though the binding looks correct.

```json
// ❌ WRONG — this suppresses the label
{ "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
  "selector": { "metadata": "_Measures.<PREFIX> Label Anchor" } }

// ✓ RIGHT — apply showSeries: false to every OTHER series, not the carrier
{ "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } } },
  "selector": { "metadata": "_Measures.<PREFIX> Base" } }
// ... plus one per Body, plus Label Pad (if horizontal) — NOT the Anchor.
```

This bit twice in the original test build. See [[pbi-labels-showseries-trap]] memory entry.

## Variant binding

Where the label is bound depends on orientation:

| Variant | Carrier | Binding location |
|---|---|---|
| Vertical Standard | Y2 line (`<PREFIX> Label Anchor` on Y2) | `labels[].dynamicLabelValue → <PREFIX> Label` with `selector.metadata = _Measures.<PREFIX> Label Anchor` |
| Vertical Detailed | Same | Bound to `<PREFIX> Label (rich)` instead |
| Horizontal Standard | Stacked Anchor (`<PREFIX> Label Anchor` in Y, stacked last) | Same selector shape |
| Horizontal Detailed | Same | Rich label |
| Stacked composition | Default per-segment + dynamic on drops | Hybrid — see [variants/stacked-composition.md](../variants/stacked-composition.md) |

## Next

[P4 — axis max + label anchor](axis-anchor.md) — the carrier measure and the dynamic value-axis
end that gives labels headroom.
