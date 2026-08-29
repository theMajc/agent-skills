#!/usr/bin/env bash
# skills/publish-to-trycloudflare/scripts/publish_status.sh
# Lists active TryCloudflare preview tunnels, their ports, PIDs, and public URLs.

set -euo pipefail

OUTPUT_JSON=false
for arg in "$@"; do
    case "$arg" in
        --output)
            ;;
        json)
            OUTPUT_JSON=true
            ;;
        --output=json)
            OUTPUT_JSON=true
            ;;
        -h|--help)
            cat <<'EOF'
Usage:
  publish_status.sh [--output json]

Options:
  --output json   Emit results in structured JSON format
  -h, --help      Show this help message
EOF
            exit 0
            ;;
    esac
done

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
PIDS_DIR="${RUNTIME_DIR}/pids"
LOGS_DIR="${RUNTIME_DIR}/logs"

python3 - <<PYEOF
import os, sys, glob, json, re

pids_dir = "${PIDS_DIR}"
logs_dir = "${LOGS_DIR}"
output_json = "${OUTPUT_JSON}".lower() == "true"

results = []

if os.path.isdir(pids_dir):
    for pid_file in glob.glob(os.path.join(pids_dir, "preview-*.pid")):
        filename = os.path.basename(pid_file)
        service_name = filename[:-4] # strip .pid
        port_match = re.search(r'preview-(\d+)', service_name)
        port = int(port_match.group(1)) if port_match else None
        
        try:
            with open(pid_file, 'r', encoding='utf-8') as f:
                pid = int(f.read().strip())
        except Exception:
            continue
        
        # Check liveness
        is_running = False
        try:
            os.kill(pid, 0)
            is_running = True
        except OSError:
            is_running = False
        
        url = None
        if is_running:
            # Scrape url from err or out log
            for ext in [".err.log", ".out.log"]:
                log_path = os.path.join(logs_dir, service_name + ext)
                if os.path.isfile(log_path):
                    try:
                        with open(log_path, 'r', encoding='utf-8', errors='replace') as lf:
                            content = lf.read()
                            urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', content)
                            if urls:
                                url = urls[-1]
                                break
                    except Exception:
                        pass

        if is_running:
            results.append({
                "service": service_name,
                "port": port,
                "pid": pid,
                "url": url,
                "status": "running"
            })

if output_json:
    print(json.dumps(results, indent=2))
else:
    if not results:
        print("No active TryCloudflare preview tunnels found.")
    else:
        print(f"{'SERVICE':<16} {'PORT':<8} {'PID':<8} {'STATUS':<10} {'URL'}")
        print("-" * 80)
        for r in results:
            url_str = r.get("url") or "establishing..."
            print(f"{r['service']:<16} {str(r.get('port')):<8} {str(r['pid']):<8} {r['status']:<10} {url_str}")
PYEOF
