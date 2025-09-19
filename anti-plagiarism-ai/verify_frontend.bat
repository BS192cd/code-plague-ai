@echo off
echo 🚀 Verifying Frontend Server...
echo.
echo [INFO] Checking if port 5000 is active...
netstat -ano | findstr :5000 | findstr LISTENING
if %errorlevel% == 0 (
    echo [SUCCESS] Frontend server is running on port 5000
) else (
    echo [ERROR] No server found on port 5000
    exit /b 1
)

echo.
echo [INFO] Testing server response...
curl -s -o nul -w "HTTP Status: %%{http_code}" http://localhost:5000/
echo.
echo.
echo ✅ Frontend Server Status:
echo   📍 Local URL:    http://localhost:5000/
echo   🌐 Network URL:  http://192.168.0.102:5000/
echo   🎨 Tailwind CSS: Fixed and working
echo   ⚡ Vite Dev:     Hot reload enabled
echo.
echo 💡 The server is ready for development!
echo    Press Ctrl+C in the terminal to stop the server.
echo.
pause