import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache configuration
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    RATELIMIT_STORAGE_OPTIONS = {
        'connection_pool': True
    }
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "200 per day"
    
    # Trading Hub Configuration
    TRADING_HUBS = {
        'forex': {
            'api_key': os.environ.get('FOREX_API_KEY'),
            'endpoint': os.environ.get('FOREX_ENDPOINT')
        },
        'crypto': {
            'api_key': os.environ.get('CRYPTO_API_KEY'),
            'endpoint': os.environ.get('CRYPTO_ENDPOINT')
        },
        'stocks': {
            'api_key': os.environ.get('STOCKS_API_KEY'),
            'endpoint': os.environ.get('STOCKS_ENDPOINT')
        }
    }
    
    # API Configuration
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', 100)
    API_TIMEOUT = os.environ.get('API_TIMEOUT', 30)
    
    # Application configuration
    ADMINS = ['admin@streamadexchange.com']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    BACKGROUND_SETTINGS = {
        'OVERLAY_OPACITY_TOP': 0.92,
        'OVERLAY_OPACITY_BOTTOM': 0.88,
        'BACKGROUND_BLUR': '5px',
        'BACKGROUND_SCALE': 1.05
    }
    
    # SERVER_NAME = 'notcheapnot2expensive.com'
    # PREFERRED_URL_SCHEME = 'https'

class DevelopmentConfig(Config):
    DEBUG = True
    RATELIMIT_STORAGE_URL = "memory://"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Override Redis settings for development
    RATELIMIT_STORAGE_URL = "memory://"
    CACHE_TYPE = "SimpleCache"

class ProductionConfig(Config):
    DEBUG = False
    # Use Redis configuration from parent class
    CACHE_TYPE = "RedisCache"
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0') 