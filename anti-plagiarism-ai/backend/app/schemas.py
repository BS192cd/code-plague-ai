from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid

# API Versioning
class APIVersion(str, Enum):
    V1 = "v1"

# User Schemas
class UserRole(str, Enum):
    HOST = "host"
    STUDENT = "student"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    username: str
    password: str
    role: UserRole

class UserResponse(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    password_hashed: str
    created_at: datetime
    updated_at: datetime

# Contest Schemas
class ContestStatus(str, Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ContestBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=1000)
    start_time: datetime
    end_time: datetime
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class ContestCreate(ContestBase):
    language: str = Field(default="javascript")
    max_participants: Optional[int] = Field(default=None, ge=1)

class ContestResponse(ContestBase):
    id: str = Field(alias="_id")
    created_by: str
    participants: List[str] = []
    status: ContestStatus
    language: str
    max_participants: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

class ContestJoin(BaseModel):
    contest_id: str

# Session Event Schemas
class EventType(str, Enum):
    KEYPRESS = "keypress"
    PASTE = "paste"
    FOCUS = "focus"
    BLUR = "blur"
    SAVE = "save"
    SELECTION = "selection"
    SCROLL = "scroll"
    COPY = "copy"
    CUT = "cut"
    UNDO = "undo"
    REDO = "redo"

class SessionEventData(BaseModel):
    content: Optional[str] = None
    position: Optional[Dict[str, Any]] = None
    selection: Optional[Dict[str, Any]] = None
    changes: Optional[List[Dict[str, Any]]] = None
    length: Optional[int] = None
    cursor_position: Optional[int] = None
    scroll_top: Optional[int] = None
    scroll_left: Optional[int] = None

class SessionEvent(BaseModel):
    t: int = Field(..., description="Timestamp in milliseconds")
    type: EventType
    data: Optional[SessionEventData] = None
    analysis: Optional[Dict[str, Any]] = None  # Client-side analytics

class SessionEventBatch(BaseModel):
    session_id: str
    user_id: str
    contest_id: Optional[str] = None
    language: str = "javascript"
    events: List[SessionEvent]
    client_analytics: Optional[Dict[str, Any]] = None

# Enhanced Session Schemas
class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FLAGGED = "flagged"
    SUSPENDED = "suspended"

class SessionAnalytics(BaseModel):
    typing_speed: float = 0.0
    pause_patterns: List[float] = []
    copy_paste_frequency: int = 0
    focus_changes: int = 0
    anomaly_flags: List[str] = []
    total_events: int = 0
    session_duration: int = 0  # in seconds

class SessionMetadata(BaseModel):
    browser: Optional[str] = None
    screen_resolution: Optional[str] = None
    timezone: Optional[str] = None
    ip_address: Optional[str] = None

class SessionCreate(BaseModel):
    contest_id: Optional[str] = None
    language: str = "javascript"

class SessionResponse(BaseModel):
    id: str = Field(alias="_id")
    session_id: str
    user_id: str
    contest_id: Optional[str]
    language: str
    events: List[SessionEvent] = []
    analytics: Optional[SessionAnalytics] = None
    metadata: Optional[SessionMetadata] = None
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

# Analytics Schemas
class AnalysisType(str, Enum):
    TYPING_PATTERN = "typing_pattern"
    ANOMALY_DETECTION = "anomaly_detection"
    SIMILARITY_ANALYSIS = "similarity_analysis"
    PLAGIARISM_DETECTION = "plagiarism_detection"

class AnalysisResults(BaseModel):
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    flags: List[str] = []
    patterns: Dict[str, Any] = {}
    recommendations: List[str] = []
    risk_level: str = Field(default="low")  # low, medium, high, critical

class AnalyticsCreate(BaseModel):
    session_id: str
    analysis_type: AnalysisType
    results: AnalysisResults

class AnalyticsResponse(BaseModel):
    id: str = Field(alias="_id")
    session_id: str
    user_id: str
    contest_id: Optional[str]
    analysis_type: AnalysisType
    results: AnalysisResults
    processed_at: datetime
    version: str = "1.0.0"
    
    class Config:
        populate_by_name = True

# WebSocket Schemas
class WSMessageType(str, Enum):
    EVENT = "event"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    ACKNOWLEDGMENT = "acknowledgment"
    ANALYTICS = "analytics"
    STATUS = "status"

class WSMessage(BaseModel):
    type: WSMessageType
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[int] = None
    session_id: Optional[str] = None
    event_id: Optional[str] = None

class WSConnectionInfo(BaseModel):
    session_id: str
    user_id: str
    contest_id: Optional[str]
    connected_at: datetime
    last_ping: datetime
    status: str = "active"

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[UserRole] = None

# API Response Schemas
class APIResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int = 1
    size: int = 10
    pages: int

class HealthCheck(BaseModel):
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    services: Optional[Dict[str, str]] = None

# Error Schemas
class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

# Feature Extraction Placeholder Schemas (for future AI integration)
class FeatureExtractionRequest(BaseModel):
    session_id: str
    analysis_types: List[AnalysisType] = [AnalysisType.TYPING_PATTERN]

class FeatureExtractionResponse(BaseModel):
    session_id: str
    features: Dict[str, Any]
    analysis_results: List[AnalyticsResponse]
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Database Models (for internal use)
class UserInDatabase(UserInDB):
    pass

class ContestInDatabase(ContestResponse):
    pass

class SessionInDatabase(SessionResponse):
    pass

class AnalyticsInDatabase(AnalyticsResponse):
    pass