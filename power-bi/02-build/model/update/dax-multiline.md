# Multi-line DAX in TMDL

Two syntaxes. Pick by complexity.

## Indented block (preferred)

DAX body is **2 levels deeper** than the enclosing declaration. Properties stay at depth 2.

```tmdl
measure 'Actuals MTD' =
        CALCULATE(
            [Actuals],
            CALCULATETABLE(
                DATESMTD('Date'[Date]),
                'Date'[IsDateInScope]
            )
        )
    formatString: #,##0
    displayFolder: 2. MTD
    lineageTag: abc-123
```

Indentation depth quick-reference:

- Declaration (`measure`, `column` inside table): depth 1
- Properties of that declaration: depth 2
- DAX body: depth 3
- Top-level `function`: depth 0; its DAX body: depth 2
- `calculationItem` inside calculation group: depth 2; its DAX body: depth 4

## Triple-backtick (when indentation is awkward)

Wrap the DAX in `` ``` ``. Whitespace inside is preserved, no need to count tabs.

```tmdl
measure 'Percentage' = ```
        VAR _Total = CALCULATE(SUM('Table'[Qty]), REMOVEFILTERS())
        RETURN
            DIVIDE(SUM('Table'[Qty]), _Total)
        ```
    formatString: 0.0%;-0.0%;0.0%
    lineageTag: abc-123
```

Useful for:

- DAX with verbatim string literals containing significant whitespace.
- Multi-line `formatStringDefinition` expressions.
- DAX you pasted from a `dax` query file and don't want to re-indent.

## Pitfall

Triple-backtick must close at the same indent level as the opening triple-backtick. Mismatched fence indentation = parse error.
