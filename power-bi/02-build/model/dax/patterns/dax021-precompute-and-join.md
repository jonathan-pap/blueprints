# DAX021 — Pre-compute and join instead of filter round-trip

When a measure computes a qualifying key set from a filtered aggregation and then uses TREATAS or IN to filter a second aggregation by those keys, the outer SUMMARIZECOLUMNS context compounds the key filter with groupby columns — generating large tuple semi-joins (e.g., 500+ `(Brand, Key)` pairs in a single WHERE clause). The compound-tuple SE scan often dominates total query time.

## Signal

`VertiPaqSEQueryEnd` with `DEFINE TABLE ... ININDEX` or `WHERE ... IN` containing hundreds of compound tuples. Single scan duration disproportionately high relative to others.

## Fix

Pre-compute both aggregations independently at the shared key grain, then join with NATURALINNERJOIN in the FE.

The table expression used to build each side — `ADDCOLUMNS(VALUES(...), ...)`, `SUMMARIZECOLUMNS(...)`, etc. — does not matter; the key is that both sides share a common lineage column for the join.

## Anti-pattern — TREATAS pushes key set back to SE, compounded by outer groupby

```dax
VAR _FilteredAgg =
    CALCULATETABLE(
        ADDCOLUMNS(VALUES('Fact'[Key]), "@Agg1", [Measure]),
        'Dim'[Filter] = "X"
    )
VAR _Qualifying = FILTER(_FilteredAgg, [@Agg1] > 1000000)
VAR _Result =
    CALCULATE(
        [Measure],
        TREATAS(SELECTCOLUMNS(_Qualifying, "K", 'Fact'[Key]), 'Fact'[Key])
    )
```

## Preferred — both aggregations pre-computed, joined in FE

```dax
VAR _FilteredAgg =
    CALCULATETABLE(
        ADDCOLUMNS(VALUES('Fact'[Key]), "@Agg1", [Measure]),
        'Dim'[Filter] = "X"
    )
VAR _Qualifying = FILTER(_FilteredAgg, [@Agg1] > 1000000)
VAR _UnfilteredAgg =
    ADDCOLUMNS(VALUES('Fact'[Key]), "@Agg2", [Measure])
VAR _Joined = NATURALINNERJOIN(_Qualifying, _UnfilteredAgg)
VAR _Result = SUMX(_Joined, [@Agg2])
```

## Why it works

Each pre-computed table generates independent SE scans — clean, no tuple filters. NATURALINNERJOIN matches on the shared `'Fact'[Key]` lineage column in the FE, replacing the expensive compound-tuple SE round-trip with a fast in-memory join over small pre-materialized tables.
