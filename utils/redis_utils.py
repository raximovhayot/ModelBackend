import os
from redis import Redis

def get_redis_connection():
    """
    Initialize and return a Redis connection using environment variables
    
    Returns:
        Redis: A Redis connection object
    """
    # Initialize Redis connection
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    # Get Redis password from environment variable if available
    redis_password = os.environ.get('REDIS_PASSWORD', 'root123')
    if redis_password and 'redis://:' not in redis_url:
        # Insert password into URL if not already present
        parts = redis_url.split('://')
        if len(parts) == 2:
            redis_url = f"{parts[0]}://:{redis_password}@{parts[1]}"

    return Redis.from_url(redis_url)