from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'hi i am aweosme and i am alex'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Import models so they are registered with SQLAlchemy
    from . import models

    # Import and register routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
