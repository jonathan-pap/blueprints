# Clear redundant visual overrides

After promoting an override to the theme (`from-visuals.md`), strip it from every visual that was setting it.

## CLI — clear one property across all visuals of a type

```bash
pbir visuals clear-formatting "<project>.Report" \
  --visual-type lineChart \
  --property "title.fontSize"
```

## Clear all overrides on a single visual

When you want a specific visual to fully inherit from the theme:

```bash
pbir visuals clear-formatting "<...>/Visual.Visual" --all
```

## Confirm

```bash
pbir audit overrides "<project>.Report" --by visual-type
```

The property should no longer appear in the override list.

## Before / after diff

Promotion + clear typically reduces each affected visual.json by 5–20 lines. Easier to review, easier to diff, less merge-conflict surface.

## After

`../../report/validate/validate.md`. Reopen Desktop and verify visuals still render identically.
