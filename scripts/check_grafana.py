#!/usr/bin/env python3

import subprocess
import requests
import os
from pathlib import Path
import json

class GrafanaChecker:
    def __init__(self):
        self.grafana_paths = {
            'binary': '/usr/local/bin/grafana',
            'config': '/usr/local/etc/grafana/grafana.ini',
            'logs': '/usr/local/var/log/grafana',
            'data': '/usr/local/var/lib/grafana',
            'brew_plist': '/usr/local/opt/grafana/homebrew.mxcl.grafana.plist'
        }

    def check_installation(self):
        """Check if Grafana is installed and print status"""
        print("\n=== Grafana Installation Check ===")
        
        # Check Homebrew installation
        try:
            result = subprocess.run(['brew', 'list', 'grafana'], 
                                 capture_output=True, 
                                 text=True)
            if result.returncode == 0:
                print("✓ Grafana is installed via Homebrew")
                
                # Get version
                version_result = subprocess.run(['grafana-server', '-v'], 
                                             capture_output=True, 
                                             text=True)
                print(f"✓ Version: {version_result.stdout.strip()}")
            else:
                print("✗ Grafana is not installed via Homebrew")
                return False
        except Exception as e:
            print(f"✗ Error checking Homebrew installation: {e}")
            return False

        # Check paths
        print("\nChecking Grafana paths:")
        for name, path in self.grafana_paths.items():
            if Path(path).exists():
                print(f"✓ {name}: {path} (exists)")
            else:
                print(f"✗ {name}: {path} (missing)")

        # Check service status
        try:
            service_result = subprocess.run(['brew', 'services', 'list'], 
                                         capture_output=True, 
                                         text=True)
            for line in service_result.stdout.splitlines():
                if 'grafana' in line:
                    status = 'running' if 'started' in line.lower() else 'stopped'
                    print(f"\nService Status: {status}")
                    break
        except Exception as e:
            print(f"✗ Error checking service status: {e}")

        # Check if Grafana is responding
        try:
            response = requests.get('http://localhost:3000')
            if response.status_code == 200:
                print("✓ Grafana is responding on http://localhost:3000")
            else:
                print(f"✗ Grafana returned status code: {response.status_code}")
        except requests.RequestException:
            print("✗ Grafana is not responding on http://localhost:3000")

        # Check logs
        log_path = Path('/usr/local/var/log/grafana/grafana.log')
        if log_path.exists():
            print("\nRecent log entries:")
            try:
                subprocess.run(['tail', '-n', '5', str(log_path)])
            except Exception as e:
                print(f"✗ Error reading logs: {e}")

        return True

    def fix_common_issues(self):
        """Fix common Grafana issues"""
        print("\nAttempting to fix common issues...")

        # Create missing directories
        for path in self.grafana_paths.values():
            if not Path(path).exists():
                try:
                    Path(path).mkdir(parents=True, exist_ok=True)
                    print(f"✓ Created directory: {path}")
                except Exception as e:
                    print(f"✗ Failed to create directory {path}: {e}")

        # Fix permissions
        try:
            user = os.getenv('USER')
            subprocess.run(['sudo', 'chown', '-R', f'{user}:staff', '/usr/local/var/log/grafana'])
            subprocess.run(['sudo', 'chown', '-R', f'{user}:staff', '/usr/local/var/lib/grafana'])
            print("✓ Fixed permissions")
        except Exception as e:
            print(f"✗ Failed to fix permissions: {e}")

        # Restart service
        try:
            subprocess.run(['brew', 'services', 'restart', 'grafana'])
            print("✓ Restarted Grafana service")
        except Exception as e:
            print(f"✗ Failed to restart service: {e}")

def main():
    checker = GrafanaChecker()
    
    if not checker.check_installation():
        print("\nGrafana is not installed. Would you like to install it? (y/n)")
        if input().lower() == 'y':
            try:
                subprocess.run(['brew', 'install', 'grafana'], check=True)
                print("✓ Grafana installed successfully")
                checker.check_installation()
            except Exception as e:
                print(f"✗ Failed to install Grafana: {e}")
    else:
        print("\nWould you like to attempt fixing common issues? (y/n)")
        if input().lower() == 'y':
            checker.fix_common_issues()

if __name__ == "__main__":
    main() 