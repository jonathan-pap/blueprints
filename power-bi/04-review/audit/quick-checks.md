# Quick smoke tests

10-second sanity checks. Run before full audit.

## Page count

```bash
ls "<project>.Report/definition/pages/" | wc -l
```

> 5–8 pages → typically excessive for executive dashboards. Discuss with user.

## Visuals per page

```bash
for d in "<project>.Report/definition/pages/"*/; do
  count=$(ls "$d/visuals/" 2>/dev/null | wc -l)
  echo "$(basename "$d"): $count"
done
```

Thresholds:
- 6–8: optimal (best perf).
- 9–12: acceptable.
- 13–15: warning (noticeable delay).
- 16+: critical (perf issues).

Simple visuals (textbox, image, shape, button) don't count for perf.

## Theme applied?

```bash
jq -r '.themeCollection.customTheme.name' "<project>.Report/definition/report.json"
```

If empty → default Power BI theme. Apply one (`../../02-build/theme/apply/template.md`).

## Slicers per page

```bash
grep -r '"visualType":"slicer"' "<project>.Report/definition/pages/" | \
  awk -F/ '{print $5}' | sort | uniq -c
```

> 3 slicers per page → move extras to filter pane.

## After

Run `full-report.md` for the structured findings.
