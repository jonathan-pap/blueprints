# Update a measure's DAX expression

Edit the expression after `=` in the measure declaration.

## Single-line → single-line

```tmdl
# Before
measure 'Total Revenue' = SUM('Sales'[Amount])

# After
measure 'Total Revenue' = SUMX('Sales', 'Sales'[Qty] * 'Sales'[Price])
```

## Single-line → multi-line

Drop the expression to the next line and indent 2 levels deeper than the declaration:

```tmdl
measure 'Total Revenue' =
        SUMX(
            'Sales',
            'Sales'[Qty] * 'Sales'[Price]
        )
    formatString: #,##0
    lineageTag: abc-123
```

Keep `formatString:` and other properties at depth 2 (one less than the DAX body).

## Multi-line indented vs triple-backtick

Triple-backtick (`` ``` ``) is useful when your DAX has complex indentation you don't want to manage with tabs:

```tmdl
measure 'Percentage' = ```
        VAR _Total = CALCULATE(SUM('Table'[Qty]), REMOVEFILTERS())
        RETURN DIVIDE(SUM('Table'[Qty]), _Total)
        ```
    formatString: 0.0%;-0.0%;0.0%
```

## Keep the lineageTag

Don't touch `lineageTag:`. The measure's identity is tied to it.

## Validate

```bash
bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"
```

If MCP is available, also live-validate the DAX itself: `../../../03-bind/via-mcp/validate-dax.md`.
