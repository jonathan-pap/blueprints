# KPI Selection (Brief-room reference)

> Picking *which* metrics to show. Implementation patterns live in `02-build/report/references/cards-and-kpis.md`.

## The 20% change test

For each candidate metric, ask: *"If this number changed 20%, should someone act differently?"*

- **Yes** → actionable metric, qualifies as a KPI.
- **No** → vanity metric, leave it off the page.

## Vanity vs actionable

| Vanity | Actionable |
|---|---|
| Total orders (always grows) | Orders vs prior year |
| Page views | Conversion rate |
| Total revenue | Revenue vs target / margin % |
| Customer count | Net new customers, churn % |

Comparative metrics (vs prior period, vs target, vs peer) almost always beat absolute ones because they answer "good or bad?" immediately.

## Working-memory cap

Human working memory holds 3–4 chunks. **Page ceiling: 5 KPIs.** If the user wants more, ask which decision they're optimizing for and cut to the top 3–5.

## Every KPI needs a target

A bare number cannot be judged. Pick a target source per metric:

| Source | When |
|---|---|
| Prior year (1YP) | Default when nothing else exists |
| Prior period | Short-term ops metrics |
| Budget / forecast | When budgets live in the model |
| Rolling average | Smoothing volatile measures |
| User-supplied threshold | One-off business rule |

If no target exists in the model, **ask the user** which one to use before building. Do not leave KPIs bare.

## Selection workflow

1. Read the page's central question (from the brief).
2. List candidate measures from the model (`pbir model "<name>.Report" -d`).
3. Apply the 20% change test to each.
4. Keep the top 3–5 that serve the page question.
5. Pair each with a target source.
6. Propose the final list back to the user before building.

## Output of this step

A locked KPI list of the form:

```
1. <Measure Name>  →  target: <source>
2. <Measure Name>  →  target: <source>
3. <Measure Name>  →  target: <source>
```

Hand off to `02-build/report/` to build the cards.
