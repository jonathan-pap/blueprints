// fix-measure-variables.cs — rename measure DAX VARs to start with '_' (declaration + references).
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.  Pairs with check-measure-variables.cs
// and the MEASURE_VAR_UNDERSCORE_PREFIX BPA rule.
//
// DRY-RUN by default. Review the list, then set  apply = true  and re-run to write, then SAVE.
// Each offending VAR name 'x' becomes '_x' wherever it appears as a BARE identifier — the rename
// skips [columns], 'tables', and longer words via a word boundary.
// CAVEAT: if a variable shares a name with something referenced bare, the dry-run will show it —
// check before applying.

bool apply = false;                    // <-- set true to actually rename

var declRx = new System.Text.RegularExpressions.Regex(@"(?i)\bVAR\s+([A-Za-z][A-Za-z0-9_]*)");

var targets = Selected.Measures.Any()
    ? Selected.Measures
    : (IEnumerable<Measure>)Model.AllMeasures;

int changed = 0;
var sb = new System.Text.StringBuilder();

foreach (var m in targets)
{
    var expr = m.Expression ?? "";

    // collect declared VAR names that don't start with '_'
    var names = new System.Collections.Generic.HashSet<string>();
    foreach (System.Text.RegularExpressions.Match mt in declRx.Matches(expr))
    {
        var n = mt.Groups[1].Value;
        if (!n.StartsWith("_")) names.Add(n);
    }
    if (names.Count == 0) continue;

    var newExpr = expr;
    foreach (var n in names)
    {
        // n -> _n, only as a whole token (not inside [..] / '..' / a longer identifier)
        var pat = @"(?<![A-Za-z0-9_'\[])" + System.Text.RegularExpressions.Regex.Escape(n) + @"(?![A-Za-z0-9_])";
        newExpr = System.Text.RegularExpressions.Regex.Replace(newExpr, pat, "_" + n);
    }

    if (newExpr != expr)
    {
        changed++;
        sb.AppendLine("• " + m.DaxObjectFullName + "  ->  " + string.Join(", ", names));
        if (apply) m.Expression = newExpr;
    }
}

Output(
    (apply ? "APPLIED — renamed vars in " : "DRY-RUN — would rename vars in ")
    + changed + " measure(s)"
    + (apply ? ". SAVE to persist:\n\n" : ". Set apply=true to write:\n\n")
    + sb.ToString());
