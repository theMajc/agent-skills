#!/usr/bin/env bash
# ==============================================================================
# compact_run.sh - Unified Terminal Compactor Orchestrator for Multica Agents
#
# Precedence Hierarchy:
#   1. rtk (Rust Token Killer) - fastest (<3ms), domain-aware parsing, auto-tee
#   2. tokenjuice - Node-based sliding-window stream wrapper
#   3. compact_fallback.py - Pure Python zero-dependency in-tree fallback
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Strip leading '--' if passed
if [[ "$1" == "--" ]]; then
    shift
fi

if [[ $# -eq 0 ]]; then
    echo "Usage: compact_run.sh [--] <command> [args...]" >&2
    exit 1
fi

PRIMARY_CMD="$1"

# ------------------------------------------------------------------------------
# Strategy 1: Delegate to RTK (Rust Token Killer)
# ------------------------------------------------------------------------------
if command -v rtk >/dev/null 2>&1; then
    RTK_BIN="$(command -v rtk)"
elif [[ -x "$SCRIPT_DIR/../bin/rtk" ]]; then
    RTK_BIN="$SCRIPT_DIR/../bin/rtk"
elif [[ -x "/home/max/.gemini/antigravity-cli/bin/rtk" ]]; then
    RTK_BIN="/home/max/.gemini/antigravity-cli/bin/rtk"
else
    RTK_BIN=""
fi

if [[ -n "$RTK_BIN" ]]; then
    case "$PRIMARY_CMD" in
        git|vitest|jest|pytest|npm|pnpm|cargo|tsc|diff|log|tree|ls|deps|env|find|summary)
            exec "$RTK_BIN" "$@"
            ;;
        *)
            # Format command safely for subshell invocation
            CMD_ESCAPED="$(printf "%q " "$@")"
            if [[ "$PRIMARY_CMD" =~ (test|check|lint|build|node|python) ]]; then
                exec "$RTK_BIN" err "$CMD_ESCAPED"
            else
                exec "$RTK_BIN" run -c "$CMD_ESCAPED"
            fi
            ;;
    esac
fi

# ------------------------------------------------------------------------------
# Strategy 2: Delegate to TokenJuice
# ------------------------------------------------------------------------------
if command -v tokenjuice >/dev/null 2>&1; then
    exec tokenjuice wrap -- "$@"
fi

# ------------------------------------------------------------------------------
# Strategy 3: Zero-dependency Python Fallback
# ------------------------------------------------------------------------------
FALLBACK_PY="$SCRIPT_DIR/compact_fallback.py"
if [[ -f "$FALLBACK_PY" ]] && command -v python3 >/dev/null 2>&1; then
    exec python3 "$FALLBACK_PY" -- "$@"
fi

# ------------------------------------------------------------------------------
# Absolute Fallback: Raw execution if no compactor runtime exists
# ------------------------------------------------------------------------------
exec "$@"
