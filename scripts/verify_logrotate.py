#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import time
from datetime import datetime

class LogrotateVerifier:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.logrotate_conf = Path("/usr/local/etc/logrotate.d/streamad")
        self.log_paths = {
            'app': self.project_root / "logs",
            'nginx': self.project_root / "nginx/logs",
            'prometheus': Path("/usr/local/var/log/prometheus"),
            'grafana': Path("/usr/local/var/log/grafana")
        }

    def verify_installation(self):
        """Verify logrotate installation"""
        print("\n=== Verifying Logrotate Installation ===")
        try:
            result = subprocess.run(['which', 'logrotate'], 
                                 capture_output=True, 
                                 text=True)
            if result.returncode == 0:
                print(f"✓ Logrotate is installed: {result.stdout.strip()}")
                return True
            else:
                print("✗ Logrotate is not installed")
                return False
        except Exception as e:
            print(f"✗ Error checking logrotate installation: {e}")
            return False

    def verify_configuration(self):
        """Verify logrotate configuration"""
        print("\n=== Verifying Logrotate Configuration ===")
        
        if not self.logrotate_conf.exists():
            print(f"✗ Configuration file not found: {self.logrotate_conf}")
            return False

        try:
            # Test configuration syntax
            result = subprocess.run(
                ['logrotate', '-d', str(self.logrotate_conf)],
                capture_output=True,
                text=True
            )
            if "error" in result.stderr.lower():
                print("✗ Configuration test failed:")
                print(result.stderr)
                return False
            print("✓ Configuration syntax is valid")
            return True
        except Exception as e:
            print(f"✗ Error testing configuration: {e}")
            return False

    def verify_permissions(self):
        """Verify log directory permissions"""
        print("\n=== Verifying Log Directory Permissions ===")
        all_correct = True
        
        for name, path in self.log_paths.items():
            if not path.exists():
                print(f"✗ {name} log directory missing: {path}")
                all_correct = False
                continue

            try:
                # Check directory permissions
                stat = path.stat()
                mode = stat.st_mode & 0o777
                owner = stat.st_uid
                group = stat.st_gid
                
                # Get user and group names
                owner_name = subprocess.run(
                    ['id', '-un', str(owner)],
                    capture_output=True,
                    text=True
                ).stdout.strip()
                group_name = subprocess.run(
                    ['id', '-gn', str(group)],
                    capture_output=True,
                    text=True
                ).stdout.strip()

                print(f"\nChecking {name} directory ({path}):")
                print(f"  Permissions: {oct(mode)[2:]}")
                print(f"  Owner: {owner_name}")
                print(f"  Group: {group_name}")

                # Verify specific permissions
                if name == 'nginx':
                    if mode != 0o750 or owner_name != 'www-data' or group_name != 'adm':
                        print("✗ Incorrect Nginx log permissions")
                        all_correct = False
                else:
                    if mode != 0o755:
                        print(f"✗ Incorrect permissions for {name} logs")
                        all_correct = False

            except Exception as e:
                print(f"✗ Error checking {name} permissions: {e}")
                all_correct = False

        return all_correct

    def verify_cron(self):
        """Verify logrotate cron job"""
        print("\n=== Verifying Logrotate Cron Job ===")
        try:
            result = subprocess.run(['crontab', '-l'], 
                                 capture_output=True, 
                                 text=True)
            
            if str(self.logrotate_conf) in result.stdout:
                print("✓ Logrotate cron job is configured")
                return True
            else:
                print("✗ Logrotate cron job not found")
                return False
        except Exception as e:
            print(f"✗ Error checking cron configuration: {e}")
            return False

    def verify_log_rotation(self):
        """Verify log rotation is working"""
        print("\n=== Testing Log Rotation ===")
        try:
            # Create a test log file
            test_log = self.log_paths['app'] / "test.log"
            with open(test_log, 'w') as f:
                f.write(f"Test log entry at {datetime.now()}\n" * 1000)

            # Force rotation
            print("Forcing log rotation...")
            subprocess.run(['sudo', 'logrotate', '-f', str(self.logrotate_conf)],
                         check=True)
            
            # Check if rotated file exists
            time.sleep(2)  # Wait for rotation to complete
            rotated_files = list(self.log_paths['app'].glob("test.log.*"))
            
            if rotated_files:
                print("✓ Log rotation successful")
                print(f"✓ Rotated file created: {rotated_files[0].name}")
                
                # Clean up test files
                test_log.unlink(missing_ok=True)
                for f in rotated_files:
                    f.unlink(missing_ok=True)
                    
                return True
            else:
                print("✗ No rotated log file found")
                return False
                
        except Exception as e:
            print(f"✗ Error testing log rotation: {e}")
            return False

    def verify_all(self):
        """Run all verifications"""
        checks = [
            (self.verify_installation, "Logrotate Installation"),
            (self.verify_configuration, "Configuration Syntax"),
            (self.verify_permissions, "Directory Permissions"),
            (self.verify_cron, "Cron Job Setup"),
            (self.verify_log_rotation, "Log Rotation Test")
        ]
        
        results = {}
        for check_func, description in checks:
            print(f"\nVerifying {description}...")
            results[description] = check_func()
            
        print("\n=== Verification Summary ===")
        for description, passed in results.items():
            print(f"{'✓' if passed else '✗'} {description}")
            
        if all(results.values()):
            print("\n✓ All checks passed!")
        else:
            print("\n✗ Some checks failed. Please review the output above.")

if __name__ == "__main__":
    verifier = LogrotateVerifier()
    verifier.verify_all() 