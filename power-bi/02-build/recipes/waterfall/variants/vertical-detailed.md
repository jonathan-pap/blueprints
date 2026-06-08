# Variant — Vertical Detailed

Same structural shape as [vertical-standard](vertical-standard.md), but the anchor binds
`<PREFIX> Label (rich)` instead of `<PREFIX> Label`. Each step shows value + share-of-total +
a contextual phrase.

## Visual

Template: [../templates/vertical.visual.json](../templates/vertical.visual.json) — substitute
`<PREFIX> Label` with `<PREFIX> Label (rich)` in every `dynamicLabelValue` selector.

## Required measures

- P1, P2, P4 as for standard
- P3: BOTH `<PREFIX> Label` AND `<PREFIX> Label (rich)` (the simple one is still useful for
  validation queries and pages where you switch label style later)

## Label binding

Position adjustments for rich labels (they're longer):
- `labelPosition`: `'OutsideEnd'` (above each bar) or stay at `'InsideEnd'` if bars are tall enough
- `fontSize`: `10D` (slightly larger to give text room)

## Contextual phrases — author per use-case

The rich label measure's per-step phrases must be authored by the user during the intake
(Q1 or follow-up). Default phrases (e.g. "of total") work as a starting point but lose impact.
Strong phrases come from domain language:

| Generic phrase | Domain-specific phrase |
|---|---|
| "of total" | "NPC take" |
| "remaining" | "meaningful tier" |
| "subtracted" | "low-tier churn" |
| "delivered" | "reached gold" |

Encourage the user to provide one phrase per step.

## When to choose this

- Stakeholder-facing dashboards meant to be read once and remembered.
- Decks/screenshots that need to communicate the story without a live audience.
- When the share-of-total context is the most important second number after the value.

## Sample read

```
Step 1: 526,274 · 100% traded         ← total + share + word
Step 2: -100,329 · 19% NPC take       ← drop + share-of-total-lost + word
Step 3: 425,945 · 81% player          ← intermediate total + share + word
Step 4: -357,701 · 68% low-tier churn ← drop + share + word
Step 5: 68,244 · 13% meaningful       ← end total + share + word
```
