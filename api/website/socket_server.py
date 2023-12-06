from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from flask_socketio import join_room, leave_room, send
from flask_login import login_required, current_user
from string import ascii_uppercase
from .models import User, questions_answers
import logging
from sqlalchemy import func
import random
from . import  socketio

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
        return redirect(url_for("socket_server.jeopardy"))
        
    return render_template("home.html", user=current_user)


@socket_server.route("/jeopardy", methods=['GET', 'POST'])  # need to figure out if we want to access the gameboard from here.
@login_required
def jeopardy():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in game_rooms:
        return redirect(url_for("home"))
    
    try:
        # Fetch categories from the database
        categories = questions_answers.query.with_entities(questions_answers.category).distinct().limit(6).all()
        category_names = [category[0] for category in categories]

        # Fetch questions from the database
        questions = questions_answers.query.all()

        # Check if there are categories and questions available
        if not category_names or not questions:
            raise Exception("No categories or questions found in the database.")

        return render_template("gameboard.html", user=current_user, categories=category_names, questions=questions)
    except Exception as e:
        # Log the error and handle it gracefully
        logging.error(f"Error in jeopardy route: {str(e)}")
        return render_template("error.html", error_message="An error occurred while fetching data.")


@socket_server.route('/question/<int:category_id>/<int:point_value>/options')
def question_options(category_id, point_value):
    # Fetch the question data from the database based on category_id and point_value
    question_data = questions_answers.query.filter_by(category=category_id, difficulty=point_value).first()

    if question_data:
        # Extract necessary information from the question data
        question_text = question_data.questionText
        
        answer_choices = [question_data.answerText]  # Put the correct answer as the first choice
        # You may want to add more logic to get multiple answer choices from the database

        # Pass the data to the template
        return render_template('question.html', question_text=question_text, answer_choices=answer_choices)
    else:
        # Handle the case where no question is found
        return render_template('question.html', question_text="No question found", answer_choices=[])

@socket_server.route('/get_question/<category>/<int:value>', methods=['GET'])
def get_question(category, value):
    try:
        logging.info(f"Received request for question - Category: {category}, Value: {value}")

        # Assuming frontend difficulty levels are 100 to 500, and backend levels are 1 to 5
        backend_difficulty = int(value) // 100  # Convert frontend level to backend level

        question_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).first()
        option_a_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).order_by(func.random()).first()
        option_b_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).order_by(func.random()).first()
        option_c_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).order_by(func.random()).first()

        if question_data:
            # Extract necessary information from the question data
            question_text = question_data.questionText
            answer_text = question_data.answerText

            # Shuffle answer choices including the correct answer
            answer_choices = [answer_text, option_a_data.answerText, option_b_data.answerText, option_c_data.answerText]
            random.shuffle(answer_choices)

            # Log the retrieved question data
            logging.info(f"Retrieved question data - Category: {category}, Value: {value}")
            logging.info(f"Question Text: {question_text}, Answer Choices: {answer_choices}")

            # Send the data as JSON
            return {
                'question_text': question_text,
                'answer_choices': answer_choices,
                'correct_answer': answer_text,  # Include correct answer for comparison
            }
        else:
            # Handle the case where no question is found
            logging.warning(f"No question found for - Category: {category}, Value: {value}")
            return jsonify({'question_text': "No question found", 'answer_choices': [], 'correct_answer': None})
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error in get_question route: {str(e)}")
        return jsonify({'question_text': "Error fetching question", 'answer_choices': [], 'correct_answer': None})


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in game_rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    game_rooms[room]["players"] += 1
    print(f"{name} joined room {room}")
    
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in game_rooms:
        game_rooms[room]["players"] -= 1
        if game_rooms[room]["players"] <= 0:
            del game_rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")