#!/bin/bash

# Anti-Plagiarism AI - Quick Setup Script

echo "🚀 Setting up Anti-Plagiarism AI System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the anti-plagiarism-ai directory"
    exit 1
fi

print_status "Step 1: Setting up environment configuration..."

# Create backend .env if it doesn't exist
if [ ! -f "backend/.env" ]; then
    print_status "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    
    # Generate JWT secret
    if command -v python3 &> /dev/null; then
        JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
        sed -i "s/JWT_SECRET=your_generated_secret_here/JWT_SECRET=$JWT_SECRET/" backend/.env
        print_success "Generated secure JWT secret"
    else
        print_warning "Python3 not found. Please run: python backend/generate_jwt_secret.py"
    fi
else
    print_success "backend/.env already exists"
fi

print_status "Step 2: Checking Docker installation..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

print_success "Docker and Docker Compose are installed"

print_status "Step 3: Building and starting services..."

# Build and start services
docker-compose up -d --build

if [ $? -eq 0 ]; then
    print_success "All services started successfully!"
else
    print_error "Failed to start services. Check docker-compose logs for details."
    exit 1
fi

print_status "Step 4: Waiting for services to be ready..."

# Wait for services to be healthy
sleep 10

# Check service health
print_status "Checking service health..."

# Check backend health
if curl -f http://localhost:9000/api/v1/health &> /dev/null; then
    print_success "Backend is healthy (http://localhost:9000)"
else
    print_warning "Backend health check failed. It might still be starting up."
fi

# Check if frontend is accessible
if curl -f http://localhost:5000 &> /dev/null; then
    print_success "Frontend is accessible (http://localhost:5000)"
else
    print_warning "Frontend might still be starting up."
fi

print_status "Step 5: Git repository setup (optional)..."

if [ ! -d ".git" ]; then
    read -p "Initialize Git repository? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit: Anti-Plagiarism AI System

- Complete FastAPI backend with JWT authentication
- React frontend with TypeScript and Monaco Editor  
- Real-time WebSocket monitoring capabilities
- Client-side analytics and pattern detection
- Docker Compose setup with MongoDB and Redis
- Comprehensive documentation and configuration guides"
        print_success "Git repository initialized with initial commit"
        
        echo
        print_status "To connect to GitHub:"
        echo "1. Create a new repository on GitHub"
        echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/anti-plagiarism-ai.git"
        echo "3. Run: git push -u origin main"
    fi
else
    print_success "Git repository already exists"
fi

echo
print_success "🎉 Setup complete!"
echo
echo "📋 Next steps:"
echo "1. Open http://localhost:5000 - Frontend application"
echo "2. Open http://localhost:9000/docs - API documentation"
echo "3. Check logs: docker-compose logs -f"
echo "4. Stop services: docker-compose down"
echo
echo "📚 Documentation:"
echo "- README.md - Complete setup guide"
echo "- CONFIGURATION_GUIDE.md - Environment setup"
echo "- GIT_SETUP.md - Git workflow guide"
echo "- PROJECT_ACTIVITY.md - Implementation timeline"
echo
echo "🔧 Configuration:"
echo "- Edit backend/.env for custom settings"
echo "- Update docker-compose.yml for production"
echo
print_status "Happy coding! 🚀"