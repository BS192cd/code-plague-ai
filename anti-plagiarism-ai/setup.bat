@echo off
REM Anti-Plagiarism AI - Quick Setup Script for Windows

echo 🚀 Setting up Anti-Plagiarism AI System...

REM Check if we're in the right directory
if not exist "docker-compose.yml" (
    echo [ERROR] Please run this script from the anti-plagiarism-ai directory
    pause
    exit /b 1
)

echo [INFO] Step 1: Setting up environment configuration...

REM Create backend .env if it doesn't exist
if not exist "backend\.env" (
    echo [INFO] Creating backend\.env from template...
    copy "backend\.env.example" "backend\.env" >nul
    
    REM Generate JWT secret using Python
    python backend\generate_jwt_secret.py > temp_secret.txt
    for /f "tokens=2 delims==" %%i in ('findstr "JWT_SECRET=" temp_secret.txt') do set JWT_SECRET=%%i
    powershell -Command "(Get-Content 'backend\.env') -replace 'JWT_SECRET=your_generated_secret_here', 'JWT_SECRET=%JWT_SECRET%' | Set-Content 'backend\.env'"
    del temp_secret.txt
    echo [SUCCESS] Generated secure JWT secret
) else (
    echo [SUCCESS] backend\.env already exists
)

echo [INFO] Step 2: Checking Docker installation...

REM Check Docker installation
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/windows/
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are installed

echo [INFO] Step 3: Building and starting services...

REM Build and start services
docker-compose up -d --build

if errorlevel 1 (
    echo [ERROR] Failed to start services. Check docker-compose logs for details.
    pause
    exit /b 1
)

echo [SUCCESS] All services started successfully!

echo [INFO] Step 4: Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo [INFO] Step 5: Git repository setup (optional)...

if not exist ".git" (
    set /p "choice=Initialize Git repository? (y/n): "
    if /i "%choice%"=="y" (
        git init
        git add .
        git commit -m "Initial commit: Anti-Plagiarism AI System"
        echo [SUCCESS] Git repository initialized with initial commit
        echo.
        echo [INFO] To connect to GitHub:
        echo 1. Create a new repository on GitHub
        echo 2. Run: git remote add origin https://github.com/YOUR_USERNAME/anti-plagiarism-ai.git
        echo 3. Run: git push -u origin main
    )
) else (
    echo [SUCCESS] Git repository already exists
)

echo.
echo [SUCCESS] 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Open http://localhost:5000 - Frontend application
echo 2. Open http://localhost:9000/docs - API documentation
echo 3. Check logs: docker-compose logs -f
echo 4. Stop services: docker-compose down
echo.
echo 📚 Documentation:
echo - README.md - Complete setup guide
echo - CONFIGURATION_GUIDE.md - Environment setup
echo - GIT_SETUP.md - Git workflow guide
echo - PROJECT_ACTIVITY.md - Implementation timeline
echo.
echo 🔧 Configuration:
echo - Edit backend\.env for custom settings
echo - Update docker-compose.yml for production
echo.
echo [INFO] Happy coding! 🚀

pause