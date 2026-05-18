# Set a page wallpaper / background

Use sparingly. A custom background can carry the page title, logo, and section dividers — but adds maintenance cost.

## CLI

```bash
pbir pages set "<project>.Report/Overview.Page" --wallpaper path/to/bg.png
```

The image is copied into `<project>.Report/StaticResources/RegisteredResources/` and the page JSON updated.

## Sizing

Match the page dimensions exactly. 1280 × 720 page → 1280 × 720 wallpaper. Mismatches cause stretching or tiling.

## Alternative: a textbox + colored rectangle

Often cleaner than an image — easier to maintain and updates with theme color changes. Use only if the user wants a graphical background.

## Generate a custom background

Two helper scripts ship in `../scripts/`:

- `generate-background-with-gemini.py` — Gemini-generated background image from a text prompt.
- `set-background-image.py` — apply an existing image as a page wallpaper, sized correctly.

Useful for branded page headers or section dividers without designing each one by hand.

## After

`../validate/validate.md`.
