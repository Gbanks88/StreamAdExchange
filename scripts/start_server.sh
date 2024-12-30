#!/bin/bash

# Project root directory
PROJECT_ROOT="/Volumes/Learn_Space/StreamAdExchange"
NGINX_DIR="$PROJECT_ROOT/nginx"
LOG_DIR="$PROJECT_ROOT/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create log file
STARTUP_LOG="$LOG_DIR/startup_${TIMESTAMP}.log"
mkdir -p "$LOG_DIR"
touch "$STARTUP_LOG"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$STARTUP_LOG"
}

check_dependencies() {
    log "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log "ERROR: Python3 is not installed"
        exit 1
    fi
    
    # Check nginx
    if ! command -v nginx &> /dev/null; then
        log "ERROR: nginx is not installed"
        exit 1
    }
    
    # Check virtual environment
    if [ ! -d "$PROJECT_ROOT/venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv "$PROJECT_ROOT/venv"
    fi
    
    log "Dependencies check completed"
}

setup_nginx() {
    log "Setting up nginx..."
    
    # Create required directories
    mkdir -p "$NGINX_DIR"/{logs,run,sites-enabled}
    
    # Check if nginx is already running
    if pgrep nginx > /dev/null; then
        log "Stopping existing nginx process..."
        sudo nginx -s stop
    fi
    
    # Start nginx with custom config
    log "Starting nginx..."
    sudo nginx -c "$NGINX_DIR/nginx.conf"
    
    if [ $? -eq 0 ]; then
        log "nginx started successfully"
    else
        log "ERROR: Failed to start nginx"
        exit 1
    fi
}

start_flask() {
    log "Starting Flask application..."
    
    # Activate virtual environment
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # Install/update requirements
    pip install -r "$PROJECT_ROOT/requirements.txt"
    
    # Export environment variables
    export FLASK_APP="$PROJECT_ROOT/run.py"
    export FLASK_ENV="development"
    export PYTHONPATH="$PROJECT_ROOT"
    
    # Start Flask in background
    python "$PROJECT_ROOT/run.py" > "$LOG_DIR/flask_${TIMESTAMP}.log" 2>&1 &
    FLASK_PID=$!
    
    # Check if Flask started successfully
    sleep 3
    if ps -p $FLASK_PID > /dev/null; then
        log "Flask application started successfully (PID: $FLASK_PID)"
        echo $FLASK_PID > "$PROJECT_ROOT/flask.pid"
    else
        log "ERROR: Failed to start Flask application"
        exit 1
    fi
}

start_monitoring() {
    log "Starting monitoring services..."
    
    # Start diagnostic monitoring
    python "$PROJECT_ROOT/diagnostic.py" > "$LOG_DIR/diagnostic_${TIMESTAMP}.log" 2>&1 &
    DIAG_PID=$!
    
    # Start failover monitoring
    python "$PROJECT_ROOT/failover_monitor.py" > "$LOG_DIR/failover_${TIMESTAMP}.log" 2>&1 &
    FAILOVER_PID=$!
    
    # Save PIDs
    echo $DIAG_PID > "$PROJECT_ROOT/diagnostic.pid"
    echo $FAILOVER_PID > "$PROJECT_ROOT/failover.pid"
    
    log "Monitoring services started"
}

cleanup() {
    log "Cleaning up..."
    
    # Stop Flask
    if [ -f "$PROJECT_ROOT/flask.pid" ]; then
        kill $(cat "$PROJECT_ROOT/flask.pid")
        rm "$PROJECT_ROOT/flask.pid"
    fi
    
    # Stop monitoring services
    if [ -f "$PROJECT_ROOT/diagnostic.pid" ]; then
        kill $(cat "$PROJECT_ROOT/diagnostic.pid")
        rm "$PROJECT_ROOT/diagnostic.pid"
    fi
    
    if [ -f "$PROJECT_ROOT/failover.pid" ]; then
        kill $(cat "$PROJECT_ROOT/failover.pid")
        rm "$PROJECT_ROOT/failover.pid"
    fi
    
    # Stop nginx
    sudo nginx -s stop
    
    log "Cleanup completed"
}

# Set up cleanup on script exit
trap cleanup EXIT

main() {
    log "Starting server initialization..."
    
    check_dependencies
    setup_nginx
    start_flask
    start_monitoring
    
    log "Server initialization completed successfully"
    
    # Keep script running and monitor services
    while true; do
        sleep 30
        
        # Check if services are still running
        if ! ps -p $(cat "$PROJECT_ROOT/flask.pid" 2>/dev/null) > /dev/null; then
            log "WARNING: Flask application stopped, restarting..."
            start_flask
        fi
        
        if ! pgrep nginx > /dev/null; then
            log "WARNING: nginx stopped, restarting..."
            setup_nginx
        fi
        
        if ! ps -p $(cat "$PROJECT_ROOT/diagnostic.pid" 2>/dev/null) > /dev/null; then
            log "WARNING: Diagnostic monitoring stopped, restarting..."
            start_monitoring
        fi
    done
}

# Run main function
main 