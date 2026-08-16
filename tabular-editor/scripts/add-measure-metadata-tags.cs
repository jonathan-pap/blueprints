// add-measure-metadata-tags.cs — stamp a metadata tag onto every measure's Description.
// Idempotent: skips any measure already tagged (the "check if they exist" requirement).
// Tag (appended at the END of the description text):
//     [Type: <type>, Created on: yyyy-MM-dd, Created by: JPA]
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Target: selected measures in the UI; whole model when run headless (CLI/CI).

// ---- config ----------------------------------------------------------------
string createdBy = "JPA";                                   // developer code (3 chars)
string createdOn = DateTime.Today.ToString("yyyy-MM-dd");   // today's date, ISO

// "Type" is CLASSIFIED from the measure's DAX + format + name into one of:
//   technical · date reference · percent · average · count · sum · other
// Heuristic + first-match-wins (order matters). Tune the keyword lists to taste.
Func<Measure, string> classify = m =>
{
    var dax  = (m.Expression   ?? "").ToUpperInvariant();
    var name = (m.Name         ?? "").ToUpperInvariant();
    var fmt  =  m.FormatString ?? "";

    // 1) technical — helpers / non-analytical output (colours, SVG, tooltips, sort, hidden)
    if (m.IsHidden || dax.Contains("DATA:IMAGE/SVG") || dax.Contains("UNICHAR(")
        || name.Contains("COLOR") || name.Contains("SVG") || name.Contains("TOOLTIP") || name.Contains("SORT"))
        return "technical";

    // 2) date reference — time-intelligence
    if (dax.Contains("DATEADD") || dax.Contains("YTD") || dax.Contains("QTD") || dax.Contains("MTD")
        || dax.Contains("SAMEPERIODLASTYEAR") || dax.Contains("DATESINPERIOD") || dax.Contains("PARALLELPERIOD")
        || dax.Contains("PREVIOUS") || dax.Contains("LASTDATE") || dax.Contains("FIRSTDATE")
        || dax.Contains("STARTOF") || dax.Contains("ENDOF") || dax.Contains("DATESBETWEEN"))
        return "date reference";

    // 3) percent — % format string or % in the name
    if (fmt.Contains("%") || name.Contains("%") || name.Contains(" PCT"))
        return "percent";

    // 4) average — AVERAGE(x), or a DIVIDE rate (per-unit)
    if (dax.Contains("AVERAGE") || dax.Contains("DIVIDE("))
        return "average";

    // 5) count
    if (dax.Contains("COUNTROWS") || dax.Contains("DISTINCTCOUNT") || dax.Contains("COUNTX")
        || dax.Contains("COUNTA") || dax.Contains("COUNT("))
        return "count";

    // 6) sum — additive default
    if (dax.Contains("SUMX") || dax.Contains("SUM("))
        return "sum";

    return "other";
};
// ----------------------------------------------------------------------------

var targets = Selected.Measures.Any()
    ? Selected.Measures
    : (IEnumerable<Measure>)Model.AllMeasures;

int added = 0, skipped = 0;

foreach (var m in targets)
{
    var desc = m.Description ?? "";

    // Already tagged? (signature = "[Type:" + "Created by:"). Leave it, count it.
    if (desc.Contains("[Type:") && desc.Contains("Created by:"))
    {
        skipped++;
        continue;
    }

    var type = classify(m);   // technical / date reference / percent / average / count / sum / other

    var tag = "[Type: " + type + ", Created on: " + createdOn + ", Created by: " + createdBy + "]";

    // append at the end; keep any existing human description above it
    m.Description = string.IsNullOrWhiteSpace(desc) ? tag : desc.TrimEnd() + "\n" + tag;
    added++;
}

Output("metadata tags — added: " + added + ", already tagged (skipped): " + skipped + ". Save to persist.");
