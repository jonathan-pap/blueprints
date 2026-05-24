# SVG — target bar (linear gauge)

A horizontal track split into red / amber / green zones with a needle marking where a 0–1
ratio lands. The KPI-card cousin of the [progress bar](progress-bar.md): progress bar shows
"how full", the target bar shows "which zone". Wider than a row micro-chart — best in a
**card** or **image** visual, or a wide table cell.

## DAX (see `examples/target-bar-svg.dax`)

```dax
Target Bar SVG =
VAR _ratio  = [Cache Hit Ratio %]                 -- any 0..1 measure
VAR _pct    = MIN ( MAX ( _ratio, 0 ), 1 ) * 100  -- clamp
VAR _x0     = 10
VAR _trackW = 290
VAR _needleX = _x0 + _trackW * _pct / 100
RETURN
"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 60'>" &
"<rect x='10'  y='28' width='87'  height='10' fill='#f4d4d0'/>" &   -- red  0-30
"<rect x='97'  y='28' width='116' height='10' fill='#f5e1c8'/>" &   -- amber 30-70
"<rect x='213' y='28' width='87'  height='10' fill='#d6e7d3'/>" &   -- green 70-100
"<polygon points='" & _needleX & ",14 " & (_needleX+5) & ",19 " & _needleX & ",24 " & (_needleX-5) & ",19' fill='#c97a3a'/>" &
"</svg>"
```

(The full measure adds a baseline, 0/30/70/100 tick labels, and the needle stem.)

## Wire it

- **Card / image visual** → `../wiring/in-image.md` (`viewBox 0 0 320 60`; remember
  `sourceType='imageData'`).
- **Wide table cell** → `../wiring/in-table-matrix.md` with `imageWidth: 150`, `imageHeight: 30`.

## Variants

- **Move the zone cut-points** — change the `0.30` / `0.70` splits (e.g. 0.5 / 0.9 for an
  SLA). Keep the three `<rect>` widths in sync with the cuts.
- **Color the needle by zone** — branch its fill on `_pct` (red < 30, amber < 70, else green)
  instead of the fixed amber, for a redundant cue.
- **Add the value label** — a `<text>` at `_needleX` showing `FORMAT(_ratio, "0%")` above the
  needle.
- **Theme the zones** — swap the hardcoded tints for sentiment colors via
  `../theme-color-references.md`.

## Notes

- Colors use `#` directly — **not** `%23` (which breaks image visuals; see `../svg-elements.md`).
- Needs a 0–1 ratio input. For an absolute actual-vs-target instead, see
  [bullet](bullet.md) or [progress-bar](progress-bar.md).

## See also

`../examples/target-bar-svg.dax` — full measure.
