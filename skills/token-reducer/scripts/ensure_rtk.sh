#!/usr/bin/env bash
# ==============================================================================
# ensure_rtk.sh - Auto-installer for RTK (Rust Token Killer) binary
#
# Checks if RTK is installed on PATH or in standard user bin directories.
# If missing, automatically downloads and installs the official static musl
# binary from GitHub Releases to make compaction 100% transparent.
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_BIN_DIR="$SCRIPT_DIR/../bin"
INSTALL_TARGET="/home/max/.gemini/antigravity-cli/bin/rtk"

if command -v rtk >/dev/null 2>&1; then
    exit 0
fi

if [[ -x "$INSTALL_TARGET" ]]; then
    exit 0
fi

if [[ -x "$SKILL_BIN_DIR/rtk" ]]; then
    exit 0
fi

# Detect architecture
ARCH="$(uname -m)"
case "$ARCH" in
    x86_64)
        ASSET="rtk-x86_64-unknown-linux-musl.tar.gz"
        ;;
    aarch64|arm64)
        ASSET="rtk-aarch64-unknown-linux-gnu.tar.gz"
        ;;
    *)
        echo "[ensure_rtk] Unsupported architecture: $ARCH" >&2
        exit 1
        ;;
esac

mkdir -p "$SKILL_BIN_DIR"
TARGET_DIR="/home/max/.gemini/antigravity-cli/bin"
if [[ ! -w "$TARGET_DIR" ]]; then
    TARGET_DIR="$SKILL_BIN_DIR"
fi

RTK_VERSION="v0.46.0"
DOWNLOAD_URL="https://github.com/rtk-ai/rtk/releases/download/${RTK_VERSION}/${ASSET}"

echo "[ensure_rtk] Downloading RTK ${RTK_VERSION} (${ARCH}) to ${TARGET_DIR}..." >&2
curl -sL "$DOWNLOAD_URL" | tar -xz -C "$TARGET_DIR"
chmod +x "$TARGET_DIR/rtk"

if [[ "$TARGET_DIR" != "$SKILL_BIN_DIR" ]]; then
    cp -f "$TARGET_DIR/rtk" "$SKILL_BIN_DIR/rtk" 2>/dev/null || true
fi

echo "[ensure_rtk] RTK installed successfully at $TARGET_DIR/rtk." >&2
