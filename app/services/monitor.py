from app.config import Config
from failover_monitor import FailoverMonitor, AWS_ENABLED
import threading
import logging

class MonitoringService:
    _instance = None
    _monitor = None
    _monitor_thread = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if self._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        
        # Create config for failover monitor
        config = {
            "primary_server": {
                "host": Config.PRIMARY_SERVER_HOST,
                "port": Config.PRIMARY_SERVER_PORT,
                "health_check_endpoint": Config.HEALTH_CHECK_ENDPOINT
            },
            "aws": {
                "access_key": Config.AWS_ACCESS_KEY,
                "secret_key": Config.AWS_SECRET_KEY,
                "region": Config.AWS_REGION,
                "instance_id": Config.AWS_INSTANCE_ID
            },
            "failure_threshold": Config.FAILURE_THRESHOLD,
            "check_interval": Config.CHECK_INTERVAL,
            "notification": {
                "slack_webhook": Config.SLACK_WEBHOOK,
                "email": Config.ALERT_EMAIL
            }
        }
        
        try:
            self._monitor = FailoverMonitor()
            self._monitor.config = config
            logging.info("Monitoring service initialized")
            if not AWS_ENABLED:
                logging.warning("AWS failover support is not available")
        except Exception as e:
            logging.error(f"Failed to initialize monitoring service: {e}")
            self._monitor = None
    
    def start(self):
        """Start the monitoring service in a separate thread"""
        if self._monitor_thread is None or not self._monitor_thread.is_alive():
            self._monitor_thread = threading.Thread(
                target=self._monitor.monitor,
                daemon=True
            )
            self._monitor_thread.start()
            logging.info("Monitoring service started")
    
    def stop(self):
        """Stop the monitoring service"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor.stop_monitoring = True
            self._monitor_thread.join(timeout=5)
            logging.info("Monitoring service stopped")
    
    @property
    def status(self):
        """Get current monitoring status"""
        if not self._monitor_thread or not self._monitor_thread.is_alive():
            return "stopped"
        return "running" 