# Change palette colors

Set the theme's `dataColors` array. These flow into every chart's `themedataColor` slots.

## Quick CLI

```bash
pbir theme set-colors "<project>.Report" \
  --color "#118DFF" --color "#12239E" --color "#E66C37" --color "#6B007B" \
  --color "#E044A7" --color "#744EC2" --color "#D9B300" --color "#D64550"
```

Order matters — index 0 is the primary, used for the first series in any chart.

## From hex list

```bash
pbir theme set-colors "<project>.Report" \
  --from-json colors.json
```

`colors.json`:

```json
["#118DFF", "#12239E", "#E66C37", "#6B007B"]
```

## Direct serialize edit

Run `serialize/split.md` first, then edit `theme/dataColors.json`. Build with `serialize/build.md`.

## In visuals — reference theme color, not hex

In visual JSON or thin-report measures, use `ThemeDataColor` not hardcoded hex so re-coloring propagates:

```json
"expr": {"ThemeDataColor": {"ColorId": 1, "Percent": 0}}
```

`ColorId` is 1-based. `Percent` is shade adjustment (-100 to 100).

## Accessibility

Pair color with a secondary cue (arrow, icon, shape). Never rely on color alone. For sentiment, set semantic colors via `sentiment-colors.md` rather than encoding meaning in `dataColors`.

## After

`../../report/validate/validate.md`. Reopen Desktop.
