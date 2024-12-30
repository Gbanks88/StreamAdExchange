# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "0.0.0.0:443"
backlog = 2048

# Worker processes
workers = 4
worker_class = 'gevent'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'streamadexchange'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL Configuration
keyfile = '/etc/letsencrypt/live/notcheapnot2expensive.com/privkey.pem'
certfile = '/etc/letsencrypt/live/notcheapnot2expensive.com/fullchain.pem'

# Trading specific settings
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30
limit_request_line = 4096
limit_request_fields = 100