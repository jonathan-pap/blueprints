# Override a single visual property

One-off override on one visual. Don't use for changes that apply to all visuals of a type — that's a theme change.

## CLI shortcuts (common cases)

```bash
pbir visuals title  "<...>/Visual.Visual" --fontSize 14 --bold --show
pbir visuals border "<...>/Visual.Visual" --show --radius 8
pbir visuals subtitle "<...>/Visual.Visual" --no-show
```

## Lookup a property name

```bash
pbir visuals format "<...>/Visual.Visual"          # show current formatting
pbir property-catalogue --visual-type lineChart    # see all properties available
```

## Direct JSON edit (when no CLI shortcut)

Edit `<project>.Report/definition/pages/<page>/visuals/<visual>/visual.json` and set the property under `visualContainerObjects` or `objects`. Then:

```bash
jq empty <visual>.json   # confirm valid JSON
pbir validate "<project>.Report"
```

## Pattern catalogue

For the JSON shape of each property, see `../../theme/` references (they document the same property schema for both visual-level and theme-level use).

## After

`../validate/validate.md`.
