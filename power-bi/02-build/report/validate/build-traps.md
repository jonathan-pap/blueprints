# Build traps — things that pass validation and still ship wrong

> Every entry here cost real time on a build and none of them are caught by `pbir validate`.
> Read this before a report build, not after.

## 1. `pbir add visual` sorts charts by the MEASURE, descending

The single most damaging default in the CLI. Every chart it creates gets:

```json
"sortDefinition": { "sort": [{ "field": { "Measure": … }, "direction": "Descending" }],
                    "isDefaultSort": true }
```

On a **time series that silently inverts the story**. A line chart of monthly revenue came out
as a smooth monotonic decline across three years — the data was growing 9% a year. It does not
look like a bug; it looks like a plausible downward trend, and it will survive review.

Fix — point the sort at the axis column:

```json
"sortDefinition": { "sort": [{ "field": { "Column": {
      "Expression": { "SourceRef": { "Entity": "DimDate" } }, "Property": "MonthYear" }},
      "direction": "Ascending" }], "isDefaultSort": false }
```

**Always set the sort explicitly on any chart whose axis has a natural order** (time, ordinal
categories). Value-descending is right for a Pareto and wrong for almost everything else.

## 2. A column's `sortByColumn` loses to the visual's own sort

Setting `Danger.sortByColumn = DangerOrder` in the model does nothing if the visual sorts by
`[Total Bounty] DESC` — the model ordinal only applies when the visual sorts on **that column**.
Symptom: the matrix reads Low/Medium/High/Extreme correctly while the bar chart next to it reads
High/Extreme/Medium/Low, from the same model. Matrices sort columns by the model; bar charts
carry their own sort.

Watch for the coincidence case: a rank ordinal (Gold/Silver/Bronze/Copper) may *happen* to match
value-descending order, so it looks correct while being unsorted. It breaks the first time the
data changes.

## 3. An ordinal sort column cannot derive from the column it sorts

```text
DangerOrder = SWITCH ( DimQuestType[Danger], "Low", 1, … )     -- then sort Danger by it
→ A circular dependency was detected: Danger, DangerOrder, Danger
```

Key the ordinal off the **surrogate key** instead, and say so in the description:

```dax
DangerOrder = SWITCH ( DimQuestType[QuestTypeKey], 2, 1, 6, 1, 4, 2, … )
```

## 4. `cardVisual` can render its title and nothing else

The newer `cardVisual` came up blank — container, title, no value — with a correct binding that
`pbir validate` passed. The legacy `card` (role `Values`, not `Data`) rendered the same measure
immediately. If a card is empty and the DAX returns a number, **swap the visual type before
debugging the binding**.

## 5. `pbir add title` writes 24pt into a 65px box

Force that box into a 40px layout rect and the text overflows its own container and Power BI
adds a **scrollbar**. Resize the font with the box or not at all: 16pt fits 48px. The same trap
applies to any textbox given a height by a layout script.

## 6. Slicers default to LIST mode and need ~160px

A `slicer` at 40–48px shows a header and a sliver of the first row — unusable, and it looks like
a rendering fault rather than a sizing one. Use Dropdown:

```json
"objects": { "data": [{ "properties": { "mode": { "expr": { "Literal": {
              "Value": "'Dropdown'" }}}}}] }
```

Also hide the **container title** when the slicer's own header is on, or the field name renders
twice, one above the other.

## 7. Slicer text size is `textSize`, not `fontSize`

`pbir set …header.fontSize` is rejected. The properties are `header.textSize` and
`items.textSize`. `pbir set` names the correct one in its error — read it rather than guessing.

## 8. `pbir page rename` leaves `pages.json` behind

It renames the folder and the display name but does **not** update `pageOrder` /
`activePageName`, so the page name, the folder name and the metadata disagree. `pbir validate`
passes; `04-review/scripts/validate_pbip.py` catches it:

```text
ERR [page_folder_missing] pageOrder lists 'e9f0b44…' but no matching folder exists
WARN [orphan_page_folder] page folder 'Guild_Overview' is not in pageOrder
```

`pbir add page` has the same shape of problem — it creates the folder under a GUID while the
display name is what you asked for. Align folder = `page.json.name` = `pageOrder` entry by hand.

## 9. Commands the room docs describe that pbir 0.9.25 does not have

`pbir filters add` (documented in `../filters/add-visual-filter.md`), `pbir bookmarks new`,
`pbir audit theme`. Check `--help` before building a step around a documented command. For a
TopN filter, write `filterConfig` by hand — it belongs at the **root** of visual.json, never
inside `visual`.

## 10. Conditional-format colours cannot follow a theme

Rule-based colour needs literal hex, so anything coloured by a conditional rule — the Pareto
recipe's vital/trivial split especially — is invisible to the theme cascade. Swap to a dark
theme and those visuals keep their light-theme palette on a black page. Either re-colour them
per theme with a script, or accept that they are pinned.

## 11. Theme corner radius may not reach the visuals

Setting `radius` in the theme JSON (11 places: `border` + `visualCorners` on the wildcard, card,
table, slicer, QnA, smartNarrative) changed nothing in Desktop — the format pane still read the
old value. `pbir visuals border --show --radius N` per visual is what actually applied.

Related: **`pbir theme build` does not remove the previous theme**. Registered themes accumulate
in `StaticResources/RegisteredResources/`; a report can end up carrying five, four of them dead.

## 12. `textSize` vs `fontSize` is per-component, not per-CLI

Trap 7 says slicers use `textSize`. `tableEx` is the opposite — `values.textSize` and
`columnHeaders.textSize` are both rejected, and the working names are `values.fontSize` /
`columnHeaders.fontSize`. There is no rule to memorise; `pbir set` names the right one in its
error and `pbir schema describe <visualType> <component>` lists them all. Read the error.

## 13. Table row height is `grid.rowPadding`, not the font size

Shrinking `values.fontSize` on a `tableEx` makes the text smaller and leaves the row height
almost unchanged, so you get the same row count in a smaller font — worse on both counts.
Row height is driven by `grid.rowPadding` (padding applied top *and* bottom). Dropping it to 1
took a 272px table from 6 visible rows to 9.

Corollary for layout: **decide table height by counting rows in a render**, not by grid spans.
A detail table sized from the grid alone lands on a half-clipped final row, which reads as a
rendering fault. Nudge the height until the last visible row is whole.

## 14. Horizontal bars need ~32px each or the chart scrolls silently

A 10-category `clusteredBarChart` at 312px tall renders 9 bars and a scrollbar; at 320px it
renders 10. Nothing warns you, and the chart looks complete — it just quietly omits the last
category, which on a "top 10" is the one the title promises. Count the bars in the render
against the TopN filter every time.

## See also

- `../../../04-review/audit/pbip-schema-drift.md` — Desktop strips `$schema` on every save
- `../../../04-review/audit/pbir-validate.md` — real errors vs the CLI's bundled-schema lag
- `../../recipes/pareto-chart/context.md` — the recipe whose colours trap 10 describes
