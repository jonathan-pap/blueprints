# Desktop strips `$schema` from `.pbir` / `.pbism`

**Symptom.** A project that validated yesterday fails today, and `git diff` shows a change
nobody made:

```
SCHEMA_ERROR  (root): '$schema' is a required property
```

```diff
 {
-  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
   "version": "4.0",
```

**Cause.** Power BI Desktop rewrites `definition.pbir` and `definition.pbism` on every save and
drops the `$schema` key while doing it. Both `pbir validate` and the Fabric item schemas treat
that key as required. So the file goes invalid because someone opened the project and pressed
Ctrl+S — no edit of yours is involved, and there is nothing to fix in your own work.

It recurs. Restoring it by hand buys you exactly one save.

---

## The fix

```bash
# check
python power-bi/04-review/scripts/validate_pbip.py <project> --no-pbir-cli

# repair (idempotent)
python power-bi/04-review/scripts/validate_pbip.py <project> --fix-schema
```

`--fix-schema` restores only these headers. `--fix` does that **and** scaffolds a `.gitignore`;
prefer the narrow flag when you only mean to undo the strip.

The repair is a text insert of a known constant at a known position — it never re-serialises the
JSON, so indentation, key order and line endings survive and the diff stays one line.

## The canonical URLs

| File | `$schema` |
|---|---|
| `definition.pbir` | `https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json` |
| `definition.pbism` | `https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json` |

Note the path segment is `definitionProperties/`, **not** the `definition/` used by the PBIR files
inside `definition/` (pages, visuals, bookmarks). Getting those two confused produces a file that
looks right and still fails.

## The hook

[`../hooks/restore-pbip-schema.sh`](../hooks/restore-pbip-schema.sh) repairs the drift instead of
reporting it. It fires:

| Trigger | Why |
|---|---|
| `Bash(*powerbi-desktop*)` | Bridge traffic is the first thing that runs after a Desktop save, so it is the natural catch point for a strip that happened inside Desktop |
| `Write`/`Edit` of `definition.pbir` or `*.pbism` | covers our own writes |

It sweeps every project under `power-bi/projects` on the bridge trigger — a grep over files that
are four to eight lines long, ~0.7s including a repair. It never blocks: exit 0 always, output
only when it changed something. Toggle with `restore_schema` in
[`../hooks/config.yaml`](../hooks/config.yaml).

`validate-pbir.sh` also reports a missing `$schema`, but only for files **Claude** wrote — which
is never how this happens. That is the gap this hook exists to close.

---

## Two traps worth knowing

**The sweep is file-oriented, not project-oriented.** `power-bi/projects/test/` holds three PBIP
projects side by side. Hand `validate_pbip.py` that directory and it picks one (`WARN
[multiple_pbip] 3 .pbip files found; validated example reports.pbip`) and ignores the rest. The
first cut of the hook did exactly that and reported success while repairing nothing. It now
resolves each drifted file to its own `.Report` / `.SemanticModel` folder.

**Read and write with `newline=""`.** Without it Python's universal-newline translation turns a
CRLF file into LF on the way in, and the repair rewrites every line ending in the file — a
one-key insert showing up as a whole-file diff.

## Related

- [`pbir-validate.md`](pbir-validate.md) — the `SCHEMA_DEGRADED` warnings are a different thing
  entirely (pbir's bundled schemas lagging the format), and are cosmetic.
- [`../structure/validate-project.md`](../structure/validate-project.md) — the wider structural check.
