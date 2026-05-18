# MDL002 — Star schema conformance

> Tier 3 — user approval required.

Snowflake schemas force multiple SE joins per query. Flatten dimension chains into a single wide dimension to reduce join depth and enable better fusion.

## Before — snowflake

```
Sales ──* Product ──* Subcategory ──* Category
```

Each query that filters by Category does 3 joins: Sales → Product → Subcategory → Category.

## After — flat dimension

```
Sales ──* Product [ProductKey, ProductName, Subcategory, Category]
```

Same query: 1 join.

## How to flatten

In Power Query (preferred — keeps the model clean):

```m
let
    Source = ...,
    JoinSubcat = Table.NestedJoin(Source, "SubcategoryKey", Subcategory, "Key", "Sub"),
    Expanded1 = Table.ExpandTableColumn(JoinSubcat, "Sub", {"Name", "CategoryKey"}, {"Subcategory", "CategoryKey"}),
    JoinCat = Table.NestedJoin(Expanded1, "CategoryKey", Category, "Key", "Cat"),
    Expanded2 = Table.ExpandTableColumn(JoinCat, "Cat", {"Name"}, {"Category"})
in
    Expanded2
```

Or via the source warehouse — preferable for large dimensions; the join happens once during ETL, not on every refresh.

## Trade-off

- Wider dimension table = larger dictionary (string columns can blow up cardinality).
- If Category and Subcategory have very low cardinality vs the flattened Product (1k:1m), the dictionary cost is negligible.
- Star schema clarity in the model wins over normalized "purity" almost every time for analytical performance.
