#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import shutil

class LogrotateSetup:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.log_paths = {
            'app': self.project_root / "logs",
            'nginx': self.project_root / "nginx/logs",
            'prometheus': Path("/usr/local/var/log/prometheus"),
            'grafana': Path("/usr/local/var/log/grafana"),
            'debug': self.project_root / "logs/debug",
            'error': self.project_root / "logs/error",
            'access': self.project_root / "logs/access"
        }
        self.logrotate_dir = Path("/usr/local/etc/logrotate.d")
        self.logrotate_conf = self.logrotate_dir / "streamad"

    def create_log_directories(self):
        """Create necessary log directories"""
        print("\nCreating log directories...")
        for name, path in self.log_paths.items():
            try:
                path.mkdir(parents=True, exist_ok=True)
                subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}:staff', str(path)])
                subprocess.run(['sudo', 'chmod', '-R', '755', str(path)])
                print(f"✓ Created {name} log directory: {path}")
            except Exception as e:
                print(f"✗ Failed to create {name} log directory: {e}")
                return False
        return True

    def create_logrotate_config(self):
        """Create logrotate configuration"""
        config = f"""# StreamAdExchange Logrotate Configuration

# Nginx Logs
{self.log_paths['nginx']}/*.log {{
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ ! -f {self.project_root}/nginx/run/nginx.pid ] || kill -USR1 `cat {self.project_root}/nginx/run/nginx.pid`
    endscript
}}

# Application Logs
{self.log_paths['app']}/*.log {{
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 50M
    prerotate
        echo "[$(date)] Starting log rotation" >> {self.log_paths['app']}/rotation.log
    endscript
    postrotate
        kill -HUP `cat {self.project_root}/run/gunicorn.pid 2>/dev/null` 2>/dev/null || true
        echo "[$(date)] Completed log rotation" >> {self.log_paths['app']}/rotation.log
    endscript
}}

# Access Logs (with detailed settings)
{self.log_paths['access']}/*.log {{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 100M
    # Add custom formatting for compressed files
    compresscmd /usr/bin/gzip
    compressext .gz
    compressoptions -9
    # Keep detailed statistics
    prerotate
        echo "[$(date)] Access log stats before rotation:" >> {self.log_paths['access']}/stats.log
        wc -l {self.log_paths['access']}/*.log >> {self.log_paths['access']}/stats.log
    endscript
}}

# API Logs (with monitoring)
{self.log_paths['app']}/api/*.log {{
    hourly
    rotate 48
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 20M
    # Monitor API errors
    prerotate
        if grep -i "error" {self.log_paths['app']}/api/*.log > /dev/null; then
            echo "[$(date)] API errors detected" | mail -s "API Error Alert" {os.getenv('USER')}@localhost
        fi
    endscript
}}

# Security Logs (with special handling)
{self.log_paths['app']}/security/*.log {{
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
    create 0600 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 10M
    # Special handling for security logs
    prerotate
        echo "[$(date)] Security log backup starting" >> {self.log_paths['app']}/security/audit.log
    endscript
    postrotate
        # Create checksum for rotated logs
        for f in {self.log_paths['app']}/security/*.gz; do
            sha256sum "$f" >> {self.log_paths['app']}/security/checksums.log
        done
    endscript
}}

# Performance Logs (with analytics)
{self.log_paths['app']}/performance/*.log {{
    hourly
    rotate 168
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 50M
    # Generate performance statistics
    prerotate
        echo "[$(date)] Performance stats:" >> {self.log_paths['app']}/performance/analysis.log
        grep "response_time" {self.log_paths['app']}/performance/*.log | \
        awk '{{ sum += $NF; count++ }} END {{ print "Average response time: " sum/count }}' \
        >> {self.log_paths['app']}/performance/analysis.log
    endscript
}}

# Backup Logs (with verification)
{self.log_paths['app']}/backup/*.log {{
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 100M
    # Verify backup integrity
    postrotate
        for f in {self.log_paths['app']}/backup/*.gz; do
            if ! gzip -t "$f" 2>/dev/null; then
                echo "[$(date)] Backup integrity check failed: $f" | \
                mail -s "Backup Log Error" {os.getenv('USER')}@localhost
            fi
        done
    endscript
}}
"""
        try:
            # Create logrotate.d directory if it doesn't exist
            self.logrotate_dir.mkdir(parents=True, exist_ok=True)
            
            # Backup existing config if it exists
            if self.logrotate_conf.exists():
                backup_path = self.logrotate_conf.with_suffix('.bak')
                shutil.copy2(self.logrotate_conf, backup_path)
                print(f"✓ Backed up existing configuration to {backup_path}")
            
            # Write new configuration
            with open(self.logrotate_conf, 'w') as f:
                f.write(config)
            print(f"✓ Created logrotate configuration: {self.logrotate_conf}")
            
            # Set correct permissions
            subprocess.run(['sudo', 'chmod', '644', str(self.logrotate_conf)])
            return True
            
        except Exception as e:
            print(f"✗ Failed to create logrotate configuration: {e}")
            return False

    def setup_cron(self):
        """Set up cron job for logrotate"""
        try:
            cron_cmd = f"0 * * * * /usr/local/sbin/logrotate {self.logrotate_conf}"
            
            # Get existing crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_crontab = result.stdout if result.returncode == 0 else ""
            
            if cron_cmd not in current_crontab:
                new_crontab = current_crontab.rstrip() + f"\n{cron_cmd}\n"
                subprocess.run(['crontab', '-'], input=new_crontab, text=True)
                print("✓ Added logrotate cron job")
            else:
                print("✓ Logrotate cron job already exists")
            return True
            
        except Exception as e:
            print(f"✗ Failed to set up cron job: {e}")
            return False

    def test_configuration(self):
        """Test logrotate configuration"""
        try:
            result = subprocess.run(
                ['logrotate', '-d', str(self.logrotate_conf)],
                capture_output=True,
                text=True
            )
            print("\nTesting configuration:")
            print(result.stdout)
            return "error" not in result.stderr.lower()
        except Exception as e:
            print(f"✗ Failed to test configuration: {e}")
            return False

    def setup_nginx_permissions(self):
        """Set up proper Nginx log permissions"""
        try:
            nginx_log_dir = self.log_paths['nginx']
            print(f"\nSetting up Nginx log permissions...")
            
            # Create nginx group if it doesn't exist
            subprocess.run(['sudo', 'groupadd', '-f', 'adm'], check=True)
            
            # Create www-data user if it doesn't exist
            subprocess.run(['sudo', 'useradd', '-r', '-g', 'adm', 'www-data'], 
                         check=False)  # Ignore if user exists
            
            # Set proper ownership and permissions
            subprocess.run(['sudo', 'chown', '-R', 'www-data:adm', str(nginx_log_dir)])
            subprocess.run(['sudo', 'chmod', '-R', '0750', str(nginx_log_dir)])
            
            print("✓ Nginx permissions set successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to set Nginx permissions: {e}")
            return False

    def setup(self):
        """Run complete logrotate setup"""
        print("=== Setting up Logrotate ===")
        
        steps = [
            (self.create_log_directories, "Creating log directories"),
            (self.setup_nginx_permissions, "Setting up Nginx permissions"),
            (self.create_logrotate_config, "Creating logrotate configuration"),
            (self.setup_cron, "Setting up cron job"),
            (self.test_configuration, "Testing configuration")
        ]
        
        for step_func, description in steps:
            print(f"\n{description}...")
            if not step_func():
                print(f"\n✗ Failed during: {description}")
                return False
        
        print("\n✓ Logrotate setup completed successfully!")
        print("\nUseful commands:")
        print("1. Test configuration: logrotate -d /usr/local/etc/logrotate.d/streamad")
        print("2. Force rotation: sudo logrotate -f /usr/local/etc/logrotate.d/streamad")
        print("3. View cron jobs: crontab -l")
        print("4. Check Nginx logs: ls -l /var/log/nginx/")
        return True

if __name__ == "__main__":
    setup = LogrotateSetup()
    setup.setup() 