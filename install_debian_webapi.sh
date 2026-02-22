#!/usr/bin/env bash
set -euo pipefail

# Bootstrap installer for Debian/Ubuntu servers.
# Purpose: clone web-api-only branch, then run deploy_debian.sh.

REPO_URL="${REPO_URL:-https://github.com/suigv/autorpc.git}"
BRANCH="${BRANCH:-web-api-only}"
TARGET_DIR="${TARGET_DIR:-demo_py_x64}"

if ! command -v apt-get >/dev/null 2>&1; then
  echo "ERROR: apt-get not found. This installer only supports Debian/Ubuntu." >&2
  exit 1
fi

if [[ "${EUID}" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

echo "[1/4] Installing bootstrap dependencies..."
${SUDO} apt-get update
${SUDO} apt-get install -y --no-install-recommends ca-certificates curl git

if [[ -e "${TARGET_DIR}" ]]; then
  if [[ -d "${TARGET_DIR}" ]] && [[ -z "$(ls -A "${TARGET_DIR}")" ]]; then
    :
  else
    echo "ERROR: target path already exists and is not empty: ${TARGET_DIR}" >&2
    echo "Tip: set TARGET_DIR to another directory, or remove the current one." >&2
    exit 1
  fi
fi

echo "[2/4] Cloning repository (${BRANCH})..."
git clone --depth 1 -b "${BRANCH}" "${REPO_URL}" "${TARGET_DIR}"

echo "[3/4] Preparing deploy script..."
chmod +x "${TARGET_DIR}/deploy_debian.sh"

echo "[4/4] Running one-click deployment..."
exec bash "${TARGET_DIR}/deploy_debian.sh"
