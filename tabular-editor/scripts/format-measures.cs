// format-measures.cs — apply house formatting + a display folder to measures.
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Target: selected measures in the UI; whole model when run headless (CLI/CI).

var targets = Selected.Measures.Any()
    ? Selected.Measures
    : (IEnumerable<Measure>)Model.AllMeasures;

int formatted = 0;
int foldered = 0;

foreach (var m in targets)
{
    var name = m.Name.ToLower();

    // Format by naming heuristic — tune to your conventions.
    if (name.Contains("%") || name.Contains(" pct") || name.EndsWith(" ratio") || name.Contains("margin"))
        m.FormatString = "0.0%;-0.0%;0.0%";
    else if (name.Contains("sales") || name.Contains("cost") || name.Contains("revenue")
             || name.Contains("profit") || name.Contains("amount") || name.StartsWith("total "))
        m.FormatString = "\\$#,##0;(\\$#,##0)";
    else if (name.Contains("count") || name.Contains("units") || name.EndsWith(" #") || name.Contains("qty"))
        m.FormatString = "#,##0";

    if (!string.IsNullOrEmpty(m.FormatString)) formatted++;

    // Park loose measures into a folder so the field list stays tidy.
    if (string.IsNullOrEmpty(m.DisplayFolder))
    {
        m.DisplayFolder = "Uncategorised";
        foldered++;
    }
}

Output("format-measures: set format on " + formatted + " measures; foldered " + foldered + ". Save to persist.");
