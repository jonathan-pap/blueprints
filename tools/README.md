# tools/ — workspace utilities

## Move the Claude setup to another machine

Your setup lives in **two layers**: the workspace (travels via git) and the user-level
Claude Code setup in `~/.claude` (travels via the export/import pair here).

### What the zip carries (and what it doesn't)

`export-claude-setup.ps1` snapshots exactly the **four portable pieces** of
`C:\Users\<you>\.claude\`:

| Piece | What it is |
|---|---|
| `settings.json` | model choice, permissions, **enabled plugins + marketplaces** (plugins reinstall themselves from GitHub on next launch — no caches needed) |
| `commands\sc\` | the SuperClaude `/sc:*` command set |
| `agents\` | custom agent definitions |
| `projects\<workspace-key>\memory\` | Claude's memory for **this workspace** (gotchas, parked decisions, feedback) |

Plus a `manifest.json` recording the source workspace path.

Deliberately **not** exported: `~/.claude.json` (OAuth/account/machine state — just
`claude login` on the new machine), caches, sessions, history. The workspace-level MCP
config needs nothing either — the repo's own `.mcp.json` wires the Power BI Modeling MCP
on any clone.

### On this machine — export (run anytime)

```powershell
pwsh tools/export-claude-setup.ps1
# -> claude-setup-YYYY-MM-DD.zip in the current folder   (or -OutFile <path>)
```

Read-only — it never modifies your setup. Re-run whenever settings, memory, or agents
changed. `claude-setup-*.zip` is gitignored, so a snapshot can sit in the repo folder
without ever being committed.

### On the new machine — four steps

```powershell
# 1. install Claude Code, then sign in
claude login

# 2. clone the workspace + install the toolchain
git clone https://github.com/jonathan-pap/blueprints.git Workspace-Blueprint
cd Workspace-Blueprint
pwsh power-bi/setup.ps1 -InstallMissing     # Python, pbir, jq, Node, Desktop, Bridge CLI

# 3. copy the zip over and import it
pwsh tools/import-claude-setup.ps1 -Zip <path-to-claude-setup-zip>

# 4. launch Claude Code inside the workspace
#    -> approve the .mcp.json trust prompt; plugins auto-install on first launch
```

The import **backs up** an existing `settings.json` to `settings.json.bak` before
replacing it, and merge-copies `commands\sc\` + `agents\`.

### The memory-folder path key (handled automatically)

Claude keys workspace memory by the workspace's **path**:
`E:\Workspace-Blueprint` → `~\.claude\projects\e--Workspace-Blueprint\memory\`
(`:` and `\` become `-`, first letter lowercased).

Clone the workspace to a *different* path on the new machine and the key changes —
which is why the import script **re-keys the memory folder automatically**: it derives
the new key from wherever the repo actually sits (the script's own location) and renames
on restore. Nothing to do by hand; copying the folder manually is when you'd need to
rename it yourself.
