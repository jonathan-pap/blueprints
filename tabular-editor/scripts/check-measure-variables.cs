// check-measure-variables.cs — report measures whose DAX VARs don't start with '_'.
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Report-only: renaming a VAR safely (the declaration AND every reference, without clashing
// with a same-named column/measure) is a careful manual edit — this lists the offenders for you.
// Target: selected measures in the UI; whole model when headless.

var rx = new System.Text.RegularExpressions.Regex(@"(?i)\bVAR\s+([A-Za-z0-9_]+)");

var targets = Selected.Measures.Any()
    ? Selected.Measures
    : (IEnumerable<Measure>)Model.AllMeasures;

int offenders = 0;
var sb = new System.Text.StringBuilder();

foreach (var m in targets)
{
    var bad = new System.Collections.Generic.List<string>();
    foreach (System.Text.RegularExpressions.Match mt in rx.Matches(m.Expression ?? ""))
    {
        var name = mt.Groups[1].Value;
        if (!name.StartsWith("_")) bad.Add(name);
    }
    if (bad.Count > 0)
    {
        offenders++;
        sb.AppendLine("• " + m.DaxObjectFullName + "  ->  VAR " + string.Join(", ", bad));
    }
}

Output(offenders == 0
    ? "All measure variables start with '_'.  OK"
    : offenders + " measure(s) with variables not starting with '_':\n\n" + sb.ToString());
