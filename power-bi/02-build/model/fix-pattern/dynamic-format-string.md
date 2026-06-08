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

## Pitfall — `formatStringDefinition` must be a block, not inline

`formatStringDefinition` is an **expression-valued** property, not a `:` property. Writing it inline:

```tmdl
    measure 'Variance' = [Actual] - [Target]
        formatStringDefinition = SWITCH(TRUE(), [Variance]<0, "(#,##0)", "#,##0")   ← BROKEN
```

makes Desktop throw *"Invalid indentation"* on the NEXT property line (or the next measure). `pbir model -d` accepts the inline form silently. The correct shape: `formatStringDefinition =` on its own line, a blank line, then the expression body indented **one level deeper than the measure's other properties** (properties at depth 2 → expression body at depth 4):

```tmdl
    measure 'Variance' = [Actual] - [Target]
        displayFolder: 3. Variance
        lineageTag: abc-123

        formatStringDefinition =
                SWITCH(
                    TRUE(),
                    [Variance] < 0, "(#,##0)",
                    "#,##0"
                )
```

The expression body itself can be a single long line — only its leading indent matters. A measure with `formatStringDefinition` carries **no** static `formatString:` line.

## Pitfall — requires `compatibilityLevel: 1601`

The default new PBIP `database.tmdl` is `compatibilityLevel: 1600`. Any `formatStringDefinition` (or any `function` block) requires **1601**:

```tmdl
database
    compatibilityLevel: 1601    ← was 1600
```

Symptom if missed: *"The database compatibility level of 1600 is below the minimal compatibility level of 1601 needed for the … FormatStringDefinition feature."* Bump it once for the whole model.

## When to use this vs static `formatString`

- **Static `formatString`** — same format always. Faster, simpler.
- **Dynamic `formatStringDefinition`** — format depends on the data value or filter context. Powerful, slightly more expensive.

A small-count measure with a plain `formatString: #,0` already renders identically under a "less than 1M → #,0" rule — leave it static (less parser surface) unless the value genuinely crosses a unit-format threshold.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
