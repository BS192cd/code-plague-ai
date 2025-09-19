@echo off
echo 🚀 Verifying Complete Anti-Plagiarism AI Setup...

cd /d "%~dp0"

echo [INFO] Step 1: Verifying JWT Configuration...
python test_jwt.py
if %errorlevel% neq 0 (
    echo [ERROR] JWT configuration failed!
    pause
    exit /b 1
)

echo.
echo [INFO] Step 2: Testing Backend Dependencies...
cd backend
python -c "
import sys
try:
    import fastapi, uvicorn, motor, pydantic, passlib, jose, redis, pymongo
    print('[SUCCESS] All backend dependencies available')
except ImportError as e:
    print(f'[ERROR] Missing dependency: {e}')
    sys.exit(1)
"
if %errorlevel% neq 0 (
    echo [INFO] Installing missing dependencies...
    pip install -r requirements.txt
)

cd ..

echo.
echo [INFO] Step 3: Testing Frontend Dependencies...
cd frontend
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies...
    npm install
)

echo [INFO] Testing frontend build...
npm run build >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Frontend builds successfully
) else (
    echo [WARNING] Frontend build issues - may need manual fix
)

cd ..

echo.
echo [INFO] Step 4: Testing Docker Setup...
docker --version >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Docker is available
    
    echo [INFO] Testing Docker Compose...
    docker-compose config >nul 2>&1
    if %errorlevel% == 0 (
        echo [SUCCESS] Docker Compose configuration is valid
    ) else (
        echo [WARNING] Docker Compose configuration issues
    )
) else (
    echo [WARNING] Docker not available - use local development
)

echo.
echo [INFO] Step 5: Checking File Structure...
if exist "backend\.env" (
    echo [SUCCESS] Backend .env file exists
) else (
    echo [ERROR] Backend .env file missing!
)

if exist "backend\app\main.py" (
    echo [SUCCESS] Backend main.py exists
) else (
    echo [ERROR] Backend main.py missing!
)

if exist "frontend\src\main.tsx" (
    echo [SUCCESS] Frontend main.tsx exists
) else (
    echo [ERROR] Frontend main.tsx missing!
)

echo.
echo 🎉 Setup Verification Complete!
echo.
echo 📋 Ready to Start:
echo.
echo 🐳 Docker Method (Recommended):
echo   docker-compose up -d --build
echo.
echo 💻 Local Development Method:
echo   start_local.bat
echo.
echo 🔍 Access Points:
echo   Backend API: http://localhost:9000/api/v1/health
echo   API Docs: http://localhost:9000/docs
echo   Frontend: http://localhost:5000
echo.
echo 📚 Documentation:
echo   README.md - Complete guide
echo   QUICK_START.md - Quick setup
echo   CONFIGURATION_GUIDE.md - Configuration help
echo.
pause