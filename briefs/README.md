# Briefs — the intake hub

A cross-blueprint starting point for writing **briefs**: pick a template, fill it in, and drop it
into the right blueprint. A brief is the contract for a piece of work — comprehensive brief = zero
discovery questions.

> This is a **utility folder, not a blueprint.** It holds no rooms and routes nothing. The
> canonical templates live inside each blueprint (so blueprints stay self-contained); this hub
> just links to them and shows filled examples.

## How to use

1. **Pick a template** from the table below and copy it.
2. **Fill it in** — replace the bracketed sections, delete what doesn't apply.
3. **Save it** to the blueprint's project folder:
   `<blueprint>/projects/<name>/brief.md`.
4. The blueprint's **brief-discovery hook** surfaces it on your next prompt (a `<recent-briefs>`
   block), and the agent reads it before asking questions or proposing a plan.

## Templates (canonical — edit in place, or copy from here)

| Template | For | Lives in |
|---|---|---|
| [Power BI report](../power-bi/01-brief/brief-template.md) | a report / dashboard | `power-bi/01-brief/` |
| [Power BI theme](../power-bi/02-build/theme/create/brief-template.md) | a theme JSON | `power-bi/02-build/theme/create/` |
| [Synthetic-data job](../synthetic-data/01-brief/brief-template.md) | a dummy-data generation job | `synthetic-data/01-brief/` |

The template stays canonical in its blueprint so a zipped blueprint still works standalone. This
hub links to it rather than keeping a second copy that could drift.

## Examples (filled — what "good" looks like)

| Example | Shows |
|---|---|
| [Power BI — Sales Overview](examples/power-bi-sales-overview.md) | a complete report brief (audience, KPIs, pages, theme, constraints) |
| [Synthetic-data — demo financials](examples/synthetic-data-demo-financials.md) | a generation job that produces the data the report above runs on |

The two examples are a **paired set**: the synthetic-data job generates a `financials` table; the
Power BI brief builds the report on it — the same cross-blueprint hand-off the blueprints support.

## Why briefs

- **File-first, chat-second.** The brief persists; chat doesn't. The agent reads the brief before
  interviewing you, so a good brief means fewer (or zero) discovery questions.
- **The source of truth** for *why* the deliverable looks the way it does — keep it updated as the
  work evolves.

## See also

- [../power-bi/01-brief/context.md](../power-bi/01-brief/context.md) — Power BI brief room (file-first pattern)
- [../synthetic-data/01-brief/context.md](../synthetic-data/01-brief/context.md) — synthetic-data brief room
- Each blueprint's `hooks.yaml` (`briefs:`) toggles the discovery hook.
