# Config schema — the declarative star grammar

> The single config the engine reads. Declare **dimensions** and **facts**; facts carry
> **measures** with a top-line `total` and `shares` per dimension/attribute. The engine
> ([`../03-generate/generate.py`](../03-generate/generate.py)) allocates the total across the
> grain and **rakes** it so every declared marginal reconciles at every granularity. One config
> = one domain; change the config, not the code. Method: [`../03-generate/engine-share-allocation.md`](../03-generate/engine-share-allocation.md).

Copy [`schema-template.yaml`](schema-template.yaml) and adapt. Validate the output with
[`../05-review/reconcile.py`](../05-review/reconcile.py).

## Top level

```yaml
name: retail-demo                 # job name; default output dir is outputs/<name>/latest
seed: 42                          # RNG seed — reproducible (records to _manifest.json)
output: { dir: outputs/retail-demo/latest }   # optional; overrides the default
dimensions: { ... }               # see below
facts: { ... }                    # see below
```

## `dimensions`

Each key is a dimension **name** (→ emitted as `Dim<Name>.csv` with a surrogate key). Three kinds:

| Kind | Declares | Produces |
|---|---|---|
| **calendar** | `type: calendar`, `range: [start, end]`, `grain: day` | `DateKey`, `Date`, `Year`, `Quarter`, `Month`, `MonthName`, `DayName` — the built-in hierarchy |
| **explicit members** | `key:`, `members: [ {Col: val, …}, … ]` | one row per member (attribute columns as declared) |
| **generated** | `key:`, `generate: N`, `attributes: {…}` | N members with a surrogate key + generated attributes |

Generated `attributes` support:
- `{ values: [...], weights: [...] }` — categorical draw (weights optional)
- `{ faker: "<provider>" }` — realistic text (needs `pip install faker`; e.g. `company`, `city`)
- `{ min: a, max: b }` — integer draw

```yaml
dimensions:
  Date:    { type: calendar, range: [2023-01-01, 2025-12-31], grain: day }
  Region:  { key: RegionKey, members: [ {Region: North, Country: USA}, {Region: West, Country: USA} ] }
  Product: { key: ProductKey, generate: 40,
             attributes: { Category: { values: [Electronics, Home, Apparel], weights: [.5,.3,.2] } } }
```

## `facts`

Each key is a fact **name** (→ `Fact<Name>.csv`, with a surrogate FK to every grain dim).

```yaml
facts:
  Sales:
    grain: [Date, Region, Product]     # which dimensions this fact is at
    sparsity: 0.35                     # 0..1 fraction of grain cells that DON'T exist (structural zeros)
    measures: { ... }
```

### `measures`

Two kinds — **allocated** (has `total` + `shares`) and **derived** (an expression).

**Allocated measure:**

```yaml
Revenue:
  total: 10000000            # the grand total across the whole fact (the anchor everything reconciles to)
  min: 0                     # soft per-row floor (guardrail on the base allocation)
  max: 6000                  # soft per-row cap
  noise: 0.20                # ±relative lognormal row jitter (0 = perfectly smooth)
  trend: { yoy: 0.08 }       # +8% year-over-year (applied on the calendar dim)
  shares:                    # ← shares across granularities; each block must sum to ~1
    Region:    { North: .40, South: .35, West: .25 }   # keyed by a grain DIMENSION's members
    MonthName: seasonal                                 # keyed by an ATTRIBUTE column; built-in curve
    Category:  { Electronics: .5, Home: .3, Apparel: .2 }
```

- **`shares` keys** are either a **grain dimension name** (members reconcile *exactly* after raking) or
  an **attribute column** on a grain dim (e.g. `Category` on Product, `MonthName`/`Month` on Date —
  also reconcile exactly because the engine splits each group's share among its members and rakes the
  grain dim). A dimension with no `shares` block is allocated **uniformly**.
- **Special values:** `seasonal` (12-month retail curve, peaks Nov/Dec — only on `Month`/`MonthName`),
  `pareto` (1/rank, an 80/20 long tail — on a member dimension), or a bare `[list]` of weights.
- **Members you omit** from a `{dict}` split the remaining share evenly.

**Derived measure** — an expression over the other measures + sampled params (no `total`):

```yaml
Orders:
  derived: "np.maximum(1, np.round(Revenue / avg_order_value))"
  avg_order_value: { min: 45, max: 130 }    # sampled per row, referenced by name in the expression
```

Expressions see the other measures as numpy arrays, plus `np` and `round`; they run in a
restricted namespace (config-controlled, no builtins).

## What you get

`Dim<Name>.csv` per dimension + `Fact<Name>.csv` per fact + `_manifest.json` (seed, row counts),
in `output.dir`. Surrogate keys resolve every FK. Hand off to Power BI via
[`../04-output/handoff-to-power-bi.md`](../04-output/handoff-to-power-bi.md).

## Reconciliation guarantee (and its edge)

After raking, **every grain dimension's marginal ties out exactly** (sum over Region = declared
Region shares × total, at any tolerance). Attribute-level shares on a grain dim reconcile exactly
too. What is **not** controlled: **higher-order** (cross) marginals — e.g. Region×Category mix — unless
you declare that cross explicitly (v1 supports 1-D shares per key). Noise and `min`/`max` shape row
values but never break the declared marginals; if a hard cap fights a marginal, raking wins (the total
is sacred). Prove any run with `reconcile.py`.
