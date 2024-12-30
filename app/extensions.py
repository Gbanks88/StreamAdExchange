from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

# Initialize extensions
cache = Cache()

try:
    redis_client = redis.Redis.from_url("redis://localhost:6379/0")
    redis_client.ping()  # Test connection
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri="redis://localhost:6379/0",
        strategy="fixed-window"
    )
except redis.ConnectionError:
    print("Warning: Redis connection failed, falling back to memory storage")
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri="memory://",
        strategy="fixed-window"
    )

def init_extensions(app):
    cache.init_app(app)
    limiter.init_app(app) 