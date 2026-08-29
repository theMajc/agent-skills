#!/usr/bin/env bash
# skills/publish-to-trycloudflare/scripts/ensure_cloudflared.sh
# Ensures cloudflared binary is installed and executable.

set -euo pipefail

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
BIN_DIR="${WORKDIR}/.multica/bin"
LOCAL_BIN="${BIN_DIR}/cloudflared"

# 1. Check if cloudflared is already in PATH
if command -v cloudflared >/dev/null 2>&1; then
    BIN_PATH="$(command -v cloudflared)"
    if "$BIN_PATH" --version >/dev/null 2>&1; then
        echo "$BIN_PATH"
        exit 0
    fi
fi

# 2. Check if cloudflared exists in .multica/bin
if [[ -x "$LOCAL_BIN" ]]; then
    if "$LOCAL_BIN" --version >/dev/null 2>&1; then
        echo "$LOCAL_BIN"
        exit 0
    fi
fi

# 3. Download standalone static binary
echo "cloudflared not found on PATH or in ${BIN_DIR}. Downloading standalone binary..." >&2

mkdir -p "$BIN_DIR"

OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH_RAW="$(uname -m)"

case "$ARCH_RAW" in
    x86_64|amd64)
        ARCH="amd64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
    armv7l|armhf)
        ARCH="arm"
        ;;
    i386|i686)
        ARCH="386"
        ;;
    *)
        echo "ERROR: Unsupported architecture: $ARCH_RAW" >&2
        exit 1
        ;;
esac

case "$OS" in
    linux)
        DOWNLOAD_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${ARCH}"
        ;;
    darwin)
        DOWNLOAD_URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-${ARCH}"
        ;;
    *)
        echo "ERROR: Unsupported operating system: $OS" >&2
        exit 1
        ;;
esac

TEMP_BIN="${BIN_DIR}/cloudflared.tmp.$$"

echo "Downloading from ${DOWNLOAD_URL} to ${LOCAL_BIN}..." >&2
if ! curl -fsSL -o "$TEMP_BIN" "$DOWNLOAD_URL"; then
    echo "ERROR: Failed to download cloudflared from ${DOWNLOAD_URL}" >&2
    rm -f "$TEMP_BIN"
    exit 1
fi

chmod +x "$TEMP_BIN"
mv -f "$TEMP_BIN" "$LOCAL_BIN"

if ! "$LOCAL_BIN" --version >/dev/null 2>&1; then
    echo "ERROR: Downloaded cloudflared at ${LOCAL_BIN} failed execution check." >&2
    rm -f "$LOCAL_BIN"
    exit 1
fi

echo "Successfully verified cloudflared: $("$LOCAL_BIN" --version 2>&1 | head -n 1)" >&2
echo "$LOCAL_BIN"
exit 0
