# In this file we will store the standard routes for the website.
# Where users can actually go to. 

# We are going to define that this file is blueprint of our application. 
# Which basically means a bunch of routes inside. So we don't have to 
# have all of our views defined in one file. We can have them defined multiple files,
# split up and nicely organized. Thats what Blueprint allows us to do. 

from flask import Blueprint, render_template

views = Blueprint('views', __name__) # defining blueprint

# we also have to register these blueprints in __init__.py 
@views.route('/')
def home():
    return render_template("home.html")