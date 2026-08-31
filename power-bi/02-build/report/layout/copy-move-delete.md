# Copy / move / delete a visual

Restructures visuals that already exist — duplicate one onto another page, rename it, or remove it. To create a new visual instead, use `../add-visual/`.

## Copy across pages

```bash
pbir cp "<project>.Report/P1.Page/Visual.Visual" "<project>.Report/P2.Page/Visual.Visual"
```

## Rename / move within the same page

```bash
pbir mv "<project>.Report/P.Page/Old.Visual" "<project>.Report/P.Page/New.Visual"
```

## Delete

```bash
pbir rm "<project>.Report/P.Page/Visual.Visual" -f
```

## After

`../validate/validate.md`. Reopen Desktop to confirm.
