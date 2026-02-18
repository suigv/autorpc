#!/bin/bash
# 启动 MYT RPA API 服务

cd "$(dirname "$0")"

echo "Starting MYT RPA API..."
echo "Install dependencies: pip3 install --break-system-packages -r requirements.txt"
echo ""

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
