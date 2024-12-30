#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import json
import yaml
from datetime import datetime
import socket
from typing import List
import time

class SecuritySetup:
    def __init__(self):
        env = os.getenv('STREAMAD_ENV', 'local')
        base_dir = Path("/Volumes/Learn_Space/StreamAdExchange" if env == "local" 
                        else "/opt/streamadexchange")
        self.project_root = base_dir
        self.config_dir = self.project_root / "config"
        self.firewall_rules = self.config_dir / "firewall_rules.json"
        self.security_config = self.config_dir / f"security_{env}.yml"
        
        # Define allowed ports and services
        self.allowed_ports = {
            80: "HTTP",
            443: "HTTPS",
            3000: "Grafana",
            9090: "Prometheus",
            9100: "Node Exporter",
            9113: "Nginx Exporter",
            5000: "Flask App"
        }

    def check_open_ports(self):
        """Check for open ports and running services"""
        print("\nChecking open ports...")
        try:
            result = subprocess.run(['lsof', '-i', '-P', '-n'], 
                                 capture_output=True, 
                                 text=True)
            
            open_ports = set()
            for line in result.stdout.splitlines():
                if "LISTEN" in line:
                    parts = line.split()
                    for part in parts:
                        if ':' in part:
                            try:
                                port = int(part.split(':')[-1])
                                open_ports.add(port)
                            except ValueError:
                                continue
            
            print("\nOpen ports:")
            for port in sorted(open_ports):
                status = "✓ Allowed" if port in self.allowed_ports else "✗ Unknown"
                service = self.allowed_ports.get(port, "Unknown service")
                print(f"Port {port}: {status} ({service})")
                
            return open_ports
            
        except Exception as e:
            print(f"Error checking ports: {e}")
            return set()

    def setup_firewall(self):
        """Configure firewall rules"""
        print("\nSetting up firewall rules...")
        try:
            # Create firewall rules
            rules = {
                "allowed_ports": list(self.allowed_ports.keys()),
                "allowed_ips": ["127.0.0.1"],  # Add your allowed IPs
                "blocked_ips": []  # Add IPs to block
            }
            
            # Save rules
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.firewall_rules, 'w') as f:
                json.dump(rules, f, indent=4)
            
            # Create pf rules file with proper syntax
            pf_rules = """# StreamAdExchange Firewall Rules
# Interfaces
set skip on lo0

# Options
set block-policy drop
set fingerprints "/etc/pf.os"

# Normalization
scrub in all

# Default blocking
block all

# Allow established connections
pass out all keep state
pass in proto tcp from any to any flags S/SA keep state

# Allow specific services
"""
            # Add rules for allowed ports
            for port, service in self.allowed_ports.items():
                pf_rules += f"pass in proto tcp from any to any port {port} flags S/SA keep state # {service}\n"
            
            pf_file = self.config_dir / "pf.conf"
            with open(pf_file, 'w') as f:
                f.write(pf_rules)
            
            # Test pf configuration
            try:
                result = subprocess.run(
                    ['sudo', 'pfctl', '-nf', str(pf_file)], 
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("✓ Firewall configuration validated")
            except subprocess.CalledProcessError as e:
                print(f"✗ Invalid firewall configuration: {e.stderr}")
                return False
            
            # Load pf rules
            try:
                # Enable pf if not already enabled
                subprocess.run(['sudo', 'pfctl', '-E'], check=False)
                # Load the rules
                subprocess.run(['sudo', 'pfctl', '-f', str(pf_file)], check=True)
                print("✓ Firewall rules applied successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"✗ Error applying firewall rules: {e}")
                return False
            
        except Exception as e:
            print(f"✗ Error setting up firewall: {e}")
            return False

    def harden_nginx(self):
        """Apply security hardening to Nginx"""
        print("\nHardening Nginx configuration...")
        try:
            nginx_conf = """
# Security headers
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header X-Content-Type-Options "nosniff";
add_header Content-Security-Policy "default-src 'self'";
add_header Referrer-Policy "strict-origin-when-cross-origin";

# SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# Rate limiting
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
limit_req zone=one burst=20 nodelay;

# Basic DDoS protection
client_body_timeout 10s;
client_header_timeout 10s;
keepalive_timeout 5s 5s;
send_timeout 10s;
"""
            nginx_security_conf = self.project_root / "nginx/conf.d/security.conf"
            nginx_security_conf.parent.mkdir(parents=True, exist_ok=True)
            
            with open(nginx_security_conf, 'w') as f:
                f.write(nginx_conf)
            
            print("✓ Nginx security configuration created")
            return True
            
        except Exception as e:
            print(f"Error hardening Nginx: {e}")
            return False

    def setup_monitoring_alerts(self):
        """Configure Prometheus alerting rules"""
        print("\nSetting up monitoring alerts...")
        try:
            alerts = {
                'groups': [{
                    'name': 'security_alerts',
                    'rules': [
                        {
                            'alert': 'HighErrorRate',
                            'expr': 'rate(nginx_http_requests_total{status=~"5.."}[5m]) > 1',
                            'for': '5m',
                            'labels': {'severity': 'critical'},
                            'annotations': {
                                'summary': 'High HTTP error rate',
                                'description': 'Error rate is {{ $value }} per second'
                            }
                        },
                        {
                            'alert': 'UnusualTraffic',
                            'expr': 'rate(nginx_http_requests_total[5m]) > 100',
                            'for': '5m',
                            'labels': {'severity': 'warning'},
                            'annotations': {
                                'summary': 'Unusual traffic pattern detected',
                                'description': 'Request rate is {{ $value }} per second'
                            }
                        }
                    ]
                }]
            }
            
            alerts_file = self.project_root / "prometheus/rules/security_alerts.yml"
            alerts_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(alerts_file, 'w') as f:
                yaml.safe_dump(alerts, f)
            
            print("✓ Monitoring alerts configured")
            return True
            
        except Exception as e:
            print(f"Error setting up alerts: {e}")
            return False

    def create_security_report(self):
        """Generate security status report"""
        print("\nGenerating security report...")
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'open_ports': list(self.check_open_ports()),
                'firewall_status': 'enabled',
                'ssl_status': self._check_ssl_status(),
                'updates_available': self._check_updates(),
                'security_headers': self._check_security_headers()
            }
            
            report_file = self.config_dir / f"security_report_{datetime.now():%Y%m%d}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=4)
            
            print(f"✓ Security report saved to {report_file}")
            return True
            
        except Exception as e:
            print(f"Error creating report: {e}")
            return False

    def _check_ssl_status(self):
        """Check SSL certificate status"""
        # Add your SSL checking logic here
        return {'status': 'valid', 'expiry': 'in 30 days'}

    def _check_updates(self):
        """Check for available updates"""
        try:
            result = subprocess.run(['brew', 'outdated'], 
                                 capture_output=True, 
                                 text=True)
            return result.stdout.splitlines()
        except:
            return []

    def _check_security_headers(self):
        """Check security headers"""
        headers = {
            'X-Frame-Options': False,
            'X-XSS-Protection': False,
            'X-Content-Type-Options': False,
            'Content-Security-Policy': False
        }
        
        try:
            response = requests.get('http://localhost')
            for header in headers:
                headers[header] = header in response.headers
        except:
            pass
            
        return headers

    def check_running_services(self):
        """Check status of critical services"""
        print("\nChecking running services...")
        services = {
            'balt_integration': {
                'process_name': 'python3.*balt_integration',  # Using regex to match python process
                'port': 5000,
                'pid_file': self.project_root / 'balt.pid'
            },
            'flask_app': {
                'process_name': 'gunicorn.*app:app',
                'port': 8000,
                'pid_file': self.project_root / 'flask.pid'
            },
            'nginx': {
                'process_name': 'nginx.*master',
                'port': 80,
                'pid_file': Path('/usr/local/var/run/nginx.pid')
            }
        }
        
        for service_name, config in services.items():
            print(f"\nChecking {service_name}...")
            try:
                # Check PID file
                pid = None
                if config['pid_file'].exists():
                    pid = config['pid_file'].read_text().strip()
                    print(f"  PID file: {pid}")
                
                # Check process using pgrep with extended regex
                result = subprocess.run(
                    ['pgrep', '-f', config['process_name']], 
                    capture_output=True, 
                    text=True
                )
                process_running = result.returncode == 0
                running_pids = result.stdout.strip().split('\n') if process_running else []
                
                # Check port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port_open = sock.connect_ex(('127.0.0.1', config['port'])) == 0
                sock.close()
                
                # Detailed status report
                if process_running:
                    print(f"  ✓ Process found: PIDs {', '.join(running_pids)}")
                    if pid and pid not in running_pids:
                        print(f"  ⚠️  PID file ({pid}) doesn't match running process")
                else:
                    print("  ✗ Process not found")
                
                if port_open:
                    print(f"  ✓ Port {config['port']} is open")
                else:
                    print(f"  ✗ Port {config['port']} is not responding")
                
                # Get process details if running
                if process_running:
                    for pid in running_pids:
                        try:
                            ps_result = subprocess.run(
                                ['ps', '-p', pid, '-o', 'pid,ppid,%cpu,%mem,start,time,command'],
                                capture_output=True,
                                text=True
                            )
                            print(f"\n  Process details:\n    {ps_result.stdout.replace('\n', '\n    ')}")
                        except Exception as e:
                            print(f"  ⚠️  Could not get process details: {e}")
                
            except Exception as e:
                print(f"  ✗ Error checking {service_name}: {e}")

    def check_balt_ix(self):
        """Check BALT-IX connectivity and costs"""
        print("\nChecking BALT-IX...")
        try:
            from app.balt_ix import BALTIX
            balt_ix = BALTIX()
            
            for peer_id in balt_ix.peers.get("peers", {}):
                analysis = balt_ix.get_cost_analysis(peer_id)
                
                print(f"\nPeer {peer_id}:")
                print(f"  Status: {analysis['connectivity']['status']}")
                
                if 'cost_savings' in analysis:
                    savings = analysis['cost_savings']
                    print("\n  Cost Analysis:")
                    print(f"    Monthly Traffic: {savings['total_traffic_gb']} GB")
                    print(f"    BALT-IX Cost: ${savings['balt_ix_cost']}")
                    print(f"    Traditional Cost: ${savings['traditional_cost']}")
                    print(f"    Savings: ${savings['savings']} ({savings['savings_percentage']}%)")
                
                if 'optimizations' in analysis:
                    print("\n  Optimization Recommendations:")
                    for action in analysis['optimizations']['immediate_actions']:
                        print(f"    • {action}")
            
            return True
        except Exception as e:
            print(f"✗ Error checking BALT-IX: {e}")
            return False

    def monitor_balt_ix(self):
        """Monitor BALT-IX traffic and costs continuously"""
        print("\nStarting BALT-IX monitoring...")
        try:
            from app.balt_ix import BALTIX
            balt_ix = BALTIX()
            
            # Monitor each peer
            for peer_id in balt_ix.peers.get("peers", {}):
                print(f"\nMonitoring Peer {peer_id}...")
                
                # Check current traffic
                if balt_ix.monitor_traffic(peer_id):
                    analysis = balt_ix.get_cost_analysis(peer_id)
                    
                    # Display real-time metrics
                    if analysis["status"] == "success":
                        metrics = analysis.get("connectivity", {}).get("metrics", {})
                        print("  Real-time Metrics:")
                        print(f"    Throughput: {metrics.get('throughput', 0):.2f} Mbps")
                        print(f"    Latency: {metrics.get('latency', 0):.2f} ms")
                        print(f"    Packet Loss: {metrics.get('packet_loss', 0):.2f}%")
                        
                        # Display cost information
                        if "cost_savings" in analysis:
                            savings = analysis["cost_savings"]
                            print("\n  Cost Analysis:")
                            print(f"    Current Tier: {savings['cost_tier']}")
                            print(f"    Monthly Traffic: {savings['total_traffic_gb']:.2f} GB")
                            print(f"    Projected Savings: ${savings['savings']:.2f}")
                            
                        # Display optimization recommendations
                        if "optimizations" in analysis:
                            recommendations = analysis["optimizations"]
                            if recommendations["immediate_actions"]:
                                print("\n  Optimization Recommendations:")
                                for action in recommendations["immediate_actions"]:
                                    print(f"    • {action}")
                    else:
                        print(f"  ✗ Error: {analysis.get('message', 'Unknown error')}")
                else:
                    print(f"  ✗ Failed to monitor traffic for peer {peer_id}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error monitoring BALT-IX: {e}")
            return False

    def setup_cost_alerts(self):
        """Configure automated cost alerts for BALT-IX"""
        print("\nSetting up cost alerts...")
        try:
            alert_config = {
                "thresholds": {
                    "cost_increase": 20,  # Alert if costs increase by 20%
                    "utilization": 80,    # Alert at 80% of committed bandwidth
                    "savings_opportunity": 100  # Alert when potential savings > $100
                },
                "notification": {
                    "slack_webhook": os.environ.get("SLACK_WEBHOOK"),
                    "email": os.environ.get("ALERT_EMAIL"),
                    "enabled": True
                },
                "monitoring": {
                    "interval": 300,  # Check every 5 minutes
                    "retention_days": 90
                }
            }
            
            # Save alert configuration
            alert_config_path = self.config_dir / "cost_alerts.json"
            with open(alert_config_path, 'w') as f:
                json.dump(alert_config, f, indent=4)
            
            # Start monitoring daemon
            monitor_script = """#!/usr/bin/env python3
import time
import json
import sys
from pathlib import Path
from app.balt_ix import BALTIX

def monitor_costs():
    balt_ix = BALTIX()
    while True:
        try:
            for peer_id in balt_ix.peers.get("peers", {}):
                analysis = balt_ix.get_cost_analysis(peer_id)
                if analysis["status"] == "success":
                    check_alerts(peer_id, analysis)
            time.sleep(300)  # Wait 5 minutes
        except Exception as e:
            print(f"Error monitoring costs: {e}", file=sys.stderr)
            time.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    monitor_costs()
"""
            
            monitor_path = self.project_root / "scripts/cost_monitor.py"
            with open(monitor_path, 'w') as f:
                f.write(monitor_script)
            
            # Make script executable
            os.chmod(monitor_path, 0o755)
            
            # Start monitoring in background
            subprocess.Popen(
                [str(monitor_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            print("✓ Cost alerts configured and monitoring started")
            return True
            
        except Exception as e:
            print(f"✗ Error setting up cost alerts: {e}")
            return False

    def check_alerts(self, peer_id: str, analysis: dict):
        """Check if any cost alerts should be triggered"""
        try:
            with open(self.config_dir / "cost_alerts.json") as f:
                alert_config = json.load(f)
            
            alerts = []
            thresholds = alert_config["thresholds"]
            
            # Check cost increase
            if "cost_savings" in analysis:
                savings = analysis["cost_savings"]
                if savings["balt_ix_cost"] > 0:
                    cost_increase = ((savings["balt_ix_cost"] - savings.get("previous_cost", 0)) 
                                   / savings["balt_ix_cost"]) * 100
                    if cost_increase > thresholds["cost_increase"]:
                        alerts.append(f"Cost increased by {cost_increase:.1f}% for peer {peer_id}")
            
            # Check utilization
            if "connectivity" in analysis:
                metrics = analysis["connectivity"].get("metrics", {})
                if "throughput" in metrics:
                    utilization = (metrics["throughput"] / float(
                        analysis["connectivity"]["peer"]["capacity"].rstrip("Gbps")) * 100)
                    if utilization > thresholds["utilization"]:
                        alerts.append(
                            f"High utilization ({utilization:.1f}%) for peer {peer_id}"
                        )
            
            # Check optimization opportunities
            if "optimizations" in analysis:
                for opportunity in analysis["optimizations"].get("cost_saving_opportunities", []):
                    if "savings of $" in opportunity:
                        savings_amount = float(opportunity.split("$")[1].split()[0])
                        if savings_amount > thresholds["savings_opportunity"]:
                            alerts.append(f"Cost saving opportunity: {opportunity}")
            
            # Send alerts if any
            if alerts and alert_config["notification"]["enabled"]:
                self._send_alerts(alerts)
            
        except Exception as e:
            print(f"Error checking alerts: {e}", file=sys.stderr)

    def _send_alerts(self, alerts: List[str]):
        """Send alerts through configured channels"""
        try:
            with open(self.config_dir / "cost_alerts.json") as f:
                alert_config = json.load(f)
            
            notification = alert_config["notification"]
            
            # Format message
            message = "BALT-IX Cost Alerts:\n" + "\n".join(f"• {alert}" for alert in alerts)
            
            # Send to Slack
            if notification.get("slack_webhook"):
                requests.post(
                    notification["slack_webhook"],
                    json={"text": message}
                )
            
            # Send email
            if notification.get("email"):
                # Implement email sending here
                pass
            
        except Exception as e:
            print(f"Error sending alerts: {e}", file=sys.stderr)

    def monitor_temporal_correlations(self):
        """Monitor temporal correlations in BALT-IX data"""
        print("\nMonitoring temporal correlations...")
        try:
            from app.balt_ix import BALTIX
            balt_ix = BALTIX()
            
            # Configure monitoring windows
            monitoring_period = 300  # 5 minutes
            start_time = time.time()
            
            print("Starting correlation analysis (press Ctrl+C to stop)...")
            while time.time() - start_time < monitoring_period:
                for peer_id in balt_ix.peers.get("peers", {}):
                    # Monitor traffic and collect temporal data
                    balt_ix.monitor_traffic(peer_id)
                    
                    # Get joined events analysis
                    analysis = balt_ix.get_cost_analysis(peer_id)
                    
                    if analysis["status"] == "success":
                        # Display traffic-cost correlations
                        if "traffic_cost_correlation" in analysis:
                            corr = analysis["traffic_cost_correlation"]
                            print(f"\nPeer {peer_id} - Traffic/Cost Correlation:")
                            print(f"  Efficiency: ${corr.get('efficiency', 0):.3f}/GB")
                            if corr.get('anomalies'):
                                print("  Anomalies detected:")
                                for anomaly in corr['anomalies']:
                                    print(f"    • {anomaly}")
                        
                        # Display performance correlations
                        if "performance_correlation" in analysis:
                            perf = analysis["performance_correlation"]
                            print(f"\nPeer {peer_id} - Performance Correlation:")
                            print(f"  Latency: {perf.get('latency', 0)}ms")
                            if perf.get('error_patterns'):
                                print("  Error Patterns:")
                                for pattern in perf['error_patterns']:
                                    print(f"    • {pattern}")
                
                time.sleep(10)  # Wait 10 seconds between checks
                
            return True
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            return True
        except Exception as e:
            print(f"✗ Error monitoring temporal correlations: {e}")
            return False

    def setup(self):
        """Run complete security setup"""
        print("=== Setting up Security ===")
        
        steps = [
            (self.check_open_ports, "Checking open ports"),
            (self.setup_firewall, "Setting up firewall"),
            (self.harden_nginx, "Hardening Nginx"),
            (self.check_balt_ix, "Checking BALT-IX status"),
            (self.setup_cost_alerts, "Setting up cost alerts"),
            (self.monitor_balt_ix, "Starting BALT-IX monitoring"),
            (self.monitor_temporal_correlations, "Monitoring temporal correlations"),
            (self.setup_monitoring_alerts, "Configuring alerts"),
            (self.create_security_report, "Generating report")
        ]
        
        for step_func, description in steps:
            print(f"\n{description}...")
            if not step_func():
                print(f"\n✗ Failed during: {description}")
                return False
        
        print("\n✓ Security setup completed!")
        print("\nNext steps:")
        print("1. Review security report")
        print("2. Monitor BALT-IX dashboard")
        print("3. Review temporal correlation patterns")
        print("4. Configure correlation thresholds")
        return True

if __name__ == "__main__":
    setup = SecuritySetup()
    setup.setup() 