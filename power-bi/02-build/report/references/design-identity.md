# Design identity — the model (tone · signature · archetype)

> The vocabulary for deciding **what a report should look like and why**, before any `pbir` command.
> This is reference material, not a workflow — the end-to-end process that *uses* it is
> [`../build-report.md`](../build-report.md) (Phase A). Theme owns appearance,
> [`../layout/design-system.md`](../layout/design-system.md) owns dimensions; this names the
> **decisions** those two then encode into a `Design Brief:` ([`../layout/design-contract.md`](../layout/design-contract.md)).

## What this covers (and what owns the rest)

| Decided here (design judgment) | Owned elsewhere (mechanics) |
|---|---|
| Tone + signature (the report's feel + its one recurring move) | colors/fonts/padding → [`../../theme/`](../../theme/context.md) |
| Per-page archetype + layout variant | sizes/positions/zones → [`../layout/`](../layout/_index.md) |
| Which chart answers which question | exact `visualType` + PBIR mechanics → [`../add-visual/`](../add-visual/_index.md) |
| The layout contract that gates authoring | hard layout checks → [`audit-layout-consistency.sh`](../../../04-review/hooks/) |

These are **decision-time** choices — they never edit `visual.json`. The output is a `Design Brief:`
block the build path reads like a spec.

## The model — three commitments

1. **Tone** — the report's feel. One named entry from [`tones.md`](tones.md) (or a remix/custom),
   chosen for audience + data + brand. A tone is a *constraint*: it pins typography, palette,
   density, gridline/border treatment. Picking it makes every later choice easier.
2. **Signature** — the one defining visual move every page shares ([`signatures.md`](signatures.md)).
   It must *emerge from* the tone, not fight it.
3. **Archetype** — routed **per page**, not per report ([`archetypes/_index.md`](archetypes/_index.md)).
   A single "cover everything" request usually decomposes into pages of *different* archetypes.

Tone + signature are uniform across the whole report; archetype + variant rotate per page.
A report where page 1 is Editorial and page 2 is Industrial reads as two reports stitched together.

## The vocabulary (atomic reference files)

- **Tone / signature** → [`tones.md`](tones.md) · [`signatures.md`](signatures.md)
- **Per-page archetype + variant** → [`archetypes/_index.md`](archetypes/_index.md)
- **Multi-page composition + variant rotation** → [`composition.md`](composition.md)
- **Which chart for the question** → [`../add-visual/pick-visual-type.md`](../add-visual/pick-visual-type.md)
- **Colour palette + assignment** → [`color-palettes.md`](color-palettes.md)
- **Interaction model** → [`interactivity.md`](interactivity.md)
- **Pre-ship checks** → [`accessibility.md`](accessibility.md) · [`anti-patterns.md`](anti-patterns.md)
- **Redesign an existing report** → [`brownfield.md`](brownfield.md)
- **The contract this feeds** → [`../layout/design-contract.md`](../layout/design-contract.md)

## Principles (apply whenever using this vocabulary)

- **Inspect the model first.** No design decision before reading the semantic model (tables, columns,
  measures, cardinality, magnitudes). A flat line or two-bar chart means the wrong visual was chosen.
  See [`../build-report.md`](../build-report.md) step A0.
- **Tone must propagate.** If the brief says `tone: editorial newsroom` but ships the same fonts,
  palette, and borders as every other report, the tone is decorative. Walk the tone's downstream
  column in [`tones.md`](tones.md).
- **One analytical question per visual.** If a visual answers two, split it.
- **Every callout earns its space.** A KPI/context tile that repeats an absolute measure already in the
  adjacent chart is noise — it needs a *derived* basis (Δ, variance %, rank, threshold, narrative).
- **Decide, don't author.** These choices end at an approved `Design Brief:`; file mechanics belong to
  the build path ([`../build-report.md`](../build-report.md) Phase B) and [`../context.md`](../context.md).

## Where it sits in the blueprint

```
01-brief/        WHAT the report must do (audience, KPIs, scope)
   │
   ▼
references/design-identity.md + catalogs   ← the vocabulary: what it looks like + why
   │                          (used by build-report.md Phase A)  →  Design Brief: contract
   ▼                                                                       │
02-build/theme/  appearance tokens     02-build/report/layout/design-system.yaml  dimensions
   │                                                                       │
   ▼                                                                       ▼
02-build/report/ build-report.md Phase B implements the contract  →  04-review/ validates
```
