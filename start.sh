#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo "  Jal Drishti AI - Groundwater Chatbot"
echo "========================================"
echo ""

echo "[1/3] Installing Node.js dependencies..."
npm install

echo "[2/3] Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "[3/3] Starting servers..."
echo "  Frontend: http://localhost:8080"
echo "  Backend:  http://localhost:5000"
echo ""
npm run dev
