class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change this to a secure secret key
    # Add other configuration settings here

class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings

class DevelopmentConfig(Config):
    DEBUG = True
    # Add development-specific settings 