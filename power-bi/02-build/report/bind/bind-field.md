# Bind a field to a visual role

Use after the visual exists. Add one field per role; repeat the command for multiple roles.

## List the roles for a visual type

```bash
pbir visuals bind "<...>/Revenue.Visual" --list-roles
```

## Bind one field

```bash
pbir visuals bind "<...>/Revenue.Visual" -a "Values:Sales.Revenue" -t Measure
```

## Bind multiple in one call

```bash
pbir visuals bind "<...>/Trend.Visual" \
  -a "Category:Date.Calendar Month (ie Jan)" -t Column \
  -a "Y:Sales.Revenue"                        -t Measure
```

## Always pass `-t`

`-t Column` or `-t Measure`. Without it the CLI guesses from the model when available, but explicit is safer. Wrong type → Power BI Desktop error "something is wrong with one or more fields" at runtime. See `column-vs-measure.md`.

## Verify

```bash
pbir visuals bind "<...>/Revenue.Visual" --show
```

## After

`../validate/validate.md`.
