from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Question, Answer

app = Flask(__name__)


# route:
# oh hey new user:
# get user_id from login
# create a new question or answer -> add it to the db in the server file

# add the user_id from the session
@app.route('/')
def login():
	"""Login page."""

	return render_template("login.html")
