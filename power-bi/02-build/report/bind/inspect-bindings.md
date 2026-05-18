# Inspect bindings

Audit which fields are bound where.

## Show all visuals + their fields

```bash
pbir tree "<project>.Report" -v
```

## Show bindings for one visual

```bash
pbir visuals bind "<...>/Visual.Visual" --show
```

## All fields used across the report

```bash
pbir fields list "<project>.Report"
```

## Where is a specific field used?

```bash
pbir fields find "<project>.Report" -f "Sales.Revenue"
```

Use this before a rename or refactor — it's the equivalent of `grep` but field-aware.
