# Fix: dynamic format string (`formatStringDefinition`)

Use when the format should be computed by DAX (variance signs, currency switching, calculation-group-driven formats).

## Pattern

Replace `formatString:` with a `formatStringDefinition =` block at depth 2:

```tmdl
measure 'Variance' = [Actual] - [Target]
    displayFolder: 3. Variance
    lineageTag: abc-123

    formatStringDefinition =
            IF([Variance] < 0, "(#,##0)", "#,##0")
```

## Multi-line definition

Same DAX indentation rules — body 2 levels deeper than its declaration:

```tmdl
measure 'Sales vs Target (%)' = DIVIDE([Sales] - [Target], [Target])
    displayFolder: 3. Variance
    lineageTag: abc-123

    formatStringDefinition =
            SWITCH(
                TRUE(),
                [Sales vs Target (%)] < -0.1,  "▼ 0.0%",
                [Sales vs Target (%)] > 0.1,   "▲ 0.0%",
                                                "  0.0%"
            )
```

## Rule

When `formatStringDefinition` is set, `formatString` is **ignored**. Don't keep both — pick one.

## When to use this vs static `formatString`

- **Static `formatString`** — same format always. Faster, simpler.
- **Dynamic `formatStringDefinition`** — format depends on the data value or filter context. Powerful, slightly more expensive.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
