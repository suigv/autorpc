#!/usr/bin/env bash
set -euo pipefail

# Update deployed web-api-only code on server.

APP_DIR="${APP_DIR:-/root/demo_py_x64}"
APP_BRANCH="${APP_BRANCH:-web-api-only}"
SERVICE_NAME="${SERVICE_NAME:-myt-rpa-api}"
PIP_BIN="${PIP_BIN:-${APP_DIR}/.venv/bin/pip}"

if [[ ! -d "${APP_DIR}" ]]; then
  echo "ERROR: APP_DIR not found: ${APP_DIR}" >&2
  exit 1
fi

echo "[1/6] Entering app directory..."
cd "${APP_DIR}"

echo "[2/6] Syncing git branch (${APP_BRANCH})..."
git fetch origin
git checkout "${APP_BRANCH}"
git pull --ff-only origin "${APP_BRANCH}"

echo "[3/6] Installing Python dependencies..."
if [[ ! -x "${PIP_BIN}" ]]; then
  echo "ERROR: pip not found: ${PIP_BIN}" >&2
  exit 1
fi
"${PIP_BIN}" install -r requirements.txt

echo "[4/6] Restarting service (${SERVICE_NAME})..."
systemctl restart "${SERVICE_NAME}"

echo "[5/6] Checking service status..."
systemctl status "${SERVICE_NAME}" --no-pager -l

echo "[6/6] Health check..."
curl -fsS http://127.0.0.1:8000/health

echo "Update done."
