#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, request
from nginx_log_viewer import NginxLogViewer
import datetime
import threading
import queue
import time

app = Flask(__name__, 
           template_folder='../templates/nginx_viewer',
           static_folder='../static/nginx_viewer')

# Initialize the log viewer
log_viewer = NginxLogViewer()

# Queue for live log updates
live_logs = queue.Queue(maxsize=1000)

def background_log_reader():
    """Background thread to read logs"""
    while True:
        try:
            process = subprocess.Popen(
                ['tail', '-f', str(log_viewer.access_log)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            while True:
                line = process.stdout.readline()
                if line:
                    match = log_viewer.access_pattern.match(line)
                    if match:
                        data = match.groupdict()
                        if live_logs.full():
                            live_logs.get()  # Remove oldest entry if queue is full
                        live_logs.put(data)
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error in background reader: {e}")
            time.sleep(5)  # Wait before retrying

# Start background thread
threading.Thread(target=background_log_reader, daemon=True).start()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/logs/recent')
def get_recent_logs():
    """Get recent log entries"""
    log_type = request.args.get('type', 'access')
    lines = int(request.args.get('lines', 100))
    
    log_file = log_viewer.access_log if log_type == 'access' else log_viewer.error_log
    entries = log_viewer.tail_log(log_file, lines)
    
    if log_type == 'access':
        return jsonify(log_viewer.parse_access_log(entries))
    return jsonify(log_viewer.parse_error_log(entries))

@app.route('/api/logs/live')
def get_live_logs():
    """Get live log updates using Server-Sent Events"""
    def generate():
        while True:
            try:
                data = live_logs.get(timeout=30)
                yield f"data: {json.dumps(data)}\n\n"
            except queue.Empty:
                yield f"data: {json.dumps({'keepalive': True})}\n\n"
            
    return app.response_class(
        generate(),
        mimetype='text/event-stream'
    )

@app.route('/api/stats')
def get_stats():
    """Get traffic statistics"""
    hours = int(request.args.get('hours', 1))
    return jsonify(log_viewer.analyze_traffic(hours))

@app.route('/api/errors')
def get_errors():
    """Get error summary"""
    return jsonify(log_viewer.get_error_summary())

@app.route('/api/search')
def search_logs():
    """Search logs"""
    pattern = request.args.get('pattern', '')
    log_type = request.args.get('type', 'access')
    if not pattern:
        return jsonify([])
    return jsonify(log_viewer.search_logs(pattern, log_type))

if __name__ == '__main__':
    app.run(port=5001, debug=True) 