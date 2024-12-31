from flask import Flask
from app.routes import main_bp
from app.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
