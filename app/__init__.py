# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') # Load config from config.py

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    Swagger(app) # Initialize Flasgger

    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app