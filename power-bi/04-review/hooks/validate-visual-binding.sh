#!/bin/bash
#
# PreToolUse hook: validate -d "role:Table.Field" arguments against the actual
# model BEFORE pbir add visual / pbir visuals bind runs.
#
# Catches the most common failure mode: Claude hallucinates a measure name
# (e.g., "Gross Profit Margin") and tries to bind it. pbir accepts the
# binding silently; the broken visual surfaces only when you reopen Desktop.
#
# Behavior:
#   - Inspects only pbir add visual / pbir visuals bind / pbir add visual --from-json commands
#   - Extracts every -d "role:Table.Field" pair
#   - Calls `pbir model -d <report>` to enumerate real fields, then greps
#   - Blocks (exit 2) on any missing field, listing closest matches as hints
#   - Skips silently when:
#       * pbir is not on PATH
#       * the Report path can't be resolved
#       * `pbir model -d` fails (thin reports without live access)
#
# Toggle:
#   - Parent: power-bi/hooks.yaml → review: false disables the whole subsystem
#   - Local:  04-review/hooks/config.yaml → binding_check: false (this hook only)
#
# Exit codes:
#   0 - OK, skipped, or not applicable
#   2 - Blocking: at least one bound field doesn't exist in the model

set -o pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)" || exit 0
HOOK_CONFIG="$HOOK_DIR/config.yaml"
PARENT_CONFIG="$HOOK_DIR/../../hooks.yaml"

# Parent kill-switch
if [[ -f "$PARENT_CONFIG" ]] && grep -qE "^review:[[:space:]]*false" "$PARENT_CONFIG" 2>/dev/null; then
    exit 0
fi

# Local kill-switches
if [[ -f "$HOOK_CONFIG" ]] && grep -qE "^all_hooks_enabled:[[:space:]]*false" "$HOOK_CONFIG" 2>/dev/null; then
    exit 0
fi
if [[ -f "$HOOK_CONFIG" ]] && grep -qE "^binding_check:[[:space:]]*false" "$HOOK_CONFIG" 2>/dev/null; then
    exit 0
fi

# Need pbir
command -v pbir &>/dev/null || exit 0

# JSON parser — prefer jq, fall back to python (pbir is python-based, so this is reliable)
parse_json() {
    local field="$1"
    if command -v jq &>/dev/null; then
        jq -r ".${field} // empty" 2>/dev/null
    elif command -v python &>/dev/null; then
        python -c "import sys,json
try:
    d=json.load(sys.stdin)
    for k in '$field'.split('.'):
        d=d.get(k,'') if isinstance(d,dict) else ''
    print(d if d else '')
except Exception: pass" 2>/dev/null
    elif command -v python3 &>/dev/null; then
        python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
    for k in '$field'.split('.'):
        d=d.get(k,'') if isinstance(d,dict) else ''
    print(d if d else '')
except Exception: pass" 2>/dev/null
    else
        cat >/dev/null
    fi
}

# Read hook stdin once
STDIN_BUF="$(cat 2>/dev/null || printf '%s' '{}')"
TOOL_NAME=$(printf '%s' "$STDIN_BUF" | parse_json 'tool_name')
[[ "$TOOL_NAME" == "Bash" ]] || exit 0
CMD=$(printf '%s' "$STDIN_BUF" | parse_json 'tool_input.command')
[[ -n "$CMD" ]] || exit 0

# Only fire on pbir binding commands
case "$CMD" in
    *"pbir add visual"*|*"pbir visuals bind"*) : ;;
    *) exit 0 ;;
esac

# Find the Report path — first token containing .Report (with or without trailing /something.Page or .Visual)
REPORT_TOKEN=$(echo "$CMD" | grep -oE '[^[:space:]"]+\.Report[^[:space:]"]*' | head -1)
[[ -n "$REPORT_TOKEN" ]] || exit 0
REPORT_PATH=$(echo "$REPORT_TOKEN" | sed -E 's|(\.Report)(/.*)?$|\1|')

