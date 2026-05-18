# Set page size

```bash
pbir pages set "<project>.Report/Overview.Page" --width 1920 --height 1080
```

## Standard sizes

- `1280 × 720` — Desktop default (16:9)
- `1920 × 1080` — high-res displays, presentations
- `816 × 1056` — letter portrait, print
- `1280 × 960` — legacy 4:3

## Re-flow visuals

Resizing the page does NOT move existing visuals. They stay at their old coordinates and may now overlap or fall off the canvas. Re-run `../layout/align-visuals-row.md` or `align-visuals-grid.md` after resizing.

## After

`../validate/validate.md`.
