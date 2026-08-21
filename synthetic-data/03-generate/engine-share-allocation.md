# Engine — top-down share allocation + raking

> How [`generate.py`](generate.py) turns a `total` + `shares` into fact rows whose marginals
> reconcile at every granularity. This is the "smart" core that makes a demo dataset tell a
> *coherent* story instead of being random noise. Config grammar: [`../02-schema/config-schema.md`](../02-schema/config-schema.md).

## Why top-down (not row-by-row)

A naïve generator draws each row independently, so the totals land wherever the RNG puts them —
Region mix, seasonality, and growth are all accidental. Here you **declare the marginals** (this
Region is 40%, December peaks, +8%/yr) and the engine allocates the top line *down* to rows, then
**rakes** to remove the drift that noise introduces. The declared story holds at day, month, region,
product — any grain a report slices by.

## The pipeline (per allocated measure)

1. **Grid.** Build the grain cross-product (Date × Region × Product…), then drop `sparsity` fraction
   of cells once per fact (structural zeros — not every product sells every day).
2. **Share vectors.** For each grain dimension, resolve a weight vector over its members that sums to 1.
   All blocks targeting the dimension **compose**:
   - **curves** (`pareto`, `seasonal`, `[list]`, `trend.yoy` on the calendar) multiply together and
     rank members;
   - the first **dict** block (dimension- or attribute-keyed) is the **exact** block: the curve product
     is normalized *within each of its groups*, then scaled to the group's declared share. So
     `Item: pareto` + `Category: {Potions: .3, …}` gives a flagship-led long tail *inside* categories
     that still sum exactly to their shares. Undeclared groups split the remainder evenly; a second
     dict on the same dim only shapes (approximate).
3. **Outer product.** Expected value per cell = `total × Π_d w_d[member]`. Because each `w_d` sums to 1,
   the grand total is `total` in expectation and each 1-D marginal equals `total × share`.
4. **Noise.** Multiply by a mean-preserving lognormal `exp(N(−½σ², σ))` (σ = `noise`) for realistic
   row-level variation without shifting the mean.
5. **Guardrails.** Soft-clamp to `[min, max]`.
6. **Rake (IPF).** Iterative proportional fitting: repeatedly, for each grain dim, scale every row by
   `target_marginal / current_marginal`. Cycling over dims converges so **all 1-D marginals match
   exactly** (to tolerance) — restoring the declared shares that noise, clamping, and sparsity perturbed.
   The grand total is a marginal too, so it lands exactly on `total`.

Derived measures are evaluated last, as expressions over the allocated columns plus per-row sampled
params (e.g. `Orders = Revenue / avg_order_value`).

## What raking guarantees — and doesn't

- **Exact:** every declared 1-D marginal (per grain dim, and per attribute on a grain dim) and the
  grand total. Verified by [`../05-review/reconcile.py`](../05-review/reconcile.py).
- **Not controlled:** cross (higher-order) marginals — Region×Category mix — unless declared as a cross
  (v1 is 1-D per key). The joint starts at the independent outer product and only its 1-D margins are
  pinned; correlations beyond that are whatever the outer product implies.
- **Precedence:** if a hard `max` would force a marginal off, **raking wins** — the total is sacred, so
  a cap can be exceeded on a few rows. Widen the cap or lower the total if that matters.

## Scaling

The cross-product is `Π |dim|` rows before sparsity — a calendar × a few dims stays in the low
millions (vectorized in numpy/pandas, fine in memory). For very large grains, raise `sparsity`, shorten
the date range, or shrink a generated dimension. Raking is ~40 cheap passes; it dominates nothing.

## Extending

- **New built-in curve** (e.g. `weekly`, `monthend`): add a branch in `share_vector`.
- **Cross shares** (2-D marginals): rake against a joint target table instead of independent 1-D targets.
- **New dimension kind**: add to `build_dimensions` (e.g. a snowflake/parent ref).
Keep the config the source of truth — never hardcode a domain in the engine.
