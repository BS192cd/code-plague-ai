@echo off
echo 🚀 Deploying Anti-Plagiarism AI System...

cd /d "%~dp0"

echo [INFO] Step 1: Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running or installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not available!
    pause
    exit /b 1
)

echo [SUCCESS] Docker is ready

echo [INFO] Step 2: Cleaning previous deployment...
docker-compose down --volumes --remove-orphans >nul 2>&1
echo [SUCCESS] Cleaned previous containers

echo [INFO] Step 3: Checking required files...
if not exist "docker-compose.yml" (
    echo [ERROR] docker-compose.yml not found!
    pause
    exit /b 1
)

if not exist "backend\.env" (
    echo [ERROR] backend\.env not found!
    echo Creating from template...
    copy "backend\.env.example" "backend\.env"
)

if not exist "backend\Dockerfile" (
    echo [ERROR] backend\Dockerfile not found!
    pause
    exit /b 1
)

if not exist "frontend\Dockerfile.dev" (
    echo [ERROR] frontend\Dockerfile.dev not found!
    pause
    exit /b 1
)

echo [SUCCESS] All required files present

echo [INFO] Step 4: Building and starting services...
echo This may take a few minutes on first run...

docker-compose up -d --build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services!
    echo Checking logs...
    docker-compose logs
    pause
    exit /b 1
)

echo [SUCCESS] Services started successfully!

echo [INFO] Step 5: Waiting for services to be ready...
timeout /t 30 /nobreak >nul

echo [INFO] Step 6: Checking service health...

echo Checking MongoDB...
docker-compose exec -T mongodb mongosh --eval "db.runCommand('ping')" >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] MongoDB is healthy
) else (
    echo [WARNING] MongoDB may still be starting...
)

echo Checking Redis...
docker-compose exec -T redis redis-cli ping >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Redis is healthy
) else (
    echo [WARNING] Redis may still be starting...
)

echo Checking Backend...
curl -f http://localhost:9000/api/v1/health >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Backend is healthy
) else (
    echo [WARNING] Backend may still be starting...
)

echo Checking Frontend...
curl -f http://localhost:5000 >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Frontend is accessible
) else (
    echo [WARNING] Frontend may still be starting...
)

echo.
echo 🎉 Deployment Complete!
echo.
echo 📋 Service Status:
docker-compose ps

echo.
echo 🔗 Access Points:
echo   Frontend:     http://localhost:5000
echo   Backend API:  http://localhost:9000/docs
echo   Health Check: http://localhost:9000/api/v1/health
echo.
echo 📊 Useful Commands:
echo   View logs:    docker-compose logs -f
echo   Stop services: docker-compose down
echo   Restart:      docker-compose restart
echo.
echo 🐛 If services aren't responding:
echo   1. Wait 1-2 minutes for full startup
echo   2. Check logs: docker-compose logs [service-name]
echo   3. Restart: docker-compose restart [service-name]
echo.
pause