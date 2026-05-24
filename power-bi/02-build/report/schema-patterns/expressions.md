# Expressions — what goes inside `expr`

> Every formatting value in PBIR is an `expr` wrapping one expression type. Literals carry
> type-suffix and quoting rules that are easy to get wrong (and the `pbir` CLI / Desktop will
> reject or silently ignore the bad ones). Source schema: `semanticQuery/1.4.0` →
> `QueryExpressionContainer`.

## Literals

```json
"expr": { "Literal": { "Value": "..." } }
```

The `Value` field is **always a JSON string**, even for numbers and booleans. The string's
*contents* follow type rules:

| Type | Pattern | Examples |
|---|---|---|
| String | single quotes inside double quotes: `"'x'"` | `"'smooth'"`, `"'straight'"` |
| Number | numeric + type suffix, no quotes | `"50D"`, `"8D"`, `"0L"` |
| Boolean | lowercase, no quotes | `"true"`, `"false"` |
| Color (hex) | inner single quotes | `"'#1971c2'"`, ARGB `"'#80FF0000'"` (first 2 = alpha) |
| DateTime | `datetime'...'` | `"datetime'2024-01-15T00:00:00.0000000'"` |
| Null | lowercase bare | `"null"` |

**Escaping:** double a single quote inside a string — `"'here''s text'"`. Font fallback chains
triple up: `"'''Segoe UI Semibold'', helvetica, sans-serif'"`.

### Numeric suffixes — `D` vs `L` are NOT interchangeable

- `D` = decimal/double (most common), `L` = long integer, `M` = money.
- `transparency` uses `D` normally **but `L` inside `dropShadow`**.
- `labelPrecision` always `L`; `labelDisplayUnits` always `D`.
- `fontSize` always `D`; `shadowBlur`/`shadowSpread`/`shadowDistance` always `L`.

When unsure, copy the suffix from a known-good example of the same property — guessing the wrong
suffix is a common cause of a property being silently dropped.

## Measure reference

```json
"expr": { "Measure": {
  "Expression": { "SourceRef": { "Entity": "Budget" } },
  "Property": "Budget vs. Turnover (%)"
} }
```

**Extension measure** (from `reportExtensions.json`, i.e. thin-report measures) adds
`"Schema": "extension"`:

```json
"expr": { "Measure": {
  "Expression": { "SourceRef": { "Schema": "extension", "Entity": "_Formatting" } },
  "Property": "ColorMeasure"
} }
```

Forgetting `"Schema": "extension"` on a report-local measure is the classic "measure not found"
break. See [../calculations/thin-report-measure.md](../calculations/thin-report-measure.md).

## ThemeDataColor reference

```json
"expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0 } }
```

- `ColorId` — 0-based index into the theme's `dataColors`.
- `Percent` — tint/shade, `-1.0`…`1.0` (negative darker, positive lighter, `0` exact).

Prefer this over hardcoded hex inside visuals; see [../references/visual-colors.md](../references/visual-colors.md).

## Column reference

```json
"expr": { "Column": {
  "Expression": { "SourceRef": { "Entity": "Date" } },
  "Property": "Calendar Month (ie Jan)"
} }
```

## FillRule — gradient (numeric measure → color)

Use when a measure returns a **numeric** value (e.g. 0.75) and you want a smooth gradient,
not a discrete color. Two-stop (`linearGradient2`) and three-stop (`linearGradient3`):

```json
"expr": { "FillRule": {
  "Input": { "Measure": { "Expression": { "SourceRef": { "Schema": "extension", "Entity": "On-Time Delivery" } }, "Property": "Cond. Color" } },
  "FillRule": { "linearGradient2": {
    "min": { "color": { "Literal": { "Value": "'minColor'" } }, "value": { "Literal": { "Value": "0D" } } },
    "max": { "color": { "Literal": { "Value": "'maxColor'" } }, "value": { "Literal": { "Value": "1D" } } },
    "nullColoringStrategy": { "strategy": { "Literal": { "Value": "'asZero'" } }, "color": { "Literal": { "Value": "'#FFFFFF'" } } }
  } }
} }
```

