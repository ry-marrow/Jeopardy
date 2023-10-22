# Database models: Users and Notes
from . import db    # '.' means from this package.
from flask_login import UserMixin
from sqlalchemy.sql import func

# Note Schema
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
# User Schema
class User(db.Model, UserMixin):
    # Defining the Schema
    id = db.Column(db.Integer, primary_key=True)
    createDate = db.Column(db.DateTime, server_default=func.now())
    deleted = db.Column(db.Boolean, default=0)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

# questions and answers schema
class questions_answers(db.Model):
    questions_id = db.Column(db.Integer, primary_key=True)
    createDate = db.Column(db.DateTime, server_default=func.now())
    deleted = db.Column(db.Boolean, default=0)
    questionText = db.Column(db.String(500))
    category = db.Column(db.String(100))
    difficulty = db.Column(db.Integer)
    answerText = db.Column(db.String(150))
    isDailyDbl = db.Column(db.Boolean, default=0) # [default = 0] 

# game data schema
class game_data(db.Model):
    gameID = db.Column(db.String(11), primary_key=True)
    createDate = db.Column(db.DateTime, server_default=func.now())
    deleted = db.Column(db.Boolean, default=0)
    playerIDList = db.Column(db.String(120))
    winner = db.Column(db.String(11))
    scores = db.Column(db.String(150))