from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
import os
# Remove incorrect imports - these are handled in app.py

login_manager = LoginManager()
mail = Mail()

def create_app():
    # Get the absolute path to the project root (Windows-compatible)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.normpath(os.path.join(basedir, 'templates')),
                static_folder=os.path.normpath(os.path.join(basedir, 'static')))
    
    # Load configuration (Windows-compatible import)
    try:
        from config.config import Config
        app.config.from_object(Config)
    except ImportError:
        # Fallback configuration
        app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
    
    # Initialize extensions
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    mail.init_app(app)
    
    # User loader and blueprints are handled in app.py
    
    return app