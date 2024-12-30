from flask import Flask
from app.config import Config
from app.extensions import cache, limiter
import logging
from app.ai_agent import trading_agent, AI_ENABLED
from app.services.monitor import MonitoringService
from prometheus_flask_exporter import PrometheusMetrics

logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    cache.init_app(app)
    limiter.init_app(app)
    
    # Start AI agent with error handling
    if AI_ENABLED and trading_agent:
        try:
            trading_agent.run()
            logger.info("Trading agent started successfully")
        except Exception as e:
            logger.error(f"Failed to start trading agent: {e}")
            logger.info("Running in fallback mode")
    else:
        logger.info("Running in fallback mode without AI agent")
    
    # Start monitoring service
    try:
        monitor_service = MonitoringService.get_instance()
        monitor_service.start()
        logger.info("Monitoring service started successfully")
    except Exception as e:
        logger.error(f"Failed to start monitoring service: {e}")
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    metrics = PrometheusMetrics(app)

    # Static information as metric
    metrics.info('streamad_info', 'Application info', version='1.0.0')

    # Add your custom metrics
    @metrics.counter('streamad_requests_total', 'Number of requests by status')
    @metrics.gauge('streamad_in_progress', 'Long running requests in progress')
    def track_requests():
        return 'tracking'
    
    return app
