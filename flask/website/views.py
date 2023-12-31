# In this file we will store the standard routes for the website.
# Where users can actually go to. 

# We are going to define that this file is blueprint of our application. 
# Which basically means a bunch of routes inside. So we don't have to 
# have all of our views defined in one file. We can have them defined multiple files,
# split up and nicely organized. Thats what Blueprint allows us to do. 

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, questions_answers
from . import db
from sqlalchemy import func
import json
import csv
from .csv_parser import process_uploaded_csv
import logging
import random
from flask_mail import Mail, Message


views = Blueprint('views', __name__) # defining blueprint

# we also have to register these blueprints in __init__.py 
# @views.route('/home', methods=['GET', 'POST'])
# @login_required # cannot get to home page unless you are logged in
# def home():
#     return render_template("home.html", user=current_user)

# @views.route('/jeopardy', methods=['GET', 'POST'])
# @login_required
# def jeopardy():
#     try:
#         # Fetch categories from the database
#         categories = questions_answers.query.with_entities(questions_answers.category).distinct().limit(6).all()
#         category_names = [category[0] for category in categories]

#         # Fetch questions from the database
#         questions = questions_answers.query.all()

#         # Check if there are categories and questions available
#         if not category_names or not questions:
#             raise Exception("No categories or questions found in the database.")

#         return render_template("gameboard.html", user=current_user, categories=category_names, questions=questions)
#     except Exception as e:
#         # Log the error and handle it gracefully
#         logging.error(f"Error in jeopardy route: {str(e)}")
#         return render_template("error.html", error_message="An error occurred while fetching data.")


# @views.route('/question/<int:category_id>/<int:point_value>/options')
# def question_options(category_id, point_value):
#     # Fetch the question data from the database based on category_id and point_value
#     question_data = questions_answers.query.filter_by(category=category_id, difficulty=point_value).first()

#     if question_data:
#         # Extract necessary information from the question data
#         question_text = question_data.questionText
        
#         answer_choices = [question_data.answerText]  # Put the correct answer as the first choice
#         # You may want to add more logic to get multiple answer choices from the database

#         # Pass the data to the template
#         return render_template('question.html', question_text=question_text, answer_choices=answer_choices)
#     else:
#         # Handle the case where no question is found
#         return render_template('question.html', question_text="No question found", answer_choices=[])

# @views.route('/get_question/<category>/<int:value>', methods=['GET'])
# def get_question(category, value):
#     try:
#         logging.info(f"Received request for question - Category: {category}, Value: {value}")

#         # Assuming frontend difficulty levels are 100 to 500, and backend levels are 1 to 5
#         backend_difficulty = int(value) // 100  # Convert frontend level to backend level

#         question_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).first()
#         option_a_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).order_by(func.random()).first()
#         option_b_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).order_by(func.random()).first()
#         option_c_data = questions_answers.query.filter_by(category=category, difficulty=backend_difficulty).order_by(func.random()).first()

#         if question_data:
#             # Extract necessary information from the question data
#             question_text = question_data.questionText
#             answer_text = question_data.answerText

#             # Shuffle answer choices including the correct answer
#             answer_choices = [answer_text, option_a_data.answerText, option_b_data.answerText, option_c_data.answerText]
#             random.shuffle(answer_choices)

#             # Log the retrieved question data
#             logging.info(f"Retrieved question data - Category: {category}, Value: {value}")
#             logging.info(f"Question Text: {question_text}, Answer Choices: {answer_choices}")

#             # Send the data as JSON
#             return {
#                 'question_text': question_text,
#                 'answer_choices': answer_choices,
#                 'correct_answer': answer_text,  # Include correct answer for comparison
#             }
#         else:
#             # Handle the case where no question is found
#             logging.warning(f"No question found for - Category: {category}, Value: {value}")
#             return jsonify({'question_text': "No question found", 'answer_choices': [], 'correct_answer': None})
#     except Exception as e:
#         # Log any exceptions that occur
#         logging.error(f"Error in get_question route: {str(e)}")
#         return jsonify({'question_text': "Error fetching question", 'answer_choices': [], 'correct_answer': None})



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


mail = Mail()

@views.route('/send_email')
def send_email():
    try:
        subject = 'Hello from our flask app!'
        body = 'Come check out the website and play some jeopardy!'
        recipients = ['robscherer6@gmail.com', 'rtm5@hood.edu', 'sm70@hood.edu', 'xx1@hood.edu' ]

        msg = Message(subject, recipients=recipients)
        msg.body = body

        mail.send(msg)
        return 'Email sent!'
    except Exception as e:
        # Log the error or handle it in an appropriate way
        logging.error(f"Error sending email: {str(e)}")
        return 'Failed to send email.'