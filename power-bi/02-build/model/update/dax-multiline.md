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

## Pitfall — body indent MUST be deeper than properties

The body must sit **strictly deeper** than the trailing `formatString:` / `displayFolder:` / `lineageTag:` lines. Same indent and the parser keeps consuming the body into the next property and reports *"The syntax for 'formatString' is incorrect"* on the first property line — which makes it look like a `formatString` typo, not an indent bug.

Right (body depth 3, properties depth 2 — shown with 4 spaces per level to match this doc's convention):

```tmdl
    measure 'Item Flow Base' =
            VAR _Sold = [Trade Quantity]
            RETURN SWITCH ( SELECTEDVALUE ( ItemFlowSteps[Step] ), "Items Placed", 0, ... )
        formatString: #,0
        displayFolder: 17. Item Flow Waterfall
        lineageTag: cc496d4a-...
```

Wrong (body and properties at the same depth — `formatString` gets parsed as DAX):

```tmdl
    measure 'Item Flow Base' =
        VAR _Sold = [Trade Quantity]
        RETURN SWITCH ( SELECTEDVALUE ( ItemFlowSteps[Step] ), "Items Placed", 0, ... )
        formatString: #,0          ← parser thinks this is still part of the DAX
```

Single-line measures (`measure 'X' = SUM(...)`) are immune — only multi-line bodies hit this. The `pbir` CLI accepts the wrong form silently; only Desktop catches it. Confirmed against working `Funnel Base` (correctly indented) and broken `Item Flow Base` (same indent) — 2026-06-04.

## Pitfall — triple-backtick fence indent

Triple-backtick must close at the same indent level as the opening triple-backtick. Mismatched fence indentation = parse error.
