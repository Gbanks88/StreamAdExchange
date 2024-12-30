#!/bin/bash

PROJECT_ROOT="/Volumes/Learn_Space/StreamAdExchange"
LOG_DIR="$PROJECT_ROOT/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/shutdown_${TIMESTAMP}.log"
}

stop_services() {
    log "Stopping services..."
    
    # Stop Flask
    if [ -f "$PROJECT_ROOT/flask.pid" ]; then
        log "Stopping Flask application..."
        kill $(cat "$PROJECT_ROOT/flask.pid")
        rm "$PROJECT_ROOT/flask.pid"
    fi
    
    # Stop monitoring services
    if [ -f "$PROJECT_ROOT/diagnostic.pid" ]; then
        log "Stopping diagnostic monitoring..."
        kill $(cat "$PROJECT_ROOT/diagnostic.pid")
        rm "$PROJECT_ROOT/diagnostic.pid"
    fi
    
    if [ -f "$PROJECT_ROOT/failover.pid" ]; then
        log "Stopping failover monitoring..."
        kill $(cat "$PROJECT_ROOT/failover.pid")
        rm "$PROJECT_ROOT/failover.pid"
    fi
    
    # Stop nginx
    log "Stopping nginx..."
    sudo nginx -s stop
    
    log "All services stopped"
}

stop_services 