from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.core.config import settings
from app.schemas import TokenData, UserRole
from app.db import get_users_collection

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings from config
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Security scheme
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Hash a password"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to hash password"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    try:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token"
        )

def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        role: str = payload.get("role")
        
        if username is None or user_id is None:
            raise credentials_exception
            
        token_data = TokenData(
            username=username,
            user_id=user_id,
            role=UserRole(role) if role else None
        )
        return token_data
        
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise credentials_exception

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        token_data = verify_token(token)
        
        # Get user from database
        users_collection = await get_users_collection()
        user = await users_collection.find_one({"_id": token_data.user_id})
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Get current active user (can be extended for user status checks)"""
    # Add any additional user status checks here
    return current_user

def require_role(required_role: UserRole):
    """Decorator to require specific user role"""
    def role_checker(current_user: dict = Depends(get_current_active_user)):
        if current_user.get("role") != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role.value}"
            )
        return current_user
    return role_checker

# Role-specific dependencies
async def get_current_host(current_user: dict = Depends(require_role(UserRole.HOST))):
    """Get current user if they are a host"""
    return current_user

async def get_current_student(current_user: dict = Depends(require_role(UserRole.STUDENT))):
    """Get current user if they are a student"""
    return current_user

async def authenticate_user(username: str, password: str, role: UserRole) -> Optional[dict]:
    """Authenticate a user with username, password, and role"""
    try:
        users_collection = await get_users_collection()
        user = await users_collection.find_one({
            "username": username,
            "role": role.value
        })
        
        if not user:
            logger.warning(f"Authentication failed: User {username} with role {role.value} not found")
            return None
        
        if not verify_password(password, user["password_hashed"]):
            logger.warning(f"Authentication failed: Invalid password for user {username}")
            return None
        
        logger.info(f"User {username} authenticated successfully")
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

def create_user_token(user: dict) -> dict:
    """Create a complete token response for a user"""
    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user["username"],
                "user_id": str(user["_id"]),
                "role": user["role"]
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "role": user["role"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"]
            }
        }
    except Exception as e:
        logger.error(f"Token creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user token"
        )

# WebSocket authentication
async def authenticate_websocket_token(token: str) -> Optional[dict]:
    """Authenticate WebSocket connection with JWT token"""
    try:
        token_data = verify_token(token)
        
        users_collection = await get_users_collection()
        user = await users_collection.find_one({"_id": token_data.user_id})
        
        if user is None:
            logger.warning(f"WebSocket authentication failed: User {token_data.user_id} not found")
            return None
        
        return user
        
    except Exception as e:
        logger.warning(f"WebSocket authentication error: {e}")
        return None

# Security utilities
def is_strong_password(password: str) -> tuple[bool, list[str]]:
    """Check if password meets security requirements"""
    errors = []
    
    if len(password) < 6:
        errors.append("Password must be at least 6 characters long")
    
    if len(password) > 100:
        errors.append("Password must be less than 100 characters")
    
    # Add more password strength checks as needed
    # if not any(c.isupper() for c in password):
    #     errors.append("Password must contain at least one uppercase letter")
    
    # if not any(c.islower() for c in password):
    #     errors.append("Password must contain at least one lowercase letter")
    
    # if not any(c.isdigit() for c in password):
    #     errors.append("Password must contain at least one digit")
    
    return len(errors) == 0, errors

def sanitize_username(username: str) -> str:
    """Sanitize username input"""
    # Remove leading/trailing whitespace and convert to lowercase
    return username.strip().lower()

# Rate limiting helpers (can be extended with Redis)
class RateLimiter:
    def __init__(self):
        self.attempts = {}
    
    def is_rate_limited(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Simple in-memory rate limiting (should use Redis in production)"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        # Clean old attempts
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier] 
            if attempt > window_start
        ]
        
        # Check if rate limited
        if len(self.attempts[identifier]) >= max_attempts:
            return True
        
        # Add current attempt
        self.attempts[identifier].append(now)
        return False

# Global rate limiter instance
rate_limiter = RateLimiter()