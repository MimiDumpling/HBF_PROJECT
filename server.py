from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Question, Answer

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# route:
# oh hey new user:
# get user_id from login
# create a new question or answer -> add it to the db in the server file

# add the user_id from the session


@app.route('/')
def login():
    """Login page."""

    print "hi"

    return render_template("login.html")


@app.route('/process_login_form', methods=["POST"])
def process_login_form():
    """Determines if user/password exists in database."""

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()


    if user.password == password:
        session['user_id'] = user.user_id
        flash("You're now logged in.")

    else:
        flash("Incorrect login information. Please try again or register.")
    
    return redirect("/user_page")


#@app.route('/user_page')









if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
