@echo off
echo 🔍 Testing Anti-Plagiarism AI Setup...

echo [INFO] Step 1: Testing Backend Configuration...
cd backend
python -c "
try:
    from app.core.config import settings, validate_settings
    validate_settings()
    print('[SUCCESS] Backend configuration is valid')
except Exception as e:
    print(f'[ERROR] Backend configuration failed: {e}')
"

echo [INFO] Step 2: Testing Backend Import...
python -c "
try:
    from app.main import app
    print('[SUCCESS] Backend imports successfully')
except Exception as e:
    print(f'[ERROR] Backend import failed: {e}')
"

cd ..

echo [INFO] Step 3: Testing Frontend Dependencies...
cd frontend
if exist "node_modules" (
    echo [SUCCESS] Frontend dependencies installed
) else (
    echo [INFO] Installing frontend dependencies...
    npm install
)

echo [INFO] Step 4: Testing Frontend Build...
npm run build >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Frontend builds successfully
) else (
    echo [ERROR] Frontend build failed
)

cd ..

echo [INFO] Step 5: Testing Docker...
docker --version >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Docker is available
) else (
    echo [ERROR] Docker is not available
)

echo.
echo 📋 Test Complete!
echo.
echo 🚀 To start the system:
echo 1. docker-compose up -d --build
echo 2. Or use: start_local.bat
echo.
pause