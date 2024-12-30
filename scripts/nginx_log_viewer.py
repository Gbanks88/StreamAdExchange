#!/usr/bin/env python3

import re
from pathlib import Path
import subprocess
import datetime
import argparse
from collections import defaultdict
import json
from typing import Dict, List, Tuple

class NginxLogViewer:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.nginx_log_dir = self.project_root / "nginx/logs"
        self.access_log = self.nginx_log_dir / "access.log"
        self.error_log = self.nginx_log_dir / "error.log"
        
        # Regular expressions for log parsing
        self.access_pattern = re.compile(
            r'(?P<ip>[\d.]+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/\d\.\d" '
            r'(?P<status>\d+) (?P<bytes>\d+) "(?P<referer>.*?)" "(?P<useragent>.*?)"'
        )
        
        self.error_pattern = re.compile(
            r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] '
            r'(?P<pid>\d+)#(?P<tid>\d+): (?P<message>.*)'
        )

    def tail_log(self, log_file: Path, lines: int = 10) -> List[str]:
        """Display last n lines of log file"""
        try:
            result = subprocess.run(
                ['tail', '-n', str(lines), str(log_file)],
                capture_output=True,
                text=True
            )
            return result.stdout.splitlines()
        except Exception as e:
            print(f"Error reading log file: {e}")
            return []

    def parse_access_log(self, lines: List[str]) -> List[Dict]:
        """Parse access log entries"""
        entries = []
        for line in lines:
            match = self.access_pattern.match(line)
            if match:
                entries.append(match.groupdict())
        return entries

    def parse_error_log(self, lines: List[str]) -> List[Dict]:
        """Parse error log entries"""
        entries = []
        for line in lines:
            match = self.error_pattern.match(line)
            if match:
                entries.append(match.groupdict())
        return entries

    def analyze_traffic(self, hours: int = 1) -> Dict:
        """Analyze recent traffic patterns"""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        stats = {
            'requests_by_ip': defaultdict(int),
            'requests_by_path': defaultdict(int),
            'status_codes': defaultdict(int),
            'methods': defaultdict(int),
            'total_bytes': 0,
            'errors': 0
        }

        try:
            with open(self.access_log) as f:
                for line in f:
                    match = self.access_pattern.match(line)
                    if match:
                        data = match.groupdict()
                        timestamp = datetime.datetime.strptime(
                            data['timestamp'].split()[0],
                            '%d/%b/%Y:%H:%M:%S'
                        )
                        
                        if timestamp >= cutoff_time:
                            stats['requests_by_ip'][data['ip']] += 1
                            stats['requests_by_path'][data['path']] += 1
                            stats['status_codes'][data['status']] += 1
                            stats['methods'][data['method']] += 1
                            stats['total_bytes'] += int(data['bytes'])
                            
                            if data['status'].startswith('5'):
                                stats['errors'] += 1
            
            # Convert defaultdict to regular dict for JSON serialization
            return {k: dict(v) if isinstance(v, defaultdict) else v 
                   for k, v in stats.items()}
        
        except Exception as e:
            print(f"Error analyzing traffic: {e}")
            return {}

    def search_logs(self, pattern: str, log_type: str = 'access') -> List[str]:
        """Search logs for specific pattern"""
        log_file = self.access_log if log_type == 'access' else self.error_log
        try:
            result = subprocess.run(
                ['grep', '-i', pattern, str(log_file)],
                capture_output=True,
                text=True
            )
            return result.stdout.splitlines()
        except Exception as e:
            print(f"Error searching logs: {e}")
            return []

    def get_error_summary(self) -> Dict:
        """Get summary of recent errors"""
        try:
            errors = defaultdict(list)
            with open(self.error_log) as f:
                for line in f:
                    match = self.error_pattern.match(line)
                    if match:
                        data = match.groupdict()
                        errors[data['level']].append({
                            'timestamp': data['timestamp'],
                            'message': data['message']
                        })
            return dict(errors)
        except Exception as e:
            print(f"Error summarizing errors: {e}")
            return {}

    def display_live_tail(self, log_type: str = 'access'):
        """Display live log updates"""
        log_file = self.access_log if log_type == 'access' else self.error_log
        try:
            process = subprocess.Popen(
                ['tail', '-f', str(log_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            print(f"Live tailing {log_type} log (Ctrl+C to stop)...")
            while True:
                line = process.stdout.readline()
                if line:
                    if log_type == 'access':
                        match = self.access_pattern.match(line)
                        if match:
                            data = match.groupdict()
                            print(f"{data['timestamp']} - {data['method']} {data['path']} - {data['status']}")
                    else:
                        print(line.strip())
                        
        except KeyboardInterrupt:
            process.terminate()
            print("\nStopped live tail")
        except Exception as e:
            print(f"Error in live tail: {e}")

def main():
    parser = argparse.ArgumentParser(description='Nginx Log Viewer')
    parser.add_argument('--action', choices=['tail', 'analyze', 'search', 'errors', 'live'],
                       required=True, help='Action to perform')
    parser.add_argument('--lines', type=int, default=10,
                       help='Number of lines to show for tail')
    parser.add_argument('--hours', type=int, default=1,
                       help='Hours of data to analyze')
    parser.add_argument('--pattern', type=str, help='Pattern to search for')
    parser.add_argument('--log', choices=['access', 'error'], default='access',
                       help='Log file to operate on')
    
    args = parser.parse_args()
    viewer = NginxLogViewer()
    
    if args.action == 'tail':
        log_file = viewer.access_log if args.log == 'access' else viewer.error_log
        lines = viewer.tail_log(log_file, args.lines)
        for line in lines:
            print(line)
            
    elif args.action == 'analyze':
        stats = viewer.analyze_traffic(args.hours)
        print(json.dumps(stats, indent=2))
        
    elif args.action == 'search':
        if not args.pattern:
            print("Please provide a search pattern")
            return
        results = viewer.search_logs(args.pattern, args.log)
        for line in results:
            print(line)
            
    elif args.action == 'errors':
        errors = viewer.get_error_summary()
        print(json.dumps(errors, indent=2))
        
    elif args.action == 'live':
        viewer.display_live_tail(args.log)

if __name__ == "__main__":
    main() 