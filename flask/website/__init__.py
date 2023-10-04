from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# creating the database:
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dbfasdfbghlasdlfa' # When in production you would not want to share this with anyone
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # this is where the database is stored. 
    # initializing the database by giving it out flask apps
    db.init_app(app)
    
    # importing the blueprints 
    from .views import views
    from .auth import auth
    # registering the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note
    
    with app.app_context():
        db.create_all()
    
    # create_database(app)
    
    return app

# def create_database(app): # checks if database exists and if it doesn't then it would create it 
#     if not path.exists('website/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created Database!')