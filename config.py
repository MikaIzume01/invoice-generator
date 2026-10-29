# Application Configuration
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    DB_NAME = os.path.join(BASE_DIR, 'instance', 'database.db')
