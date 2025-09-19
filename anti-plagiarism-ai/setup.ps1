# Anti-Plagiarism AI - PowerShell Setup Script

Write-Host "🚀 Setting up Anti-Plagiarism AI System..." -ForegroundColor Blue

# Check if we're in the right directory
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "[ERROR] Please run this script from the anti-plagiarism-ai directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[INFO] Step 1: Setting up environment configuration..." -ForegroundColor Cyan

# Create backend .env if it doesn't exist
if (-not (Test-Path "backend\.env")) {
    Write-Host "[INFO] Creating backend\.env from template..." -ForegroundColor Cyan
    Copy-Item "backend\.env.example" "backend\.env"
    
    # Generate JWT secret using Python
    try {
        $secret = python -c "import secrets; print(secrets.token_urlsafe(32))"
        if ($secret) {
            (Get-Content "backend\.env") -replace "JWT_SECRET=your_generated_secret_here", "JWT_SECRET=$secret" | Set-Content "backend\.env"
            Write-Host "[SUCCESS] Generated secure JWT secret" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "[WARNING] Python not found. Please manually set JWT_SECRET in backend\.env" -ForegroundColor Yellow
        Write-Host "Run: python backend\generate_jwt_secret.py" -ForegroundColor Yellow
    }
} else {
    Write-Host "[SUCCESS] backend\.env already exists" -ForegroundColor Green
}

Write-Host "[INFO] Step 2: Checking Docker installation..." -ForegroundColor Cyan

# Check Docker installation
try {
    docker --version | Out-Null
    Write-Host "[SUCCESS] Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Visit: https://docs.docker.com/desktop/windows/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    docker-compose --version | Out-Null
    Write-Host "[SUCCESS] Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker Compose is not installed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[INFO] Step 3: Building and starting services..." -ForegroundColor Cyan

# Build and start services
try {
    docker-compose up -d --build
    Write-Host "[SUCCESS] All services started successfully!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to start services. Check docker-compose logs for details." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[INFO] Step 4: Waiting for services to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Write-Host "[INFO] Step 5: Git repository setup (optional)..." -ForegroundColor Cyan

if (-not (Test-Path ".git")) {
    $choice = Read-Host "Initialize Git repository? (y/n)"
    if ($choice -eq "y" -or $choice -eq "Y") {
        git init
        git add .
        git commit -m "Initial commit: Anti-Plagiarism AI System"
        Write-Host "[SUCCESS] Git repository initialized with initial commit" -ForegroundColor Green
        Write-Host ""
        Write-Host "[INFO] To connect to GitHub:" -ForegroundColor Cyan
        Write-Host "1. Create a new repository on GitHub" -ForegroundColor White
        Write-Host "2. Run: git remote add origin https://github.com/YOUR_USERNAME/anti-plagiarism-ai.git" -ForegroundColor White
        Write-Host "3. Run: git push -u origin main" -ForegroundColor White
    }
} else {
    Write-Host "[SUCCESS] Git repository already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:5000 - Frontend application" -ForegroundColor White
Write-Host "2. Open http://localhost:9000/docs - API documentation" -ForegroundColor White
Write-Host "3. Check logs: docker-compose logs -f" -ForegroundColor White
Write-Host "4. Stop services: docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "- README.md - Complete setup guide" -ForegroundColor White
Write-Host "- CONFIGURATION_GUIDE.md - Environment setup" -ForegroundColor White
Write-Host "- GIT_SETUP.md - Git workflow guide" -ForegroundColor White
Write-Host "- PROJECT_ACTIVITY.md - Implementation timeline" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Configuration:" -ForegroundColor Cyan
Write-Host "- Edit backend\.env for custom settings" -ForegroundColor White
Write-Host "- Update docker-compose.yml for production" -ForegroundColor White
Write-Host ""
Write-Host "[INFO] Happy coding! 🚀" -ForegroundColor Blue

Read-Host "Press Enter to exit"