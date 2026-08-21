#!/bin/bash
#
# PostToolUse hook: put back the "$schema" header Power BI Desktop strips.
#
# Desktop rewrites definition.pbir and definition.pbism on every save and drops
# the "$schema" key while doing it. Both `pbir validate` and the Fabric item
# schemas treat that key as required, so a project starts failing validation
# purely because someone opened it and pressed Ctrl+S:
#
#   SCHEMA_ERROR  (root): '$schema' is a required property
#
# validate-pbir.sh already REPORTS this, but only for files Claude wrote — it
# never fires for a strip that happened inside Desktop, which is the only way it
# actually happens. This hook closes that gap by repairing instead of reporting.
#
# Triggers (see hooks.json):
#   - Bash(*powerbi-desktop*)  — bridge traffic; the first thing we run after a
#                               Desktop save, so it is the natural catch point
#   - Write/Edit of definition.pbir or *.pbism — covers our own writes
#
# The repair is a pure insert of a known constant at a known position. It cannot
# lose content and it is idempotent, so this hook never blocks: exit 0 always,
# printing only when it actually changed something.
#
# Toggle with restore_schema in config.yaml.
#
# Exit codes:
#   0 - always (advisory repair, never a gate)
#

# Strict mode intentionally relaxed, matching the other hooks here: on Windows
# Git Bash a spurious non-zero exit shows up as a scary "PostToolUse hook error".
set -o pipefail

INPUT=$(cat 2>/dev/null || printf '%s' '{}')

# Deliberately NO jq dependency. The other hooks in this folder open with
# `command -v jq || exit 0`, which means they silently do nothing on a machine
# without jq — and Git Bash on Windows does not ship it. Python is already
# required here to run the repair, so it parses the hook payload too.
PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null)
[[ -n "$PY" ]] || exit 0

# ── Config ──────────────────────────────────────────────────────────────────
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)" || exit 0
HOOK_CONFIG="$HOOK_DIR/config.yaml"
PARENT_CONFIG="$HOOK_DIR/../../hooks.yaml"
VALIDATOR="$HOOK_DIR/../scripts/validate_pbip.py"

[[ -f "$VALIDATOR" ]] || exit 0

# Parent kill-switch (power-bi/hooks.yaml — review: false disables this subsystem)
if [[ -f "$PARENT_CONFIG" ]] && grep -qE "^review:[[:space:]]*false" "$PARENT_CONFIG" 2>/dev/null; then
    exit 0
fi

# Local kill-switch (Windows escape hatch)
if [[ -f "$HOOK_CONFIG" ]] && grep -qE "^all_hooks_enabled:[[:space:]]*false" "$HOOK_CONFIG" 2>/dev/null; then
    exit 0
fi

# Per-check toggle
if [[ -f "$HOOK_CONFIG" ]] && grep -qE "^restore_schema:[[:space:]]*false" "$HOOK_CONFIG" 2>/dev/null; then
    exit 0
fi

# ── Work out what to sweep ──────────────────────────────────────────────────
#
# A Write/Edit names its file, so we can go straight to that project. A bridge
# command names nothing, so we sweep every project under power-bi/projects.
# The sweep is a grep over files that are 4-8 lines long — cheap enough to run
# on every bridge call, and it normally finds nothing and stops.

FILE_PATH=$(printf '%s' "$INPUT" | "$PY" -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if d.get("tool_name") in ("Write", "Edit"):
    p = (d.get("tool_input") or {}).get("file_path") or ""
    print(p.replace("\\\\", "/"))
' 2>/dev/null)

SEARCH_ROOTS=()
if [[ -n "$FILE_PATH" ]]; then
    case "$(basename "$FILE_PATH")" in
        definition.pbir|definition.pbism|*.pbism) ;;
        *) exit 0 ;;
    esac
    SEARCH_ROOTS+=("$(dirname "$FILE_PATH")")
else
    # Bridge traffic. Anchor on the repo, not the cwd — a hook's cwd is not
    # guaranteed to be anywhere near the project.
    ROOT="${CLAUDE_PROJECT_DIR:-}"
    [[ -n "$ROOT" ]] && ROOT=$(printf '%s' "$ROOT" | tr '\134' '/')
    [[ -z "$ROOT" ]] && ROOT="$HOOK_DIR/../../.."
    [[ -d "$ROOT/power-bi/projects" ]] || exit 0
    while IFS= read -r d; do
        SEARCH_ROOTS+=("$d")
    done < <(find "$ROOT/power-bi/projects" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)
fi

[[ ${#SEARCH_ROOTS[@]} -eq 0 ]] && exit 0

# ── Repair only what is actually broken ─────────────────────────────────────

# Collect the drifted FILES, then repair each one via its own .Report /
# .SemanticModel folder. Not via the project folder: power-bi/projects/test
# holds three PBIP projects side by side, and handing the validator that
# directory makes it pick one and quietly ignore the rest — which is exactly
# how the first cut of this hook managed to "succeed" while repairing nothing.
DRIFTED=()
for PROJ in "${SEARCH_ROOTS[@]}"; do
    [[ -d "$PROJ" ]] || continue
    while IFS= read -r f; do
        # grep is the fast pre-filter: it skips python's ~200ms start-up in the
        # overwhelmingly common case where nothing has drifted.
        grep -q '"\$schema"' "$f" 2>/dev/null || DRIFTED+=("$f")
    done < <(find "$PROJ" -maxdepth 2 \( -name "definition.pbir" -o -name "*.pbism" \) 2>/dev/null)
done

[[ ${#DRIFTED[@]} -eq 0 ]] && exit 0

REPAIRED=()
SEEN=""
for f in "${DRIFTED[@]}"; do
    ITEM_DIR=$(dirname "$f")
    # one validator run per .Report / .SemanticModel folder
    case "$SEEN" in *"|$ITEM_DIR|"*) continue ;; esac
    SEEN="$SEEN|$ITEM_DIR|"
    # --fix-schema, NOT --fix: the broad flag also scaffolds a .gitignore, and a
    # hook that silently creates unrelated files is a hook nobody trusts.
    OUT=$("$PY" "$VALIDATOR" "$ITEM_DIR" --fix-schema --no-pbir-cli --quiet 2>/dev/null)
    while IFS= read -r line; do
        line="${line%$'\r'}"
        [[ "$line" == *"restored \$schema"* ]] && REPAIRED+=("$line")
    done <<< "$OUT"
done

[[ ${#REPAIRED[@]} -eq 0 ]] && exit 0

echo "Restored the \$schema header Power BI Desktop stripped:" >&2
for line in "${REPAIRED[@]}"; do
    echo "  ${line#*FIX   }" >&2
done
echo "" >&2
echo "This is Desktop's doing, not an edit of yours. It will recur on the next" >&2
echo "save; see 04-review/audit/pbip-schema-drift.md." >&2

exit 0
