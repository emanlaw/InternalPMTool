"""Flask app factory and configuration."""

from flask import Flask
from flask_login import LoginManager

from app.models.user import User
from app.services.data_service import load_data
from app.services.firebase_service import get_firestore_client
from app.utils.helpers import (
    get_due_date_text_class, get_due_date_status, get_comment_count,
    format_timestamp, format_date, get_label_by_id
)


# Predefined labels with colors
PREDEFINED_LABELS = [
    {'id': 'bug', 'name': 'Bug', 'color': '#ff5630'},
    {'id': 'feature', 'name': 'Feature', 'color': '#0052cc'},
    {'id': 'urgent', 'name': 'Urgent', 'color': '#ff8b00'},
    {'id': 'enhancement', 'name': 'Enhancement', 'color': '#36b37e'}
]


def create_app():
    """Create and configure the Flask application."""
    import os
    # Get the parent directory (project root) for templates and static files
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = 'your-secret-key-change-in-production'
    
    # Initialize Firebase
    db = get_firestore_client()
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        data = load_data(db)
        user_data = next((u for u in data.get('users', []) if u['id'] == int(user_id)), None)
        if user_data:
            return User(
                user_data['id'], 
                user_data['username'], 
                user_data['password_hash'],
                user_data.get('email'),
                user_data.get('display_name'),
                user_data.get('role', 'user'),
                user_data.get('status', 'active')
            )
        return None
    
    # Register template functions and filters
    app.jinja_env.globals.update(
        get_due_date_text_class=get_due_date_text_class,
        get_due_date_status=get_due_date_status,
        get_comment_count=lambda card_id: get_comment_count(card_id, lambda: load_data(db)),
        format_timestamp=format_timestamp,
        predefined_labels=PREDEFINED_LABELS,
        get_label_by_id=lambda label_id: get_label_by_id(label_id, PREDEFINED_LABELS)
    )
    
    app.add_template_filter(format_date, 'format_date')
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.projects import projects_bp
    from app.routes.sprints import sprints_bp
    from app.routes.api import api_bp
    from app.routes.issues import issues_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(sprints_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(issues_bp)
    
    return app