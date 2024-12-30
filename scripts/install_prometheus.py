#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import requests
import tarfile
import shutil
import time

class PrometheusInstaller:
    def __init__(self):
        self.version = "2.32.1"  # This version is compatible with macOS 10.15
        self.install_dir = Path("/usr/local/prometheus")
        self.data_dir = Path("/usr/local/var/prometheus")
        self.config_dir = Path("/usr/local/etc/prometheus")
        self.log_dir = Path("/usr/local/var/log/prometheus")

    def download_prometheus(self):
        """Download Prometheus binary"""
        print("Downloading Prometheus...")
        url = f"https://github.com/prometheus/prometheus/releases/download/v{self.version}/prometheus-{self.version}.darwin-amd64.tar.gz"
        response = requests.get(url, stream=True)
        tar_file = Path(f"prometheus-{self.version}.tar.gz")
        
        with open(tar_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return tar_file

    def create_config(self):
        """Create Prometheus configuration"""
        config = """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'grafana'
    static_configs:
      - targets: ['localhost:3000']

  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
"""
        config_file = self.config_dir / "prometheus.yml"
        with open(config_file, 'w') as f:
            f.write(config)
        return config_file

    def create_launch_agent(self):
        """Create LaunchAgent for Prometheus"""
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.prometheus.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.install_dir}/prometheus</string>
        <string>--config.file={self.config_dir}/prometheus.yml</string>
        <string>--storage.tsdb.path={self.data_dir}</string>
        <string>--web.console.templates={self.install_dir}/consoles</string>
        <string>--web.console.libraries={self.install_dir}/console_libraries</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{self.log_dir}/prometheus.err.log</string>
    <key>StandardOutPath</key>
    <string>{self.log_dir}/prometheus.log</string>
    <key>WorkingDirectory</key>
    <string>{self.install_dir}</string>
</dict>
</plist>"""

        plist_path = Path.home() / "Library/LaunchAgents/com.prometheus.server.plist"
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        return plist_path

    def install(self):
        """Install Prometheus"""
        try:
            print("\n=== Installing Prometheus ===")
            
            # Create directories with sudo
            for directory in [self.install_dir, self.data_dir, self.config_dir, self.log_dir]:
                if not directory.exists():
                    print(f"Creating directory: {directory}")
                    subprocess.run(['sudo', 'mkdir', '-p', str(directory)], check=True)
                    subprocess.run(['sudo', 'chown', f'{os.getenv("USER")}', str(directory)], check=True)

            # Download and extract
            tar_file = self.download_prometheus()
            print("Extracting files...")
            with tarfile.open(tar_file) as tar:
                temp_dir = Path("./prometheus_temp")
                temp_dir.mkdir(exist_ok=True)
                tar.extractall(temp_dir)

            # Copy files
            extracted_dir = temp_dir / f"prometheus-{self.version}.darwin-amd64"
            print("Installing files...")
            for item in ['prometheus', 'promtool', 'consoles', 'console_libraries']:
                src = extracted_dir / item
                dst = self.install_dir / item
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

            # Create configuration
            print("Creating configuration...")
            self.create_config()

            # Create and load launch agent
            print("Setting up launch agent...")
            plist_path = self.create_launch_agent()
            subprocess.run(['launchctl', 'unload', str(plist_path)], check=False)
            subprocess.run(['launchctl', 'load', str(plist_path)], check=True)

            print("\n✓ Prometheus installed successfully!")
            print(f"Configuration file: {self.config_dir}/prometheus.yml")
            print("Access Prometheus at: http://localhost:9090")

        except Exception as e:
            print(f"Error installing Prometheus: {e}")
            raise
        finally:
            # Cleanup
            if 'tar_file' in locals() and tar_file.exists():
                tar_file.unlink()
            if 'temp_dir' in locals() and temp_dir.exists():
                shutil.rmtree(temp_dir)

    def verify_installation(self):
        """Verify Prometheus installation"""
        print("\nVerifying installation...")
        time.sleep(5)  # Wait for Prometheus to start

        try:
            # Check if process is running
            result = subprocess.run(['pgrep', '-f', 'prometheus'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Prometheus process is running")
            else:
                print("✗ Prometheus process is not running")

            # Check HTTP endpoint
            response = requests.get('http://localhost:9090/-/healthy')
            if response.status_code == 200:
                print("✓ Prometheus is responding to HTTP requests")
            else:
                print(f"✗ Prometheus returned status code: {response.status_code}")

        except Exception as e:
            print(f"Error verifying installation: {e}")

if __name__ == "__main__":
    installer = PrometheusInstaller()
    installer.install()
    installer.verify_installation() 