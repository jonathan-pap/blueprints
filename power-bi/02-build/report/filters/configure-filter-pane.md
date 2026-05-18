# Configure the filter pane

Show or hide the right-side filter pane; control which filters appear inside it.

## Show / hide the pane

```bash
pbir pages set "<project>.Report/Overview.Page" --filter-pane-visible true
pbir pages set "<project>.Report/Overview.Page" --filter-pane-visible false
```

## Filter pane width

Default 240 px. Reduce only if you have very few filter labels.

## Show/hide per filter

In each filter (page-level or visual-level), set:

- `displayName` — friendlier label
- `isHiddenInViewMode: true` — filter is active but invisible to consumers
- `isLockedInViewMode: true` — visible but consumers can't change it

## Style

Pane background and font come from the report theme. To customize per-report, see `../../theme/format/override-property.md`.

## After

`../validate/validate.md`.
