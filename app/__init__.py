from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler

from .config import config_by_name
from .db import init_app as init_db_app, init_db

def create_app(config_name='prod'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize DB teardown
    init_db_app(app)
    
    # Configure logging for production
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/sarpras.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Sarpras startup')
        
    with app.app_context():
        init_db()

    # Register blueprints
    from .routes.main import main_bp
    from .routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
