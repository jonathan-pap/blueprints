# object-types/ — property reference per type

> Use to look up valid values for any property. Load only the file matching the type you're editing.

- `column-properties.md` — DataColumn + CalculatedColumn
- `measure-properties.md`
- `table-properties.md`
- `relationship-properties.md`
- `partition-properties.md`
- `role-properties.md`
- `model-properties.md`

## Universal properties

These apply to almost every object:

- `lineageTag: <guid>` — never change for existing objects
- `description: '...'` (or `///` line above) — free-text
- `annotation Key = Value` — custom metadata
- `extendedProperty Key = { ... }` — structured (JSON) metadata
- `isHidden` — bare flag

## Boolean flag syntax

Boolean properties (`isHidden`, `isKey`, `isActive`, `isNullable`, `isUnique`, `isAvailableInMdx`, `isDataTypeInferred`, `isDefaultLabel`, `isDefaultImage`, `keepUniqueRows`) are written as **bare keywords on their own line**, no value:

```tmdl
column 'X'
    dataType: int64
    isHidden                       ← correct
    isHidden: true                 ← WRONG, parse error
    lineageTag: <guid>
```
