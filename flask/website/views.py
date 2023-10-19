# In this file we will store the standard routes for the website.
# Where users can actually go to. 

# We are going to define that this file is blueprint of our application. 
# Which basically means a bunch of routes inside. So we don't have to 
# have all of our views defined in one file. We can have them defined multiple files,
# split up and nicely organized. Thats what Blueprint allows us to do. 

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__) # defining blueprint

# we also have to register these blueprints in __init__.py 
@views.route('/home', methods=['GET', 'POST'])
@login_required # cannot get to home page unless you are logged in
def home():
    return render_template("home.html", user=current_user)

@views.route('/jeopardy', methods=['GET', 'POST'])
@login_required
def jeopardy():
    return render_template("jeopardy.html", user=current_user)

@views.route('/question/<int:category_id>/<int:point_value>/options')
def question_options(category_id, point_value):
    return render_template('question.html')