# Conditional formatting — rule-based

Discrete colors based on thresholds. Use for status indicators ("over budget", "delayed", "on track").

## Apply

```bash
pbir visuals conditional-format "<...>/Visual.Visual" \
  --target "Sales.Variance" \
  --type rule \
  --rule "x < 0:#D4602E" \
  --rule "x >= 0 and x < 0.1:#FFA500" \
  --rule "x >= 0.1:#2B7A78"
```

## Driven by an extension measure (preferred)

Define a DAX measure that returns a theme sentiment color:

```dax
Variance Status =
SWITCH(
    TRUE(),
    [Variance] < 0,    "bad",
    [Variance] < 0.1,  "neutral",
                       "good"
)
```

Then bind that measure as the color source in the visual JSON. Re-theming the report changes all status colors at once.

## After

`../validate/validate.md`.
