"""Development configuration"""

DEBUG = True
TESTING = False
DATABASE_URI = "sqlite:///dev.db"
SECRET_KEY = "dev-secret-key"  # Change in production

# BALT-IX Settings
BALT_IX_CONFIG = {
    "local_asn": "AS12345",
    "peers_file": "config/local/peers.json",
    "monitoring_interval": 60
}

# Cortex Settings
CORTEX_CONFIG = {
    "window_size": 300,
    "batch_size": 100,
    "storage_path": "data/cortex"
} 