- **Explicit bounds:** include `value` on `min`/`max` to pin the range (e.g. `0D`…`1D`).
- **Data-driven bounds:** omit the `value` entries; Power BI derives min/max from the data.
- `nullColoringStrategy.strategy`: `'asZero'` or `'specificColor'` (+ `color`).
- `linearGradient3` adds a `mid` stop (e.g. red `-1D` → white `0D` → grey `1D`).
- Color stops accept theme semantic names (`'minColor'`, `'midColor'`, `'maxColor'`, `'good'`,
  `'neutral'`, `'bad'`) or hex.

## Conditional — discrete color bands

Use when you want explicit thresholds, not a gradient. Cases evaluate **in order; first match wins.**

```json
"expr": { "Conditional": { "Cases": [
  { "Condition": { "Comparison": { "ComparisonKind": 0,
      "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "Sales" } }, "Property": "Δ vs PY (%)" } },
      "Right": { "Literal": { "Value": "null" } } } },
    "Value": { "Literal": { "Value": "'#b3b3b3'" } } },
  { "Condition": { "Comparison": { "ComparisonKind": 4,
      "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "Sales" } }, "Property": "Δ vs PY (%)" } },
      "Right": { "Literal": { "Value": "-0.5D" } } } },
    "Value": { "Literal": { "Value": "'#ad5129'" } } }
] } }
```

### ComparisonKind values

| Value | Operator |
|---|---|
| 0 | `==` |
| 1 | `>` |
| 2 | `>=` |
| 3 | `<=` |
| 4 | `<` |

### Compound conditions

Wrap two `Comparison`s in `And` (or `Or`):

```json
"Condition": { "And": {
  "Left":  { "Comparison": { "ComparisonKind": 2, "Left": {...}, "Right": { "Literal": { "Value": "-0.25D" } } } },
  "Right": { "Comparison": { "ComparisonKind": 3, "Left": {...}, "Right": { "Literal": { "Value": "0.25D" } } } }
} }
```

→ `(x >= -0.25) AND (x <= 0.25)`.

**Conditional vs FillRule:** Conditional for discrete bands with explicit thresholds; FillRule
for a smooth gradient across a numeric range.

## Nested color shape

Color properties nest the `expr` two levels down:

```json
"strokeColor": { "solid": { "color": { "expr": { "Measure": { ... } } } } }
```

## SourceRef context

`SourceRef` uses a **different field** depending on where it sits:

| Context | Field | Example |
|---|---|---|
| Query projections (`queryState`) | `Entity` | `{ "SourceRef": { "Entity": "Sales" } }` |
| Filter `Where` conditions (filter pane, bookmark filters) | `Source` (alias from `From[]`) | `{ "SourceRef": { "Source": "s" } }` |
| `scopeId` selectors (formatting objects) | `Entity` | `{ "SourceRef": { "Entity": "Products" } }` |

Where `Source` is used, a `From[]` must declare the alias: `"From": [{ "Name": "s", "Entity": "Sales", "Type": 0 }]`.
Using `Entity` inside a filter `Where` produces broken filter JSON. See [../filters/_index.md](../filters/_index.md).

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `"smooth"` ignored | missing inner quotes | `"'smooth'"` |
| number dropped | missing suffix | `"50D"` (or `L`/`M` per property) |
| boolean dropped | bare JSON `true` | `"Value": "true"` (quoted string) |
| boolean dropped | wrong case `"True"` | `"true"` lowercase |
| "measure not found" | missing `Schema` | add `"Schema": "extension"` for report measures |

## Related

- [selectors.md](selectors.md) — where/what an `expr` applies to
- [property-catalogue.md](property-catalogue.md) — which container/property to put the `expr` on
- [../format/conditional-fmt-rule.md](../format/conditional-fmt-rule.md) — full conditional-format recipe
