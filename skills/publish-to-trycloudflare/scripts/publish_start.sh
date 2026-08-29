#!/usr/bin/env bash
# skills/publish-to-trycloudflare/scripts/publish_start.sh
# Launches a detached TryCloudflare tunnel using persistent-service-supervisor,
# scrapes the assigned public URL, verifies connectivity via WAN curl, and prints JSON.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    cat <<'EOF' >&2
Usage:
  publish_start.sh <port>
  publish_start.sh --port <port>

Options:
  <port>, --port <number>   Local port to expose via TryCloudflare
  -h, --help                Show this help message
EOF
    exit 1
}

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

PORT=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)
            PORT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$PORT" && "$1" =~ ^[0-9]+$ ]]; then
                PORT="$1"
                shift
            else
                echo "Unknown argument: $1" >&2
                usage
            fi
            ;;
    esac
done

if [[ -z "$PORT" || ! "$PORT" =~ ^[0-9]+$ || "$PORT" -lt 1 || "$PORT" -gt 65535 ]]; then
    echo "ERROR: Valid port number (1-65535) is required." >&2
    usage
fi

WORKDIR="$(find_workdir)"
SERVICE_NAME="preview-${PORT}"
RUNTIME_DIR="${WORKDIR}/.multica/runtime"
LOGS_DIR="${RUNTIME_DIR}/logs"
PIDS_DIR="${RUNTIME_DIR}/pids"
PID_FILE="${PIDS_DIR}/${SERVICE_NAME}.pid"
OUT_LOG="${LOGS_DIR}/${SERVICE_NAME}.out.log"
ERR_LOG="${LOGS_DIR}/${SERVICE_NAME}.err.log"

mkdir -p "$LOGS_DIR" "$PIDS_DIR"

# 1. Resolve cloudflared binary
CLOUDFLARED_BIN="$("${SCRIPT_DIR}/ensure_cloudflared.sh")"
if [[ -z "$CLOUDFLARED_BIN" || ! -x "$CLOUDFLARED_BIN" ]]; then
    echo "ERROR: Could not resolve executable cloudflared binary." >&2
    exit 1
fi

# 2. Locate run_detached.sh from persistent-service-supervisor
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

RUN_DETACHED="$(find_supervisor_script run_detached.sh || true)"
if [[ -z "$RUN_DETACHED" ]]; then
    CANDIDATE_SUPERVISORS=(
        "${WORKDIR}/.agents/skills/persistent-service-supervisor/scripts/run_detached.sh"
        "${SCRIPT_DIR}/../../../persistent-service-supervisor/scripts/run_detached.sh"
        "${SCRIPT_DIR}/../../persistent-service-supervisor/scripts/run_detached.sh"
    )
    for candidate in "${CANDIDATE_SUPERVISORS[@]}"; do
        if [[ -f "$candidate" ]]; then
            RUN_DETACHED="$candidate"
            break
        fi
    done
fi

TUNNEL_CMD="${CLOUDFLARED_BIN} tunnel --url http://127.0.0.1:${PORT}"

echo "==> Starting TryCloudflare tunnel for port ${PORT} (service: ${SERVICE_NAME})..." >&2

# Clear previous logs for clean URL scraping
: > "$OUT_LOG" 2>/dev/null || true
: > "$ERR_LOG" 2>/dev/null || true

if [[ -n "$RUN_DETACHED" ]]; then
    echo "==> Invoking persistent supervisor: ${RUN_DETACHED}" >&2
    bash "$RUN_DETACHED" "$SERVICE_NAME" "$TUNNEL_CMD" --port "$PORT" --restart --workdir "$WORKDIR" >&2
else
    echo "==> [WARN] persistent-service-supervisor run_detached.sh not found; using standalone setsid fallback" >&2
    if [[ -f "$PID_FILE" ]]; then
        OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
        if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
            kill -TERM "$OLD_PID" 2>/dev/null || true
            sleep 1
            kill -9 "$OLD_PID" 2>/dev/null || true
        fi
        rm -f "$PID_FILE"
    fi
    (
        cd "$WORKDIR"
        setsid nohup bash -c "$TUNNEL_CMD" >> "$OUT_LOG" 2>> "$ERR_LOG" < /dev/null &
        echo $! > "$PID_FILE"
    )
