# TMDL nesting rules

Validator-enforced. Wrong parent = parse error.

## Root-level (indent 0)

`model`, `database`, `table`, `relationship`, `role`, `cultureInfo`, `perspective`, `dataSource`, `expression`, `queryGroup`, `function`.

## Child of `table`

`column`, `measure`, `hierarchy`, `partition`, `calculationGroup`.

## Child of others

- `level` → inside `hierarchy`
- `calculationItem` → inside `calculationGroup`
- `tablePermission` → inside `role`
- `columnPermission` → inside `tablePermission`
- `perspectiveTable` → inside `perspective`
- `perspectiveColumn`, `perspectiveMeasure`, `perspectiveHierarchy` → inside `perspectiveTable`
- `linguisticMetadata`, `translation` → inside `cultureInfo`
- `dataAccessOptions` → inside `model`
- `formatStringDefinition` → inside `measure` or `calculationItem`
- `detailRowsDefinition` → inside `measure` or `table`
- `alternateOf` → inside `column`
- `member` → inside `role`
- `ref` → inside `model` or `table`

## Universal

`annotation` and `extendedProperty` can attach to almost any object (`model`, `table`, `column`, `measure`, `hierarchy`, `level`, `partition`, `role`, `perspective`, `culture`, `relationship`, `expression`, `dataSource`, `queryGroup`, `function`).
