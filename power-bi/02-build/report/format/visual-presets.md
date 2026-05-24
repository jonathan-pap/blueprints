# Style presets (one-shot formatting bundles)

> A preset writes a curated set of container properties (title, border, background, padding,
> header…) onto a visual in one command. It overrides those slots only and does **not** touch
> the theme. Use it to make a visual stand out from the cascade, or to normalize a page's look fast.

## List

```bash
pbir visuals preset --list
```

Returns `minimal`, `clean`, `bold`, `emphasis`, `presentation`:

| Preset | Character |
|---|---|
| `minimal` | removes borders, shadows, headers; lighter title |
| `clean` | light borders, subtle title, no shadow |
| `bold` | heavier borders, prominent title, stronger background contrast |
| `emphasis` | card-style background, accent border, prominent title |
| `presentation` | large titles + padding tuned for slide-style review |

## Apply

```bash
# single visual
pbir visuals preset "<project>.Report/Overview.Page/Visual.Visual" --name minimal
# bulk via glob (no -f needed; presets overwrite named slots only)
pbir visuals preset "<project>.Report/Overview.Page/*.Visual" --name clean
pbir visuals preset "<project>.Report/**/*.Visual" --name presentation
```

Don't chain presets — on overlapping slots the **last one wins**.

## Preset vs theme

- **Theme** = colors, fonts, visual-type defaults that cascade everywhere → `../../theme/`.
- **Preset** = one-shot bundle for a specific visual or page.

Set the theme first, then use presets sparingly for the exceptions. If you find yourself
applying the same preset to every visual of a type, that belongs in the theme instead
(`../../theme/modify/visual-type-override.md`).

## When NOT to use

- A custom property bundle the user describes → build once with the targeted commands
  (`override-property.md`) and consider promoting to a theme rule.
- Bespoke single-property tweak → use `override-property.md` directly.

## After

`../validate/validate.md`.
