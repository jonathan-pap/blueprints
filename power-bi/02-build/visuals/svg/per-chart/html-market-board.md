# HTML-in-SVG — ranked board / listing

A leaderboard-style listing of TopN rows, composed with XHTML+CSS inside `<foreignObject>`. Reads the
foundation first: `../html-in-svg.md`. Worked example (grand-exchange market board):
`../examples/html-market-board-measure.dax`.

## What it renders

A framed board with a header, column labels, and N rows — each row a **CSS grid** of: rarity-colored
item name (left accent border), right-aligned **price** (tabular figures), **listings** count, and a
**relative value bar** (gradient, sized by the row's share of the max). Ranking by `[Total Trade Value]`.

The flex/grid alignment + tabular-figure columns + the inline value bar are the things raw `<text>`/`<rect>`
make tedious; here they're a few CSS rules.

## Drive it

- `TOPN ( _N, FILTER ( _Items, [@value] > 0 ), [@value], DESC )` over `SUMMARIZE(ALLSELECTED(DimItem), …)`
  — respects outer slicers, drops zero-value items.
- For an **interactive row count**, replace the literal `_N` with a harvested disconnected what-if slicer
  (`GENERATESERIES` → slicer → `SELECTEDVALUE`) — see `../../recipes/disconnected-selection-emphasis/`.

## Wire

`dataCategory = ImageUrl`; single-cell `tableEx` sized ~620×460 (`../wiring/in-table-matrix.md`). Size the
`<foreignObject>` height for `_N` rows — it clips, so more rows need more height.

## Variants

- **Order book** — two boards side by side (top buyers vs sellers) using the role-playing `BuyerSellerKey`.
- **Top movers** — rank by day-over-day price delta; arrow + color the delta inline.
- **Pulse header** — add a SMIL "● LIVE" dot (`../html-in-svg.md` → Animation) for a live-feed feel.

## Caveats

foreignObject renders in Desktop + Service only — **blank in PDF/PowerPoint export**; inert to hover/click.
Marshals rows via `CONCATENATEX` — keep N small (~5–30). 32 KB string ceiling. See `../html-in-svg.md`.

## See also

`../examples/html-market-board-measure.dax` · `html-item-card.md` · `../html-in-svg.md`
