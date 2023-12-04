from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager  # will help manage all the loggin in related things 
from flask_migrate import Migrate
import logging

# creating the database:
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6LetRNQoAAAAALJACuSqiZF5XmUBHnenNtyc8O9-' # When in production you would not want to share this with anyone
    app.config['SITE_KEY'] = '6LetRNQoAAAAAHH5mTVv3tvIJuyTN1h_jwvf1HoG'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # this is where the database is stored.
    app.logger.setLevel(logging.INFO)

    # initializing the database by giving it out flask apps
    db.init_app(app)
    
    # importing the blueprints 
    from .views import views
    from .auth import auth
    from .facial_recognition import facial_recognition
    from .socket_server import socket_server
    # registering the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(facial_recognition, url_prefix='/')
    app.register_blueprint(socket_server, url_prefix='/')
    
    
    from .models import User, questions_answers, game_data
    
    with app.app_context():
        db.create_all()

    
    # create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # The code below is telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app