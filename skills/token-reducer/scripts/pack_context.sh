#!/usr/bin/env bash
# ==============================================================================
# pack_context.sh - Optimized Codebase Context Packager using Repomix
#
# Automatically injects high-efficiency token reduction flags:
#   --compress: Tree-sitter AST structural outline (classes/functions/interfaces)
#   --remove-comments: Strip non-essential comments
#   --no-file-summary: Remove verbose narrative file summary preamble
# ==============================================================================

set -eo pipefail

TARGET_DIR="."
OUTPUT_FILE=""
BUDGET=""
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --token-budget|--budget)
            BUDGET="$2"
            shift 2
            ;;
        --dir|-d)
            TARGET_DIR="$2"
            shift 2
            ;;
        *)
            EXTRA_ARGS+=("$1")
            shift
            ;;
    esac
done

if ! command -v repomix >/dev/null 2>&1 && ! command -v npx >/dev/null 2>&1; then
    echo "Error: Neither repomix nor npx is available in the current environment." >&2
    exit 1
fi

REPOMIX_CMD="repomix"
if ! command -v repomix >/dev/null 2>&1; then
    REPOMIX_CMD="npx -y repomix"
fi

CMD=($REPOMIX_CMD "$TARGET_DIR" --compress --remove-comments --no-file-summary)

if [[ -n "$OUTPUT_FILE" ]]; then
    CMD+=(--output "$OUTPUT_FILE")
fi

if [[ -n "$BUDGET" ]]; then
    CMD+=(--token-budget "$BUDGET")
fi

if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
    CMD+=("${EXTRA_ARGS[@]}")
fi

echo "[pack_context] Packing codebase at '$TARGET_DIR' with AST compression..." >&2
exec "${CMD[@]}"
