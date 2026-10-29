import os
from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # index.html berada di root repo (untuk hosting), template lain di app/templates
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.jinja_loader = ChoiceLoader([
        app.jinja_loader,               # default: app/templates/
        FileSystemLoader(root_dir),     # root: index.html
    ])

    # Initialize Database
    with app.app_context():
        from app.services.invoice_service import init_db
        init_db()

    # Register Blueprints
    from app.routes.invoice_routes import invoice_bp
    app.register_blueprint(invoice_bp)

    return app
