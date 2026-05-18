# Add an image

Use for logos, illustrations, page headers. No data bindings.

## Create

```bash
pbir add image "<project>.Report/Overview.Page" path/to/logo.png \
  --x 1180 --y 16 --width 76 --height 56
```

The CLI copies the image into `<project>.Report/StaticResources/RegisteredResources/` and wires the visual JSON.

## Supported formats

PNG, JPG, SVG, GIF. Prefer SVG for logos (scales cleanly).

## Alt text

Always set alt text for accessibility — see `../format/override-property.md` and search for `altText`.

## Templates

- `../examples/visuals/default/image.json` — static image
- `../examples/visuals/formatted/image-svg-measure.json` — image fed by a DAX SVG measure (see `../../visuals/svg/wiring/in-card.md`)

## After

`../validate/validate.md`.
