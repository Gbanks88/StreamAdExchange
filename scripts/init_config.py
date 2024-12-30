#!/usr/bin/env python3
from pathlib import Path
import json
import logging
import sys
import os

def setup_logging(env: str):
    """Configure logging based on environment"""
    base_dir = Path("/Volumes/Learn_Space/StreamAdExchange" if env == "local" 
                    else "/opt/streamadexchange")
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG if env == "local" else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f'setup_{env}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('init_config')

def get_env_config(env: str) -> dict:
    """Get environment-specific configuration"""
    base_configs = {
        "local": {
            "base_dir": "/Volumes/Learn_Space/StreamAdExchange",
            "ports": {
                "balt_ix": 5000,
                "prometheus": 9090,
                "grafana": 3000
            },
            "debug": True,
            "ssl_enabled": False,
            "monitoring": {
                "interval": 60,  # More frequent for testing
                "retention_days": 7
            }
        },
        "prod": {
            "base_dir": "/opt/streamadexchange",
            "ports": {
                "balt_ix": 443,
                "prometheus": 9090,
                "grafana": 3000
            },
            "debug": False,
            "ssl_enabled": True,
            "monitoring": {
                "interval": 300,
                "retention_days": 90
            }
        }
    }
    return base_configs.get(env, base_configs["local"])

def init_configs(env: str = "local"):
    """Initialize all configuration files for specific environment"""
    logger = setup_logging(env)
    logger.info(f"Starting configuration initialization for {env} environment")
    
    env_config = get_env_config(env)
    config_dir = Path(env_config["base_dir"]) / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create initial configurations
    configs = {
        "balt_ix.json": {
            "peers": {
                "default": {
                    "ip": "127.0.0.1" if env == "local" else "192.168.1.1",
                    "asn": "AS12345",
                    "capacity": "1G" if env == "local" else "10G",
                    "enabled": True,
                    "service_type": "premium",
                    "billing_currency": "USD",
                    "location": "US-East",
                    "peering_type": "direct"
                }
            },
            "settings": {
                "max_latency": 100 if env == "local" else 10,
                "min_throughput": 100 if env == "local" else 1000,
                "max_packet_loss": 1.0 if env == "local" else 0.1,
                "debug_mode": env_config["debug"]
            }
        },
        "cortex.json": {
            "window_configs": {
                "traffic_cost": {
                    "window_size": 60 if env == "local" else 300,
                    "slide_interval": 30 if env == "local" else 60,
                    "retention_days": env_config["monitoring"]["retention_days"]
                },
                "performance_alerts": {
                    "window_size": 120 if env == "local" else 600,
                    "slide_interval": 60 if env == "local" else 120
                }
            },
            "enrichment_rules": {
                "join_fields": ["peer_id", "timestamp"],
                "data_sources": ["traffic", "cost", "performance"]
            }
        },
        "cost_alerts.json": {
            "thresholds": {
                "cost_increase": 10 if env == "local" else 20,
                "utilization": 50 if env == "local" else 80,
                "savings_opportunity": 10 if env == "local" else 100
            },
            "notification": {
                "slack_webhook": os.getenv("SLACK_WEBHOOK", ""),
                "email": os.getenv("ALERT_EMAIL", ""),
                "enabled": True
            },
            "monitoring": env_config["monitoring"]
        },
        f"security_{env}.yml": {
            "firewall": {
                "default_policy": "drop",
                "allowed_ports": list(env_config["ports"].values()),
                "trusted_ips": ["127.0.0.1"] if env == "local" else []
            },
            "monitoring": {
                "enabled": True,
                "prometheus_port": env_config["ports"]["prometheus"],
                "grafana_port": env_config["ports"]["grafana"]
            },
            "ssl": {
                "enabled": env_config["ssl_enabled"],
                "protocols": ["TLSv1.2", "TLSv1.3"],
                "ciphers": [
                    "ECDHE-ECDSA-AES128-GCM-SHA256",
                    "ECDHE-RSA-AES128-GCM-SHA256"
                ]
            }
        }
    }

    try:
        for filename, content in configs.items():
            file_path = config_dir / filename
            logger.info(f"Creating configuration file: {file_path}")
            
            with open(file_path, 'w') as f:
                if filename.endswith('.yml'):
                    import yaml
                    yaml.dump(content, f, default_flow_style=False)
                else:
                    json.dump(content, f, indent=4)
            
            logger.info(f"Successfully created {filename}")
            
            # Create symlink for active security config
            if filename.startswith('security_'):
                active_security = config_dir / 'security.yml'
                if active_security.exists():
                    active_security.unlink()
                active_security.symlink_to(file_path)
                logger.info(f"Created symlink for active security config: {active_security}")
        
        logger.info(f"Configuration initialization completed successfully for {env} environment")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing configurations: {e}")
        return False

if __name__ == "__main__":
    # Get environment from command line argument or environment variable
    env = sys.argv[1] if len(sys.argv) > 1 else os.getenv('STREAMAD_ENV', 'local')
    if env not in ['local', 'prod']:
        print("Error: Environment must be either 'local' or 'prod'")
        sys.exit(1)
    
    success = init_configs(env)
    sys.exit(0 if success else 1) 