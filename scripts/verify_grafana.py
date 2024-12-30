#!/usr/bin/env python3

import subprocess
import requests
import os
from pathlib import Path
import time
import json

class GrafanaVerifier:
    def __init__(self):
        self.paths = {
            'binary': Path('/usr/local/grafana/bin/grafana-server'),
            'config': Path('/usr/local/etc/grafana/grafana.ini'),
            'logs': Path('/usr/local/var/log/grafana'),
            'data': Path('/usr/local/var/lib/grafana'),
            'plist': Path.home() / "Library/LaunchAgents/com.grafana.server.plist"
        }
        self.port = 3000

    def verify_installation(self):
        """Verify Grafana installation and print detailed status"""
        print("\n=== Grafana Installation Verification ===")
        issues_found = False

        # Check binary
        if self.paths['binary'].exists():
            print("✓ Grafana binary found")
            try:
                version = subprocess.run(
                    [str(self.paths['binary']), '-v'],
                    capture_output=True,
                    text=True
                )
                print(f"✓ Version: {version.stdout.strip()}")
            except Exception as e:
                print(f"✗ Error checking version: {e}")
                issues_found = True
        else:
            print("✗ Grafana binary not found")
            issues_found = True

        # Check directories and permissions
        for name, path in self.paths.items():
            if path.exists():
                print(f"✓ {name}: exists")
                try:
                    # Test write permission
                    if path.is_dir():
                        test_file = path / '.test'
                        test_file.touch()
                        test_file.unlink()
                        print(f"✓ {name}: writable")
                    else:
                        print(f"✓ {name}: readable")
                except PermissionError:
                    print(f"✗ {name}: permission denied")
                    issues_found = True
            else:
                print(f"✗ {name}: missing")
                issues_found = True

        # Check if process is running
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'grafana-server'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                pid = result.stdout.strip()
                print(f"✓ Grafana process running (PID: {pid})")
            else:
                print("✗ Grafana process not running")
                issues_found = True
        except Exception as e:
            print(f"✗ Error checking process: {e}")
            issues_found = True

        # Check port
        try:
            result = subprocess.run(
                ['lsof', '-i', f':{self.port}'],
                capture_output=True,
                text=True
            )
            if 'grafana' in result.stdout:
                print(f"✓ Port {self.port} is being used by Grafana")
            else:
                print(f"✗ Port {self.port} not in use by Grafana")
                issues_found = True
        except Exception as e:
            print(f"✗ Error checking port: {e}")
            issues_found = True

        # Check HTTP response
        try:
            response = requests.get(f'http://localhost:{self.port}')
            if response.status_code == 200:
                print("✓ Grafana is responding to HTTP requests")
            else:
                print(f"✗ Grafana returned status code: {response.status_code}")
                issues_found = True
        except requests.RequestException as e:
            print(f"✗ Error connecting to Grafana: {e}")
            issues_found = True

        # Check recent logs
        log_file = self.paths['logs'] / 'grafana-stdout.log'
        if log_file.exists():
            print("\nRecent log entries:")
            try:
                subprocess.run(['tail', '-n', '5', str(log_file)])
            except Exception as e:
                print(f"✗ Error reading logs: {e}")
                issues_found = True

        if issues_found:
            print("\nIssues were found. Try these fixes:")
            print("1. Restart Grafana:")
            print("   launchctl unload ~/Library/LaunchAgents/com.grafana.server.plist")
            print("   launchctl load ~/Library/LaunchAgents/com.grafana.server.plist")
            print("2. Check logs:")
            print("   tail -f /usr/local/var/log/grafana/grafana-stdout.log")
            print("3. Fix permissions:")
            print("   sudo chown -R $(whoami) /usr/local/grafana")
            print("   sudo chown -R $(whoami) /usr/local/var/lib/grafana")
            return False
        else:
            print("\n✓ All checks passed! Grafana is properly installed and running")
            print("Access Grafana at: http://localhost:3000")
            print("Default credentials: admin/admin")
            return True

if __name__ == "__main__":
    verifier = GrafanaVerifier()
    verifier.verify_installation() 