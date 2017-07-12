from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Question, Answer
from datetime import datetime
from pytz import timezone
import pytz
pacific = pytz.timezone('US/Pacific')

from random import randint

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


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
    """Lists questions."""
   
    questions = Question.query.order_by(Question.title).all()

    for question in questions:
        if question.title == "":
            question.title == "No Title"

    return render_template('questions.html', questions=questions)


@app.route("/questions", methods=['POST'])
def creates_new_question():
    """Creates a new question and updates questions table."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    user_question = request.form["user_question"]
    question_id = str(randint(1, 9999999))
    new_question = Question(user_id=user_id, 
                            question_id=question_id, 
                            title=user_question)

    db.session.add(new_question)
    db.session.commit()
    flash("Question added.")

    question = Question.query.get(question_id)
    the_time = question.created_at

    return render_template('question_info_page.html', 
                            question=question, 
                            created_at=the_time)


@app.route("/questions/<question_id>")
def makes_question_info_page(question_id):
    """Makes a question info page."""

    user_id = session.get("user_id")
    question = Question.query.get(question_id)
    answered = Answer.query.filter_by(user_id=user_id, 
                                    question_id=question_id).first()

    return render_template('question_info_page.html', 
                            question=question, 
                            answer=answered)


@app.template_filter('pacific')
def converts_to_pacific(time):
    """Converts utc to pacific timezone. Called in jinja."""

    time = time.astimezone(timezone('US/Pacific'))
    formated_time = time.strftime("%A %d, %B %Y %I:%M%p")

    return formated_time


@app.route("/questions/<question_id>", methods=['POST'])
def updates_question_info_page(question_id):
    """Updates question info page with a new answer."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    question = Question.query.get(question_id)
    answer = request.form.get("user_answer")
    edited_answer = request.form.get("updated_answer")

    if answer:
        new_answer = Answer(user_id=user_id, 
                            question_id=question_id, 
                            body=answer)

        db.session.add(new_answer)
        db.session.commit()
        flash("Answer added.")

        the_time = new_answer.created_at
        
        return render_template('question_info_page.html', 
                        question=question, 
                        answer=new_answer, 
                        created_at=the_time)

    elif edited_answer:
        answer = Answer.query.filter(Answer.user_id == user_id, 
                                    Answer.question_id == question_id).one()
        answer.body = edited_answer
        answer.edited_at = datetime.now(pytz.timezone('US/Pacific'))

        db.session.commit()
        flash("Answer updated.")
        
        return render_template('question_info_page.html', 
                        question=question,
                        answer=answer)


@app.route("/question_vote/<question_id>", methods=['POST'])
def calculates_question_vote():
    """Calculates number of votes a question has accrued."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    question = Question.query.get(question_id)
    question_voting = question.question_votes
    #counts number of rows with this question_id
    question_vote_count = question_voting.count()
    



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
