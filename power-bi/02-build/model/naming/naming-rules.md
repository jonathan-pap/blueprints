# Naming rules (11 categories)

Default rules. Override per business context (`core-principle.md`).

## 1. Human-readable names (no programming conventions)

Standard casing with spaces. No CamelCase, snake_case, UPPER_CASE.

- `OrderStatus` → `Order Status`
- `past_due_orders` → `Past Due Orders`
- `TOTAL_COST` → `Total Cost`

## 2. No abbreviations or acronyms

Spell out full words. Exceptions: universally understood time abbreviations (MTD, YTD, QTD) or business acronyms defined in descriptions.

- `Del. Mrgn %` → `Delivery Margin (%)`
- `NetSls` → `Net Sales`
- `shp_dt` → `Ship Date`
- `CustKey` → `Customer Key`

## 3. No technical prefixes

No `DIM_`, `FACT_`, `STG_`, `RAW_` on table names. Use Tabular Editor Table Groups annotation for categorization.

- `DIM_Customer` → `Customer`
- `FACT_Invoices` → `Invoices`

**Exception:** `_Measures`, `_Formatting`, `FP_` (field parameters), `CG_` (calculation groups) — technical tables that shouldn't appear to end users / AI schemas.

## 4. No excessive symbols / special characters

No emojis, no `$$$`, no Unicode decorations. `#` only when meaningful (`# Customers`).

## 5. Consistent aggregation syntax

Pick one convention, apply uniformly. Recommended: `MTD`, `QTD`, `YTD` as suffixes.

- `mtd_turnover_ly` → `MTD Turnover 1YP`
- `MonthToDateSales` → `Sales MTD`

## 6. Consistent unit syntax

Recommended: `Measure Name (Unit)` with `(%)`, `(EUR)`, `(Quantity)`, `(Value)`, `(Units)`.

- `SellMrgn%` → `Selling Margin (%)`
- `TrnOvr_Qty` → `Turnover (Quantity)`

## 7. Consistent period syntax

Recommended: `nYP` (n-Year Prior).

- `Turnover_Last_Year` → `Turnover 1YP`
- `S.M. % LY` → `Standard Margin 1YP (%)`

## 8. Consistent comparison syntax

Recommended: `Base Measure vs. Target (Unit)`.

- `Turnover vs 1YP (%)` — variance %
- `Budget MTD vs. Turnover (delta)` — variance absolute

Pick one of `vs`/`vs.` (with/without period) and one of `(delta)`/`(Δ)` and apply uniformly.

## 9. Display folder organization

Numbered prefixes for sort order, logical hierarchy.

**Fact tables:**

```
0. Measures\
    1. Value\
        i. Total
        ii. 1YP
        iii. 2YP
    2. Quantity
    3. Lines
1. Facts
2. Degenerate Dimensions
3. Keys\
    Dates
```

**Dimension tables:**

```
1. [Primary Hierarchy Name]
2. [Attributes]
3. Managers
4. Keys
```

## 10. Descriptions

All visible measures and columns need `///` descriptions (TMDL native syntax — see `../update/property.md`). Explain:

- What the measure calculates
- Business context for interpretation
- Filter context requirements (for field parameters)
- Definition of any acronyms in the name

## 11. Synonyms (for AI)

When configuring "Prep your data for AI" or setting synonyms:

- Only list real synonyms people in the org use
- Consider multilingual synonyms for international orgs
- Synonyms primarily benefit AI / agent queries (Copilot, data agents)

## Detection patterns (regex)

For TMDL grep:

- `measure [a-z]+_[a-z]+` — snake_case measures
- `measure [A-Z][a-z]+[A-Z]` — CamelCase measures
- `measure [A-Z_]{4,}` — UPPER_CASE measures
- `table (DIM|FACT|dim|fact|STG|stg|RAW|raw)_` — technical prefixes
- `\w+\.\s` — abbreviation dots
- Names < 5 chars not common words
