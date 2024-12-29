from flask import Flask, render_template, request, jsonify, url_for
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.cortex_integration import analyze_engagement
from app.balt_integration import process_payment

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['DEBUG'] = True
    
    # Initialize extensions
    csrf = CSRFProtect(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Add context processor for static URLs
    @app.context_processor
    def utility_processor():
        def static_url(filename):
            return url_for('static', filename=filename)
        return dict(static_url=static_url)
    
    # Register routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    @app.route('/')
    def home():
        return "Welcome to StreamAd Exchange!"

    @app.route('/engage', methods=['POST'])
    def engage():
        ad_data = request.json
        analysis_result = analyze_engagement(ad_data)
        return jsonify(analysis_result)

    @app.route('/payment', methods=['POST'])
    def payment():
        payment_data = request.json
        user_id = payment_data.get('user_id')
        amount = payment_data.get('amount')
        payment_method = payment_data.get('payment_method')
        payment_result = process_payment(user_id, amount, payment_method)
        return jsonify(payment_result)

    return app
