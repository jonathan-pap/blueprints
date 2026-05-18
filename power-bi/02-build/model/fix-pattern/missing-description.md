# Fix: add a description to a measure / column / table

`///` (triple-slash) sets the `Description` property on the **next** declaration. Native TMDL syntax, not a comment.

## Correct

```tmdl
/// Sum of Sales[Amount] in the current filter context.
measure 'Total Revenue' = SUM('Sales'[Amount])
    formatString: #,##0
    lineageTag: abc-123
```

## Wrong — blank line between

```tmdl
/// This description does NOT attach.

measure 'Total Revenue' = SUM('Sales'[Amount])
```

Blank line breaks the connection. Property silently doesn't set.

## Wrong — comment masquerading

```tmdl
// This is a regular comment. Description NOT set.
measure 'Total Revenue' = SUM('Sales'[Amount])
```

`//` is a plain comment. Only `///` sets descriptions.

## Multi-line description

Multiple `///` lines concatenate:

```tmdl
/// Sum of Sales[Amount] in current filter context.
/// Excludes returns. Currency: USD.
measure 'Total Revenue' = SUM('Sales'[Amount])
```

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
