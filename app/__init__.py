import os
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Database
    with app.app_context():
        from app.services.invoice_service import init_db
        init_db()

    # Register Blueprints
    from app.routes.invoice_routes import invoice_bp
    app.register_blueprint(invoice_bp)

    return app
