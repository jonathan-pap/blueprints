#!/bin/bash
#
# PostToolUse hook: lint TMDL for Desktop-strict traps that the structural
# validator (validate-tmdl.sh + tmdl-validate binary) does NOT catch.
#
# Two checks, both derived from incidents (see memory entries):
#
#   1. TRAP_MULTILINE_INDENT — Multi-line measure body indented at the same
#      level (or shallower) than `formatString:` / `displayFolder:` /
#      `lineageTag:` properties. The CLI parser accepts this, but Power BI
#      Desktop reports "syntax for 'formatString' is incorrect" on open.
#      See memory entry [[tmdl-multiline-measures]].
#
#   2. TRAP_STANDALONE_DOUBLE_SLASH — `//` comments inside measure bodies.
#      Desktop rejects them even though TMDL CLI accepts. Only `///` docstrings
#      are valid. See memory entry [[tmdl-comment-syntax]].
#
# Handles Write and Edit on any .tmdl file. Bash tool not matched (validate-tmdl.sh
# already handles those — this is a sidecar lint, not a duplicate validator).
#
# Toggleable via config.yaml: lint_tmdl_traps. Parent kill-switch: power-bi/hooks.yaml review.
#
# Exit codes:
#   0 - OK or not applicable
#   2 - Blocking: one or more traps detected
#

set -o pipefail

INPUT=$(cat 2>/dev/null || printf '%s' '{}')

command -v jq &>/dev/null || exit 0

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)" || exit 0
HOOK_CONFIG="$HOOK_DIR/config.yaml"
PARENT_CONFIG="$HOOK_DIR/../../hooks.yaml"

check_enabled() {
    local check_name="$1"
    [[ -f "$HOOK_CONFIG" ]] || return 0
    grep -qE "^${check_name}:\\s*false" "$HOOK_CONFIG" 2>/dev/null && return 1
    return 0
}

# Parent kill-switch
if [[ -f "$PARENT_CONFIG" ]] && grep -qE "^review:[[:space:]]*false" "$PARENT_CONFIG" 2>/dev/null; then
    exit 0
fi

# Local kill-switch
if [[ -f "$HOOK_CONFIG" ]] && grep -qE "^all_hooks_enabled:[[:space:]]*false" "$HOOK_CONFIG" 2>/dev/null; then
    exit 0
fi

check_enabled lint_tmdl_traps || exit 0

# ── Lint a single TMDL file ────────────────────────────────────────────────

lint_tmdl_file() {
    local FILE_PATH="$1"
    # Normalize backslashes to forward slashes via tr — Git Bash's ${VAR//\\//}
    # substitution mis-parses on some MSYS builds and strips forward slashes.
    FILE_PATH=$(printf '%s' "$FILE_PATH" | tr '\134' '/')

    [[ "$FILE_PATH" == *.tmdl ]] || return 0

    if [[ ! "$FILE_PATH" =~ \.SemanticModel/ ]] && \
       [[ ! "$FILE_PATH" =~ \.Dataset/ ]] && \
       [[ ! "$FILE_PATH" =~ /definition/ ]]; then
        return 0
    fi

    [[ -f "$FILE_PATH" ]] || return 0

    # awk does both checks in one pass. Emits one finding per line; FILENAME and NR
    # let the caller produce clickable file:line references.
    local FINDINGS
    FINDINGS=$(awk '
        # Track multi-line measure context.
        # A measure line ending with "=" starts a multi-line declaration.
        # The body is any line indented deeper than the measure declaration line,
        # until a property line (formatString|displayFolder|lineageTag) closes it.

        function indent_width(line,    n) {
            # count leading tabs (treat space-prefixed lines the same — sum tabs+spaces)
            n = 0
            while (n < length(line) && (substr(line, n+1, 1) == "\t" || substr(line, n+1, 1) == " ")) n++
            return n
        }

        # Reset on table boundary
        /^table / { in_measure = 0; body_min = -1 }

        # Detect measure start. Multi-line = line ends with "=" and the value is on
        # subsequent lines. Single-line = "measure X = expression" (no need to lint).
        /measure / {
            if ($0 ~ /=[[:space:]]*$/) {
                in_measure = 1
                measure_indent = indent_width($0)
                body_min = -1
                measure_line = NR
                next
            } else {
                in_measure = 0
            }
        }

        # In-measure: detect body lines and properties.
        in_measure {
            if (/^[[:space:]]*$/) next   # skip blanks within the measure body

            iw = indent_width($0)

            # Property line — formatString/displayFolder/lineageTag/formatStringExpression/dataType/etc.
            if ($0 ~ /^[[:space:]]+(formatString|displayFolder|lineageTag|formatStringExpression|dataType|isHidden|displayName|description):/) {
                if (body_min >= 0 && iw >= body_min) {
                    printf "%s:%d: TRAP_MULTILINE_INDENT — property at indent %d >= body min indent %d (measure started L%d). Body must sit DEEPER than properties or Desktop errors on open. See [[tmdl-multiline-measures]].\n", FILENAME, NR, iw, body_min, measure_line
                    errors++
                }
                # Properties stack at the same indent until measure ends
                next
            }

            # Body line — track minimum indent
            if (iw > measure_indent) {
                if (body_min < 0 || iw < body_min) body_min = iw
            } else {
                # de-dented to <= measure level → measure block ended
                in_measure = 0
            }
        }

        # TRAP 2: standalone // comments (not ///). Match anywhere in the file —
        # both inside measures and at table scope (Desktop rejects either).
        # Heuristic: a // sequence with neither / before nor after, and NOT inside
        # a string literal (rough approximation: line does not have an odd count of " before //).
        {
            line = $0
            pos = match(line, /[^\/]\/\/[^\/]/)
            if (pos == 0 && line ~ /^\/\/[^\/]/) pos = 1   # line starts with //
            if (pos > 0) {
                # Skip if it appears to be inside a string literal (best-effort)
                before = substr(line, 1, pos)
                gsub(/[^"]/, "", before)
                if (length(before) % 2 == 0) {   # even number of quotes before == outside string
                    printf "%s:%d: TRAP_STANDALONE_DOUBLE_SLASH — `//` comment found; Desktop only accepts `///` docstrings. See [[tmdl-comment-syntax]].\n", FILENAME, NR
                    errors++
                }
            }
        }

        END { exit (errors > 0 ? 1 : 0) }
    ' "$FILE_PATH" 2>&1)

    if [[ -n "$FINDINGS" ]]; then
        echo "TMDL lint failed: $FILE_PATH" >&2
        echo "" >&2
        echo "$FINDINGS" >&2
        echo "" >&2
        echo "Fix the trap(s) above. These pass tmdl-validate but Power BI Desktop rejects them on open." >&2
        return 2
    fi

    return 0
}


# ── Dispatch from tool input ───────────────────────────────────────────────

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    [[ -z "$FILE_PATH" ]] && exit 0
    lint_tmdl_file "$FILE_PATH"
    exit $?
fi

exit 0
