// document-model.cs — export every measure to a Markdown table (model documentation).
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Whole-model (no selection needed). Edit 'path' to your outputs folder.

string path = @"C:\Temp\model-measures.md";

var sb = new System.Text.StringBuilder();
sb.AppendLine("# Model measures");
sb.AppendLine();
sb.AppendLine("| Table | Measure | Format | Folder | Description |");
sb.AppendLine("|---|---|---|---|---|");

int n = 0;
foreach (var m in Model.AllMeasures.OrderBy(x => x.Table.Name).ThenBy(x => x.Name))
{
    var desc = (m.Description ?? "").Replace("\r", " ").Replace("\n", " ").Replace("|", "\\|");
    sb.AppendLine("| " + m.Table.Name
                + " | " + m.Name
                + " | " + (m.FormatString ?? "")
                + " | " + (m.DisplayFolder ?? "")
                + " | " + desc + " |");
    n++;
}

System.IO.File.WriteAllText(path, sb.ToString());
Output("document-model: wrote " + n + " measures to " + path);
