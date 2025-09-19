from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import configuration
from app.core.config import settings, validate_settings

# Import database connection
from app.db import connect_to_mongo, close_mongo_connection

# Import routes
from app.routes import auth_routes
# from app.routes import contest_routes, event_routes

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Anti-Plagiarism AI Backend...")
    
    # Validate configuration
    try:
        validate_settings()
        logger.info("Configuration validation passed")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    
    # Connect to database
    await connect_to_mongo()
    logger.info("Database connection established")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Anti-Plagiarism AI Backend...")
    await close_mongo_connection()
    logger.info("Database connection closed")

app = FastAPI(
    title="Anti-Plagiarism AI Backend",
    version="1.0.0",
    description="Real-time coding session monitoring and plagiarism detection system",
    lifespan=lifespan
)

# CORS setup - use configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "ok", 
        "message": "Anti-Plagiarism AI Backend running on port 9000",
        "version": "1.0.0",
        "features": [
            "Real-time WebSocket monitoring",
            "Client-side analytics integration", 
            "Enhanced error handling",
            "API versioning",
            "Database indexing optimization"
        ]
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Anti-Plagiarism AI Backend API v1.0.0"}

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1")
# app.include_router(contest_routes.router, prefix="/api/v1")
# app.include_router(event_routes.router, prefix="/api/v1")