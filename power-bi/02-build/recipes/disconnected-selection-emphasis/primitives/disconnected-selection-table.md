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
- Keep the column name identical to the source so tokens read cleanly.
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
