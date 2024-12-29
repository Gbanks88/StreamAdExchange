class DevelopmentConfig:
    # Basic Flask Configuration
    SECRET_KEY = 'dev-secret-key'
    DEBUG = True
    TESTING = False
    
    # Rate Limiting
    RATELIMIT_DEFAULT = ["200 per day", "50 per hour"] 