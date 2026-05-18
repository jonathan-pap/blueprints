# Lakehouse sources

Fabric Lakehouse Delta tables as a Power Query source.

## Pattern

```m
let
    Source = Lakehouse.Contents(null),
    Data = Source{[Id="lakehouse-guid"]}[Data],
    Table = Data{[Id="table-name", ItemKind="Table"]}[Data]
in
    Table
```

## Finding the IDs

```bash
# Get lakehouse ID
fab get "WS.Workspace/MyLakehouse.Lakehouse" -q "id" | tr -d '"'

# List tables in the lakehouse
fab ls "WS.Workspace/MyLakehouse.Lakehouse/Tables"
```

## Variations

### Direct Lake (preferred for large tables)

If the model uses Direct Lake mode, the partition is generated automatically by the engine — you don't write M for it. The model points at the Delta table; the engine reads parquet directly.

For Direct Lake-specific tuning, see `../../dax/model-tuning/dl001-v-ordering.md` and `dl002-segment-size.md`.

### Import mode (this pattern)

Use the M expression above when:

- Table is small enough for full import
- You need to combine with other sources (lakehouse + SQL, e.g.)
- You need Power Query transformations the source can't express

## Limitations

- M against Lakehouse is **slower than Direct Lake** for read-heavy workloads
- Folding is limited compared to SQL sources (lakehouse engine differs)
- Some transformations push down efficiently via Spark; others don't

## See also

- `../best-practices/query-folding.md` — folding rules differ by source
- `../../dax/model-tuning/dl001-v-ordering.md` — Direct Lake alternative
