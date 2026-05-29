# HTML-in-SVG — entity detail card

A "360" card for a single selected entity, composed with XHTML+CSS inside `<foreignObject>`. Reads the
foundation first: `../html-in-svg.md`. Worked example (grand-exchange item): `../examples/html-item-card-measure.dax`.

## What it renders

For the single item in filter context: a **rarity-colored name + rarity pill**, a 3-tile **stat grid**
(CSS grid), the recipe's **ingredient chips** (flex-wrap, per-ingredient rarity border), and a
**Craft-vs-Buy verdict** badge (green = craft cheaper, amber = buy cheaper, neutral = no recipe).

The verdict does a one-level craft-cost roll-up: `Σ(ingredient [Avg Market Price] × QtyRequired) ÷ YieldQty`
vs the item's market price. (True *recursive* BOM cost is a deeper DAX job — this is immediate ingredients
at market, which is the meaningful "buy mats → craft → sell" comparison.)

## Drive it

- `HASONEVALUE` guard → shows a "select an item" prompt when 0 or many items are in context.
- Bind to a single selection: an item **slicer** (`DimItem[ItemName]`), or a click on a board/table row.
- The recipe lookup filters `DimRecipe[OutputItemKey]` **directly** (that relationship is intentionally
  inactive to avoid an ambiguous second path to DimItem — see the model's `relationships.tmdl`).

## Wire

`dataCategory = ImageUrl`; single-cell `tableEx` sized ~440×380 (`../wiring/in-table-matrix.md`). The
`<foreignObject>` clips at its height — size for the worst-case ingredient count or chips get cut.

## Variants

- **Generic entity card** — swap item→customer/product, chips→child rows (orders, tickets), verdict→a status rule.
- **No-verdict** — drop the craft-vs-buy block for a pure profile card.
- **Sparkline header** — add a pure-SVG price sparkline above the grid (`sparkline.md`) for a trend at a glance.

## Caveats

foreignObject renders in Desktop + Service only — **blank in PDF/PowerPoint export**; inert to hover/click
(use native buttons for interaction). 32 KB string ceiling. See `../html-in-svg.md`.

## See also

`../examples/html-item-card-measure.dax` · `html-market-board.md` · `../html-in-svg.md`
