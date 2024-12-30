#!/usr/bin/env python3
import os
from pathlib import Path

def create_project_structure():
    """Create the initial project structure"""
    base_dir = Path(__file__).parent.parent
    
    # Define project structure
    directories = [
        'app/templates',
        'app/static',
        'app/config',
        'scripts',
        'config/local',
        'config/prod',
        'tests/unit',
        'tests/integration',
        'logs'
    ]
    
    # Create directories
    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

if __name__ == "__main__":
    create_project_structure() 