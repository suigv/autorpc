#!/usr/bin/env bash
set -euo pipefail

# One-click deploy for Debian server (API + Web only)
# - No GUI runtime
# - No MCP/Skills dependencies

APP_NAME="${APP_NAME:-myt-rpa-api}"
APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
APP_HOST="${APP_HOST:-0.0.0.0}"
APP_PORT="${APP_PORT:-8000}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

if [[ "${EUID}" -eq 0 ]]; then
  SUDO=""
  RUN_USER="${RUN_USER:-root}"
else
  SUDO="sudo"
  RUN_USER="${RUN_USER:-$USER}"
fi

RUN_GROUP="${RUN_GROUP:-$(id -gn "${RUN_USER}")}"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"

echo "[1/7] Checking project layout..."
if [[ ! -f "${APP_DIR}/requirements.txt" ]]; then
  echo "ERROR: requirements.txt not found in ${APP_DIR}" >&2
  exit 1
fi
if [[ ! -f "${APP_DIR}/app/main.py" ]]; then
  echo "ERROR: app/main.py not found in ${APP_DIR}" >&2
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "ERROR: apt-get not found. This script is for Debian/Ubuntu." >&2
  exit 1
fi

echo "[2/7] Installing system packages..."
${SUDO} apt-get update
${SUDO} apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  ${PYTHON_BIN} \
  python3-venv \
  python3-pip

echo "[3/7] Creating virtual environment..."
if [[ ! -d "${APP_DIR}/${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${APP_DIR}/${VENV_DIR}"
fi

echo "[4/7] Installing Python dependencies (API/Web only)..."
"${APP_DIR}/${VENV_DIR}/bin/pip" install --upgrade pip
"${APP_DIR}/${VENV_DIR}/bin/pip" install -r "${APP_DIR}/requirements.txt"

echo "[5/7] Writing systemd service: ${SERVICE_FILE}"
${SUDO} tee "${SERVICE_FILE}" >/dev/null <<EOF
[Unit]
Description=MYT RPA FastAPI Service
After=network.target

[Service]
Type=simple
User=${RUN_USER}
Group=${RUN_GROUP}
WorkingDirectory=${APP_DIR}
Environment=MYT_ROOT_PATH=${APP_DIR}
Environment=PYTHONPATH=${APP_DIR}
ExecStart=${APP_DIR}/${VENV_DIR}/bin/python -m uvicorn app.main:app --host ${APP_HOST} --port ${APP_PORT}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "[6/7] Enabling and starting service..."
${SUDO} systemctl daemon-reload
${SUDO} systemctl enable --now "${APP_NAME}"

echo "[7/7] Health check..."
sleep 1
if curl -fsS "http://127.0.0.1:${APP_PORT}/health" >/dev/null; then
  echo "OK: service is running."
  echo "- Service: ${APP_NAME}"
  echo "- URL: http://<server-ip>:${APP_PORT}/web"
else
  echo "WARNING: health check failed. Check logs:" >&2
  echo "  ${SUDO} journalctl -u ${APP_NAME} -n 200 --no-pager" >&2
  exit 1
fi

echo "Done."
