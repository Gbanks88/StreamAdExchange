import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # AWS Configuration
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-west-2')
    AWS_INSTANCE_ID = os.environ.get('AWS_INSTANCE_ID')
    
    # Server Configuration
    PRIMARY_SERVER_HOST = os.environ.get('PRIMARY_SERVER_HOST', 'localhost')
    PRIMARY_SERVER_PORT = int(os.environ.get('PRIMARY_SERVER_PORT', 80))
    HEALTH_CHECK_ENDPOINT = os.environ.get('HEALTH_CHECK_ENDPOINT', '/health')
    
    # Monitoring Configuration
    FAILURE_THRESHOLD = int(os.environ.get('FAILURE_THRESHOLD', 3))
    CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 30))
    
    # Notification Configuration
    SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
    ALERT_EMAIL = os.environ.get('ALERT_EMAIL')
    
    # Backup Server Configuration
    BACKUP_SERVER_HOST = os.environ.get('BACKUP_SERVER_HOST')
    BACKUP_SERVER_PORT = int(os.environ.get('BACKUP_SERVER_PORT', 80))
