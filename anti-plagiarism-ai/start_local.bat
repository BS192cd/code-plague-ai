@echo off
echo 🚀 Starting Anti-Plagiarism AI (Local Development)

echo [INFO] Step 1: Starting Backend...
cd backend

echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

echo [INFO] Starting FastAPI server...
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 9000"

cd ..

echo [INFO] Step 2: Starting Frontend...
cd frontend

echo [INFO] Installing Node dependencies...
npm install

echo [INFO] Starting Vite dev server...
start "Frontend Server" cmd /k "npm run dev"

cd ..

echo [SUCCESS] Services starting...
echo.
echo 📋 Access Points:
echo - Backend API: http://localhost:9000
echo - API Docs: http://localhost:9000/docs
echo - Frontend: http://localhost:5000
echo.
echo Press any key to exit...
pause >nul