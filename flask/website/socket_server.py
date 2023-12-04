from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import login_required, current_user
from string import ascii_uppercase
import random

socket_server = Blueprint('socket_server', __name__)


game_rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
            
        if code not in game_rooms:
            break
        
    return code
                


@socket_server.route('/home', methods=['GET', 'POST'])
@login_required # cannot get to home page unless you are logged in
def home():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        
        if not name:
            return render_template("home.html", user=current_user, error="Please enter a name", code=code, name=name)
        
        if join != False and not code:
            return render_template("home.html", user=current_user, error="Please enter a code", code=code, name=name)
    
        room = code
        if create != False:
            room = generate_unique_code(4)
            game_rooms[room] = {"players": 0, "messages": []}
        elif code not in game_rooms:
            return render_template("home.html", user=current_user, error="Room does not exist")
            
        session["room"] = room
        session["name"] = name
        return redirect(url_for("views.jeopardy"))
        
    return render_template("home.html", user=current_user)
