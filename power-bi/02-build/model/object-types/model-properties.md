# Model-level properties

Set in `model.tmdl` at the top.

## Common

- `culture: 'en-US'` — model's default culture
- `defaultPowerBIDataSourceVersion: powerBI_V3` — `powerBI_V1`, `powerBI_V2`, `powerBI_V3`
- `discourageImplicitMeasures` (flag) — disables auto-generated SUM/COUNT/etc when users drag columns
- `directLakeBehavior` — `automatic`, `directLakeOnly`, `directQueryOnly`

## Pattern

```tmdl
model Model
    culture: en-US
    defaultPowerBIDataSourceVersion: powerBI_V3
    discourageImplicitMeasures

    annotation PBI_QueryOrder = ["Sales Query","Customers Query","Date"]
```

## `ref table` entries

After defining a table in `tables/<Name>.tmdl`, register it in `model.tmdl`:

```tmdl
ref table 'Sales'
ref table 'Customers'
ref table 'Date'
```

Order in `model.tmdl` controls table order in the Desktop sidebar.

## `queryGroup` entries

Groupings shown in the Power Query editor's left sidebar:

```tmdl
queryGroup 'Sources'
    annotation PBI_QueryGroupOrder = 0

queryGroup 'Transformations'
    annotation PBI_QueryGroupOrder = 1
```

## Annotations Power BI manages

- `PBI_QueryOrder` — order of M expressions in the editor
- `PBI_QueryGroupOrder` — query group display order
- `__PBI_TimeIntelligenceEnabled` — auto date hierarchies toggle

Leave these alone; Desktop manages them.
