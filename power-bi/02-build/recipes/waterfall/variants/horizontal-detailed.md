# Variant — Horizontal Detailed

Same structural shape as [horizontal-standard](horizontal-standard.md), but the Anchor binds
`<PREFIX> Label (rich)` for value + share + phrase per step.

## Visual

Template: [../templates/horizontal.visual.json](../templates/horizontal.visual.json) —
substitute `<PREFIX> Label` with `<PREFIX> Label (rich)` in the `dynamicLabelValue` selector
on the Anchor.

## Required measures

- P1, P2, P4, P5 as for horizontal-standard
- P3: BOTH `<PREFIX> Label` AND `<PREFIX> Label (rich)`

## Layout tip — wider labels mean a wider chart

Rich labels are 2–4× the character length of standard. Allow more chart width so labels don't
crowd the visible bars. Reduce the page-level `width` for the visual if you need narrower
bars to fit the labels.

`labelOverflow: true` (already in the horizontal template) handles overflow without clipping
to a hard width.

## When to choose this

- Same use cases as horizontal-standard, but the labels need to carry the story by themselves.
- Reports embedded in slides where each chart's labels are quoted verbatim.

## Sample read

```
  Total Volume        ████████████████████████ 526,274 · 100% traded
  NPC Mediated                            ███ -100,329 · 19% NPC take
  Player Volume       ████████████████████ 425,945 · 81% player
  Common+Uncommon                       ████ -357,701 · 68% low-tier churn
  Rare+ Player        ████ 68,244 · 13% meaningful
```
