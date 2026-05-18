# MDL001 — Many-to-many relationship optimization

> Tier 3 — user approval required. Warn downstream report impact.

Bridge tables create expanded tables the engine materializes every query. The right layout depends on filter paths, bridge cardinality, and RLS. **Test each option.**

## Scenario

`User` (security), `Customer` (dimension), `UserCustomer` (bridge), `Fact`.

## Option A — Canonical (bidir bridge)

```
User 1──* UserCustomer *──bidir──1 Customer 1──* Fact
```

Customer filters Fact directly; bridge only traversed for User. Best when User is rarely a slicer alongside Customer. Bidir causes high FE cost when both filter together.

## Option B — M2M bridge to fact (no bidir)

```
User 1──* UserCustomer *──1 Customer
                │
                *──M2M──* Fact
```

Both dims always filter through bridge M2M. Best when consistent query times matter more than peak Customer-only performance.

## Option C — Optimized hybrid

```
User 1──* UserCustomer *──M2M──* Fact *──1 Customer
```

Customer filters Fact directly; User filters through bridge M2M. No bidir. **Best general-purpose layout.** Use inactive relationship + `USERELATIONSHIP` if you need Customer↔UserCustomer cross-queries.

## Option D — Pre-computed combination key

```
User 1──* UserCombinations *──M2M──* Fact *──1 Customer
```

ETL assigns a surrogate key per unique set of customers a user can access — users with identical access share one key. Best when bridge is very large or many users share the same access patterns.

## Decision

Test all four against actual workload. The trade-off matrix changes with bridge cardinality, RLS user count, and which slicers are most-used.
