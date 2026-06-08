# Variant — Vertical Standard

Default. `lineStackedColumnComboChart` (vertical combo) + Y2 anchor + `<PREFIX> Label` for
labels. The simplest, most-tested combination.

## Visual

Template: [../templates/vertical.visual.json](../templates/vertical.visual.json) — no
substitutions beyond the standard tokens.

## Required measures

- P1: [steps disconnected table](../primitives/steps-table.md)
- P2: `<PREFIX> Base` + one `<PREFIX> Body · <Step>` per step
- P3: `<PREFIX> Label` (not the rich version)
- P4: `<PREFIX> Axis Max` + `<PREFIX> Label Anchor`

Skip P5 (horizontal pad) and P6 (stacked sub-segments).

## Label binding

In the template's `labels[]`, ensure all `dynamicLabelValue` selectors point at `<PREFIX> Label`
(not `<PREFIX> Label (rich)`). Default position: `'InsideEnd'` (top of each bar).

## When to choose this

- First waterfall you build on a new model.
- Domains where the labels are dense and rich context would clutter (e.g. multiple bars at
  similar values).
- When the story is read at a glance (dashboards, screensavers).

## Sample read

```
Step 1: 526,274     ← total
Step 2: -100,329    ← drop
Step 3: 425,945     ← intermediate total
Step 4: -357,701    ← drop
Step 5: 68,244      ← end total
```