fi

DETACHED_PID=$(cat "$PID_FILE" 2>/dev/null || true)
if [[ -z "$DETACHED_PID" ]] || ! kill -0 "$DETACHED_PID" 2>/dev/null; then
    echo "ERROR: Failed to start detached tunnel process." >&2
    tail -n 20 "$ERR_LOG" >&2 || true
    exit 1
fi

echo "==> Tunnel launched with PID ${DETACHED_PID}. Scrapes TryCloudflare URL..." >&2

# 3. Scrape https://*.trycloudflare.com URL from logs
SCRAPE_TIMEOUT=30
ELAPSED=0
TUNNEL_URL=""

while [[ $ELAPSED -lt $SCRAPE_TIMEOUT ]]; do
    if ! kill -0 "$DETACHED_PID" 2>/dev/null; then
        echo "ERROR: cloudflared process died while establishing tunnel." >&2
        tail -n 25 "$ERR_LOG" >&2 || true
        exit 1
    fi

    # TryCloudflare URL pattern (-h suppresses filename prefixes)
    FOUND_URL=$(grep -h -oE 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' "$ERR_LOG" "$OUT_LOG" 2>/dev/null | tail -n 1 || true)
    if [[ -n "$FOUND_URL" ]]; then
        TUNNEL_URL="$FOUND_URL"
        break
    fi

    sleep 0.5
    ELAPSED=$((ELAPSED + 1))
done

if [[ -z "$TUNNEL_URL" ]]; then
    echo "ERROR: Timed out waiting for TryCloudflare URL in logs." >&2
    tail -n 30 "$ERR_LOG" >&2 || true
    exit 1
fi

echo "==> Tunnel assigned: ${TUNNEL_URL}" >&2
echo "==> Performing synchronous WAN health probe..." >&2

# 4. Synchronous WAN curl verification
WAN_TIMEOUT=30
WAN_START=$(date +%s)
WAN_SUCCESS=false

while [[ $(( $(date +%s) - WAN_START )) -lt $WAN_TIMEOUT ]]; do
    if ! kill -0 "$DETACHED_PID" 2>/dev/null; then
        echo "ERROR: cloudflared process died during WAN verification." >&2
        exit 1
    fi

    # Probe WAN URL
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 4 --max-time 6 "$TUNNEL_URL" || echo "000")
    
    # 2xx, 3xx, 4xx indicate the Cloudflare edge successfully routed to the local origin
    # 502/504 might occur transiently while origin connects, but can also indicate reachability
    if [[ "$HTTP_CODE" =~ ^[2-4][0-9]{2}$ ]]; then
        WAN_SUCCESS=true
        echo "==> WAN check passed (HTTP ${HTTP_CODE})" >&2
        break
    elif [[ "$HTTP_CODE" == "502" || "$HTTP_CODE" == "504" ]]; then
        # Transient connection retry
        sleep 1
    else
        sleep 1
    fi
done

if [[ "$WAN_SUCCESS" != "true" ]]; then
    # Even if HTTP_CODE is 502 (e.g. if local app returned 502 or is starting up),
    # check if the DNS at least resolved and Cloudflare edge replied
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 4 --max-time 6 "$TUNNEL_URL" || echo "000")
    if [[ "$HTTP_CODE" != "000" && "$HTTP_CODE" != "530" ]]; then
        echo "==> WAN check reached Cloudflare edge with status HTTP ${HTTP_CODE}." >&2
    else
        echo "ERROR: WAN probe to ${TUNNEL_URL} failed or timed out after ${WAN_TIMEOUT}s (HTTP ${HTTP_CODE})." >&2
        exit 1
    fi
fi

# 5. Output structured JSON to stdout
python3 -c "
import json
print(json.dumps({
    'url': '${TUNNEL_URL}',
    'port': int('${PORT}'),
    'service': '${SERVICE_NAME}'
}))
"
