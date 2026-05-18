# MDL006 — Row-based time intelligence table

> Tier 3 — user approval required.

DAX TI functions break vertical fusion — each period measure gets its own SE query (see `../engine/fusion.md`).

A row-based TI table pre-materializes all periods as data rows so all period measures fuse into a **single SE scan**.

## Structure

A new `Period` table:

- `Period` — slicer label ("YTD", "PY YTD", "MTD", "Last 30 Days")
- `Date` — actual dates → relationship to fact
- `AxisDate` — x-axis anchor (typically the last day of the period for charts)

## Relationship

Either:

- M2M to Fact (preferred when Fact is large)
- BiDir through Calendar (simpler but adds bidir overhead — see `mdl001-many-to-many.md`)

## How it works

A slicer on `Period[Period]` filters down to the relevant date rows. All measures that operate on Fact respect that filter via the relationship — no TI function needed in the measure.

```dax
MEASURE 'Sales'[Revenue Selected Period] = SUM('Fact'[Revenue])
-- Slicer = "YTD" → 'Period' filtered to YTD rows → 'Fact' filtered to YTD dates → measure aggregates only YTD revenue
```

Multiple period measures on the same fact under the same slicer all fuse into one SE scan.

## Trade-off

- **One table to maintain** with the date ranges for each period — easy to keep current with a CALCULATETABLE.
- **Loss of independent control** — every measure sees the same period filter; you can't easily mix "Revenue YTD" with "Revenue PY" in the same visual without DAX gymnastics.
- **Best for dashboards** where the user picks one period at a time and all visuals respect it.

## When NOT to use

- Reports that need side-by-side period comparisons (CY vs PY in the same chart) — `DATEADD` and `SAMEPERIODLASTYEAR` in measures is cleaner
- Few period measures total — TI in DAX is fine

## See also

- `../patterns/dax019-vertical-fusion-ti.md` — DAX-only fix; lift TI to outer CALCULATE
