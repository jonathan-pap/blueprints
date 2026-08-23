# Building a model over MCP against an OPEN Desktop — what breaks

> Written after building a full star schema (5 tables, 10 measures, 2 ordinal columns) through
> the Modeling MCP while Desktop stayed open. It works, but four things bite in sequence and
> each one looks like a different problem.

## The short version

If Desktop can be **closed**, splice TMDL on disk and open it — the whole class of problem below
disappears. Build over MCP when Desktop must stay open, and expect to ask the user for two
clicks.

## 1. Desktop's save does NOT serialize MCP-created tables

Create tables over XMLA, hit Ctrl+S in Desktop, and `model.tmdl` comes back **still empty** —
`ref table` lines absent, `definition/tables/` not created. Desktop writes its own model tree,
and tables created through the XMLA endpoint are not in it. `hasUnsavedChanges` flips to false,
so it looks like a successful save.

Consequence: `pbir` cannot see the model, because `pbir` reads TMDL from disk:

```text
byPath: Failed to parse TMDL at …\demo.SemanticModel
```

so every `pbir add visual` fails to resolve fields until the model is on disk.

**Fix** — export the live model yourself and copy it into the project:

```text
database_operations ExportToTmdlFolder → <temp>
cp -r <temp>/. <project>.SemanticModel/definition/
```

The export lands in exactly the PBIP `definition/` shape (model.tmdl with `ref table` lines,
tables/, cultures/, expressions.tmdl, relationships.tmdl). Then **restart Desktop** so memory and
disk agree — otherwise Desktop's next save can overwrite what you just wrote.

## 2. Desktop shows the data as "pending changes", not as data

After the model is on disk and Desktop reopens, visuals render **empty** with two banners:

- *One or more calculated objects need to be manually refreshed*
- *Some of the tables have incomplete or no data*

A DAX query over MCP returns correct values the whole time, which is what makes this confusing —
the engine has the data and Desktop's Power Query layer does not agree. `RefreshWithXMLA` does
not clear it. Neither does F5 or `powerbi-desktop reload`.

**What cleared it in practice**: the banner's **Refresh now**, then **Apply changes** — i.e. two
user clicks. This is still the observed workaround rather than a proven limit, but note it is a
*different* problem from trap 3: trap 3 (a calculated column holding no data) is now known to be
fixable from the MCP with a table-scoped refresh, so do not reach for the click just because
these two banners look alike.

The banners also reappear on every `reload` afterwards — at that point they are stale chrome and
the data behind them is current.

## 3. A new calculated column holds no data until you refresh — and the MCP can do it

Create a calculated column over MCP and it exists but is empty. `column_operations Create` tells
you so in its own response, which is the signal to act on:

```text
Refresh required: 1 item(s) created but values have not been computed yet
(Column [_RefreshProbe] on table [DimQuestType]). Important: This must be followed
with a model refresh operation call.
```

Query it before refreshing and you get:

```text
The expression referenced column 'DimQuestType'[_RefreshProbe] which does not hold any data
because it needs to be recalculated or refreshed.
```

**Measured 2026-08-23** against an open Desktop (demo model, 40k-row fact, healthy and loaded),
by creating throwaway calculated columns and querying them immediately after each refresh path:

| Path | Result |
|---|---|
| `table_operations RefreshWithXMLA` (references: the one table) | **works** — column computed, no Desktop click |
| `model_operations RefreshWithXMLA` refreshType `Calculate` | **works** — column computed, no Desktop click |
| `model_operations RefreshWithAPI` | **refused**: *"RefreshWithAPI is only supported for Fabric cloud connections. Use RefreshWithXMLA instead."* Local Desktop models are out of scope for it, permanently |
| `partition_operations` refresh | not tested — unnecessary, both broader scopes already work |

**Prefer the table-scoped call.** Both XMLA paths worked here, but on the original build
model-scoped `Calculate`/`Full` failed with:

```text
The base version must not be negative when impact is requested for a transaction.
```

That error did **not** reproduce on retest, so it is state-dependent rather than a property of
model-scoped refresh. The difference that matters: on the original build the model had been
created entirely over MCP and Desktop's Power Query layer had never loaded it — the trap 2
"pending changes" state. Scope the refresh to the table and you sidestep the model-level
transaction entirely.

Do **not** ask the user to click **Refresh now** for a calculated column. That was the workaround
documented here before this was tested, and it was wrong — it cost several rounds on the demo
build, including shipping two pages with alphabetical Danger ordering because the ordinal column
was backed out rather than refreshed.

Still worth **batching every calculated column into one pass** — one refresh beats discovering
them one at a time.

## 4. The model lives only in memory until Desktop saves

Everything created over MCP is lost if Desktop closes without saving, and the bridge has **no
save command**. Ask for Ctrl+S at each milestone. `hasUnsavedChanges` does track MCP model edits
(it flips true), so it is a usable check — it just does not mean the TMDL will be complete when
the save lands. See trap 1.

## Order that works

1. Desktop closed → run the TMDL splice → open. *(If possible, stop here — the rest is the
   open-Desktop path.)*
2. Desktop open → MCP: named expressions, tables, relationships, MarkAsDateTable, measures.
3. `RefreshWithXMLA` Full — verify totals with a DAX query before building any visual.
4. `ExportToTmdlFolder` → copy into `.SemanticModel/definition/` → restart Desktop.
5. Ask for **Refresh now** + **Apply changes**, then Ctrl+S.
6. All calculated columns in ONE batch → `table_operations RefreshWithXMLA` on each affected
   table. No click needed here — verify with a DAX query against the new columns.
7. Build visuals with `pbir`; `powerbi-desktop reload` + `screenshot` to verify.

## See also

- `../../02-build/context.md` — the hard rule: edit TMDL with Desktop CLOSED
- `../../02-build/report/validate/build-traps.md` — the report-side equivalents
- `../desktop-bridge.md` — reload/screenshot loop, and what the bridge cannot do
