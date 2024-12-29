import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Process naming
proc_name = 'streamad_exchange'
pythonpath = '.'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# SSL (if using)
# keyfile = 'path/to/keyfile'
# certfile = 'path/to/certfile'

# Environment variables
raw_env = [
    f"FLASK_ENV=production",
    f"FLASK_APP=run.py"
] 