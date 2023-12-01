from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import requests
# import cv2
# import numpy as np


auth = Blueprint('auth', __name__)
#camera = cv2.VideoCapture(0)

RECAPTCHA_SECRET_KEY = "6LeNFdUoAAAAAAmEGJ3TWUcEYHYEKkpwyHfNEHDh"

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')

        data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if not result['success']:
            flash('reCAPTCHA verification failed. Please try again.', category='error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)

####################################################################################################
# def generate_frames():
#     while True:
        
#         ## Reading the camera frames
#         success,frame = camera.read()
#         if not success:
#             flash("Camera not detected!")
#         else:
            
            
#             ## This will encode an image into a memory buffer
#             ret, buffer = cv2.imencode('.jpg', frame)
#             ## Converting buffer back to bytes
#             frame = buffer.tobytes()
            
#         yield(b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    


# @auth.route('/faceid')
# def faceid():
#     return render_template("faceid.html", user=current_user)

# @auth.route('/video', methods=['GET', 'POST'])
# def video():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


####################################################################################################
@auth.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html')

# Special templating language called JINJA which allows us to write a little bit of python inside our
# HTML documents. Also that we can pass multiple variables or values through them. 