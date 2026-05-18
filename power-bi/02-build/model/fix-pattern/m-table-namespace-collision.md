# Fix: "duplicate member" — M expression and table share a name

## Symptom

Power BI Desktop fails to load the model with `'duplicate member <name>'`.

## Cause

Named M expressions in `expressions.tmdl` and tables in `tables/*.tmdl` share a namespace. `expression Sales` and `table Sales` collide.

## Fix

Suffix the M expression name with ` Query` (or ` Source`), and update partition references:

```tmdl
# In expressions.tmdl
expression 'Sales Query' = ```                          ← was 'Sales', now 'Sales Query'
        let
            Source = Sql.Database("srv", "db"),
            Sales  = Source{[Schema="dbo", Item="Sales"]}[Data]
        in
            Sales
        ```
```

```tmdl
# In tables/Sales.tmdl
table 'Sales'
    ...
    partition 'Sales-Partition' = m
        mode: import
        source = #"Sales Query"                          ← reference via #"..." syntax
```

## Find all candidates

```bash
# Names declared in expressions.tmdl
grep -E "^expression " "<project>.SemanticModel/definition/expressions.tmdl"

# Names declared as tables
ls "<project>.SemanticModel/definition/tables/"

# Spot collisions
```

## Validator

`validate_pbip.py` enforces this as an ERROR. Run it before opening in Desktop:

```bash
python ../../../04-review/scripts/validate_pbip.py "<project>"
```
