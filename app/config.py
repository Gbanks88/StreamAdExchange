import secrets

class Config:
    SECRET_KEY = secrets.token_hex(32)
    CSRF_ENABLED = True
    
    # Database configuration (if using a database)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///affiliate_tracking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security headers
    SECURITY_HEADERS = {
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https:;",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    }
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://" 