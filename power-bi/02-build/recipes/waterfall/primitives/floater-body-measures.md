# P2 — Floater + body measures

The engine. One **transparent floater** (`<PREFIX> Base`) plus **one body measure per step**
(`<PREFIX> Body · <Step>`). Stacked, they render the waterfall.

## The floater — `<PREFIX> Base`

Returns the **floor** that each step's colored bar should float at:

```dax
<PREFIX> Base =
VAR <Source1> = [<source measure for step 1>]
VAR <Source2> = [<source measure for step 2>]
-- ... one VAR per source measure
RETURN
    SWITCH (
        SELECTEDVALUE ( <STEPS_TABLE>[Step] ),
        "<Step 1>", 0,            -- total: sits at 0
        "<Step 2>", <RunningFloor>, -- drop: floats at the lower running value
        "<Step 3>", 0,
        -- ...
        BLANK ()
    )
```

**Per step:**
- **Total step** → floor = `0` (the colored body starts at 0 and rises to the cumulative value).
- **Drop step** → floor = the **running value the drop falls to** (the body floats between the
  running floor and the previous total). Examples:
  - 5-step funnel (Total → Drop1 → Intermediate → Drop2 → End): Drop1's floor = Intermediate
    value; Drop2's floor = End value.

The drop floors are derived from the source measures, not hardcoded. The recipe's intake (Q1)
gives the source for each step; the floor math is a sum/difference of those sources.

## The bodies — `<PREFIX> Body · <Step name>`

One per step. Each returns the **height** of its bar (the visible colored segment), or BLANK
on every other step:

```dax
<PREFIX> Body · <Step 1 name> =
    IF ( SELECTEDVALUE ( <STEPS_TABLE>[Step] ) = "<Step 1 name>", [<source measure>] )
```

For a 5-step funnel, that's 5 separate measures. The cost (more measures) buys:

| What you get | Why it matters |
|---|---|
| **Per-step color** via `dataPoint` selector on `_Measures.<PREFIX> Body · <Step>` | One IF per step, one color per step. The native waterfall can't do this. |
| **Per-step label format** via `labels[]` selector | Drops can show signed values; totals can show plain values. |
| **Per-step visibility** via `showSeries: false` on specific bodies | Hide a body without removing it from the math. |
| **Independent stacking position** | The Y projection order on the visual controls bottom-to-top. |

## How the stack reads

Bottom-to-top per step, the rendered bar is:

```
   <bar top> ←── visible body color
   ┄┄┄┄┄┄┄┄
   <floor>   ←── transparent floater (Base)
   0
```

For drops, the floor is positive, so the body sits in mid-air (the "drop" shape). For totals,
floor is 0, so the body sits on the axis baseline. Visually identical to a native waterfall —
mechanically a stacked column.

## `fillTransparency: 100D` on Base

Critical for the visual. In `visual.json`:

```json
{ "properties": { "fillTransparency": { "expr": { "Literal": { "Value": "100D" } } } },
  "selector": { "metadata": "_Measures.<PREFIX> Base" } }
```

The floater bar is rendered (it has to be — it occupies the stack slot) but its fill is fully
transparent. Without this, the floater shows as a solid block under each drop and ruins the
waterfall illusion.

## Validation DAX

Run this immediately after creating the measures to confirm the math:

```dax
EVALUATE
SUMMARIZECOLUMNS (
    <STEPS_TABLE>[Step], <STEPS_TABLE>[StepSort],
    "Base", [<PREFIX> Base],
    "Body", COALESCE ( [<PREFIX> Body · <Step 1>], [<PREFIX> Body · <Step 2>], /* ... */ ),
    "BarTop", [<PREFIX> Base] + COALESCE ( [<PREFIX> Body · <Step 1>], /* ... */ )
)
ORDER BY [StepSort]
```

Expected: `BarTop` for a drop step equals the prior step's running total (the top edge of the
drop bar). `BarTop` for a total step equals its own value. If anything's off, a step's
total/drop classification is wrong — fix it in the intake before building the visual.

## Next

[P3 — label measures](label-measures.md) — what to show on each bar (and the showSeries trap).
