# Rebind a visual to a different field

Swap an existing visual's binding to a different model field (e.g., the model was rebuilt and `Sales.Revenue` is now `Sales.Net Revenue`).

## Single visual

```bash
pbir visuals bind "<...>/Visual.Visual" --clear-role "Y"
pbir visuals bind "<...>/Visual.Visual" -a "Y:Sales.Net Revenue" -t Measure
```

Same as `../bind/swap-field.md` — listed here too because rebinding is a common semantic-model-side operation.

## All visuals using the old field

```bash
pbir fields find "<project>.Report" -f "Sales.Revenue"   # list affected
```

Then iterate the clear+bind per visual.

## Full project-wide rename (the model has dropped the old name entirely)

Use `../pbip-format/rename-measure.md` — it handles every place the old name appears (TMDL, visual JSON, report extensions, DAX queries, cultures).

## After

`../validate/validate.md`.
