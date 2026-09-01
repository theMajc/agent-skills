#!/usr/bin/env bash
set -euo pipefail

# Directory resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BIN_DIR="${SKILL_ROOT}/bin"
TYPST_BIN="${BIN_DIR}/typst"
TYPST_VERSION="v0.15.1"

if command -v typst >/dev/null 2>&1; then
    echo "Using system Typst: $(command -v typst)"
    typst --version
    exit 0
fi

if [[ -x "${TYPST_BIN}" ]]; then
    echo "Using cached Typst: ${TYPST_BIN}"
    "${TYPST_BIN}" --version
    exit 0
fi

mkdir -p "${BIN_DIR}"

ARCH="$(uname -m)"
case "${ARCH}" in
    x86_64)
        TARGET="x86_64-unknown-linux-musl"
        ;;
    aarch64|arm64)
        TARGET="aarch64-unknown-linux-musl"
        ;;
    *)
        echo "Unsupported architecture: ${ARCH}" >&2
        exit 1
        ;;
esac

TARBALL_URL="https://github.com/typst/typst/releases/download/${TYPST_VERSION}/typst-${TARGET}.tar.xz"
echo "Fetching standalone static Typst binary from ${TARBALL_URL}..."

curl -L -s "${TARBALL_URL}" | tar -xJ -C "${BIN_DIR}" --strip-components=1

if [[ -x "${TYPST_BIN}" ]]; then
    echo "Typst successfully bootstrapped at ${TYPST_BIN}:"
    "${TYPST_BIN}" --version
else
    echo "Failed to install Typst binary." >&2
    exit 1
fi
