#!/usr/bin/env python3

import argparse
from setup_monitoring import MonitoringSetup

def main():
    parser = argparse.ArgumentParser(description='Manage monitoring services')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status'])
    parser.add_argument('--service', help='Specific service to manage (optional)')
    
    args = parser.parse_args()
    manager = MonitoringSetup()
    
    if args.service:
        # Manage specific service
        if args.action == 'start':
            manager.start_service(args.service)
        elif args.action == 'stop':
            manager.stop_service(args.service)
        elif args.action == 'restart':
            manager.stop_service(args.service)
            manager.start_service(args.service)
        elif args.action == 'status':
            status = manager.get_service_status(args.service)
            print(f"{args.service}: {status}")
    else:
        # Manage all services
        if args.action == 'start':
            manager.setup_all()
        elif args.action == 'stop':
            for service in ['prometheus', 'grafana', 'node_exporter', 'nginx-prometheus-exporter']:
                manager.stop_service(service)
        elif args.action == 'restart':
            manager.restart_services()
        elif args.action == 'status':
            manager.check_services()

if __name__ == "__main__":
    main() 