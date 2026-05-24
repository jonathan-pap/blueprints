# Variant — Count Pareto (quality / root-cause)

Pareto's original home: defect and incident analysis — *"80% of the problems come from 20%
of the causes."* The category is a **failure mode / root cause / complaint type**; the value
is a **count of occurrences** rather than a currency. Mechanically it's the base recipe with
the value measure swapped — but the framing, sort, and labels differ enough to call out.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| `<CATEGORY_COLUMN>` | a cause/defect-type column (`Defect Type`, `Complaint Reason`, `Error Code`). |
| `<VALUE_MEASURE>` | a **count** — `COUNTROWS(<fact>)` or `# Defects`, not a sum of money. |
| P2 share | identical — `DIVIDE([# Defects], COLLAPSEALL([# Defects], ROWS))`. |
| P3 / P4 / P5 | identical. |

## The count measure

If there isn't one already:

```dax
# Defects = COUNTROWS ( fct_defects )
```

Then every token from the base recipe uses `# Defects` as `<VALUE_MEASURE>`. The visual calcs
become:

```dax
Percent of grand total = DIVIDE ( [# Defects], COLLAPSEALL ( [# Defects], ROWS ) )
Easy Pareto            = RUNNINGSUM ( [Percent of grand total], ORDERBY ( [# Defects], DESC ) )
```

## Framing differences worth keeping

- **Bar data labels = raw counts** (`InsideBase`), so the reader sees both "how many" and the
  cumulative %. Currency Paretos often hide the bar labels; count Paretos usually show them.
- **Sort descending by count** — same rule as P1; the most frequent cause sits leftmost.
- The green/red split now reads as *"these few causes explain 80% of all defects — fix these
  first."* Consider relabeling the secondary axis from `Pareto` to `Cumulative % of defects`.

## Optional — cumulative *count* instead of %

Some QC audiences prefer the line in absolute counts. Swap P3 for:

```dax
Cumulative Defects = RUNNINGSUM ( [# Defects], ORDERBY ( [# Defects], DESC ) )
```

…and scale the secondary axis to the total count instead of 0–1 (P5). The 80% reference
then needs a line at `0.8 × total`, which is easier to keep as a **percentage** axis — so
prefer the % form unless stakeholders insist on counts.

## Use when

- Defect / incident / complaint / downtime-cause analysis.
- Any "what few things cause most of the events" question where the metric is a frequency.

## Note

This is the textbook Pareto. The only thing that changes from the base is the *meaning* of
the value — which is exactly why building it as a generic recipe pays off: one technique,
many domains.
