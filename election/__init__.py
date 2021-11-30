from flask import Flask
from flask_login import LoginManager
from . import db
import os
import datetime

loginmanager = LoginManager()

def init_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'dbname=test')
    loginmanager.init_app(app)
    db.init_app(app)


    with app.app_context():

        from . import routes

        return app