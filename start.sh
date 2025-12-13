#!/bin/bash
echo "========================================"
echo "  Jal Drishti AI - Groundwater Chatbot"
echo "========================================"
echo ""
echo "Installing dependencies..."
npm install
echo ""
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..
echo ""
echo "Starting servers..."
echo "Frontend: http://localhost:8080"
echo "Backend:  http://localhost:5000"
echo ""
npm run dev