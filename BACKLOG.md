# Backlog

Work that is intentionally **not shipped** (kept on disk, excluded from git) plus parked
decisions, so nothing has to be re-derived later.

## Not ready to ship — git-ignored (2026-06-08)

- **grand-exchange project** (both blueprints) — `power-bi/projects/grand-exchange/` (report + semantic
  model) and `synthetic-data/projects/grand-exchange/` (generate.py, brief, schema). WIP dashboard:
  Market Watch / Market Board pages in progress; many measures live-only. Untracked from the remote
  on 2026-06-08; re-ship once the report is finished and reviewed.
- **candlestick (OHLC + volume) recipe** — `power-bi/02-build/recipes/candlestick/` (incl. the
  `volume-overlay` variant). Not validated/finalized. Ship once proven against a real report.

> These are in `.gitignore`. Local files remain; they are simply not synced to `origin`.

## Parked workstreams

- **grand-exchange dynamic period / date-window** (parked 2026-06-08, pending possible data extension).
  Decided direction when resumed:
  1. "Date · Last N Days" filter must use the **data-anchored `Range` table** (`Selected Days Back` +
     `Date In Range`, anchored to `MAX(data date)`) — NOT the built-in relative-date slicer (anchors to
     system today, drifts off the fixed 2026-06-05 data).
  2. Add **7D / 14D / 120D** buckets to `Range` (only has 1D/5D/30/90/180); default the slicer to 120D.
  3. Wire each Market Watch visual with `Date In Range = 1` (the candle pattern) so one slicer drives
     the page.
  4. Build additive `… (Period)` measures (Trade Value / Avg Price / Volume / Price Change % / Momentum,
     + `Period Label`) reading `Selected Days Back`; **keep** fixed anchors (52W, YoY, dual 7D/30D
     comparison tiles) — hybrid, not a rewrite.
  5. Drop the mockup's "Realm · All Realms" slicer (no realm dimension exists).
