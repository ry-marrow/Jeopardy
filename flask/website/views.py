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
@views.route('/', methods=['GET', 'POST'])
@login_required # cannot get to home page unless you are logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})