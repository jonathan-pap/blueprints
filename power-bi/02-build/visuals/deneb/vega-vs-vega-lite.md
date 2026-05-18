# Vega-Lite vs Vega

Pick before writing the spec.

| | Vega-Lite | Vega |
| --- | --- | --- |
| Verbosity | Concise | Verbose |
| Learning curve | Lower | Higher |
| Capability | Standard charts (bar, line, scatter, faceted, layered) | Anything (custom marks, signals, complex interactivity) |
| Default | Yes | When Lite cannot express it |

## Default to Vega-Lite

Vega-Lite handles 80% of Deneb use cases with one-third the JSON. Start there.

## Switch to Vega when

- You need custom mark geometries (waterfall steps, swoosh paths).
- You need fine-grained scale/signal control across multiple layered marks.
- You need event handlers Vega-Lite doesn't expose.

## Both share

- `data.values` (or `data.name` referencing the bound `dataset`)
- Power BI selection signal `pbiSelection`
- Theme color helper `pbiColor(N)`
