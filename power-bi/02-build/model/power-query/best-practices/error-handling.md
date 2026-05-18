# Error handling

For production partitions, **avoid `try...otherwise` patterns that silently swallow errors.** A failed refresh is better than silently loading wrong data.

## When `try...otherwise` is appropriate

Optional columns where missing is expected:

```m
#"Safe Amount" = Table.TransformColumns(Data, {
    {"Amount", each try Number.FromText(_) otherwise null, type number}
})
```

Make the error handling explicit and narrow. Only catch the specific failure you anticipate.

## When `try...otherwise` is dangerous

Wrapping the whole expression to "make refresh succeed":

```m
-- DANGEROUS
let
    Source = try Sql.Database(...) otherwise ...
in
    Source
```

This silently masks real connection / schema problems. The refresh succeeds, the table loads empty or with stale defaults, downstream reports look fine but show wrong numbers.

## Better: let it fail loudly

If the source isn't available, the refresh should fail with a clear error so someone investigates. Refreshes are recoverable; silent data corruption isn't.

## When you can't avoid it

For genuinely-optional sources (user-uploaded files, optional integrations), document the fallback and notify someone:

```m
#"Optional Data" = try
    Sql.Database(OptionalServer, OptionalDb)
  otherwise
    Table.FromRecords({}, type table [...])  -- empty table with correct schema

-- Separate query / measure flag to detect when the optional source is missing
#"Has Optional Data" = Table.RowCount(#"Optional Data") > 0
```

Then surface `Has Optional Data` in the model so report builders can show "no data available" instead of empty visuals.

## See also

- `anti-patterns.md` — broader list of common mistakes
- `../validation/_index.md` — validate before deploying
