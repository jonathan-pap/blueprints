# SVG elements reference for DAX

Quick reference for the SVG elements you'll assemble in DAX measures. All examples use
**single quotes** for attributes — that's the convention in `examples/*.dax`, so there's no
double-quote doubling to escape (see `data-uri-format.md` for the escaping rules and the
data-URI prefix).

## Rectangle

```dax
"<rect x='10' y='5' width='50' height='10' fill='#2196F3' rx='2'/>"
```

| Attribute | Description |
|-----------|-------------|
| x, y | Position (top-left) |
| width, height | Dimensions |
| fill | Fill color |
| stroke | Border color |
| stroke-width | Border thickness |
| opacity | 0–1 transparency |
| rx, ry | Corner radius |

## Circle

```dax
"<circle cx='50' cy='10' r='5' fill='#F44336'/>"
```

| Attribute | Description |
|-----------|-------------|
| cx, cy | Center position |
| r | Radius |
| fill, stroke, opacity | Styling |

## Line

```dax
"<line x1='0' y1='10' x2='100' y2='10' stroke='#333333' stroke-width='2'/>"
```

| Attribute | Description |
|-----------|-------------|
| x1, y1 | Start point |
| x2, y2 | End point |
| stroke | Color |
| stroke-width | Thickness |
| stroke-dasharray | Dash pattern (e.g. `'4,2'`) |

## Polyline (sparklines)

```dax
"<polyline fill='none' stroke='#01B8AA' stroke-width='3' points='0,50 10,30 20,40 30,10'/>"
```

| Attribute | Description |
|-----------|-------------|
| points | Space-separated `x,y` pairs |
| fill | `none` for line only, color for area fill |
| stroke | Line color |
| stroke-width | Line thickness |

Build `points` with CONCATENATEX:

```dax
VAR _Points = CONCATENATEX ( <Table>, [X] & "," & [Y], " ", [SortColumn] )
```

## Text

```dax
"<text x='50' y='10' font-size='12' fill='#333333' font-weight='bold' text-anchor='middle' dominant-baseline='middle'>Label</text>"
```

| Attribute | Description |
|-----------|-------------|
| x, y | Position |
| font-size | Size in px |
| fill | Text color |
| font-weight | `normal`, `bold`, `700` |
| font-family | `Segoe UI` recommended |
| text-anchor | `start`, `middle`, `end` |
| dominant-baseline | `auto`, `middle`, `hanging` |

## Path (arcs, curves)

```dax
"<path d='M 10,10 L 50,10 L 30,30 Z' fill='#4CAF50'/>"
```

| Command | Meaning | Example |
|---------|---------|---------|
| M x,y | Move to | `M 10,10` |
| L x,y | Line to | `L 50,10` |
| A rx ry rot large-arc sweep x y | Arc | `A 40 40 0 0 1 90 50` |
| C x1 y1 x2 y2 x y | Cubic bézier | |
| Q x1 y1 x y | Quadratic bézier | |
| Z | Close path | |

Arc for a gauge / donut:

```dax
"<path d='M 10 50 A 40 40 0 0 1 90 50' fill='none' stroke='#2196F3' stroke-width='8'/>"
```

## Group

```dax
"<g transform='translate(10,10)'>" & _Shape1 & _Shape2 & "</g>"
```

| Transform | Example |
|-----------|---------|
| translate(x, y) | Move group |
| rotate(angle) | Rotate around origin |
| scale(x, y) | Scale group |

## Gradient definition

```dax
"<defs><linearGradient id='grad' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0000FF'/><stop offset='1' stop-color='#00000000'/></linearGradient></defs>"
```

Reference it in a fill: `fill='url(#grad)'`.

| Attribute | Description |
|-----------|-------------|
| id | Reference name |
| x1, y1, x2, y2 | Gradient direction (0–1 normalized) |
| stop offset | Position along gradient (0–1) |
| stop-color | Color at this stop |

## SVG container

```dax
"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
```

| Attribute | Description |
|-----------|-------------|
| xmlns | Required: `http://www.w3.org/2000/svg` |
| viewBox | Coordinate system: `minX minY width height` |
| width, height | Fixed dimensions (optional with viewBox) |
| preserveAspectRatio | `none` to stretch, `xMidYMid meet` to keep ratio |

## Common patterns

- **Responsive sizing** — use `viewBox` instead of fixed `width`/`height`.
- **Hex colors** — write `#` directly (`fill='#01B8AA'`). **Do not** URL-encode as `%23`: it
  throws `VisualDataProxyExecutionUnknownError` in image visuals and is unreliable elsewhere.
  Avoid named colors (`blue`, `red`) — always hex.
- **Coordinate inversion** — SVG Y=0 is the *top*; invert for charts: `VAR _Y = 100 - [Normalized]`.
- **Render order** — document order = back-to-front. Draw backgrounds first, labels last.

## See also

- `data-uri-format.md` — the `data:image/svg+xml;utf8,` prefix + quote escaping.
- `theme-color-references.md` — pull colors from the theme instead of hardcoding.
- `per-chart/` — these elements assembled into complete chart measures.
