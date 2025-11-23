from flask import Flask
from sqlalchemy import text
from config import Config
from .extensions import db, login_manager
import time
from sqlalchemy.exc import OperationalError
from .seed_data import populate_seed_data

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

    # CREATE TABLES + SEED DATA now that DB is  ready)
    create_database(app)

    from .models import User  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        populate_seed_data()