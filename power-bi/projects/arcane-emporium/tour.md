# The Arcane Emporium — tour + tutorial

Five stops, driven by the bar across the bottom of every page. Built by
[`build_tour.py`](build_tour.py).

**The bookmarks navigate only.** They do not restore filters or visual visibility
(`suppressData` / `suppressDisplay`). That is deliberate: a tour that resets the slicers fights
the person giving it — set Realm = Grimmwald to answer a question, press Next, and your
selection is gone. The tour owns the running order; you own the filters. The moments below that
call for a filter are **live clicks**, marked 🖱.

---

## 1 · The chain — *Emporium Overview*

> "Eight enchanted-goods shops across three realms. Twenty-five million Gold over four years,
> and it grows twelve percent a year, every year."

- **25.00M** — the generator was told to hit exactly 25,000,000. It landed on 25,000,000.76.
- **+12.0%** — growth of the latest year against the year before.
- The trend chart is the one to linger on: **every November–December is the Frostfall festival**,
  and the gold line is a trailing three-month mean, so the spike reads as a spike rather than as
  the trend moving.

🖱 **Set Year = 2024** and point at **+12.25%**. It runs hot because 2024 is a leap year — 366
days of daily allocation against 365. Better to say it than to be asked.

---

## 2 · Where it comes from — *Realms & Shops*

> "Three realms, and they are not equal: Eldoria takes 45% of the Gold, Grimmwald 30%,
> Sunspire 25%."

- Bar colour is the realm — Eldoria blue, Grimmwald plum, Sunspire gold.
- The ledger on the right re-bases its **Share** column to whatever the slicers have selected, so
  it always reads as a share of what is on screen rather than of the whole four years.

🖱 **Set Realm = Eldoria** and watch Share recompute from 15% to 33% per shop.

> ⚠️ **Do not zoom in on individual shops.** Within a realm they are near-identical —
> 3,750,001 / 3,750,000 / 3,749,999 — because the generator splits each realm's Gold evenly
> across its shops. The realm split is pinned and meaningful; the shop split is not. If someone
> notices, say so; it is a property of synthetic data, not a bug in the report.

---

## 3 · What sells — *The Ledger of Wares*

**The best stop in the deck.** A Pareto: bars are Gold, the line is the running share.

> "Twenty-four wares. Four of them carry over half the takings, eleven carry eighty percent,
> and the other thirteen are the long tail."

- Gold bars up to the 80% mark, iron beyond it. The split is the whole point.
- The cumulative line is a **visual calculation** — no rank column, no cumulative measure, nothing
  in the model. `RUNNINGSUM([share], ORDERBY([value], DESC))`.

🖱 **Click a column header in the table below to re-sort it.** The Pareto line stays correct.
That `ORDERBY` is the reason: accumulation is pinned to value-descending regardless of how the
visual is sorted. The naive version zig-zags the moment you re-sort.

🖱 **Set Category = Potions.** The Pareto rebuilds for potions alone and the 80% line lands in a
different place — the vital few are relative to what you are looking at.

---

## 4 · Who buys — *Patrons*

> "Twenty named buyers in four kinds. Adventurers are 40% of the Gold, nobles 15%."

- The average-purse chart is the counter-intuitive one: **adventurers have the biggest average
  purse (284), nobles the smallest (190)** — the opposite of what the names suggest. Every patron
  visits about as often as every other, so average purse just tracks the pinned Gold share.
- **Kaelen Swiftblade alone is 24% of everything**, more than the whole Noble type.

---

## 5 · Back to the top — *Emporium Overview*

Land back on the Overview to close. If you filtered anything during the tour, clear the three
slicers first — the bookmarks will not do it for you, by design.

---

## If you would rather the tour staged the filters

It can. Each bookmark would capture the three slicers as well as the page, scoped with
`applyOnlyToTargetVisuals` so nothing else is touched. Two reasons it does not, today:

1. It fights live exploration, as above.
2. It could not be verified from here. The Desktop Bridge reloads and screenshots but cannot
   click, so a staged bookmark with the wrong slicer state would look perfect in every screenshot
   and fail in front of an audience. Say the word and it is a short change — but it wants
   click-testing in Desktop before it goes anywhere near a demo.

---

# The tutorial

The **right-hand bar** on every page is a second navigator, pointed at that page's tutorial
group. Ten steps in all. Each one puts a single graph on stage, **hides everything else**, and
reveals a caption that explains it. `Show all` is the first tile on every page — it is the way
out.

| Page | Steps |
|---|---|
| Overview | Numbers · Trend · Splits |
| Realms | Shops · Ledger |
| Items | Pareto · Ware list |
| Patrons | By kind · Avg purse · Spenders |

The steps carry `suppressData`, so like the tour they never touch the reader's slicers — you can
set Realm = Eldoria and walk the whole tutorial with it still applied.

## The bubbles

Each step's explanation is a **coach mark** — a rounded speech bubble with a tail pointing at the
graph, the way a game onboards you. Gold border, dark fill, drop shadow, a small all-caps step
counter, a gold heading and body copy with inline bold.

It is an SVG `ImageUrl` measure in an `image` visual, one per step, generated by
[`build_bubbles.py`](build_bubbles.py). A textbox could not do it: no tail, no radius, no shadow,
no mixed type in one block. The wrapped text comes from `<foreignObject>` holding real XHTML —
raw SVG `<text>` has no word wrap at all.

**Do not hand-edit the `Bubble NN` measures.** Re-run the generator; it is the source of truth,
and it computes each bubble's height from its own text.

## Why it hides rather than dims

You asked for either. Hiding won on mechanics: dimming needs a scrim **above** the other visuals
and the focused one **above the scrim**, and z-order is static in PBIR — it cannot change per
bookmark. The usual workaround is to duplicate every focusable visual at a high z and reveal the
duplicate, which doubles the visual count and the query load. Hiding needs one property
(`display.mode`), no z-order reasoning, no duplicates — and it hands the freed space to the
explanation, which dimming does not.

A shape-based scrim was never really available either: a `shape` visual would not render its
fill in this workspace before (see the panel note in `churnkit.py`). If you want the dim look, an
SVG `image` overlay would do it — that mechanism is proven here — but it still needs the
duplicate-visual trick to put the focused graph above the scrim. Say the word.

## What is verified and what is not

The bridge cannot click a bookmark, so **the restore behaviour is unproven**. What *is* proven,
by applying each step's state to the page files, screenshotting and reverting
(`preview_step.py`): the captions render where they should, the right graph is left standing, and
both navigator bars survive the step.

That last one was a real bug the preview caught — the first cut hid `tutorBar` along with
everything else, which strands the reader mid-step with no way to advance and no way back: the
page tour cannot rescue them either, because those bookmarks carry `suppressDisplay` and will
not un-hide anything.

