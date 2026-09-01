#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8080}"
DIR="${2:-./dist}"

if [[ ! -d "${DIR}" ]]; then
    echo "Directory ${DIR} does not exist. Please generate artifacts first." >&2
    exit 1
fi

echo "Starting local HTTP artifact preview server on port ${PORT}..."
echo "Serving files from: $(cd "${DIR}" && pwd)"
echo "To expose publicly via zero-trust tunnel, run:"
echo "  multica skill run publish-to-trycloudflare --port ${PORT}"
echo "--------------------------------------------------------"

exec python3 -m http.server "${PORT}" --directory "${DIR}"
