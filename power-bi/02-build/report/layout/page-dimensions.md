# Page dimensions

Always query actual dimensions before placing visuals. Templates and existing reports vary — assuming 1280×720 causes overruns.

## Query

```bash
pbir get "<project>.Report/Overview.Page"
```

Returns `width` and `height` plus other page properties.

## Standard sizes

- `1280 × 720` — desktop default (16:9)
- `1920 × 1080` — Full HD presentations
- `816 × 1056` — letter portrait, print
- `1280 × 960` — legacy 4:3

## Set a new size

```bash
pbir pages set "<project>.Report/Overview.Page" --width 1920 --height 1080
```

## Re-flow visuals

Resizing the page does NOT reposition existing visuals. Run `align-visuals-row.md` or `align-visuals-grid.md` after resizing.

## Bounds rule

When resizing a visual: set `width`/`height` BEFORE `x`/`y`. Otherwise an intermediate state can exceed page bounds and fail validation.
