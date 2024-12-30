#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import shutil

class LogrotateInstaller:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.log_dirs = {
            'app': self.project_root / "logs",
            'nginx': self.project_root / "nginx/logs",
            'prometheus': Path("/usr/local/var/log/prometheus"),
            'grafana': Path("/usr/local/var/log/grafana")
        }
        self.logrotate_dir = Path("/usr/local/etc/logrotate.d")
        self.logrotate_conf = self.logrotate_dir / "streamad"

    def install_logrotate(self):
        """Install logrotate using Homebrew"""
        try:
            print("\n=== Installing Logrotate ===")
            subprocess.run(['brew', 'install', 'logrotate'], check=True)
            print("✓ Logrotate installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install logrotate: {e}")
            return False

    def create_directories(self):
        """Create necessary directories with proper permissions"""
        print("\nCreating log directories...")
        
        for name, directory in self.log_dirs.items():
            try:
                # First try to create with sudo
                print(f"Creating {name} log directory: {directory}")
                
                if not directory.exists():
                    try:
                        # Create directory with sudo
                        subprocess.run([
                            'sudo', 'mkdir', '-p', str(directory)
                        ], check=True)
                        
                        # Set ownership
                        subprocess.run([
                            'sudo', 'chown', '-R',
                            f'{os.getenv("USER")}:staff',
                            str(directory)
                        ], check=True)
                        
                        # Set permissions
                        subprocess.run([
                            'sudo', 'chmod', '-R', '755',
                            str(directory)
                        ], check=True)
                        
                        print(f"✓ Created {name} log directory with proper permissions")
                    except subprocess.CalledProcessError as e:
                        print(f"✗ Failed to create {name} directory with sudo: {e}")
                        raise
                else:
                    print(f"✓ Directory already exists: {directory}")
                    
                    # Ensure proper permissions on existing directory
                    subprocess.run([
                        'sudo', 'chown', '-R',
                        f'{os.getenv("USER")}:staff',
                        str(directory)
                    ], check=True)
                    subprocess.run([
                        'sudo', 'chmod', '-R', '755',
                        str(directory)
                    ], check=True)
                    
            except Exception as e:
                print(f"✗ Error setting up {name} directory: {e}")
                print("\nTry running these commands manually:")
                print(f"sudo mkdir -p {directory}")
                print(f"sudo chown -R $(whoami):staff {directory}")
                print(f"sudo chmod -R 755 {directory}")
                return False
        
        return True

    def create_config(self):
        """Create custom logrotate configuration"""
        config = f"""# Custom Logrotate configuration for StreamAdExchange

# Application logs
{self.log_dirs['app']}/*.log {{
    # Rotate logs daily
    daily
    
    # Keep 7 days of logs
    rotate 7
    
    # Compress old logs with gzip
    compress
    delaycompress
    
    # Don't error if log file is missing
    missingok
    
    # Don't rotate empty log files
    notifempty
    
    # Create new log files with these permissions
    create 0644 {os.getenv('USER')} staff
    
    # Add date extension to rotated logs
    dateext
    dateformat -%Y%m%d-%s
    
    # Copy and truncate instead of moving files
    copytruncate
    
    # Maximum size before rotation (optional)
    size 50M
    
    # Custom script before rotation (optional)
    prerotate
        echo "Backing up logs for $(date)" >> {self.log_dirs['app']}/rotation.log
    endscript
}}

# Nginx logs with custom settings
{self.log_dirs['nginx']}/*.log {{
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%s
    size 100M
    postrotate
        [ ! -f {self.project_root}/nginx/run/nginx.pid ] || kill -USR1 $(cat {self.project_root}/nginx/run/nginx.pid)
    endscript
}}

# Prometheus logs with monitoring
{self.log_dirs['prometheus']}/*.log {{
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%s
    size 50M
    postrotate
        echo "Rotated Prometheus logs on $(date)" >> {self.log_dirs['prometheus']}/rotation.log
    endscript
}}

# Grafana logs with custom retention
{self.log_dirs['grafana']}/*.log {{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%s
    size 50M
    postrotate
        echo "Rotated Grafana logs on $(date)" >> {self.log_dirs['grafana']}/rotation.log
    endscript
}}

# Debug logs with different settings
{self.log_dirs['app']}/debug/*.log {{
    # Rotate more frequently for debug logs
    hourly
    rotate 24
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%H%M
    size 10M
}}

# Error logs with special handling
{self.log_dirs['app']}/error/*.log {{
    # Keep error logs longer
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER')} staff
    dateext
    dateformat -%Y%m%d-%s
    # Email notifications for error log rotations
    mail {os.getenv('USER')}@localhost
    mailfirst
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
            print(f"✓ Created custom logrotate configuration: {self.logrotate_conf}")
            
            # Test the configuration
            result = subprocess.run(
                ['logrotate', '-d', str(self.logrotate_conf)],
                capture_output=True,
                text=True
            )
            if "error" in result.stderr.lower():
                print("✗ Configuration test failed:")
                print(result.stderr)
                # Restore backup if test failed
                if backup_path.exists():
                    shutil.copy2(backup_path, self.logrotate_conf)
                    print("✓ Restored previous configuration")
                return False
            
            print("✓ Configuration test passed")
            return True
            
        except Exception as e:
            print(f"✗ Failed to create configuration: {e}")
            return False

    def setup_cron(self):
        """Set up daily cron job for logrotate"""
        try:
            print("\nSetting up cron job...")
            cron_cmd = f"0 0 * * * /usr/local/sbin/logrotate {self.logrotate_conf}"
            
            # Get existing crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_crontab = result.stdout if result.returncode == 0 else ""
            
            # Add our entry if it's not already there
            if cron_cmd not in current_crontab:
                new_crontab = current_crontab.rstrip() + f"\n{cron_cmd}\n"
                subprocess.run(['crontab', '-'], input=new_crontab, text=True)
                print("✓ Added cron job for logrotate")
            else:
                print("✓ Cron job already exists")
            return True
        except Exception as e:
            print(f"✗ Failed to set up cron job: {e}")
            return False

    def test_config(self):
        """Test logrotate configuration"""
        try:
            print("\nTesting logrotate configuration...")
            result = subprocess.run(
                ['logrotate', '-d', str(self.logrotate_conf)],
                capture_output=True,
                text=True
            )
            print("\nConfiguration test output:")
            print(result.stdout)
            return True
        except Exception as e:
            print(f"✗ Failed to test configuration: {e}")
            return False

    def set_permissions(self):
        """Set correct permissions for log directories"""
        print("\nSetting permissions...")
        try:
            for directory in self.log_dirs.values():
                subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}:staff', str(directory)])
                subprocess.run(['sudo', 'chmod', '-R', '755', str(directory)])
            print("✓ Permissions set successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to set permissions: {e}")
            return False

    def install(self):
        """Run complete logrotate setup"""
        steps = [
            (self.install_logrotate, "Installing logrotate"),
            (self.create_directories, "Creating directories"),
            (self.create_config, "Creating configuration"),
            (self.set_permissions, "Setting permissions"),
            (self.setup_cron, "Setting up cron job"),
            (self.test_config, "Testing configuration")
        ]

        for step_func, description in steps:
            print(f"\n=== {description} ===")
            if not step_func():
                print(f"\n✗ Failed during: {description}")
                return False

        print("\n✓ Logrotate setup completed successfully!")
        print("\nUseful commands:")
        print("1. Test configuration: logrotate -d /usr/local/etc/logrotate.d/streamad")
        print("2. Force rotation: sudo logrotate -f /usr/local/etc/logrotate.d/streamad")
        print("3. View cron jobs: crontab -l")
        return True

if __name__ == "__main__":
    installer = LogrotateInstaller()
    installer.install() 