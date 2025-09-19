# Anti-Plagiarism AI System

A comprehensive real-time coding session monitoring and plagiarism detection system built with FastAPI, React, and MongoDB.

## 🚀 Features

### ✅ **Real-time Monitoring**
- WebSocket-based real-time session monitoring
- Comprehensive event capture (keystrokes, paste, focus, scroll, selections)
- Automatic reconnection with exponential backoff
- Offline mode with local event queuing

### ✅ **Client-side Analytics**
- Typing pattern analysis (speed, rhythm, pauses)
- Real-time anomaly detection
- Event compression and optimization
- Performance metrics collection

### ✅ **Enhanced Security**
- JWT-based authentication with role-based access control
- Password hashing with bcrypt
- Rate limiting for API endpoints
- CORS protection

### ✅ **Performance Optimization**
- Database indexing for large-scale data
- Connection pooling for MongoDB
- Redis caching layer
- Event batching and compression

### ✅ **Professional UI/UX**
- Modern React interface with Radix UI components
- Monaco Editor integration
- Real-time connection status indicators
- Responsive design with Tailwind CSS

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │    MongoDB      │
│   (Port 5000)   │◄──►│   (Port 9000)   │◄──►│   (Port 27017)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  Redis Cache    │◄─────────────┘
                        │  (Port 6379)    │
                        └─────────────────┘
```

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended)
- **Node.js 18+** (for local development)
- **Python 3.11+** (for local development)
- **MongoDB 7.0+** (for local development)
- **Redis 7.2+** (for caching)

## 🚀 Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd anti-plagiarism-ai
```

### 2. Environment Setup
```bash
# Copy environment file
cp backend/.env.example backend/.env

# Update the .env file with your settings
# At minimum, change the JWT_SECRET for production
```

### 3. Start All Services
```bash
# Start all services (MongoDB, Redis, Backend, Frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Access the Application
- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:9000
- **API Documentation**: http://localhost:9000/docs
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

## 🛠️ Local Development Setup

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your MongoDB and Redis URLs
```

5. **Start the backend server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

The frontend will be available at http://localhost:5000

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

### Contest Endpoints (Coming Soon)
- `POST /api/v1/contests` - Create contest
- `GET /api/v1/contests` - List contests
- `POST /api/v1/contests/{id}/join` - Join contest

### Session Monitoring Endpoints (Coming Soon)
- `POST /api/v1/events` - Submit session events
- `GET /api/v1/sessions/{id}` - Get session data
- `WebSocket /api/v1/ws/{session_id}` - Real-time monitoring

### Health Check
- `GET /api/v1/health` - System health status

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=anti_plagiarism_ai

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Redis
REDIS_URL=redis://localhost:6379

# Application
DEBUG=True
LOG_LEVEL=INFO
```

#### Frontend (vite.config.ts)
```typescript
server: {
  port: 5000,
  host: true
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Start all services first
docker-compose up -d

# Run integration tests
npm run test:integration
```

## 📊 Monitoring & Analytics

### Database Indexes
The system automatically creates optimized indexes for:
- User lookups by username and role
- Contest queries by creator and time
- Session queries by user, contest, and status
- Analytics queries with TTL for data retention

### Performance Metrics
- Real-time typing speed (WPM)
- Event capture rate
- WebSocket connection status
- Database query performance

### Anomaly Detection
- Unusual typing patterns
- Excessive copy/paste operations
- Frequent focus changes
- Extended absence periods

## 🔒 Security Features

### Authentication
- JWT tokens with configurable expiration
- Role-based access control (Host/Student)
- Password strength validation
- Rate limiting on auth endpoints

### Data Protection
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- Request timeout handling

### Session Security
- Unique session IDs (UUID)
- WebSocket authentication
- Event data validation
- Audit trail logging

## 🚀 Deployment

### Production Docker Setup
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Considerations
- Change JWT_SECRET in production
- Use strong MongoDB credentials
- Enable Redis authentication
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Configure log aggregation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

#### "Cannot find module 'react'" Error
```bash
cd frontend
npm install --save-dev @types/react @types/react-dom
```

#### MongoDB Connection Failed
```bash
# Check if MongoDB is running
docker-compose ps mongodb

# View MongoDB logs
docker-compose logs mongodb
```

#### WebSocket Connection Issues
- Ensure backend is running on port 9000
- Check CORS configuration
- Verify JWT token is valid

#### Frontend Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Getting Help
- Check the [Issues](https://github.com/your-repo/issues) page
- Review the API documentation at http://localhost:9000/docs
- Check Docker logs: `docker-compose logs -f`

## 🎯 Roadmap

- [ ] Advanced AI-based plagiarism detection
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Mobile application support
- [ ] Integration with popular IDEs
- [ ] Machine learning model training
- [ ] Advanced reporting system
- [ ] Multi-language support

---

**Built with ❤️ using FastAPI, React, MongoDB, and modern web technologies.**