from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Question, Answer, QuestionVotes, AnswerVotes
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


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    user_name = request.form["user_name"]

    new_user = User(email=email, password=password, user_name=user_name)

    db.session.add(new_user)
    db.session.commit()

    flash("%s, you've been added. :) Please login." % user_name)
    return redirect("/")


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


@app.route("/search", methods=['POST'])
def searches_words_in_questions():
    """Takes user's inputed words and searches in question titles."""

    user_search = request.form["user_search"]
    user_words = user_search.split(" ")
    questions = Question.query.order_by(Question.title).all()
    search_words = []
    search_results = []

    for word in user_words:
        word = word.lower()
        search_words.append(word)
    
    for question in questions:
        phrase = []
        words = []
        split_words = question.title.split(" ")

        for word in split_words:
            word = word.lower()
            words.append(word)

        for word in words:
            if word.lower() in search_words:
                phrase.append(word)

        if set(phrase) == set(search_words):
            search_results.append(question)

    return render_template('search_results.html',
                            search_results=search_results,
                            questions=questions)


@app.route("/graph")
def graphs_trending_words():
    """Displays graphs of trending words in question titles."""

    return render_template('graph.html')


@app.route("/graph-radar.json")
def trending_words_radar():
    """parses trending words from question titles and displays in radar chart."""
    
    questions = Question.query.order_by(Question.title).all()
    month_to_15 = []
    month_past_15 = []

    for question in questions:
        formated_time = question.created_at.strftime("%A %d, %B %Y %I:%M%p")
        split_time = formated_time.split(" ")
        date = split_time[1]
        split_date = date.split(",")
        date_num = int(split_date[0])

        if date_num < 16:
            month_to_15.append(question.title)
        else:
            month_past_15.append(question.title)

    # begin finding trending words for first half of month         
    word_freq_1 = {}
    words_1 = []

    for title in month_to_15:
        split_title = title.split(" ")

        for word in split_title:
            word = word.lower()
            words_1.append(word)

    for word in words_1:
        if word in word_freq_1:
            word_freq_1[word] += 1
        else:
            word_freq_1[word] = 1

    dict_counter = 0
    ignore = ["way", "day", "thing", "be", "have", "do", "say", "get", "make", 
                "go", "know", "use", "tell", "ask", "seem", "to", "of", "in", "for",
                "on", "with", "at", "by", "from", "up", "about", "into", "over", 
                "after", "the", "and", "a", "that", "I", "it", "not", "he", "as",
                "you", "this", "but", "his", "they", "her", "she", "or", "an", 
                "will", "my", "one", "all", "would", "there", "their", "what",
                "is", "how", "are", "if", "why", "was", "does", "we", "can", "did",
                "i", "has", "just", "us", "could", "who", "trump's", "been", "more",
                "so", "donald", "new", "think", "people"]
    # sorts the dictionary by value            
    sorted_word_freq_1 = sorted(word_freq_1, key=word_freq_1.get, reverse=True)
    trending_1 = []

    for word in sorted_word_freq_1:
        if word not in ignore:
            trending_1.append(word)

    # begin finding trending words for second half of month
    word_freq_2 = {}
    words_2 = []

    for title in month_past_15:
        split_title = title.split(" ")

        for word in split_title:
            word = word.lower()
            words_2.append(word)

    for word in words_2:
        if word in word_freq_2:
            word_freq_2[word] += 1
        else:
            word_freq_2[word] = 1

    # sorts the dictionary by value
    sorted_word_freq_2 = sorted(word_freq_2, key=word_freq_2.get, reverse=True)
    trending_2 = []

    for word in sorted_word_freq_2:
        if word not in ignore:
            trending_2.append(word)

    freq_trends_1 = trending_1[:7]
    freq_trends_2 = trending_2[:7]

    # top 7 word frequencies. Ex) [166, 52, 36, 32, 27, 23, 21]
    # map(takes 2 args) loops thru a list and returns a new list
        # the new list is a result of a function (lambda) being used on the first list
    # lambda is an inline function that runs on every loop and x is the parameter
        # x is the current item in the list

    # lambda x: value from word_freq_1, map is looping over first 7 words (freq_trends_1)
    # map (function, list)
    freqs_1 = list(map(lambda x: word_freq_1[x], freq_trends_1))
    freqs_2 = list(map(lambda x: word_freq_2[x], freq_trends_2))

    data_dict_1 = {
        "labels": trending_1[:7],
        "datasets": [
            {
                "label": "1/1 - 1/15",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(255, 99, 132, 0.4)",
                "borderColor":"rgb(255, 99, 132)",
                "borderCapStyle": 'round',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(0,0,0,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": freqs_1,
                "spanGaps": False
            }, {
                "label": "1/16 - 1/31",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(0,0,255,0.2)",
                "borderColor": "rgba(255,0,255,0.4)",
                "borderCapStyle": 'round',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(0,0,0,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": freqs_2,
                "spanGaps": False
            }
        ]
    }

    return jsonify(data_dict_1)


@app.route("/graph-line.json")
def trending_words_line():
    """Parses out trending words and displays them in a line chart."""
    questions = Question.query.order_by(Question.title).all()
    month_to_15 = []
    month_past_15 = []

    for question in questions:
        formated_time = question.created_at.strftime("%A %d, %B %Y %I:%M%p")
        split_time = formated_time.split(" ")
        date = split_time[1]
        split_date = date.split(",")
        date_num = int(split_date[0])

        if date_num < 16:
            month_to_15.append(question.title)
        else:
            month_past_15.append(question.title)

    # begin finding trending words for first half of month         
    word_freq_1 = {}
    words_1 = []

    for title in month_to_15:
        split_title = title.split(" ")

        for word in split_title:
            word = word.lower()
            words_1.append(word)

    for word in words_1:
        if word in word_freq_1:
            word_freq_1[word] += 1
        else:
            word_freq_1[word] = 1

    dict_counter = 0
    ignore = ["way", "day", "thing", "be", "have", "do", "say", "get", "make", 
                "go", "know", "use", "tell", "ask", "seem", "to", "of", "in", "for",
                "on", "with", "at", "by", "from", "up", "about", "into", "over", 
                "after", "the", "and", "a", "that", "I", "it", "not", "he", "as",
                "you", "this", "but", "his", "they", "her", "she", "or", "an", 
                "will", "my", "one", "all", "would", "there", "their", "what",
                "is", "how", "are", "if", "why", "was", "does", "we", "can", "did",
                "i", "has", "just", "us", "could", "who", "trump's", "been", "more",
                "so", "donald", "new", "think", "people"]
    # sorts the dictionary by value            
    sorted_word_freq_1 = sorted(word_freq_1, key=word_freq_1.get, reverse=True)
    trending_1 = []

    for word in sorted_word_freq_1:
        if word not in ignore:
            trending_1.append(word)

    # begin finding trending words for second half of month
    word_freq_2 = {}
    words_2 = []

    for title in month_past_15:
        split_title = title.split(" ")

        for word in split_title:
            word = word.lower()
            words_2.append(word)

    for word in words_2:
        if word in word_freq_2:
            word_freq_2[word] += 1
        else:
            word_freq_2[word] = 1

    # sorts the dictionary by value
    sorted_word_freq_2 = sorted(word_freq_2, key=word_freq_2.get, reverse=True)
    trending_2 = []

    for word in sorted_word_freq_2:
        if word not in ignore:
            trending_2.append(word)

    # nice to have this, but can't jsonify a set()
    trending = set(trending_1[:7] + trending_2[:7])

    freq_trends_1 = trending_1[:7]
    freq_trends_2 = trending_2[:7]

    # top 7 word frequencies. Ex) [166, 52, 36, 32, 27, 23, 21]
    # map(takes 2 args) loops thru a list and returns a new list
        # the new list is a result of a function (lambda) being used on the first list
    # lambda is an inline function that runs on every loop and x is the parameter
        # x is the current item in the list

    # lambda x: value from word_freq_1, map is looping over first 7 words (freq_trends_1)
    # map (function, list)
    freqs_1 = list(map(lambda x: word_freq_1[x], freq_trends_1))
    freqs_2 = list(map(lambda x: word_freq_2[x], freq_trends_2))

    data_dict_2 = {
        "labels": trending_1[:7],
        "datasets": [
            {
                "label": "1/1 - 1/15",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(255, 99, 132, 0.4)",
                "borderColor":"rgb(255, 99, 132)",
                "borderCapStyle": 'round',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(0,0,0,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": freqs_1,
                "spanGaps": False
            }, {
                "label": "1/16 - 1/31",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(0,0,255,0.2)",
                "borderColor": "rgba(255,0,255,0.4)",
                "borderCapStyle": 'round',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(0,0,0,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": freqs_2,
                "spanGaps": False
            }
        ]
    }

    return jsonify(data_dict_2)


# @app.route("/answers-radar.json")
# def displays_radar_chart():
#     """Parses answers for trending words and displays them in a radar chart."""

#     print "++++++++++++++++++++++++"
#     print "IT'S WORKING"

#     answers = Answer.query.order_by(Answer.body).all()
#     jan = []
#     july = []

#     for answer in answers:
#         formated_time = answer.created_at.strftime("%A %d, %B %Y %I:%M%p")
#         split_time = formated_time.split(" ")
#         month = split_time[2]

#         if month == "January":
#             jan.append(answer.body)
#         else:
#             july.append(answer.body)

#     # begin finding trending words for jan-feb         
#     word_freq_1 = {}
#     words_1 = []

#     for text in jan:
#         split_text = text.split(" ")

#         for word in split_text:
#             word = word.lower()
#             words_1.append(word)

#     for word in words_1:
#         if word in word_freq_1:
#             word_freq_1[word] += 1
#         else:
#             word_freq_1[word] = 1

#     dict_counter = 0
#     ignore = ["way", "day", "thing", "be", "have", "do", "say", "get", "make", 
#                 "go", "know", "use", "tell", "ask", "seem", "to", "of", "in", "for",
#                 "on", "with", "at", "by", "from", "up", "about", "into", "over", 
#                 "after", "the", "and", "a", "that", "I", "it", "not", "he", "as",
#                 "you", "this", "but", "his", "they", "her", "she", "or", "an", 
#                 "will", "my", "one", "all", "would", "there", "their", "what",
#                 "is", "how", "are", "if", "why", "was", "does", "we", "can", "did",
#                 "i", "has", "just", "us", "could", "who", "trump's", "been", "more",
#                 "so", "donald", "new", "think", "people"]

#     # sorts the dictionary by value            
#     sorted_word_freq_1 = sorted(word_freq_1, key=word_freq_1.get, reverse=True)
#     trending_1 = []

#     for word in sorted_word_freq_1:
#         if word not in ignore:
#             trending_1.append(word)

#     # begin finding trending words for second half of month
#     word_freq_2 = {}
#     words_2 = []

#     for text in july:
#         split_text = text.split(" ")

#         for word in split_text:
#             word = word.lower()
#             words_2.append(word)

#     for word in words_2:
#         if word in word_freq_2:
#             word_freq_2[word] += 1
#         else:
#             word_freq_2[word] = 1         

#     print word_freq_2        

#     data_dict3 = {}

#     return jsonify(data_dict3)


@app.route("/questions/<question_id>", methods=['GET'])
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

    elif edited_answer:
        answer = Answer.query.filter(Answer.user_id == user_id, 
                                    Answer.question_id == question_id).one()
        answer.body = edited_answer
        answer.edited_at = datetime.now(pytz.timezone('US/Pacific'))

        db.session.commit()
        flash("Answer updated.")
    
    return redirect("/questions/" + question_id)


@app.route("/question_vote/<question_id>.json", methods=['POST'])
def calculates_question_vote(question_id):
    """Calculates number of votes a question has accrued."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    question = Question.query.get(question_id)
    question_voting = question.question_votes
    question_vote_count = len(question.question_votes)

    if QuestionVotes.query.filter(QuestionVotes.question_id == question_id, 
                                    QuestionVotes.user_id == user_id).first():

        flash("You've already voted for this question.")

    else:
        new_question_vote = QuestionVotes(user_id=user_id,
                                            question_id=question_id)
        question_vote_count += 1
        db.session.add(new_question_vote)
        db.session.commit()

    return jsonify(question_vote_count)


@app.route("/answer_vote/<answer_id>.json", methods=['POST'])
def calculates_answer_vote(answer_id):
    """Calculates number of votes a answer has accrued."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    answer = Answer.query.get(answer_id)
    answer_voting = answer.answer_votes
    answer_vote_count = len(answer.answer_votes)

    if AnswerVotes.query.filter(AnswerVotes.answer_id == answer_id, 
                                    AnswerVotes.user_id == user_id).first():

        flash("You've already voted for this answer.")

    else:
        new_answer_vote = AnswerVotes(user_id=user_id,
                                        answer_id=answer_id)
        answer_vote_count += 1
        # db.session.add(new_answer_vote)
        # db.session.commit()

    return jsonify(answer_vote_count)


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
