#!/bin/bash
#
# UserPromptSubmit hook: surface recently-modified briefs so Claude reads them.
#
# Scans `power-bi/projects/**/brief.md` (and brief/*.md folder form) for files
# modified within the threshold and emits a system-reminder block listing them.
# Claude then reads any flagged brief before continuing.
#
# Catches three cases:
#   1. User created a new brief.md in their IDE between turns
#   2. User edited an existing brief.md in their IDE between turns
#   3. Brief exists in a project we haven't touched yet this session
#
# Toggle via power-bi/hooks.yaml: set `briefs: false` to disable.
# Threshold via env var BRIEF_DISCOVERY_MINUTES (default 60).
#
# Exit codes:
#   0 - always (this hook never blocks; it only adds context)

set -o pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)" || exit 0
PARENT_CONFIG="$HOOK_DIR/../../hooks.yaml"

# Honor parent toggle (briefs: false)
if [[ -f "$PARENT_CONFIG" ]] && grep -qE "^briefs:[[:space:]]*false" "$PARENT_CONFIG" 2>/dev/null; then
    exit 0
fi

# Resolve projects/ root (relative to this hook script)
PROJECTS_DIR="$HOOK_DIR/../../projects"
[[ -d "$PROJECTS_DIR" ]] || exit 0

THRESHOLD_MINUTES="${BRIEF_DISCOVERY_MINUTES:-60}"

# Single-file briefs (brief.md at any depth under projects/)
recent_files=$(find "$PROJECTS_DIR" -maxdepth 4 -name "brief.md" -mmin "-${THRESHOLD_MINUTES}" 2>/dev/null)

# Folder-form briefs (brief/ folder containing .md files modified recently)
recent_folder_files=$(find "$PROJECTS_DIR" -maxdepth 5 -path "*/brief/*.md" -mmin "-${THRESHOLD_MINUTES}" 2>/dev/null)

if [[ -z "$recent_files" && -z "$recent_folder_files" ]]; then
    exit 0
fi

# Emit additional context block on stdout (UserPromptSubmit hook contract)
{
    echo "<recent-briefs threshold=\"${THRESHOLD_MINUTES}min\">"
    echo "The following project briefs were created or modified recently."
    echo "If the user's intent touches any of these projects/themes, READ the brief"
    echo "before asking discovery questions or proposing a plan."
    echo ""
    if [[ -n "$recent_files" ]]; then
        while IFS= read -r f; do
            [[ -z "$f" ]] && continue
            rel="${f#${PROJECTS_DIR}/}"
            mtime=$(stat -c '%y' "$f" 2>/dev/null | cut -d. -f1)
            echo "  - power-bi/projects/${rel}    (modified: ${mtime:-unknown})"
        done <<< "$recent_files"
    fi
    if [[ -n "$recent_folder_files" ]]; then
        # De-dupe to one entry per brief/ folder
        echo "$recent_folder_files" | sed 's|/[^/]*$||' | sort -u | while IFS= read -r d; do
            [[ -z "$d" ]] && continue
            rel="${d#${PROJECTS_DIR}/}"
            echo "  - power-bi/projects/${rel}/  (folder-form brief)"
        done
    fi
    echo "</recent-briefs>"
} 2>/dev/null

exit 0
