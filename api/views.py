# In this file we will store the standard routes for the website.
# Where users can actually go to. 

# We are going to define that this file is blueprint of our application. 
# Which basically means a bunch of routes inside. So we don't have to 
# have all of our views defined in one file. We can have them defined multiple files,
# split up and nicely organized. Thats what Blueprint allows us to do. 

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json
import csv
from .csv_parser import process_uploaded_csv


views = Blueprint('views', __name__) # defining blueprint

# we also have to register these blueprints in __init__.py 
@views.route('/home', methods=['GET', 'POST'])
@login_required # cannot get to home page unless you are logged in
def home():
    return render_template("home.html", user=current_user)

@views.route('/jeopardy', methods=['GET', 'POST'])
@login_required
def jeopardy():
    return render_template("gameboard.html", user=current_user)

@views.route('/question/<int:category_id>/<int:point_value>/options')
def question_options(category_id, point_value):
    return render_template('question.html')

@views.route('/upload', methods=['POST'])
@login_required
def upload_csv():
    # Check if the user has the necessary permissions to access the upload functionality
    if not current_user.is_admin:
        flash('Access denied. You do not have permission to upload CSV files.', category='error')
        return redirect(url_for('views.home'))

    if 'csvFile' not in request.files:
        flash('No file part', category='error')
        return redirect(url_for('auth.admin_page'))

    file = request.files['csvFile']

    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(url_for('auth.admin_page'))

    if file:
        #result of function in another file, imported at top
        result = process_uploaded_csv(file)
        if result:
            flash('CSV file uploaded and processed successfully', category='success')
        else:
            flash('Failed to process the uploaded CSV file', category='error')

    return redirect(url_for('auth.admin_page'))