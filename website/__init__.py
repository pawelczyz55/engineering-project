from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import path
from flask_login import LoginManager
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()
DB_NAME = "database.db"
db_connector = ''

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .import_csv import importCsv
    from .test import test

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(test, url_prefix='/')
    app.register_blueprint(importCsv, url_prefix='/')

    from . import models

    with app.app_context():
        db.create_all()

    engine = create_engine(f"sqlite:///{DB_NAME}")
    #engine = db.get_engine()
    db_connector = engine.connect()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app
