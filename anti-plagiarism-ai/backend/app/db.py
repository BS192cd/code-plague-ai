from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    """Create database connection with connection pooling"""
    try:
        # Get MongoDB URL from settings
        mongodb_url = settings.MONGO_URL
        database_name = settings.MONGO_DB
        
        # Create client with connection pooling
        db.client = AsyncIOMotorClient(
            mongodb_url,
            maxPoolSize=50,  # Maximum number of connections
            minPoolSize=10,  # Minimum number of connections
            maxIdleTimeMS=30000,  # Close connections after 30 seconds of inactivity
            serverSelectionTimeoutMS=5000,  # 5 second timeout for server selection
            connectTimeoutMS=10000,  # 10 second connection timeout
            socketTimeoutMS=20000,  # 20 second socket timeout
        )
        
        db.database = db.client[database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB: {database_name}")
        
        # Create indexes for performance optimization
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db.database

async def create_indexes():
    """Create comprehensive database indexes for performance optimization"""
    try:
        database = await get_database()
        
        # Users Collection Indexes
        users_indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("role", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
        ]
        await database.users.create_indexes(users_indexes)
        
        # Contests Collection Indexes
        contests_indexes = [
            IndexModel([("created_by", ASCENDING)]),
            IndexModel([("start_time", ASCENDING), ("end_time", ASCENDING)]),
            IndexModel([("participants", ASCENDING)]),  # Multikey index
            IndexModel([("status", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("title", TEXT), ("description", TEXT)]),  # Text search
        ]
        await database.contests.create_indexes(contests_indexes)
        
        # Sessions Collection Indexes (Critical for performance)
        sessions_indexes = [
            IndexModel([("session_id", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING), ("contest_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("created_at", DESCENDING)]),
            IndexModel([("contest_id", ASCENDING), ("created_at", DESCENDING)]),
            IndexModel([("status", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("language", ASCENDING)]),
            # Compound index for common queries
            IndexModel([("user_id", ASCENDING), ("contest_id", ASCENDING), ("status", ASCENDING)]),
        ]
        await database.sessions.create_indexes(sessions_indexes)
        
        # Analytics Collection Indexes
        analytics_indexes = [
            IndexModel([("session_id", ASCENDING), ("analysis_type", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("processed_at", DESCENDING)]),
            IndexModel([("contest_id", ASCENDING), ("processed_at", DESCENDING)]),
            IndexModel([("processed_at", DESCENDING)]),
            # TTL index for data retention (30 days)
            IndexModel([("processed_at", ASCENDING)], expireAfterSeconds=2592000),
        ]
        await database.analytics.create_indexes(analytics_indexes)
        
        # Events Collection Indexes (for real-time processing)
        events_indexes = [
            IndexModel([("session_id", ASCENDING), ("timestamp", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("timestamp", DESCENDING)]),
            IndexModel([("event_type", ASCENDING)]),
            IndexModel([("processed", ASCENDING)]),  # For batch processing
            # TTL index for raw events (7 days)
            IndexModel([("created_at", ASCENDING)], expireAfterSeconds=604800),
        ]
        await database.events.create_indexes(events_indexes)
        
        # WebSocket Connections Collection (for active session tracking)
        connections_indexes = [
            IndexModel([("session_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("connected_at", DESCENDING)]),
            # TTL index for connection cleanup (1 hour)
            IndexModel([("last_ping", ASCENDING)], expireAfterSeconds=3600),
        ]
        await database.ws_connections.create_indexes(connections_indexes)
        
        logger.info("Successfully created all database indexes")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")
        raise

# Collection getters for easy access
async def get_users_collection():
    database = await get_database()
    return database.users

async def get_contests_collection():
    database = await get_database()
    return database.contests

async def get_sessions_collection():
    database = await get_database()
    return database.sessions

async def get_analytics_collection():
    database = await get_database()
    return database.analytics

async def get_events_collection():
    database = await get_database()
    return database.events

async def get_ws_connections_collection():
    database = await get_database()
    return database.ws_connections

# Health check for database
async def check_database_health():
    """Check database connection health"""
    try:
        await db.client.admin.command('ping')
        return {"status": "healthy", "message": "Database connection is active"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"Database connection failed: {str(e)}"}

# Database statistics
async def get_database_stats():
    """Get database statistics for monitoring"""
    try:
        database = await get_database()
        stats = await database.command("dbStats")
        
        # Get collection counts
        collections_stats = {}
        for collection_name in ["users", "contests", "sessions", "analytics", "events"]:
            count = await database[collection_name].count_documents({})
            collections_stats[collection_name] = count
        
        return {
            "database_size": stats.get("dataSize", 0),
            "storage_size": stats.get("storageSize", 0),
            "index_size": stats.get("indexSize", 0),
            "collections": collections_stats,
            "indexes": stats.get("indexes", 0)
        }
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {"error": str(e)}