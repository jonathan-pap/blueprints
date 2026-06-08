# P1 — Disconnected selection table

A calculated table that mirrors a source column but has **no relationships** to any
other table. Its only job is to feed a slicer; because nothing is related, picking a
value filters *nothing* — it just becomes an input other measures read back.

## TMDL

```tmdl
table '<SELECTION_TABLE_NAME>'
	lineageTag: <SELECTION_TABLE_LINEAGE_TAG>

	column <SOURCE_COLUMN>
		formatString: Short Date          // omit/adjust for numeric or text sources
		lineageTag: <SELECTION_COLUMN_LINEAGE_TAG>
		summarizeBy: none
		isNameInferred
		sourceColumn: <SOURCE_TABLE>[<SOURCE_COLUMN>]

		annotation SummarizationSetBy = Automatic

	partition '<SELECTION_TABLE_NAME>' = calculated
		mode: import
		source = ```

				VALUES( <SOURCE_TABLE>[<SOURCE_COLUMN>] )

				```

	annotation PBI_Id = <SELECTION_TABLE_PBI_ID>
```

## Rules

- **No relationships.** This is the whole point — verify in Model view it sits alone. A relationship would turn selection back into filtering and break the recipe.
- `VALUES(...)` gives the distinct domain to pick from. Use `DISTINCT` / `CALENDAR` / a numeric `GENERATESERIES` instead if the source column isn't ideal (see variants).
- **The column name MUST match the partition's output** — `VALUES(SourceTable[SourceCol])` produces a column named `SourceCol` verbatim, and `isNameInferred` locks that in. Declaring `column 'Pretty Name'` while the source emits `SourceCol` errors at Desktop open: *"Column 'Pretty Name' in table 'X' cannot be found or may not be used in this expression"* — at every measure or visual that binds to the declared name. Either match the source name exactly (simplest), or rename the column at the partition with `SELECTCOLUMNS`:

  ```tmdl
  source = SELECTCOLUMNS ( VALUES ( <SOURCE_TABLE>[<SOURCE_COLUMN>] ), "<PRETTY_NAME>", [<SOURCE_COLUMN>] )
  ```

  Plain `VALUES`/`DISTINCT`/`ALL` cannot rename — they pass the source name through. Only `SELECTCOLUMNS`, `ADDCOLUMNS`, `ROW`, or `UNION/ROW(...)` can name a column.
- The triple-backtick `source` block is indentation-sensitive in Desktop — keep the body indented exactly as shown, or collapse to one line `source = VALUES( <SOURCE_TABLE>[<SOURCE_COLUMN>] )`.

## Source by variant

| Variant | source expression |
|---|---|
| Time window | `VALUES( dimDate[Date] )` |
| Numeric band | `GENERATESERIES( 0, 1000000, 1000 )` or `VALUES( fact[Amount] )` |
| Comparison period | `VALUES( dimDate[YearQuarter] )` |
| Category spotlight | `VALUES( dimProduct[Category] )` |

## Next

[P2 — boundary measures](boundary-measures.md) read the selection back.
