from fastapi import APIRouter, HTTPException, status, Depends, Request
from datetime import datetime
import logging
from bson import ObjectId

from app.schemas import (
    UserCreate, UserLogin, UserResponse, Token, APIResponse, ErrorResponse
)
from app.auth import (
    get_password_hash, authenticate_user, create_user_token, 
    is_strong_password, sanitize_username, rate_limiter,
    get_current_active_user
)
from app.db import get_users_collection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, request: Request):
    """Register a new user"""
    try:
        # Rate limiting
        client_ip = request.client.host
        if rate_limiter.is_rate_limited(f"register_{client_ip}", max_attempts=3, window_minutes=60):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many registration attempts. Please try again later."
            )
        
        # Validate password strength
        is_valid, password_errors = is_strong_password(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password validation failed: {', '.join(password_errors)}"
            )
        
        # Sanitize username
        username = sanitize_username(user_data.username)
        
        # Check if user already exists
        users_collection = await get_users_collection()
        existing_user = await users_collection.find_one({
            "username": username,
            "role": user_data.role.value
        })
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with username '{username}' and role '{user_data.role.value}' already exists"
            )
        
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Create user document
        user_doc = {
            "_id": str(ObjectId()),
            "username": username,
            "password_hashed": password_hash,
            "role": user_data.role.value,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert user
        result = await users_collection.insert_one(user_doc)
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Create and return token
        token_response = create_user_token(user_doc)
        
        logger.info(f"User registered successfully: {username} ({user_data.role.value})")
        return token_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

@router.post("/login", response_model=Token)
async def login_user(login_data: UserLogin, request: Request):
    """Authenticate user and return access token"""
    try:
        # Rate limiting
        client_ip = request.client.host
        username = sanitize_username(login_data.username)
        
        if rate_limiter.is_rate_limited(f"login_{client_ip}", max_attempts=5, window_minutes=15):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please try again later."
            )
        
        if rate_limiter.is_rate_limited(f"login_user_{username}", max_attempts=3, window_minutes=15):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts for this user. Please try again later."
            )
        
        # Authenticate user
        user = await authenticate_user(username, login_data.password, login_data.role)
        
        if not user:
            # Log failed attempt
            logger.warning(f"Failed login attempt: {username} ({login_data.role.value}) from {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username, password, or role"
            )
        
        # Create and return token
        token_response = create_user_token(user)
        
        logger.info(f"User logged in successfully: {username} ({login_data.role.value})")
        return token_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """Get current user information"""
    try:
        return UserResponse(
            id=str(current_user["_id"]),
            username=current_user["username"],
            role=current_user["role"],
            created_at=current_user["created_at"],
            updated_at=current_user["updated_at"]
        )
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: dict = Depends(get_current_active_user)):
    """Refresh access token"""
    try:
        # Create new token
        token_response = create_user_token(current_user)
        
        logger.info(f"Token refreshed for user: {current_user['username']}")
        return token_response
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token"
        )

@router.post("/logout")
async def logout_user(current_user: dict = Depends(get_current_active_user)):
    """Logout user (client should discard token)"""
    try:
        # In a more sophisticated setup, you might want to blacklist the token
        # For now, we just log the logout event
        logger.info(f"User logged out: {current_user['username']}")
        
        return APIResponse(
            success=True,
            message="Successfully logged out"
        )
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout"
        )

