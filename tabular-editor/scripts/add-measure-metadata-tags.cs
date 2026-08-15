// add-measure-metadata-tags.cs — stamp a metadata tag onto every measure's Description.
// Idempotent: skips any measure already tagged (the "check if they exist" requirement).
// Tag (appended at the END of the description text):
//     [Type: <type>, Created on: yyyy-MM-dd, Created by: JPA]
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Target: selected measures in the UI; whole model when run headless (CLI/CI).

// ---- config ----------------------------------------------------------------
string createdBy = "JPA";                                   // developer code (3 chars)
string createdOn = DateTime.Today.ToString("yyyy-MM-dd");   // today's date, ISO
// "Type": default = the measure's TOP display folder (auto-classify).
//   To use a FIXED type for all, replace the two "type" lines in the loop with:  var type = "Base";
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

    // derive the type from the top-level display folder; fall back to "General"
    var folder = (m.DisplayFolder ?? "").Split('\\')[0].Trim();
    var type = string.IsNullOrEmpty(folder) ? "General" : folder;

    var tag = "[Type: " + type + ", Created on: " + createdOn + ", Created by: " + createdBy + "]";

    // append at the end; keep any existing human description above it
    m.Description = string.IsNullOrWhiteSpace(desc) ? tag : desc.TrimEnd() + "\n" + tag;
    added++;
}

Output("metadata tags — added: " + added + ", already tagged (skipped): " + skipped + ". Save to persist.");
