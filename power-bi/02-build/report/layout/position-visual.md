# Position a visual

Set x, y of an existing visual.

## CLI

```bash
pbir visuals position "<...>/Visual.Visual" --x 24 --y 120
```

## Rules

- Top-left corner = (24, 24) by convention (24 px margin).
- Avoid y < 120 unless you've removed the default page-title textbox.
- Never overlap another visual. Run `inspect-bindings.md` from `../bind/` to see current positions, or `pbir tree "<project>.Report" -v`.

## See also

- `size-visual.md` — set dimensions
- `align-visuals-row.md` — equal-gap row
- `page-dimensions.md` — confirm page bounds first
