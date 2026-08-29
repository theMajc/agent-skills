#!/usr/bin/env bash
# skills/publish-to-trycloudflare/scripts/publish_stop.sh
# Gracefully stops a TryCloudflare tunnel and verifies process/socket release.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    cat <<'EOF' >&2
Usage:
  publish_stop.sh <port | service-name>

Examples:
  publish_stop.sh 3000
  publish_stop.sh preview-3000
EOF
    exit 1
}

if [[ $# -eq 0 ]]; then
    usage
fi

TARGET="$1"
if [[ "$TARGET" =~ ^[0-9]+$ ]]; then
    SERVICE_NAME="preview-${TARGET}"
    PORT="$TARGET"
elif [[ "$TARGET" =~ ^preview-[0-9]+$ ]]; then
    SERVICE_NAME="$TARGET"
    PORT="${TARGET#preview-}"
else
    SERVICE_NAME="$TARGET"
    PORT=""
fi

find_workdir() {
    local dir="${1:-$(pwd)}"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.multica" || -d "$dir/.git" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "$(pwd)"
}

WORKDIR="$(find_workdir)"
RUNTIME_DIR="${WORKDIR}/.multica/runtime"
PID_FILE="${RUNTIME_DIR}/pids/${SERVICE_NAME}.pid"

# Locate stop_service.sh from persistent-service-supervisor
find_supervisor_script() {
    local target="$1"
    local dir="$(pwd)"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "${dir}/.agents/skills/persistent-service-supervisor/scripts/${target}" ]]; then
            echo "${dir}/.agents/skills/persistent-service-supervisor/scripts/${target}"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

STOP_SERVICE="$(find_supervisor_script stop_service.sh || true)"
if [[ -z "$STOP_SERVICE" ]]; then
    CANDIDATE_SUPERVISORS=(
        "${WORKDIR}/.agents/skills/persistent-service-supervisor/scripts/stop_service.sh"
        "${SCRIPT_DIR}/../../../persistent-service-supervisor/scripts/stop_service.sh"
        "${SCRIPT_DIR}/../../persistent-service-supervisor/scripts/stop_service.sh"
    )
    for candidate in "${CANDIDATE_SUPERVISORS[@]}"; do
        if [[ -f "$candidate" ]]; then
            STOP_SERVICE="$candidate"
            break
        fi
    done
fi

echo "==> Stopping preview tunnel service '${SERVICE_NAME}'..." >&2

if [[ -n "$STOP_SERVICE" ]]; then
    bash "$STOP_SERVICE" --name "$SERVICE_NAME" --workdir "$WORKDIR" >&2
else
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE" 2>/dev/null || true)
        if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
            echo "==> Sending SIGTERM to PID ${PID}..." >&2
            kill -TERM "$PID" 2>/dev/null || true
            for _ in {1..10}; do
                if ! kill -0 "$PID" 2>/dev/null; then
                    break
                fi
                sleep 0.5
            done
            if kill -0 "$PID" 2>/dev/null; then
                echo "==> Escalating to SIGKILL for PID ${PID}..." >&2
                kill -9 "$PID" 2>/dev/null || true
            fi
        fi
        rm -f "$PID_FILE"
    fi
fi

# Verify process is terminated
if [[ -f "$PID_FILE" ]]; then
    ACTIVE_PID=$(cat "$PID_FILE" 2>/dev/null || true)
    if [[ -n "$ACTIVE_PID" ]] && kill -0 "$ACTIVE_PID" 2>/dev/null; then
        echo "ERROR: Process ${ACTIVE_PID} is still active for ${SERVICE_NAME}." >&2
        exit 1
    fi
    rm -f "$PID_FILE"
fi

echo "==> Tunnel service '${SERVICE_NAME}' has been successfully stopped." >&2

# Output structured JSON
python3 -c "
import json
print(json.dumps({
    'service': '${SERVICE_NAME}',
    'status': 'stopped'
}))
"
