from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Question, Answer
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# route:
# oh hey new user:
# get user_id from login
# create a new question or answer -> add it to the db in the server file

# add the user_id from the session


@app.route('/')
def show_login():
    """Login page."""

    return render_template("login.html")


@app.route('/', methods=["POST"])
def process_login_form():
    """Determines if user/password exists in database."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("You are logged in")
    return redirect("/questions")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/questions")
def lists_questions():
    """Lists questions. """
    
    questions = Question.query.order_by(Question.title).all()

    for question in questions:
        if question.title == "":
            question.title == "No Title"

    return render_template('questions.html', questions=questions)


@app.route("/questions/<question_id>")
def makes_question_info_page(question_id):
    """makes a question info page """

    user_id = session.get("user_id")
    question = Question.query.get(question_id)

    answered = Answer.query.filter_by(user_id=user_id, question_id=question_id).first()

    return render_template('question_info_page.html', question=question, answer=answered)


@app.route("/questions/<question_id>", methods=['POST'])
def updates_question_info_page(question_id):
    """Updates question info page with a new answer."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    answer = request.form["user_answer"]
    new_answer = Answer(user_id=user_id, question_id=question_id, body=answer)
    flash("Answer added.")
    db.session.add(new_answer)
    db.session.commit()

    created_at = datetime.now(timezone('UTC'))

    question = Question.query.get(question_id)

    return render_template('question_info_page.html', question=question, answer=new_answer, created_at=created_at)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
