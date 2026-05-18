# Clear a field binding

Remove a field from a visual role without deleting the visual.

## Clear one role

```bash
pbir visuals bind "<...>/Visual.Visual" --clear-role "Legend"
```

## Clear all bindings

```bash
pbir visuals bind "<...>/Visual.Visual" --clear-all
```

The visual stays on the page but renders empty until rebound.

## After

`../validate/validate.md`.
