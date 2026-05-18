# SVG — overlapping bars with variance

Like `overlapping-bars.md` but adds a colored overlay on the variance region — same idea as `ibcs-bar.md` with slightly different framing.

## DAX

See `../../examples/overlapping-bars-with-variance-measure.dax` for the full measure.

Key differences from plain overlapping bars:

- A third `<rect>` element fills the gap between PY end and Actual end.
- Color of that overlay depends on `[Actual] >= [PY]` (good vs bad).
- Optionally semi-transparent (`opacity="0.5"`) so the underlying bars still show through.

## When to use this vs ibcs-bar

- **This pattern**: Actual bar visually "growing past" PY, with the growth highlighted.
- **`ibcs-bar.md`**: more rigid IBCS conventions (specific colors, specific bar heights). Use IBCS when stakeholders explicitly request IBCS compliance.

## See also

- `overlapping-bars.md` — the simpler base pattern
- `ibcs-bar.md` — IBCS-styled variant
- `../../examples/overlapping-bars-with-variance-measure.dax`
