#!/usr/bin/env python3
import os
from pathlib import Path
import json

def create_project_structure():
    """Create the initial project structure"""
    base_dir = Path(__file__).parent.parent
    
    # Define project structure
    directories = [
        'app/templates',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/config',
        'scripts',
        'config/local',
        'config/prod',
        'tests/unit',
        'tests/integration',
        'logs',
        'data/cortex'
    ]
    
    # Create directories
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    # Create requirements.txt if it doesn't exist
    requirements_path = base_dir / "requirements.txt"
    if not requirements_path.exists():
        with open(requirements_path, 'w') as f:
            f.write("""# Core dependencies
requests>=2.28.0
PyYAML>=6.0
prometheus_client>=0.16.0

# Web framework
Flask>=2.0.0
Werkzeug>=2.0.0

# Database
SQLAlchemy>=1.4.0

# Security
python-dotenv>=0.19.0
cryptography>=3.4.0

# Monitoring
psutil>=5.8.0
""")
        print("Created requirements.txt")

    # Create .env file
    env_path = base_dir / ".env"
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write("""STREAMAD_ENV=local
SECRET_KEY=dev-secret-key
DEBUG=True
DATABASE_URL=sqlite:///dev.db
""")
        print("Created .env file")

    # Create example configuration
    example_config = {
        "peers": {
            "default": {
                "ip": "127.0.0.1",
                "asn": "AS12345",
                "capacity": "1G",
                "enabled": True
            }
        }
    }
    
    config_path = base_dir / "config/local/config.json"
    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=4)
    print("Created example configuration")

if __name__ == "__main__":
    create_project_structure() 