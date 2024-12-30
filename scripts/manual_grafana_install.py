#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import requests
import tarfile
import shutil

class GrafanaManualInstaller:
    def __init__(self):
        self.version = "8.5.27"
        self.install_dir = Path("/usr/local/grafana")
        self.data_dir = Path("/usr/local/var/lib/grafana")
        self.log_dir = Path("/usr/local/var/log/grafana")
        self.config_dir = Path("/usr/local/etc/grafana")

    def download_grafana(self):
        """Download Grafana binary"""
        print("Downloading Grafana...")
        url = f"https://dl.grafana.com/oss/release/grafana-{self.version}.darwin-amd64.tar.gz"
        response = requests.get(url, stream=True)
        tar_file = Path(f"grafana-{self.version}.tar.gz")
        
        with open(tar_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return tar_file

    def install(self):
        """Install Grafana manually"""
        try:
            # First set up directories with sudo
            print("Setting up directories...")
            for directory in [self.install_dir, self.data_dir, self.log_dir, self.config_dir]:
                if not directory.exists():
                    try:
                        # Try creating directory with sudo
                        subprocess.run([
                            'sudo', 'mkdir', '-p', str(directory)
                        ], check=True)
                        # Change ownership to current user
                        subprocess.run([
                            'sudo', 'chown', f'{os.getenv("USER")}', str(directory)
                        ], check=True)
                        print(f"✓ Created directory: {directory}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error creating directory {directory}: {e}")
                        raise

            # Download
            tar_file = self.download_grafana()

            # Extract
            print("Extracting...")
            with tarfile.open(tar_file) as tar:
                tar_dir = Path("./grafana_temp")
                tar_dir.mkdir(exist_ok=True)
                tar.extractall(path=tar_dir)

            # Move files with sudo
            print("Installing files...")
            extracted_dir = tar_dir / f"grafana-{self.version}"
            if extracted_dir.exists():
                try:
                    # Copy files with sudo
                    subprocess.run([
                        'sudo', 'cp', '-R', 
                        str(extracted_dir) + '/.', 
                        str(self.install_dir)
                    ], check=True)
                    print("✓ Files copied successfully")
                except subprocess.CalledProcessError as e:
                    print(f"Error copying files: {e}")
                    raise

            # Set permissions recursively
            print("Setting permissions...")
            try:
                subprocess.run([
                    'sudo', 'chown', '-R',
                    f'{os.getenv("USER")}:staff',
                    str(self.install_dir)
                ], check=True)
                subprocess.run([
                    'sudo', 'chown', '-R',
                    f'{os.getenv("USER")}:staff',
                    str(self.data_dir)
                ], check=True)
                subprocess.run([
                    'sudo', 'chown', '-R',
                    f'{os.getenv("USER")}:staff',
                    str(self.log_dir)
                ], check=True)
                subprocess.run([
                    'sudo', 'chmod', '-R',
                    '755',
                    str(self.install_dir)
                ], check=True)
                print("✓ Permissions set successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error setting permissions: {e}")
                raise

            # Create launch agent
            print("Creating launch agent...")
            self.create_launch_agent()

            print("✓ Grafana installed successfully")
            print("\nYou can access Grafana at: http://localhost:3000")
            print("Default credentials: admin/admin")
            
        except Exception as e:
            print(f"Error installing Grafana: {e}")
            raise
        finally:
            # Cleanup
            if 'tar_file' in locals() and tar_file.exists():
                tar_file.unlink()
            if 'tar_dir' in locals() and tar_dir.exists():
                shutil.rmtree(tar_dir)

    def create_launch_agent(self):
        """Create LaunchAgent for Grafana"""
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.grafana.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.install_dir}/bin/grafana-server</string>
        <string>--config</string>
        <string>{self.config_dir}/grafana.ini</string>
        <string>--homepath</string>
        <string>{self.install_dir}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{self.log_dir}/grafana-stderr.log</string>
    <key>StandardOutPath</key>
    <string>{self.log_dir}/grafana-stdout.log</string>
</dict>
</plist>"""

        plist_path = Path.home() / "Library/LaunchAgents/com.grafana.server.plist"
        with open(plist_path, 'w') as f:
            f.write(plist_content)

        # Load launch agent
        subprocess.run(['launchctl', 'load', str(plist_path)])

if __name__ == "__main__":
    installer = GrafanaManualInstaller()
    installer.install() 