# Enumerate fields from the live model. Cache per-run in /tmp.
MODEL_CACHE="${TMPDIR:-/tmp}/.pbir-model-$(echo "$REPORT_PATH" | md5sum 2>/dev/null | cut -c1-8).txt"
if ! pbir model "$REPORT_PATH" -d > "$MODEL_CACHE" 2>/dev/null; then
    # Thin report or model unreachable — skip rather than block
    exit 0
fi
[[ -s "$MODEL_CACHE" ]] || exit 0

# Extract every -d / --data argument value. Tolerate single + double quotes.
# Output format: one "role:Table.Field" per line.
extract_data_args() {
    local cmd="$1"
    # Match -d "..." or -d '...' or --data "..." or --data '...'
    # Strategy: replace with newlines, then grep the quoted blocks
    printf '%s' "$cmd" |
        grep -oE -- '(-d|--data)[[:space:]]+("[^"]+"|'"'"'[^'"'"']+'"'"')' |
        sed -E -e 's/^(-d|--data)[[:space:]]+//' -e 's/^["'"'"']//' -e 's/["'"'"']$//'
}

# Suggest the closest field name from the model output
suggest_field() {
    local needle="$1"
    local needle_lc
    needle_lc=$(echo "$needle" | tr '[:upper:]' '[:lower:]')
    # Pull bullet entries from pbir model output, strip leading "    • " and trailing "(format)"
    local candidates
    candidates=$(grep -oE '•[[:space:]]+[^(]+' "$MODEL_CACHE" | sed -E 's/^•[[:space:]]+//;s/[[:space:]]+$//' | sort -u)
    # Pass 1: substring (case-insensitive)
    local hits
    hits=$(printf '%s\n' "$candidates" | while IFS= read -r c; do
        c_lc=$(echo "$c" | tr '[:upper:]' '[:lower:]')
        if [[ "$c_lc" == *"$needle_lc"* ]] || [[ "$needle_lc" == *"$c_lc"* ]]; then
            echo "$c"
        fi
    done | head -3)
    if [[ -n "$hits" ]]; then
        echo "$hits" | sed 's/^/    → /'
        return
    fi
    # Pass 2: first-word match
    local first
    first=$(echo "$needle" | awk '{print tolower($1)}')
    if [[ ${#first} -ge 3 ]]; then
        printf '%s\n' "$candidates" | while IFS= read -r c; do
            c_first=$(echo "$c" | awk '{print tolower($1)}')
            if [[ "$c_first" == "$first" ]]; then echo "$c"; fi
        done | head -3 | sed 's/^/    → /'
    fi
}

# Validate each binding
errors=""
while IFS= read -r d_arg; do
    [[ -z "$d_arg" ]] && continue
    # role:Table.Field — strip role:
    field_ref="${d_arg#*:}"
    # Table.Field → Field
    field_name="${field_ref##*.}"
    [[ -z "$field_name" ]] && continue
    # Check the field name appears as a bullet entry in the model output.
    # Match leading "• " followed by the exact name, then end-of-line or " (format)"
    if ! grep -qE "•[[:space:]]+${field_name}([[:space:]]+\(|[[:space:]]*$)" "$MODEL_CACHE"; then
        suggestions=$(suggest_field "$field_name")
        errors+="  Field not found in model: '${field_ref}'"$'\n'
        if [[ -n "$suggestions" ]]; then
            errors+="    Did you mean:"$'\n'
            errors+="${suggestions}"$'\n'
        fi
    fi
done < <(extract_data_args "$CMD")

if [[ -n "$errors" ]]; then
    {
        echo "Visual binding validation failed:"
        printf '%s' "$errors"
        echo ""
        echo "Run \`pbir model \"$REPORT_PATH\" -d\` to list real fields before retrying."
        echo "(Set binding_check: false in $HOOK_CONFIG or review: false in $PARENT_CONFIG to disable.)"
    } >&2
    exit 2
fi

exit 0
