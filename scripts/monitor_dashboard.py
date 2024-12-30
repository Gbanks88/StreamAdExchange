#!/usr/bin/env python3

import os
import sys
import psutil
import time
import json
from datetime import datetime
import subprocess
import requests
from pathlib import Path

class ServiceMonitor:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.log_dir = self.project_root / "logs"
        self.nginx_dir = self.project_root / "nginx"
        self.pid_files = {
            'flask': self.project_root / "flask.pid",
            'diagnostic': self.project_root / "diagnostic.pid",
            'failover': self.project_root / "failover.pid"
        }
        self.log_files = {
            'nginx_access': self.nginx_dir / "logs/access.log",
            'nginx_error': self.nginx_dir / "logs/error.log",
            'flask': self.log_dir / f"flask_{datetime.now().strftime('%Y%m%d')}.log",
            'diagnostic': self.log_dir / f"diagnostic_{datetime.now().strftime('%Y%m%d')}.log"
        }

    def get_service_status(self, pid_file):
        """Check if a service is running based on its PID file"""
        try:
            if pid_file.exists():
                pid = int(pid_file.read_text().strip())
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    return {
                        'status': 'running',
                        'pid': pid,
                        'cpu_percent': process.cpu_percent(),
                        'memory_percent': process.memory_percent(),
                        'uptime': time.time() - process.create_time()
                    }
            return {'status': 'stopped'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_nginx_status(self):
        """Get nginx status and metrics"""
        try:
            nginx_processes = [p for p in psutil.process_iter(['name']) if p.info['name'] == 'nginx']
            if nginx_processes:
                master_process = nginx_processes[0]
                return {
                    'status': 'running',
                    'pid': master_process.pid,
                    'workers': len(nginx_processes) - 1,
                    'connections': self._get_nginx_connections(),
                    'cpu_percent': sum(p.cpu_percent() for p in nginx_processes),
                    'memory_percent': sum(p.memory_percent() for p in nginx_processes)
                }
            return {'status': 'stopped'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _get_nginx_connections(self):
        """Get current nginx connections"""
        try:
            result = subprocess.run(['nginx', '-v'], capture_output=True, text=True)
            return {
                'active': result.stdout.count('Active connections'),
                'reading': result.stdout.count('Reading'),
                'writing': result.stdout.count('Writing'),
                'waiting': result.stdout.count('Waiting')
            }
        except:
            return {}

    def get_system_metrics(self):
        """Get system-wide metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network': psutil.net_io_counters()._asdict()
        }

    def check_application_health(self):
        """Check application endpoints"""
        try:
            response = requests.get('http://localhost:5000/health')
            return {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_recent_logs(self, log_file, lines=10):
        """Get recent log entries"""
        try:
            if log_file.exists():
                with open(log_file) as f:
                    return list(f.readlines()[-lines:])
            return []
        except Exception as e:
            return [f"Error reading logs: {e}"]

    def generate_report(self):
        """Generate comprehensive status report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'services': {
                'flask': self.get_service_status(self.pid_files['flask']),
                'nginx': self.get_nginx_status(),
                'diagnostic': self.get_service_status(self.pid_files['diagnostic']),
                'failover': self.get_service_status(self.pid_files['failover'])
            },
            'system': self.get_system_metrics(),
            'application': self.check_application_health(),
            'recent_logs': {
                name: self.get_recent_logs(log_file)
                for name, log_file in self.log_files.items()
            }
        }

def print_status_report(report):
    """Print formatted status report"""
    print("\n=== StreamAdExchange Status Report ===")
    print(f"Time: {datetime.fromisoformat(report['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("Services Status:")
    for service, status in report['services'].items():
        print(f"  {service.upper()}: {status['status']}")
        if status['status'] == 'running':
            print(f"    CPU: {status.get('cpu_percent', 0):.1f}%")
            print(f"    Memory: {status.get('memory_percent', 0):.1f}%")

    print("\nSystem Metrics:")
    system = report['system']
    print(f"  CPU Usage: {system['cpu_percent']}%")
    print(f"  Memory Usage: {system['memory_percent']}%")
    print(f"  Disk Usage: {system['disk_usage']}%")

    print("\nApplication Health:")
    app = report['application']
    print(f"  Status: {app['status']}")
    if 'response_time' in app:
        print(f"  Response Time: {app['response_time']:.3f}s")

    print("\nRecent Errors (last 5):")
    for log in report['recent_logs'].get('nginx_error', [])[-5:]:
        print(f"  {log.strip()}")

def main():
    monitor = ServiceMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        # Output JSON format
        print(json.dumps(monitor.generate_report(), indent=2))
    else:
        # Output human-readable format
        print_status_report(monitor.generate_report())

if __name__ == "__main__":
    main() 