#!/usr/bin/env python3

import subprocess
import sys
import pkg_resources
import requests
from pathlib import Path
import time

class DependencyChecker:
    def __init__(self):
        self.required_packages = {
            'Flask': '3.0.0',
            'PyYAML': '6.0.1',
            'prometheus-client': '0.21.0',
            'prometheus-flask-exporter': '0.18.2',
            'requests': '2.28.0'
        }
        
        self.required_services = {
            'prometheus': 9090,
            'grafana': 3000,
            'node_exporter': 9100,
            'nginx-exporter': 9113,
            'redis-exporter': 9121
        }
        
        self.exporters = {
            'node_exporter': 'node_exporter',
            'nginx-prometheus-exporter': 'nginx-exporter',
            'redis_exporter': 'redis-exporter',
            'process-exporter': 'process-exporter'
        }

    def check_python_packages(self):
        """Check if required Python packages are installed"""
        print("\nChecking Python packages...")
        missing_packages = []
        outdated_packages = []
        
        for package, min_version in self.required_packages.items():
            try:
                installed = pkg_resources.get_distribution(package)
                if pkg_resources.parse_version(installed.version) < pkg_resources.parse_version(min_version):
                    outdated_packages.append(f"{package} (installed: {installed.version}, minimum required: {min_version})")
                else:
                    print(f"✓ {package} {installed.version}")
            except pkg_resources.DistributionNotFound:
                missing_packages.append(package)
        
        if missing_packages:
            print("\n✗ Missing packages:")
            for package in missing_packages:
                print(f"  - {package}")
            print("\nInstall missing packages with:")
            print(f"pip install {' '.join(missing_packages)}")
        
        if outdated_packages:
            print("\n✗ Outdated packages:")
            for package in outdated_packages:
                print(f"  - {package}")
            print("\nUpdate packages with:")
            print("pip install --upgrade [package_name]")
        
        return not (missing_packages or outdated_packages)

    def check_brew_services(self):
        """Check if required services are installed via Homebrew"""
        print("\nChecking Homebrew services...")
        missing_services = []
        
        try:
            result = subprocess.run(['brew', 'services', 'list'], 
                                 capture_output=True, 
                                 text=True)
            
            for service in self.exporters.keys():
                if service not in result.stdout:
                    missing_services.append(service)
                else:
                    print(f"✓ {service} is installed")
                    
            if missing_services:
                print("\n✗ Missing services:")
                for service in missing_services:
                    print(f"  - {service}")
                print("\nInstall missing services with:")
                print(f"brew install {' '.join(missing_services)}")
                
        except subprocess.CalledProcessError:
            print("✗ Error checking Homebrew services")
            return False
            
        return not missing_services

    def check_service_ports(self):
        """Check if required services are running on their ports"""
        print("\nChecking service ports...")
        not_running = []
        
        for service, port in self.required_services.items():
            try:
                response = requests.get(f"http://localhost:{port}")
                print(f"✓ {service} is running on port {port}")
            except requests.RequestException:
                not_running.append(f"{service} (port {port})")
        
        if not_running:
            print("\n✗ Services not responding:")
            for service in not_running:
                print(f"  - {service}")
            print("\nStart services with:")
            print("brew services start [service_name]")
            
        return not not_running

    def verify_configurations(self):
        """Check if configuration files exist and are valid"""
        print("\nChecking configurations...")
        project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        
        configs = {
            'prometheus': project_root / "prometheus/prometheus.yml",
            'grafana': project_root / "grafana/grafana.ini",
            'nginx': project_root / "nginx/nginx.conf"
        }
        
        missing_configs = []
        
        for name, path in configs.items():
            if path.exists():
                print(f"✓ {name} configuration exists at {path}")
            else:
                missing_configs.append(f"{name} ({path})")
        
        if missing_configs:
            print("\n✗ Missing configurations:")
            for config in missing_configs:
                print(f"  - {config}")
            print("\nRun setup script to create configurations:")
            print("./scripts/configure_monitoring.py")
            
        return not missing_configs

    def verify_service(self, service_name, port):
        """Verify if a service is running and responding"""
        try:
            # First check if service is running via brew
            result = subprocess.run(['brew', 'services', 'list'], 
                                 capture_output=True, 
                                 text=True)
            
            if f"{service_name} started" not in result.stdout:
                print(f"Starting {service_name}...")
                subprocess.run(['brew', 'services', 'start', service_name], 
                             check=True)
                time.sleep(2)  # Wait for service to start
            
            # Then check if port is responding
            try:
                response = requests.get(f"http://localhost:{port}/metrics")
                if response.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            
            return False
        except Exception as e:
            print(f"Error verifying {service_name}: {e}")
            return False

    def check_all(self):
        """Run all dependency checks"""
        print("=== Dependency Check ===")
        
        results = {
            'packages': self.check_python_packages(),
            'services': self.check_brew_services(),
            'ports': self.check_service_ports(),
            'configs': self.verify_configurations()
        }
        
        print("\nSummary:")
        for check, passed in results.items():
            print(f"{'✓' if passed else '✗'} {check.capitalize()}")
        
        if all(results.values()):
            print("\n✓ All dependencies satisfied!")
        else:
            print("\n✗ Some checks failed. Please address the issues above.")
            sys.exit(1)

def main():
    checker = DependencyChecker()
    checker.check_all()

if __name__ == "__main__":
    main() 