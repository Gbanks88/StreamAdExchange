import logging
import json
import time
from datetime import datetime
import socket
import requests

# Try to import boto3, but provide fallback
try:
    import boto3
    AWS_ENABLED = True
except ImportError:
    AWS_ENABLED = False
    logging.warning("AWS support disabled: boto3 not installed. Run 'pip install boto3' to enable AWS failover.")

class FailoverMonitor:
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        
        # Initialize AWS client if available
        if AWS_ENABLED:
            try:
                self.ec2 = boto3.client(
                    'ec2',
                    aws_access_key_id=self.config['aws']['access_key'],
                    aws_secret_access_key=self.config['aws']['secret_key'],
                    region_name=self.config['aws']['region']
                )
                logging.info("AWS client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize AWS client: {e}")
                AWS_ENABLED = False
        else:
            self.ec2 = None
        
        self.primary_server = self.config['primary_server']
        self.aws_instance_id = self.config['aws'].get('instance_id')
        self.failover_active = False
        self.consecutive_failures = 0
        self.failure_threshold = self.config['failure_threshold']
        self.check_interval = self.config['check_interval']
        self.last_check_time = None
        self.stop_monitoring = False
        self.backup_server = self.config.get('backup_server')
        self.current_server = 'primary'
        self.failback_attempts = 0
        self.max_failback_attempts = 3

    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('failover_config.json', 'r') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            # Create default config if not exists
            default_config = {
                "primary_server": {
                    "host": "localhost",
                    "port": 80,
                    "health_check_endpoint": "/health"
                },
                "aws": {
                    "access_key": "YOUR_AWS_ACCESS_KEY",
                    "secret_key": "YOUR_AWS_SECRET_KEY",
                    "region": "us-west-2",
                    "instance_id": "YOUR_EC2_INSTANCE_ID"
                },
                "failure_threshold": 3,
                "check_interval": 30,
                "notification": {
                    "slack_webhook": "",
                    "email": ""
                }
            }
            with open('failover_config.json', 'w') as f:
                json.dump(default_config, f, indent=4)
            logging.warning("Config file not found. Created default config.json")
            return default_config

    def check_nginx_status(self):
        """Check if nginx is running on primary server"""
        try:
            # Try to connect to nginx
            url = f"http://{self.primary_server['host']}:{self.primary_server['port']}{self.primary_server['health_check_endpoint']}"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logging.error(f"Error checking nginx status: {e}")
            return False

    def check_server_connectivity(self):
        """Check if server is reachable"""
        try:
            socket.create_connection(
                (self.primary_server['host'], self.primary_server['port']), 
                timeout=5
            )
            return True
        except (socket.timeout, socket.error) as e:
            logging.error(f"Server connectivity error: {e}")
            return False

    def start_aws_instance(self):
        """Start the AWS EC2 instance"""
        try:
            self.ec2.start_instances(InstanceIds=[self.aws_instance_id])
            logging.info("AWS instance starting...")
            
            # Wait for instance to be running
            waiter = self.ec2.get_waiter('instance_running')
            waiter.wait(InstanceIds=[self.aws_instance_id])
            
            # Get instance public IP
            response = self.ec2.describe_instances(InstanceIds=[self.aws_instance_id])
            public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            logging.info(f"AWS instance running at {public_ip}")
            return public_ip
        except Exception as e:
            logging.error(f"Error starting AWS instance: {e}")
            return None

    def update_dns(self, new_ip):
        """Update DNS records to point to new IP"""
        try:
            # Implement your DNS update logic here
            # This could be using Route53 or another DNS provider
            logging.info(f"Updating DNS to point to {new_ip}")
            return True
        except Exception as e:
            logging.error(f"Error updating DNS: {e}")
            return False

    def notify_team(self, message):
        """Send notification to team"""
        if self.config['notification']['slack_webhook']:
            try:
                requests.post(
                    self.config['notification']['slack_webhook'],
                    json={"text": message}
                )
            except Exception as e:
                logging.error(f"Error sending Slack notification: {e}")

    def failover_to_aws(self):
        """Execute failover to AWS"""
        if not AWS_ENABLED:
            logging.error("Cannot failover: AWS support not enabled")
            return False
            
        if not self.failover_active:
            logging.info("Initiating failover to AWS...")
            self.notify_team("⚠️ Primary server down! Initiating failover to AWS...")
            
            try:
                new_ip = self.start_aws_instance()
                if new_ip:
                    if self.update_dns(new_ip):
                        self.failover_active = True
                        self.notify_team(f"✅ Failover complete! New server IP: {new_ip}")
                        logging.info("Failover completed successfully")
                        return True
                    else:
                        logging.error("Failover failed - DNS update failed")
                else:
                    logging.error("Failover failed - couldn't start AWS instance")
            except Exception as e:
                logging.error(f"Failover failed: {e}")
                
        return False

    def failover_to_backup(self):
        """Failover to local backup server"""
        if not self.backup_server:
            logging.error("No backup server configured")
            return False

        try:
            logging.info("Attempting failover to backup server...")
            self.notify_team("⚠️ Primary server down! Attempting failover to backup server...")

            if self.check_backup_server():
                if self.update_dns(self.backup_server['host']):
                    self.failover_active = True
                    self.current_server = 'backup'
                    self.notify_team(f"✅ Failover complete! Using backup server: {self.backup_server['host']}")
                    logging.info("Failover to backup server completed successfully")
                    return True
                else:
                    logging.error("Failover failed - DNS update failed")
            else:
                logging.error("Backup server is not responding")
            
            return False
        except Exception as e:
            logging.error(f"Failover to backup server failed: {e}")
            return False

    def check_backup_server(self):
        """Check if backup server is available"""
        try:
            if not self.backup_server:
                return False

            url = f"http://{self.backup_server['host']}:{self.backup_server['port']}/health"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Error checking backup server: {e}")
            return False

    def attempt_failback(self):
        """Try to fail back to primary server"""
        if self.check_primary_health():
            logging.info("Primary server appears to be healthy, attempting failback...")
            if self.update_dns(self.primary_server['host']):
                self.failover_active = False
                self.current_server = 'primary'
                self.failback_attempts = 0
                self.notify_team("✅ Failed back to primary server successfully")
                return True
            else:
                self.failback_attempts += 1
                logging.error(f"Failback attempt {self.failback_attempts} failed")
        return False

    def monitor(self):
        """Main monitoring loop"""
        logging.info("Starting failover monitor...")
        
        while not self.stop_monitoring:
            try:
                self.last_check_time = datetime.now().isoformat()
                primary_ok = self.check_nginx_status() and self.check_server_connectivity()
                
                if not primary_ok:
                    self.consecutive_failures += 1
                    logging.warning(f"Server check failed ({self.consecutive_failures}/{self.failure_threshold})")
                    
                    if self.consecutive_failures >= self.failure_threshold:
                        if AWS_ENABLED:
                            if not self.failover_to_aws():
                                # If AWS failover fails, try backup server
                                self.failover_to_backup()
                        else:
                            # No AWS available, try backup server directly
                            self.failover_to_backup()
                else:
                    if self.consecutive_failures > 0:
                        logging.info("Server recovered")
                    self.consecutive_failures = 0
                    
                    # If we're on backup/AWS and primary is healthy, try failback
                    if self.failover_active and self.failback_attempts < self.max_failback_attempts:
                        self.attempt_failback()
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logging.info("Monitoring stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(self.check_interval)

if __name__ == "__main__":
    monitor = FailoverMonitor()
    monitor.monitor() 