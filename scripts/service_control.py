#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import time
import requests

class ServiceController:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.services = {
            'prometheus': {
                'plist': 'com.prometheus.server',
                'port': 9090,
                'health_url': 'http://localhost:9090/-/healthy'
            },
            'grafana': {
                'plist': 'com.grafana.server',
                'port': 3000,
                'health_url': 'http://localhost:3000/api/health'
            },
            'logrotate': {
                'config': '/usr/local/etc/logrotate.d/streamad'
            }
        }

    def start_service(self, service_name):
        """Start a specific service"""
        print(f"\nStarting {service_name}...")
        try:
            if service_name == 'logrotate':
                # For logrotate, run manually
                subprocess.run(['sudo', 'logrotate', self.services['logrotate']['config']], check=True)
                print(f"✓ Ran logrotate manually")
                return True

            # For other services, use launchctl
            plist = self.services[service_name]['plist']
            subprocess.run(['launchctl', 'load', f'~/Library/LaunchAgents/{plist}.plist'], check=True)
            
            # Wait for service to start
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    response = requests.get(self.services[service_name]['health_url'])
                    if response.status_code == 200:
                        print(f"✓ {service_name} started successfully")
                        return True
                except:
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue
            
            print(f"✗ Failed to verify {service_name} is running")
            return False

        except Exception as e:
            print(f"✗ Error starting {service_name}: {e}")
            return False

    def stop_service(self, service_name):
        """Stop a specific service"""
        print(f"\nStopping {service_name}...")
        try:
            if service_name == 'logrotate':
                print("Note: logrotate is not a running service")
                return True

            # For other services, use launchctl
            plist = self.services[service_name]['plist']
            subprocess.run(['launchctl', 'unload', f'~/Library/LaunchAgents/{plist}.plist'], check=True)
            print(f"✓ {service_name} stopped successfully")
            return True

        except Exception as e:
            print(f"✗ Error stopping {service_name}: {e}")
            return False

    def enable_service(self, service_name):
        """Enable a service to start at boot"""
        print(f"\nEnabling {service_name}...")
        try:
            if service_name == 'logrotate':
                # Set up cron job for logrotate
                cron_cmd = f"0 0 * * * /usr/local/sbin/logrotate {self.services['logrotate']['config']}"
                self._add_to_crontab(cron_cmd)
                print("✓ Logrotate cron job enabled")
                return True

            # For other services, ensure plist is loaded
            plist = self.services[service_name]['plist']
            plist_path = Path.home() / f"Library/LaunchAgents/{plist}.plist"
            
            if not plist_path.exists():
                print(f"✗ Service plist not found: {plist_path}")
                return False

            subprocess.run(['launchctl', 'load', '-w', str(plist_path)], check=True)
            print(f"✓ {service_name} enabled successfully")
            return True

        except Exception as e:
            print(f"✗ Error enabling {service_name}: {e}")
            return False

    def _add_to_crontab(self, cron_cmd):
        """Add command to crontab if not already present"""
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_crontab = result.stdout if result.returncode == 0 else ""
            
            if cron_cmd not in current_crontab:
                new_crontab = current_crontab.rstrip() + f"\n{cron_cmd}\n"
                subprocess.run(['crontab', '-'], input=new_crontab, text=True)
                print("✓ Added to crontab")
            else:
                print("✓ Already in crontab")
            
        except Exception as e:
            print(f"✗ Error modifying crontab: {e}")
            raise

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Control monitoring services')
    parser.add_argument('action', choices=['start', 'stop', 'enable'], help='Action to perform')
    parser.add_argument('service', choices=['prometheus', 'grafana', 'logrotate', 'all'], help='Service to control')
    
    args = parser.parse_args()
    controller = ServiceController()
    
    services = ['prometheus', 'grafana', 'logrotate'] if args.service == 'all' else [args.service]
    
    for service in services:
        if args.action == 'start':
            controller.start_service(service)
        elif args.action == 'stop':
            controller.stop_service(service)
        elif args.action == 'enable':
            controller.enable_service(service)

if __name__ == "__main__":
    main() 