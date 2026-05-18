# Partition properties

## Required

- A name
- A source — `= m` (Power Query), `= calculated` (DAX table), `= entity` (Direct Lake), etc.
- `mode` — storage mode

## Mode enum

- `import` — VertiPaq in-memory (most common)
- `directQuery` — pass-through to source
- `dual` — both
- `directLake` — Fabric Direct Lake
- `push` — streaming-pushed data
- `default`

## Source kinds

- `m` — M / Power Query expression
- `calculated` — DAX expression
- `entity` — Direct Lake entity reference
- `query` — SQL query (legacy)
- `none`
- `calculationGroup`
- `inferred`
- `policyRange` — incremental refresh range

## Example: M partition

```tmdl
partition 'Sales-Partition' = m
    mode: import
    source = ```
            let Source = Sql.Database("srv", "db"),
                Sales  = Source{[Schema="dbo", Item="Sales"]}[Data]
            in Sales
            ```
```

## Example: calculated partition

```tmdl
partition 'Date-Partition' = calculated
    mode: import
    source = CALENDAR(DATE(2020,1,1), DATE(2030,12,31))
```

## Multiple partitions per table

Common for incremental refresh — one partition per period (Q1, Q2, Q3, Q4 of each year). Each has its own `source` and refresh policy. Out of scope for a typical thick PBIP — Power BI Service manages this for published models.
