from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize extensions with simpler configuration
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    strategy="fixed-window"
)

def init_extensions(app):
    cache.init_app(app)
    limiter.init_app(app) 