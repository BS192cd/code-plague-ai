# Quick Start Guide

## 🚀 Option 1: Automated Setup (Recommended)

```bash
# Run the setup script (handles everything automatically)
./setup.sh        # Linux/Mac
setup.bat          # Windows
```

## 🔧 Option 2: Manual Setup

### 1. Generate JWT Secret
```bash
cd backend
python generate_jwt_secret.py
# Copy the generated JWT_SECRET
```

### 2. Create .env File
```bash
# Copy template
cp backend/.env.example backend/.env

# Edit backend/.env and replace:
# JWT_SECRET=your_generated_secret_here
# with your generated secret
```

### 3. Start Services
```bash
# With Docker (recommended)
docker-compose up -d

# Or manually
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 9000

# In another terminal
cd frontend
npm install
npm run dev
```

## 🔍 Verify Setup

1. **Backend Health**: http://localhost:9000/api/v1/health
2. **API Docs**: http://localhost:9000/docs
3. **Frontend**: http://localhost:5000

## 📋 Configuration Files

- `backend/.env` - Your environment variables
- `backend/app/core/config.py` - Configuration management
- `backend/generate_jwt_secret.py` - JWT secret generator

## 🔒 Security Checklist

- [ ] JWT_SECRET is generated and secure (32+ characters)
- [ ] .env file is not committed to Git
- [ ] MongoDB and Redis URLs are configured
- [ ] CORS origins are properly set

## 🐛 Troubleshooting

### Configuration Errors
```bash
# Check configuration validation
python -c "from app.core.config import validate_settings; validate_settings()"
```

### JWT Secret Issues
```bash
# Generate new secret
python backend/generate_jwt_secret.py
# Update backend/.env with new secret
```

### Database Connection
```bash
# Check MongoDB connection
docker-compose logs mongodb

# Check backend logs
docker-compose logs backend
```