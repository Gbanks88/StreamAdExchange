#!/usr/bin/env python3
from service_control import ServiceController
import sys

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['start', 'stop', 'enable']:
        print("Usage: prometheus_control.py [start|stop|enable]")
        sys.exit(1)
    
    controller = ServiceController()
    action = sys.argv[1]
    
    if action == 'start':
        controller.start_service('prometheus')
    elif action == 'stop':
        controller.stop_service('prometheus')
    elif action == 'enable':
        controller.enable_service('prometheus')

if __name__ == "__main__":
    main() 