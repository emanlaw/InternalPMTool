from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
import os
from app.models.user import User, load_data
from app.utils.template_filters import register_template_filters

login_manager = LoginManager()
mail = Mail()

def create_app():
    # Get the absolute path to the project root
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Load configuration
    from config.config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    mail.init_app(app)
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        data = load_data()
        user_data = next((u for u in data.get('users', []) if u['id'] == int(user_id)), None)
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['password_hash'])
        return None
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register template filters
    register_template_filters(app)
    
    return app