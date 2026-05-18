# Find visual-level overrides

List visuals that have `objects` or `visualContainerObjects` overrides — i.e., bypass the theme.

## CLI — across the report

```bash
pbir audit overrides "<project>.Report"
```

Returns one line per overridden property per visual.

## Group by visual type

```bash
pbir audit overrides "<project>.Report" --by visual-type
```

Useful for spotting "every line chart has its own title fontSize" patterns — candidates for `../promote/from-visuals.md`.

## Group by property name

```bash
pbir audit overrides "<project>.Report" --by property
```

Useful for spotting "fontSize is bespoke on 30 visuals" patterns — strong candidate for `../modify/wildcard.md` or `text-classes.md`.

## Raw grep alternative

```bash
grep -rE '"objects":|"visualContainerObjects":' "<project>.Report/definition/pages/" | wc -l
```

Faster but no aggregation.

## Output to outputs/

```bash
pbir audit overrides "<project>.Report" -o ../../../outputs/$(date +%Y-%m-%d)-<project>-overrides.md
```

## After

Decide per finding: keep as one-off, promote to theme (`../promote/from-visuals.md`), or accept as bespoke.
