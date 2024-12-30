#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path
import time
import requests
import socket
from datetime import datetime
import json
import shutil

class MonitoringSetup:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.prometheus_dir = self.project_root / "prometheus"
        self.grafana_dir = self.project_root / "grafana"
        
    def _manage_service(self, service_name, action):
        """Manage service using brew services or launchctl"""
        try:
            if action == 'start':
                # Try brew services first
                result = subprocess.run(['brew', 'services', 'start', service_name], 
                                     capture_output=True, 
                                     text=True)
                if 'Successfully started' in result.stdout:
                    return True
                    
                # Fallback to launchctl
                plist_path = f"/usr/local/opt/{service_name}/homebrew.mxcl.{service_name}.plist"
                subprocess.run(['launchctl', 'load', plist_path], check=True)
                
            elif action == 'stop':
                # Try brew services first
                result = subprocess.run(['brew', 'services', 'stop', service_name],
                                     capture_output=True,
                                     text=True)
                if 'Successfully stopped' in result.stdout:
                    return True
                    
                # Fallback to launchctl
                plist_path = f"/usr/local/opt/{service_name}/homebrew.mxcl.{service_name}.plist"
                subprocess.run(['launchctl', 'unload', plist_path], check=True)
                
            elif action == 'restart':
                self._manage_service(service_name, 'stop')
                time.sleep(2)  # Wait for service to stop
                self._manage_service(service_name, 'start')
                
            return True
        except Exception as e:
            print(f"Error managing {service_name} ({action}): {e}")
            return False

    def start_service(self, service_name):
        """Start a service"""
        print(f"Starting {service_name}...")
        return self._manage_service(service_name, 'start')

    def stop_service(self, service_name):
        """Stop a service"""
        print(f"Stopping {service_name}...")
        return self._manage_service(service_name, 'stop')

    def restart_service(self, service_name):
        """Restart a service"""
        print(f"Restarting {service_name}...")
        return self._manage_service(service_name, 'restart')

    def get_service_status(self, service_name):
        """Get service status"""
        try:
            # Check brew services status
            result = subprocess.run(['brew', 'services', 'list'], 
                                 capture_output=True, 
                                 text=True)
            
            for line in result.stdout.splitlines():
                if service_name in line:
                    return 'started' if 'started' in line.lower() else 'stopped'
            
            # Fallback to launchctl
            plist_name = f"homebrew.mxcl.{service_name}"
            result = subprocess.run(['launchctl', 'list'], 
                                 capture_output=True, 
                                 text=True)
            
            return 'started' if plist_name in result.stdout else 'stopped'
        except Exception as e:
            print(f"Error checking {service_name} status: {e}")
            return 'unknown'

    def setup_prometheus(self):
        """Set up Prometheus"""
        print("Setting up Prometheus...")
        
        try:
            # Create directories
            self.prometheus_dir.mkdir(exist_ok=True)
            data_dir = self.prometheus_dir / "data"
            data_dir.mkdir(exist_ok=True)
            
            # Stop existing Prometheus
            self.stop_service('prometheus')
            
            # Set permissions
            subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}', str(self.prometheus_dir)])
            
            # Create configuration
            config_file = self.prometheus_dir / "prometheus.yml"
            with open(config_file, 'w') as f:
                f.write(self.get_prometheus_config())
            
            # Create brew service configuration
            plist_path = "/usr/local/opt/prometheus/homebrew.mxcl.prometheus.plist"
            with open(plist_path, 'w') as f:
                f.write(self._generate_brew_service_config(
                    config=config_file,
                    data=data_dir
                ))
            
            # Start Prometheus
            if not self.start_service('prometheus'):
                raise Exception("Failed to start Prometheus")
            
            # Verify it's running
            time.sleep(5)  # Wait for startup
            try:
                response = requests.get('http://localhost:9090/-/healthy', timeout=5)
                if response.status_code == 200:
                    print("✓ Prometheus started successfully")
                else:
                    raise Exception(f"Prometheus health check failed: {response.status_code}")
            except requests.RequestException as e:
                raise Exception(f"Prometheus health check failed: {e}")
            
        except Exception as e:
            print(f"Error setting up Prometheus: {e}")
            self.troubleshoot_prometheus()
            raise

    def _fix_prometheus_setup(self):
        """Attempt to fix common Prometheus issues"""
        print("\nApplying automatic fixes...")
        
        # Install Prometheus if missing
        try:
            subprocess.run(['which', 'prometheus'], check=True)
        except subprocess.CalledProcessError:
            print("Installing Prometheus...")
            subprocess.run(['brew', 'install', 'prometheus'])
        
        # Fix permissions
        directories = [
            self.prometheus_dir,
            self.prometheus_dir / "data",
            Path("/usr/local/etc/prometheus"),
            self.project_root / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}', str(directory)])
        
        # Clean up old data
        old_data = Path("/usr/local/var/prometheus")
        if old_data.exists():
            print("Cleaning up old data...")
            subprocess.run(['rm', '-rf', str(old_data)])

    def _cleanup_prometheus(self):
        """Stop and clean up existing Prometheus instances"""
        print("Cleaning up existing Prometheus instances...")
        
        # Stop brew service
        subprocess.run(['brew', 'services', 'stop', 'prometheus'], check=False)
        
        # Kill any remaining processes
        try:
            subprocess.run(['pkill', '-f', 'prometheus'], check=False)
        except:
            pass
        
        # Wait for port to be available
        max_attempts = 5
        attempt = 0
        while attempt < max_attempts:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', 9090))
                    return True
            except socket.error:
                attempt += 1
                if attempt == max_attempts:
                    raise Exception("Port 9090 is still in use after cleanup")
                time.sleep(1)

    def _generate_brew_service_config(self, config, data):
        """Generate Prometheus brew service configuration"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>homebrew.mxcl.prometheus</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/opt/prometheus/bin/prometheus</string>
        <string>--config.file={config}</string>
        <string>--storage.tsdb.path={data}</string>
        <string>--web.console.templates=/usr/local/opt/prometheus/consoles</string>
        <string>--web.console.libraries=/usr/local/opt/prometheus/console_libraries</string>
        <string>--web.listen-address=:9090</string>
        <string>--web.enable-lifecycle</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{self.project_root}/logs/prometheus.err.log</string>
    <key>StandardOutPath</key>
    <string>{self.project_root}/logs/prometheus.log</string>
    <key>WorkingDirectory</key>
    <string>{self.prometheus_dir}</string>
  </dict>
</plist>"""

    def setup_grafana(self):
        """Set up Grafana"""
        print("Setting up Grafana...")
        
        # Create directories
        self.grafana_dir.mkdir(exist_ok=True)
        
        # Create Grafana launch agent
        plist_path = Path.home() / "Library/LaunchAgents/com.streamad.grafana.plist"
        with open(plist_path, 'w') as f:
            f.write(self.get_grafana_plist())
        
        # Load and start Grafana
        subprocess.run(['launchctl', 'load', str(plist_path)])
        self.start_service('grafana')
        
        print("Grafana setup complete")
        print("Access Grafana at: http://localhost:3000")
        print("Default credentials: admin/admin")
    
    def setup_logrotate(self):
        """Set up Logrotate"""
        print("Setting up Logrotate...")
        
        logrotate_conf = """
/Volumes/Learn_Space/StreamAdExchange/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root wheel
}
"""
        
        # Write logrotate configuration
        with open('/usr/local/etc/logrotate.d/streamad', 'w') as f:
            f.write(logrotate_conf)
        
        # Set up daily cron job for logrotate
        cron_job = '0 0 * * * /usr/local/sbin/logrotate /usr/local/etc/logrotate.d/streamad'
        subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        print("Logrotate setup complete")
    
    def install_dependencies(self):
        """Install required packages"""
        print("Installing dependencies...")
        
        packages = [
            'prometheus',
            'grafana',
            'logrotate',
            'node_exporter',  # For system metrics
            'nginx-prometheus-exporter'  # For nginx metrics
        ]
        
        for package in packages:
            subprocess.run(['brew', 'install', package])
        
        print("Dependencies installed")
    
    def setup_all(self):
        """Run complete setup"""
        self.install_dependencies()
        self.setup_prometheus()
        self.setup_grafana()
        self.setup_logrotate()
        
        print("\nSetup complete!")
        print("\nNext steps:")
        print("1. Access Grafana at http://localhost:3000")
        print("2. Add Prometheus data source (http://localhost:9090)")
        print("3. Import dashboards for monitoring")

    def get_prometheus_plist(self):
        """Generate Prometheus launchd plist"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.streamad.prometheus</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/prometheus</string>
        <string>--config.file={self.prometheus_dir}/prometheus.yml</string>
        <string>--storage.tsdb.path={self.prometheus_dir}/data</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{self.project_root}/logs/prometheus.err.log</string>
    <key>StandardOutPath</key>
    <string>{self.project_root}/logs/prometheus.log</string>
</dict>
</plist>"""

    def get_prometheus_config(self):
        """Generate Prometheus configuration"""
        return """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'streamad'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
"""

    def get_grafana_plist(self):
        """Generate Grafana launchd plist"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.streamad.grafana</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/opt/grafana/bin/grafana</string>
        <string>server</string>
        <string>--config</string>
        <string>{self.grafana_dir}/grafana.ini</string>
        <string>--homepath</string>
        <string>/usr/local/opt/grafana</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{self.project_root}/logs/grafana.err.log</string>
    <key>StandardOutPath</key>
    <string>{self.project_root}/logs/grafana.log</string>
</dict>
</plist>"""

    def check_services(self):
        """Check status of all monitoring services"""
        services = {
            'prometheus': self.get_service_status('prometheus'),
            'grafana': self.get_service_status('grafana'),
            'node_exporter': self.get_service_status('node_exporter'),
            'nginx-prometheus-exporter': self.get_service_status('nginx-prometheus-exporter')
        }
        
        print("\nService Status:")
        for service, status in services.items():
            print(f"{service}: {status}")
        
        return all(status == 'started' for status in services.values())

    def restart_services(self):
        """Restart all monitoring services"""
        services = ['prometheus', 'grafana', 'node_exporter', 'nginx-prometheus-exporter']
        
        for service in services:
            print(f"\nRestarting {service}...")
            self.stop_service(service)
            self.start_service(service)

    def troubleshoot_prometheus(self):
        """Troubleshoot Prometheus setup and startup issues"""
        print("\nTroubleshooting Prometheus...")
        issues_found = False
        
        # Check if Prometheus is installed
        try:
            subprocess.run(['which', 'prometheus'], check=True)
            print("✓ Prometheus is installed")
        except subprocess.CalledProcessError:
            print("✗ Prometheus is not installed")
            print("  Run: brew install prometheus")
            issues_found = True
        
        # Check directories and permissions
        directories = {
            'prometheus_dir': self.prometheus_dir,
            'data_dir': self.prometheus_dir / "data",
            'config_dir': "/usr/local/etc/prometheus",
            'log_dir': self.project_root / "logs"
        }
        
        for name, directory in directories.items():
            if not directory.exists():
                print(f"✗ Directory missing: {directory}")
                print(f"  Creating directory...")
                directory.mkdir(parents=True, exist_ok=True)
                issues_found = True
            
            # Check permissions
            try:
                test_file = directory / ".test"
                test_file.touch()
                test_file.unlink()
                print(f"✓ {name} permissions OK")
            except PermissionError:
                print(f"✗ Permission denied for {directory}")
                print(f"  Run: sudo chown -R $(whoami) {directory}")
                issues_found = True
        
        # Check configuration
        config_file = self.prometheus_dir / "prometheus.yml"
        if not config_file.exists():
            print("✗ Configuration file missing")
            print("  Creating default configuration...")
            with open(config_file, 'w') as f:
                f.write(self.get_prometheus_config())
            issues_found = True
        else:
            print("✓ Configuration file exists")
            
            # Validate configuration
            try:
                subprocess.run(['promtool', 'check', 'config', str(config_file)], check=True)
                print("✓ Configuration syntax is valid")
            except subprocess.CalledProcessError:
                print("✗ Invalid configuration syntax")
                print("  Check the configuration file for errors")
                issues_found = True
        
        # Check port availability
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', 9090))
            print("✓ Port 9090 is available")
            sock.close()
        except socket.error:
            print("✗ Port 9090 is in use")
            print("  Check if another instance is running:")
            print("  lsof -i :9090")
            issues_found = True
        
        # Check brew services
        try:
            result = subprocess.run(['brew', 'services', 'list'], capture_output=True, text=True)
            if 'prometheus' in result.stdout:
                print("✓ Prometheus service is registered")
                if 'started' in result.stdout:
                    print("✓ Prometheus service is running")
                else:
                    print("✗ Prometheus service is not running")
                    issues_found = True
            else:
                print("✗ Prometheus service is not registered")
                issues_found = True
        except subprocess.CalledProcessError:
            print("✗ Error checking brew services")
            issues_found = True
        
        # Check logs
        log_file = self.project_root / "logs/prometheus.log"
        err_log_file = self.project_root / "logs/prometheus.err.log"
        
        if log_file.exists():
            print("\nRecent log entries:")
            try:
                with open(log_file) as f:
                    last_lines = f.readlines()[-5:]
                    for line in last_lines:
                        print(f"  {line.strip()}")
            except Exception as e:
                print(f"✗ Error reading log file: {e}")
        
        if err_log_file.exists() and err_log_file.stat().st_size > 0:
            print("\nError log entries:")
            try:
                with open(err_log_file) as f:
                    last_lines = f.readlines()[-5:]
                    for line in last_lines:
                        print(f"  {line.strip()}")
                issues_found = True
            except Exception as e:
                print(f"✗ Error reading error log file: {e}")
        
        if issues_found:
            print("\nTry these steps to resolve issues:")
            print("1. Stop Prometheus: brew services stop prometheus")
            print("2. Remove old data: rm -rf /usr/local/var/prometheus")
            print("3. Fix permissions: sudo chown -R $(whoami) /usr/local/etc/prometheus")
            print("4. Start Prometheus: brew services start prometheus")
            print("5. Check logs: tail -f /usr/local/var/log/prometheus.log")
        else:
            print("\n✓ No issues found")

    def backup_monitoring_data(self):
        """Backup Prometheus and Grafana data"""
        print("\nBacking up monitoring data...")
        
        backup_dir = self.project_root / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Stop services before backup
            self.stop_service('prometheus')
            self.stop_service('grafana')
            
            # Backup Prometheus data
            prometheus_backup = backup_dir / "prometheus"
            prometheus_backup.mkdir(exist_ok=True)
            
            if self.prometheus_dir.exists():
                subprocess.run([
                    'cp', '-r',
                    str(self.prometheus_dir),
                    str(prometheus_backup)
                ])
                print("✓ Prometheus data backed up")
            
            # Backup Grafana data
            grafana_backup = backup_dir / "grafana"
            grafana_backup.mkdir(exist_ok=True)
            
            if self.grafana_dir.exists():
                subprocess.run([
                    'cp', '-r',
                    str(self.grafana_dir),
                    str(grafana_backup)
                ])
                print("✓ Grafana data backed up")
            
            # Create backup metadata
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'prometheus_version': self._get_version('prometheus'),
                'grafana_version': self._get_version('grafana'),
                'configs': {
                    'prometheus': str(self.prometheus_dir / "prometheus.yml"),
                    'grafana': str(self.grafana_dir / "grafana.ini")
                }
            }
            
            with open(backup_dir / "backup_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✓ Backup completed: {backup_dir}")
            return str(backup_dir)
            
        finally:
            # Restart services
            self.start_service('prometheus')
            self.start_service('grafana')

    def restore_monitoring_data(self, backup_path=None):
        """Restore Prometheus and Grafana data from backup"""
        if backup_path is None:
            # Use latest backup if none specified
            backup_root = self.project_root / "backups"
            if not backup_root.exists():
                raise Exception("No backups found")
            
            backups = sorted(backup_root.glob("*"))
            if not backups:
                raise Exception("No backups found")
            
            backup_path = backups[-1]
        
        backup_path = Path(backup_path)
        print(f"\nRestoring from backup: {backup_path}")
        
        try:
            # Verify backup metadata
            with open(backup_path / "backup_metadata.json") as f:
                metadata = json.load(f)
            
            # Stop services before restore
            self.stop_service('prometheus')
            self.stop_service('grafana')
            
            # Backup current data before restore
            current_backup = self.backup_monitoring_data()
            print(f"Current data backed up to: {current_backup}")
            
            # Restore Prometheus data
            prometheus_backup = backup_path / "prometheus"
            if prometheus_backup.exists():
                if self.prometheus_dir.exists():
                    shutil.rmtree(self.prometheus_dir)
                shutil.copytree(prometheus_backup, self.prometheus_dir)
                print("✓ Prometheus data restored")
            
            # Restore Grafana data
            grafana_backup = backup_path / "grafana"
            if grafana_backup.exists():
                if self.grafana_dir.exists():
                    shutil.rmtree(self.grafana_dir)
                shutil.copytree(grafana_backup, self.grafana_dir)
                print("✓ Grafana data restored")
            
            # Fix permissions
            subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}', str(self.prometheus_dir)])
            subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}', str(self.grafana_dir)])
            
            print("✓ Restore completed")
            
        finally:
            # Restart services
            self.start_service('prometheus')
            self.start_service('grafana')

    def _get_version(self, service):
        """Get service version"""
        try:
            if service == 'prometheus':
                result = subprocess.run(['prometheus', '--version'], capture_output=True, text=True)
                return result.stdout.split('\n')[0]
            elif service == 'grafana':
                result = subprocess.run(['grafana-server', '-v'], capture_output=True, text=True)
                return result.stdout.strip()
        except:
            return 'unknown'

    def list_backups(self):
        """List available backups"""
        backup_root = self.project_root / "backups"
        if not backup_root.exists():
            print("No backups found")
            return []
        
        backups = []
        for backup_dir in sorted(backup_root.glob("*")):
            try:
                with open(backup_dir / "backup_metadata.json") as f:
                    metadata = json.load(f)
                
                backups.append({
                    'path': str(backup_dir),
                    'timestamp': metadata['timestamp'],
                    'prometheus_version': metadata['prometheus_version'],
                    'grafana_version': metadata['grafana_version']
                })
            except Exception as e:
                print(f"Error reading backup {backup_dir}: {e}")
        
        if backups:
            print("\nAvailable backups:")
            for backup in backups:
                print(f"\nBackup: {backup['path']}")
                print(f"  Timestamp: {backup['timestamp']}")
                print(f"  Prometheus: {backup['prometheus_version']}")
                print(f"  Grafana: {backup['grafana_version']}")
        else:
            print("No valid backups found")
        
        return backups

if __name__ == "__main__":
    setup = MonitoringSetup()
    setup.setup_all() 