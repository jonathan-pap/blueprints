# Swap a bound field

Replace one field with another in the same role. Used for "use Margin instead of Revenue" or rebinding after a model change.

## Procedure

```bash
# 1. Clear the existing field
pbir visuals bind "<...>/Visual.Visual" --clear-role "Values"

# 2. Bind the new field
pbir visuals bind "<...>/Visual.Visual" -a "Values:Sales.Margin" -t Measure
```

## Mass swap across many visuals

```bash
# Find every visual using the old field
pbir fields find "<project>.Report" -f "Sales.Revenue"

# Repeat the clear+bind per visual returned
```

For a project-wide rename (where the old field stops existing entirely), use `../pbip-format/rename-measure.md` instead.

## After

`../validate/validate.md`.
