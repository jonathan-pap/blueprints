# Deneb in PBIR

A Deneb visual is a normal visual entry in `<project>.Report/definition/pages/<page>/visuals/<visual>/visual.json`. The Deneb-specific bits live inside the visual's `objects.vegaViewport`.

## Where the spec lives

```json
"objects": {
  "vegaViewport": [{
    "properties": {
      "jsonSpec": {
        "expr": { "Literal": { "Value": "'{\"$schema\":...}'" } }
      }
    }
  }]
}
```

The spec is a stringified JSON value inside a `Literal` expression. Newlines and double-quotes inside the spec get escaped — this is why you author the spec in `examples/spec/*` as separate files and inline at build time.

## Custom visual GUID

The visual's `visualType` is the Deneb GUID: `Deneb_VegaVisual` (string). Check the value in `examples/visual/*.json` for the canonical form.

## Static config

The `standard-config.json` example contains baseline settings: rendering mode, tooltip behavior, theme integration. Drop into the visual's config when scaffolding a new Deneb visual.

## To scaffold

1. Use `pbir add visual` with `--visual-type Deneb_VegaVisual`.
2. Paste the spec from `examples/spec/*` into `objects.vegaViewport.properties.jsonSpec`.
3. Bind data fields normally via `pbir visuals bind` — they appear as `dataset` to the spec.
