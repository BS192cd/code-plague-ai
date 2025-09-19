# Configuration Guide

## 🔑 Required Configuration (YOUR CREDENTIALS)

### 1. Backend Environment Variables (.env)

Create `backend/.env` file with YOUR settings:

```bash
# Database Configuration (YOUR MongoDB)
# Option 1: Local MongoDB
MONGODB_URL=mongodb://localhost:27017/anti_plagiarism_ai

# Option 2: MongoDB Atlas (Cloud) - GET YOUR OWN
# MONGODB_URL=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/anti_plagiarism_ai?retryWrites=true&w=majority

# JWT Configuration (CHANGE THESE!)
JWT_SECRET=YOUR_SUPER_SECRET_JWT_KEY_MINIMUM_32_CHARACTERS_LONG
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Redis Configuration (YOUR Redis instance)
# Option 1: Local Redis
REDIS_URL=redis://localhost:6379

# Option 2: Redis Cloud - GET YOUR OWN
# REDIS_URL=redis://YOUR_USERNAME:YOUR_PASSWORD@YOUR_REDIS_HOST:YOUR_PORT

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# WebSocket Configuration
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=1000

# Analytics Configuration
ANALYTICS_BATCH_SIZE=100
ANALYTICS_PROCESSING_INTERVAL=60
```

### 2. How to Get Your Own Credentials

#### MongoDB Atlas (Free Tier Available)
1. Go to https://www.mongodb.com/atlas
2. Sign up for free account
3. Create a new cluster (free M0 tier)
4. Create database user with username/password
5. Whitelist your IP address (or 0.0.0.0/0 for development)
6. Get connection string from "Connect" button
7. Replace placeholders with your credentials

#### Redis Cloud (Free Tier Available)
1. Go to https://redis.com/try-free/
2. Sign up for free account
3. Create new database (30MB free)
4. Get connection details from dashboard
5. Use the provided connection string

#### Local Setup (No External Services)
If you prefer local development:
```bash
# Install MongoDB locally
# Windows: Download from https://www.mongodb.com/try/download/community
# macOS: brew install mongodb-community
# Linux: Follow MongoDB installation guide

# Install Redis locally
# Windows: Download from https://redis.io/download
# macOS: brew install redis
# Linux: sudo apt-get install redis-server

# Use local URLs in .env:
MONGODB_URL=mongodb://localhost:27017/anti_plagiarism_ai
REDIS_URL=redis://localhost:6379
```

### 3. Security Notes

⚠️ **IMPORTANT SECURITY REQUIREMENTS:**

1. **JWT_SECRET**: Must be at least 32 characters long and completely random
   ```bash
   # Generate secure JWT secret (run in terminal):
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Never commit .env files** to Git (already in .gitignore)

3. **Change default passwords** in docker-compose.yml for production

4. **Use strong MongoDB credentials** for production

### 4. Docker Compose Credentials

Update `docker-compose.yml` with YOUR credentials:

```yaml
mongodb:
  environment:
    MONGO_INITDB_ROOT_USERNAME: YOUR_MONGO_USERNAME
    MONGO_INITDB_ROOT_PASSWORD: YOUR_STRONG_PASSWORD
    MONGO_INITDB_DATABASE: anti_plagiarism_ai

redis:
  command: redis-server --appendonly yes --requirepass YOUR_REDIS_PASSWORD

backend:
  environment:
    - MONGODB_URL=mongodb://YOUR_MONGO_USERNAME:YOUR_STRONG_PASSWORD@mongodb:27017/anti_plagiarism_ai?authSource=admin
    - REDIS_URL=redis://:YOUR_REDIS_PASSWORD@redis:6379
    - JWT_SECRET=YOUR_GENERATED_JWT_SECRET
```

## 🔒 Production Security Checklist

- [ ] Change all default passwords
- [ ] Use strong, unique JWT secret
- [ ] Enable MongoDB authentication
- [ ] Enable Redis authentication
- [ ] Use HTTPS in production
- [ ] Restrict CORS origins
- [ ] Set up proper firewall rules
- [ ] Enable database encryption at rest
- [ ] Set up monitoring and logging
- [ ] Regular security updates

## 🚀 Quick Setup Commands

```bash
# 1. Copy environment template
cp backend/.env.example backend/.env

# 2. Generate JWT secret
python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))" >> backend/.env

# 3. Edit .env file with your database URLs
nano backend/.env  # or use your preferred editor

# 4. Start services
docker-compose up -d
```