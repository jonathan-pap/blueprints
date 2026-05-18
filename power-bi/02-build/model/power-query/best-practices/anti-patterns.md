# Anti-patterns

Common M mistakes and what to do instead.

## 1. Pulling entire tables then filtering

```m
-- Anti-pattern: filter after all transforms
Data = Source{[Schema="dbo", Item="BigTable"]}[Data],
#"Added Column" = Table.AddColumn(Data, ...),    -- breaks folding
#"Filtered" = Table.SelectRows(#"Added Column", each [Year] >= 2023)
-- Filter runs locally on ALL rows
```

**Fix:** filter first, then add columns. See `row-filtering.md`.

## 2. Using `Table.Buffer` unnecessarily

`Table.Buffer` forces the entire table into memory. Only use when the same table is referenced multiple times and re-evaluation would be expensive.

Casual use of `Table.Buffer` doubles memory and breaks folding for everything after it. Almost always a mistake.

## 3. Cross-query references

Accessing a column from a different query breaks folding and can cause cascading performance issues. The engine has to evaluate one query to provide values to another, which often fails to fold.

**Fix:** if you need data from another query, either:

- Merge the queries with `Table.NestedJoin` (folds when same SQL source)
- Make the cross-reference at the source via a view

## 4. Excessive step count

Each step adds overhead. Combine related operations where natural.

**Bad:**

```m
#"Renamed1" = Table.RenameColumns(Data, {{"OldName1", "NewName1"}}),
#"Renamed2" = Table.RenameColumns(#"Renamed1", {{"OldName2", "NewName2"}})
```

**Good:**

```m
#"Renamed" = Table.RenameColumns(Data, {
    {"OldName1", "NewName1"},
    {"OldName2", "NewName2"}
})
```

`Table.RenameColumns` handles multiple in one call. Same for `Table.TransformColumnTypes`, `Table.TransformColumns`, `Table.RemoveColumns`, `Table.SelectColumns`.

## 5. Generic step names

```m
#"Custom1" = ...
#"Step1" = ...
```

Future-you and future-coworkers can't read these. Use descriptive names matching what the step does.

## 6. Sorting unnecessarily

`Table.Sort` folds to `ORDER BY` but adds source-side work that's almost always pointless — Power BI ignores sort order on load. Only sort if a downstream step requires it (e.g., `Table.AddIndexColumn` after sort).

## See also

- `naming-conventions.md`
- `query-folding.md`
- `error-handling.md`
