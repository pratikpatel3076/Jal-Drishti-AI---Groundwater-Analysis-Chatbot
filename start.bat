@echo off
echo ========================================
echo   Jal Drishti AI - Groundwater Chatbot
echo ========================================
echo.

echo [1/3] Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo FAILED: npm install
    pause
    exit /b 1
)
echo.

echo [2/3] Installing Python dependencies...
pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo FAILED: pip install
    pause
    exit /b 1
)
echo.

echo [3/3] Starting servers...
echo   Frontend: http://localhost:8080
echo   Backend:  http://localhost:5000
echo.
call npm run dev
pause
