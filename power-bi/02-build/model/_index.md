# 02-build/model — atomic file index

## add/

- `measure.md`
- `column.md` (DataColumn — most common)
- `calculated-column.md`
- `table-m.md` (sourced from Power Query M)
- `table-calculated.md` (sourced from DAX)
- `relationship.md`
- `hierarchy.md`
- `role.md` (RLS / OLS)
- `perspective.md`
- `culture.md` (translations)
- `calculation-group.md`

## update/

- `property.md` — change a property (formatString, summarizeBy, displayFolder, description)
- `measure-expression.md` — change a measure's DAX body
- `dax-multiline.md` — indented-block vs triple-backtick syntax

## fix-pattern/

- `_index.md`
- `summarize-by-key.md` — flip key columns from sum → none
- `missing-description.md` — add `///` description
- `format-string-by-type.md` — pick the right format pattern
- `dynamic-format-string.md` — replace `formatString` with `formatStringDefinition`
- `m-table-namespace-collision.md` — suffix M expressions with ` Query`
- `pbi-format-hint-readded.md` — accept the auto-annotation

## object-types/

- `_index.md` — picker
- `column-properties.md` — every column property + enum values
- `measure-properties.md`
- `table-properties.md`
- `relationship-properties.md`
- `partition-properties.md`
- `role-properties.md`
- `model-properties.md`

## File-type primer (top-level reference)

- `file-types.md` — what's in `model.tmdl`, `database.tmdl`, `relationships.tmdl`, etc.
- `nesting-rules.md` — which object can live inside which parent
