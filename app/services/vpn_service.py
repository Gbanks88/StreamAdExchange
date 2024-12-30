import subprocess
import os
import logging
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict
import psutil
import time
import threading
import sys

class VPNService:
    def __init__(self, config_dir='vpn'):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.config = self.load_config()
        self.setup_logging()
        self.bandwidth_stats = defaultdict(lambda: {
            'rx_bytes': 0,
            'tx_bytes': 0,
            'last_update': datetime.now()
        })
        self.start_bandwidth_monitor()

    def setup_logging(self):
        log_dir = self.config_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger('vpn_service')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(
            log_dir / f'vpn_{datetime.now().strftime("%Y%m%d")}.log'
        )
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(handler)

    def load_config(self):
        config_file = self.config_dir / 'vpn_config.json'
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        
        # Default configuration
        default_config = {
            "server": {
                "port": 1194,
                "protocol": "udp",
                "subnet": "10.8.0.0",
                "subnet_mask": "255.255.255.0",
                "cipher": "AES-256-GCM",
                "auth": "SHA256"
            },
            "clients": [],
            "dns_servers": [
                "8.8.8.8",
                "8.8.4.4"
            ]
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

    def install_openvpn(self):
        """Install OpenVPN server"""
        try:
            self.logger.info("Installing OpenVPN...")
            if sys.platform == "darwin":  # macOS
                subprocess.run(['brew', 'update'])
                subprocess.run(['brew', 'install', 'openvpn'])
                subprocess.run(['brew', 'install', 'nginx'])
                self.configure_nginx()  # Configure nginx after installation
            else:  # Linux
                subprocess.run(['sudo', 'apt-get', 'update'])
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'openvpn'])
            
            self.logger.info("OpenVPN installed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to install OpenVPN: {e}")
            return False

    def generate_server_keys(self):
        """Generate server certificates and keys"""
        try:
            easy_rsa_dir = self.config_dir / 'easy-rsa'
            if not easy_rsa_dir.exists():
                subprocess.run(['make-cadir', str(easy_rsa_dir)])
            
            os.chdir(str(easy_rsa_dir))
            subprocess.run(['./easyrsa', 'init-pki'])
            subprocess.run(['./easyrsa', 'build-ca', 'nopass'])
            subprocess.run(['./easyrsa', 'build-server-full', 'server', 'nopass'])
            subprocess.run(['./easyrsa', 'gen-dh'])
            
            self.logger.info("Server certificates generated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate server certificates: {e}")
            return False

    def generate_client_config(self, client_name):
        """Generate client configuration"""
        try:
            easy_rsa_dir = self.config_dir / 'easy-rsa'
            os.chdir(str(easy_rsa_dir))
            
            # Generate client certificates
            subprocess.run(['./easyrsa', 'build-client-full', client_name, 'nopass'])
            
            # Create client config
            client_dir = self.config_dir / 'clients' / client_name
            client_dir.mkdir(parents=True, exist_ok=True)
            
            client_config = f"""client
dev tun
proto {self.config['server']['protocol']}
remote {self.get_server_ip()} {self.config['server']['port']}
resolv-retry infinite
nobind
persist-key
persist-tun
cipher {self.config['server']['cipher']}
auth {self.config['server']['auth']}
verb 3
"""
            
            with open(client_dir / f'{client_name}.ovpn', 'w') as f:
                f.write(client_config)
            
            # Add client to config
            self.config['clients'].append({
                'name': client_name,
                'created_at': datetime.now().isoformat()
            })
            self.save_config()
            
            self.logger.info(f"Client configuration generated for {client_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate client configuration: {e}")
            return False

    def get_server_ip(self):
        """Get server's public IP"""
        try:
            import requests
            return requests.get('https://api.ipify.org').text
        except:
            return 'YOUR_SERVER_IP'

    def save_config(self):
        """Save current configuration"""
        with open(self.config_dir / 'vpn_config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def start_server(self):
        """Start OpenVPN server"""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(['brew', 'services', 'start', 'openvpn'])
                subprocess.run(['brew', 'services', 'start', 'nginx'])
            else:  # Linux
                subprocess.run(['sudo', 'service', 'openvpn', 'start'])
            
            self.logger.info("OpenVPN server started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start OpenVPN server: {e}")
            return False

    def stop_server(self):
        """Stop OpenVPN server"""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(['brew', 'services', 'stop', 'openvpn'])
                subprocess.run(['brew', 'services', 'stop', 'nginx'])
            else:  # Linux
                subprocess.run(['sudo', 'service', 'openvpn', 'stop'])
            
            self.logger.info("OpenVPN server stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop OpenVPN server: {e}")
            return False

    def start_bandwidth_monitor(self):
        """Start bandwidth monitoring in a separate thread"""
        self.monitor_thread = threading.Thread(
            target=self._monitor_bandwidth,
            daemon=True
        )
        self.monitor_thread.start()

    def _monitor_bandwidth(self):
        """Monitor bandwidth usage for VPN interface"""
        while True:
            try:
                # Get network stats for tun0 (OpenVPN interface)
                stats = psutil.net_io_counters(pernic=True).get('tun0')
                if stats:
                    for client in self.config['clients']:
                        client_ip = self._get_client_ip(client['name'])
                        if client_ip:
                            self.bandwidth_stats[client['name']].update({
                                'rx_bytes': stats.bytes_recv,
                                'tx_bytes': stats.bytes_sent,
                                'last_update': datetime.now()
                            })
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.logger.error(f"Bandwidth monitoring error: {e}")
                time.sleep(5)

    def _get_client_ip(self, client_name):
        """Get client IP from OpenVPN status"""
        try:
            with open('/var/log/openvpn/status.log', 'r') as f:
                for line in f:
                    if client_name in line:
                        return line.split(',')[0]
        except Exception as e:
            self.logger.error(f"Error getting client IP: {e}")
        return None

    def get_client_stats(self, client_name):
        """Get bandwidth statistics for a client"""
        stats = self.bandwidth_stats[client_name]
        now = datetime.now()
        time_diff = (now - stats['last_update']).total_seconds()
        
        if time_diff > 0:
            rx_rate = stats['rx_bytes'] / time_diff
            tx_rate = stats['tx_bytes'] / time_diff
        else:
            rx_rate = tx_rate = 0
            
        return {
            'rx_bytes': stats['rx_bytes'],
            'tx_bytes': stats['tx_bytes'],
            'rx_rate': rx_rate,
            'tx_rate': tx_rate,
            'last_update': stats['last_update'].isoformat()
        }

    def revoke_client(self, client_name):
        """Revoke client access"""
        try:
            easy_rsa_dir = self.config_dir / 'easy-rsa'
            os.chdir(str(easy_rsa_dir))
            
            # Revoke certificate
            subprocess.run(['./easyrsa', 'revoke', client_name])
            subprocess.run(['./easyrsa', 'gen-crl'])
            
            # Update client list
            self.config['clients'] = [
                c for c in self.config['clients'] 
                if c['name'] != client_name
            ]
            self.save_config()
            
            # Disconnect client
            self._disconnect_client(client_name)
            
            self.logger.info(f"Client {client_name} revoked successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to revoke client {client_name}: {e}")
            return False

    def _disconnect_client(self, client_name):
        """Force disconnect a client"""
        try:
            client_ip = self._get_client_ip(client_name)
            if client_ip:
                subprocess.run([
                    'sudo', 'killall', '-HUP', 
                    '-u', f'vpn_{client_name}', 'openvpn'
                ])
                self.logger.info(f"Client {client_name} disconnected")
        except Exception as e:
            self.logger.error(f"Error disconnecting client: {e}")

    def get_status(self):
        """Enhanced status information"""
        status = super().get_status()
        status.update({
            'active_connections': self._get_active_connections(),
            'bandwidth_usage': self._get_total_bandwidth(),
            'uptime': self._get_server_uptime()
        })
        return status

    def _get_active_connections(self):
        """Get list of currently connected clients"""
        active = []
        try:
            with open('/var/log/openvpn/status.log', 'r') as f:
                for line in f:
                    if 'CLIENT_LIST' in line:
                        parts = line.split(',')
                        active.append({
                            'name': parts[1],
                            'ip': parts[0],
                            'connected_since': parts[4]
                        })
        except Exception as e:
            self.logger.error(f"Error getting active connections: {e}")
        return active

    def _get_total_bandwidth(self):
        """Get total bandwidth usage"""
        total_rx = total_tx = 0
        for stats in self.bandwidth_stats.values():
            total_rx += stats['rx_bytes']
            total_tx += stats['tx_bytes']
        return {
            'rx_total': total_rx,
            'tx_total': total_tx
        }

    def _get_server_uptime(self):
        """Get VPN server uptime"""
        try:
            result = subprocess.run(
                ['systemctl', 'show', 'openvpn@server', '--property=ActiveEnterTimestamp'],
                capture_output=True,
                text=True
            )
            start_time = datetime.fromisoformat(result.stdout.split('=')[1].strip())
            uptime = datetime.now() - start_time
            return str(uptime)
        except Exception as e:
            self.logger.error(f"Error getting server uptime: {e}")
            return "Unknown" 

    def configure_nginx(self):
        """Configure nginx for the application"""
        try:
            nginx_config = f"""server {{
    listen 80;
    server_name {self.get_server_ip()};

    location / {{
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}

    location /static {{
        alias /Volumes/Learn_Space/StreamAdExchange/app/static;
    }}
}}"""
            
            config_path = "/Volumes/Learn_Space/StreamAdExchange/nginx/sites-available/streamad.conf"
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                f.write(nginx_config)
            
            # Create symbolic link
            enabled_path = "/Volumes/Learn_Space/StreamAdExchange/nginx/sites-enabled/streamad.conf"
            if not os.path.exists(enabled_path):
                os.symlink(config_path, enabled_path)
            
            # Test and reload nginx
            subprocess.run(['nginx', '-t'])
            subprocess.run(['nginx', '-s', 'reload'])
            
            self.logger.info("Nginx configured successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to configure nginx: {e}")
            return False 