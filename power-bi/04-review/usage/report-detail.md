# Single-report usage deep-dive

Daily views, per-viewer breakdown, page views by day for one report.

## Script

```bash
python ../scripts/get_report_detail.py -w <workspace-id> -r <report-id> \
  -o ../../outputs/$(date +%Y-%m-%d)-<report>-usage.json
```

## Output covers

- Daily view count over the last 60 days (rolling 7-day avg)
- Per-viewer counts (with non-consumer filtering — see `exclude-non-consumers.md`)
- Per-page view distribution
- Time-of-day pattern (when users typically open it)
- Average load time

## What to look for

- **Spikes** — does usage spike on Mondays (weekly ops review) or month-end? Confirms intended audience pattern.
- **Decline** — sustained drop > 30% over 4 weeks → ask the team if the underlying decision moved elsewhere.
- **Page concentration** — if Page 1 gets 90% of views, the other pages are candidates for removal or merging.
- **Load time** — > 5 sec is felt by users; investigate via `../audit/performance.md`.

## Auth

Same as `workspace.md` — service principal recommended.
