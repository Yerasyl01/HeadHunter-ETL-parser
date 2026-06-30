class DatabaseError(Exception):
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when MongoDB connection fails."""
    pass

class RedisConnectionError(DatabaseError):
    pass
