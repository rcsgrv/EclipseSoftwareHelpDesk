from flask import Flask
from sqlalchemy import text
from config import Config
from .extensions import db, login_manager
import time
from sqlalchemy.exc import OperationalError
from .seed_data import populate_seed_data
from .models import User  

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(Config)

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from .views.home import home_bp
    from .views.auth import auth_bp
    from .views.tickets import tickets_bp
    from .views.users import users_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(tickets_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/')

    # Create database tables and populate seed data
    create_database(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING", False):
            populate_seed_data()