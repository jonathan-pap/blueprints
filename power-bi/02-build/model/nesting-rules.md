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

## Comments — only `///` docstrings work

TMDL supports exactly one comment syntax: a `///` triple-slash docstring on the line immediately preceding an object. There is no `//` line comment and no `/* */` block comment. Writing a `// section header` or `// block comment` line at the property-indent level makes Desktop's TMDL parser treat it as a malformed property and surface "Invalid indentation" on the next valid line — pointing at the wrong place.

Right (docstring attaches to the next measure):

```tmdl
    /// Sum of FactTrade[TotalPrice] in the current filter context.
    measure 'Total Trade Value' = SUM(FactTrade[TotalPrice])
        formatString: $#,##0
        lineageTag: 64b3333c-c7a3-4c02-8af7-d3d274581236
```

Wrong (Desktop throws "Invalid indentation" on the measure line below):

```tmdl
    // ───── Headline measures ─────
    measure 'Total Trade Value' = SUM(FactTrade[TotalPrice])
```

If you need to group/explain a region:

1. Put the explanation inside the next object's `///` docstring.
2. Use `displayFolder` to visually group measures in the field list.
3. Keep the explanation in a separate `.md` doc in the room.

`pbir validate` and `pbir model -d` DO accept `//` comments (different parser path), so a file can pass CLI checks and still fail to open in Desktop. CLI parsing is not proof of Desktop validity.
