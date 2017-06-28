"""Utility file to seed convo database from data in Data/"""

import datetime
from sqlalchemy import func

from model import User, Question, Answer, connect_to_db, db
from server import app

from faker import Faker

from pprint import pprint
import json


def load_users():
    """Load users."""
    
    User.query.delete()

    fake = Faker()

    print "Users"

    for item in range(0, 50):
        user_name = fake.user_name()
        email = fake.free_email()
        password = fake.password()

        user = User(user_id=user_id,
            user_name=user_name,
            email=email,
            password=password)

        # adds to the session
        db.session.add(user)

    # commits to database
    db.session.commit()


def load_questions():
    """Load questions from Data/reddit_2017_01_posts.json"""

    with open('reddit_2017_01_posts.json') as posts_file:
        posts_dict = json.load(posts_file)

    pprint(posts_dict)

    for item in posts_dict:
        question_id = posts_dict["id"]
        created_at = datetime.utcfromtimestamp(posts_dict["created_utc"])
        title = posts_dict["title"]
        description = posts_dict["selftext"]
        user_name = posts_dict["author"]
        # user_id ... assign from the user table random.randint(1, 50) or query the user table for the user_name affiliated with user_id

        question = Question(question=question,
            title=title,
            description=description,
            user_id=user_id,
            created_at=created_at)

        db.session.add(question)

    db.session.commit()


def load_answers():
    """Load answers from Data/"""

    data_list = ['reddit_2017_01_comments.json', 'reddit_2017_02_comments.json', 'reddit_2017_03_comments.json',
                    'reddit_2017_04_comments.json', 'reddit_2017_05_comments.json']

    for item in data_list:
        with open(item) as comments_file:
            comments_dict = json.load(comments_file)

        pprint(comments_dict)

    for item in comments_dict:
        answer_id = comments_dict["parent_id"]
        #question_id = assign from question table
        #user_id = assign with random.randint(0,50) 
        body = 
        created_at = 
        edited_at = 












