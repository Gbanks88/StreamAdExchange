#!/usr/bin/env python3

from setup_monitoring import MonitoringSetup
import subprocess
import time
import requests

def start_grafana():
    setup = MonitoringSetup()
    
    print("Starting Grafana...")
    try:
        # Stop any existing instance
        setup.stop_service('grafana')
        time.sleep(2)
        
        # Start Grafana
        if setup.start_service('grafana'):
            print("Waiting for Grafana to start...")
            time.sleep(5)  # Give it time to start
            
            # Check if Grafana is responding
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    response = requests.get('http://localhost:3000')
                    if response.status_code == 200:
                        print("✓ Grafana started successfully")
                        print("Access Grafana at: http://localhost:3000")
                        print("Default credentials: admin/admin")
                        return True
                except requests.RequestException:
                    if attempt < max_attempts - 1:
                        print(f"Waiting... (attempt {attempt + 1}/{max_attempts})")
                        time.sleep(3)
                    else:
                        print("✗ Failed to connect to Grafana")
                        
            # Check logs if startup failed
            print("\nChecking Grafana logs:")
            subprocess.run(['tail', '-n', '20', '/usr/local/var/log/grafana/grafana.log'])
            
        else:
            print("✗ Failed to start Grafana service")
            
    except Exception as e:
        print(f"Error starting Grafana: {e}")
        return False

if __name__ == "__main__":
    start_grafana() 