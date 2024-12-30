from flask import Flask
from app.extensions import cache, limiter

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.update(
        SECRET_KEY='your-secret-key-here',  # Change this to a secure key
        CACHE_TYPE='SimpleCache',  # Changed from 'simple' to 'SimpleCache'
        CACHE_DEFAULT_TIMEOUT=300,
        RATELIMIT_STORAGE_URL="memory://",  # Explicitly set rate limiter storage
    )
    
    # Initialize extensions
    cache.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
