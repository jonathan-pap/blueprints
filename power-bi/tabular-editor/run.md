# Run a script — UI, CLI, CI

Every script in [`scripts/`](scripts/) runs the same way in TE2 and TE3. Pick the model source, run,
then **save** to persist.

## From the UI (either version)

1. Open the model:
   - **TE3:** *File → Open → Power BI Desktop model* (live), or open the **PBIP/TMDL** folder directly.
   - **TE2:** *File → Open → From DB…* and pick the local instance (`localhost:<port>`), or open a `.bim`.
   - Port of the running Desktop model: `../03-bind/via-powershell/quickstart.md` (or the MCP
     `connection_operations ListLocalInstances`).
2. Open the **C# Script** tab (TE3) / **Advanced Scripting** tab (TE2).
3. Paste the script (or open the `.cs`), select target objects if the script uses `Selected.*`, **Run** (▶ / F5).
4. Review the `Output()` result, then **Save** (Ctrl+S) to write changes back to the model.

## From the CLI (headless / batch)

Both expose `-S <script>`. `Selected.*` is empty headless — the library scripts fall back to the whole
model (see [`compatibility.md`](compatibility.md#3-selection-vs-whole-model-ui-vs-cli)).

```bash
# TE2 (free) — against a saved model file, write the result back
TabularEditor.exe "projects/<p>/<name>.SemanticModel/model.bim" -S "tabular-editor/scripts/format-measures.cs" -B "projects/<p>/<name>.SemanticModel/model.bim"

# TE2 — against the live local Desktop model
TabularEditor.exe "Provider=MSOLAP;Data Source=localhost:<port>" "<db-id>" -S "tabular-editor/scripts/format-measures.cs"

# TE3 — against a PBIP/TMDL folder, save in place
TabularEditor3.exe "projects/<p>/<name>.SemanticModel" -S "tabular-editor/scripts/format-measures.cs" -SAVE
```

Flag notes: TE2 `-B <file>` writes a `.bim`; `-S` runs a script; `-D` deploys. TE3 uses `-S` + `-SAVE`
(and `-TMDL <folder>` to serialize). Run `TabularEditor.exe -?` / `TabularEditor3.exe -?` for the full
set on your build.

## In CI

Point the CLI at the serialized model in the repo (`.SemanticModel/`), run the script, and let the
tool re-serialize — commit the diff. Pair with the Best Practice Analyzer (`-A`/`-BPA`) as a gate.
TE2 is free and CI-friendly; TE3 needs a licensed runner.

## After

Reopen/refresh in Power BI Desktop (or `../03-bind/desktop-bridge.md` `reload`) to see model changes,
then validate with `../04-review/`.
