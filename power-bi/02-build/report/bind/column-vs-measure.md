# Column vs Measure (field kind)

Every binding has a kind. Wrong kind passes JSON schema validation but fails at runtime in Power BI Desktop. This is the #1 binding bug.

## Rule

- Pass `-t Column` for columns (dimensions, attributes, dates).
- Pass `-t Measure` for measures (aggregations, calculations).

## Check the kind before binding

```bash
pbir model "<project>.Report" -d -t Sales | grep -A1 "Revenue"
```

Or read TMDL directly:

```bash
grep -E "^\s*(measure|column) " "<project>.SemanticModel/definition/tables/Sales.tmdl"
```

## Fix a wrong-kind binding

Clear the role, then re-add with the right kind:

```bash
pbir visuals bind "<...>/Visual.Visual" --clear-role "Values"
pbir visuals bind "<...>/Visual.Visual" -a "Values:Sales.Revenue" -t Measure
```

## In visual.json (manual edits)

The kind shows up as the JSON key inside `queryState` projections:

- Column: `{"Column": {"Expression": {...}, "Property": "Field"}}`
- Measure: `{"Measure": {"Expression": {...}, "Property": "Field"}}`

Swap the outer key to fix the kind without re-running the CLI.
