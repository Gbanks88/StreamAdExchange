#!/usr/bin/env python3

import yaml
import os
from pathlib import Path
import subprocess

class MonitoringConfigurator:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.prometheus_config = self.project_root / "prometheus/prometheus.yml"
        self.grafana_config = self.project_root / "grafana/grafana.ini"

    def configure_prometheus(self):
        """Configure Prometheus with monitoring targets"""
        config = {
            'global': {
                'scrape_interval': '15s',
                'evaluation_interval': '15s',
                'scrape_timeout': '10s',
            },
            'alerting': {
                'alertmanagers': [{
                    'static_configs': [{
                        'targets': ['localhost:9093']
                    }]
                }]
            },
            'rule_files': [
                'rules/*.yml'
            ],
            'scrape_configs': [
                {
                    'job_name': 'prometheus',
                    'static_configs': [{
                        'targets': ['localhost:9090']
                    }]
                },
                {
                    'job_name': 'flask_app',
                    'static_configs': [{
                        'targets': ['localhost:5000']
                    }],
                    'metrics_path': '/metrics'
                },
                {
                    'job_name': 'node_exporter',
                    'static_configs': [{
                        'targets': ['localhost:9100']
                    }]
                },
                {
                    'job_name': 'nginx',
                    'static_configs': [{
                        'targets': ['localhost:9113']
                    }]
                },
                {
                    'job_name': 'grafana',
                    'static_configs': [{
                        'targets': ['localhost:3000']
                    }]
                }
            ]
        }

        # Add recording rules
        recording_rules = {
            'groups': [{
                'name': 'app_metrics',
                'rules': [
                    {
                        'record': 'request_latency_seconds_avg',
                        'expr': 'rate(flask_http_request_duration_seconds_sum[5m]) / rate(flask_http_request_duration_seconds_count[5m])'
                    },
                    {
                        'record': 'request_rate_per_second',
                        'expr': 'rate(flask_http_request_total[5m])'
                    }
                ]
            }]
        }

        # Create rules directory
        rules_dir = self.project_root / "prometheus/rules"
        rules_dir.mkdir(parents=True, exist_ok=True)

        # Write recording rules
        with open(rules_dir / "recording_rules.yml", 'w') as f:
            yaml.safe_dump(recording_rules, f)

        # Write main config
        with open(self.prometheus_config, 'w') as f:
            yaml.safe_dump(config, f)

        print("✓ Prometheus configuration created")

    def configure_grafana(self):
        """Configure Grafana with datasources and dashboards"""
        # Basic Grafana configuration
        grafana_ini = f"""
[server]
http_port = 3000
domain = localhost

[security]
admin_user = admin
admin_password = admin

[auth.anonymous]
enabled = false

[analytics]
reporting_enabled = false

[metrics]
enabled = true
"""
        self.grafana_config.parent.mkdir(parents=True, exist_ok=True)
        with open(self.grafana_config, 'w') as f:
            f.write(grafana_ini)

        # Create provisioning directories
        datasources_dir = self.project_root / "grafana/provisioning/datasources"
        dashboards_dir = self.project_root / "grafana/provisioning/dashboards"
        datasources_dir.mkdir(parents=True, exist_ok=True)
        dashboards_dir.mkdir(parents=True, exist_ok=True)

        # Configure Prometheus datasource
        datasource = {
            'apiVersion': 1,
            'datasources': [{
                'name': 'Prometheus',
                'type': 'prometheus',
                'access': 'proxy',
                'url': 'http://localhost:9090',
                'isDefault': True,
                'jsonData': {
                    'timeInterval': '15s'
                }
            }]
        }

        with open(datasources_dir / "prometheus.yml", 'w') as f:
            yaml.safe_dump(datasource, f)

        print("✓ Grafana configuration created")

    def create_dashboards(self):
        """Create default Grafana dashboards"""
        dashboards_dir = self.project_root / "grafana/dashboards"
        dashboards_dir.mkdir(parents=True, exist_ok=True)

        # Application Dashboard
        app_dashboard = {
            'title': 'Application Metrics',
            'panels': [
                {
                    'title': 'Request Rate',
                    'type': 'graph',
                    'targets': [{
                        'expr': 'rate(flask_http_request_total[5m])',
                        'legendFormat': '{{method}} {{path}}'
                    }]
                },
                {
                    'title': 'Response Time',
                    'type': 'graph',
                    'targets': [{
                        'expr': 'rate(flask_http_request_duration_seconds_sum[5m]) / rate(flask_http_request_duration_seconds_count[5m])',
                        'legendFormat': '{{method}} {{path}}'
                    }]
                }
            ]
        }

        with open(dashboards_dir / "app_dashboard.json", 'w') as f:
            json.dump(app_dashboard, f, indent=2)

        print("✓ Default dashboards created")

    def verify_configuration(self):
        """Verify Prometheus and Grafana configurations"""
        print("\nVerifying configurations...")
        
        # Check Prometheus config
        try:
            result = subprocess.run(
                ['promtool', 'check', 'config', str(self.prometheus_config)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Prometheus configuration is valid")
            else:
                print("✗ Prometheus configuration error:")
                print(result.stderr)
        except Exception as e:
            print(f"✗ Error checking Prometheus config: {e}")

        # Check Grafana config
        try:
            if self.grafana_config.exists():
                print("✓ Grafana configuration exists")
            else:
                print("✗ Grafana configuration missing")
        except Exception as e:
            print(f"✗ Error checking Grafana config: {e}")

    def setup(self):
        """Run complete monitoring setup"""
        print("\n=== Configuring Monitoring Services ===")
        
        self.configure_prometheus()
        self.configure_grafana()
        self.create_dashboards()
        self.verify_configuration()
        
        print("\nConfiguration complete!")
        print("\nNext steps:")
        print("1. Restart Prometheus: ./scripts/prometheus_control.py restart")
        print("2. Restart Grafana: ./scripts/grafana_control.py restart")
        print("3. Access Grafana: http://localhost:3000")
        print("4. Login with admin/admin and change password")
        print("5. Import dashboards from grafana/dashboards/")

if __name__ == "__main__":
    configurator = MonitoringConfigurator()
    configurator.setup() 