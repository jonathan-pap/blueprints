# P1 — Variance measures

The measure layer the whole visual reads. Six measures: the variance itself, its percent, the
taller-of-the-two overlay, the two **gated** bounds that become the error-bar connectors, and a
color. Append them to `<MEASURE_TABLE>.tmdl` (template: [variance-measures.tmdl](../templates/variance-measures.tmdl)).

## The measures

```dax
Delta = [<ACTUAL_MEASURE>] - [<TARGET_MEASURE>]

% Delta = DIVIDE ( [Delta], [<TARGET_MEASURE>] )   -- format "▲0%;▼0%;0%"

MAX VALUE = IF ( [<ACTUAL_MEASURE>] > [<TARGET_MEASURE>], [<ACTUAL_MEASURE>], [<TARGET_MEASURE>] )

GREEN MAX = IF ( [Delta] > 0, [MAX VALUE] )   -- non-blank only when actual beat target
RED MAX   = IF ( [Delta] < 0, [MAX VALUE] )   -- non-blank only when actual missed

Delta Color =
SWITCH ( TRUE (), [Delta] > 0, "<POS_COLOR>", [Delta] < 0, "<NEG_COLOR>", BLANK () )
```

## What each is for

| Measure | Consumed by | Why |
|---|---|---|
| `Delta` | everything | the signed variance; the recipe's pivot |
| `% Delta` | [P4](directional-variance-label.md) label | the ▲/▼ percentage shown on top |
| `MAX VALUE` | [P2](overlay-series-scaffold.md) transparent series | positions the label above the taller bar; also the connector's far end |
| `GREEN MAX` / `RED MAX` | [P3](error-bar-variance-connector.md) error bounds | gated so exactly one connector fires per period |
| `Delta Color` | [P4](directional-variance-label.md) label color | green/red by sign (measure-driven conditional color) |

## Why `GREEN MAX` / `RED MAX` are blank-gated

The connector (P3) is an error bar whose `upperBound` is one of these. Because each is
**BLANK** unless the variance has its sign, the error bar simply doesn't draw on the wrong
side — no extra "show/hide" logic in the visual. The gating *is* the on/off switch.

- Beat (`Delta>0`): `GREEN MAX = max = actual`, `RED MAX = BLANK` → only the green connector.
- Miss (`Delta<0`): `RED MAX = max = target`, `GREEN MAX = BLANK` → only the red connector.

## Notes

- `% Delta`'s arrow format `"▲0%;▼0%;0%"` is a **dynamic format string** — see
  [P4](directional-variance-label.md) and the compatibility-level gotcha in [workflow](../workflow.md).
- `Delta Color` returns a hex string; bind it to a label/data-point color via conditional
  formatting (`../../report/format/conditional-fmt-rule.md`).
- For dynamic K/M/B value formatting on actual/target, see the optional
  [dynamic-format-udf.tmdl](../templates/dynamic-format-udf.tmdl).

## Next

[P2 — overlay-series scaffold](overlay-series-scaffold.md) puts these on the chart.
