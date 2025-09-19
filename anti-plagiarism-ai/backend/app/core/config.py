from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Security
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    MONGO_URL: str
    MONGO_DB: str
    
    # Redis
    REDIS_URL: str
    
    # Application Configuration
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 1000
    
    # Analytics Configuration
    ANALYTICS_BATCH_SIZE: int = 100
    ANALYTICS_PROCESSING_INTERVAL: int = 60
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Validation function
def validate_settings():
    """Validate critical settings on startup"""
    errors = []
    
    if not settings.JWT_SECRET or settings.JWT_SECRET == "your_generated_secret_here":
        errors.append("JWT_SECRET must be set to a secure random value")
    
    if len(settings.JWT_SECRET) < 32:
        errors.append("JWT_SECRET should be at least 32 characters long")
    
    if not settings.MONGO_URL:
        errors.append("MONGO_URL must be configured")
    
    if not settings.MONGO_DB:
        errors.append("MONGO_DB must be configured")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True

# Helper functions
def get_database_url() -> str:
    """Get the complete MongoDB URL"""
    return settings.MONGO_URL

def get_redis_url() -> str:
    """Get the Redis URL"""
    return settings.REDIS_URL

def is_development() -> bool:
    """Check if running in development mode"""
    return settings.DEBUG

def get_cors_origins() -> list:
    """Get allowed CORS origins"""
    return settings.ALLOWED_ORIGINS