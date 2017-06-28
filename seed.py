"""Utility file to seed convo database from data in Data/"""

import datetime
from sqlalchemy import func

from model import User, Question, Answer, connect_to_db, db
from server import app

from faker import Faker

from pprint import pprint
import json

from random import randint


def load_users():
    """Load users."""
    
    User.query.delete()

    fake = Faker()

    print "Users"

    for item in range(0, 50):
        user_name = fake.user_name()
        email = fake.free_email()
        password = fake.password()

        # model.py will autoincrement user_id

        user = User(user_name=user_name,
            email=email,
            password=password)

        # adds to the session
        db.session.add(user)

    # commits to database
    db.session.commit()


def load_questions():
    """Load questions from Data/reddit_2017_01_posts.json"""

    Question.query.delete()

    with open("Data/reddit_2017_01_posts.json") as posts_file:
        # parsing multiple dicts, each on a separate line
        posts_list = [json.loads(line) for line in posts_file]

    pprint(posts_list)

    #print posts_list

    for item in posts_list:
        question_id = item["id"]
        created_at = item["created_utc"]
        title = item["title"]
        description = item["selftext"]
        # user_id: can also query user table for user_name affiliated with user_id
        user_id = randint(0, 50)

        question = Question(question=question,
            title=title,
            description=description,
            user_id=user_id,
            created_at=created_at)

        db.session.add(question)

    db.session.commit()


def load_answers():
    """Load answers from Data/"""

    Answer.query.delete()

    data_list = ['reddit_2017_01_comments.json', 'reddit_2017_02_comments.json', 'reddit_2017_03_comments.json',
                    'reddit_2017_04_comments.json', 'reddit_2017_05_comments.json']

    for item in data_list:
        with open(item) as comments_file:
            comments_dict = json.load(comments_file)

        pprint(comments_dict)

        for item in comments_dict:
            answer_id = comments_dict["parent_id"]
            question_id = Question.query.filter_by(question_id=answer_id).first()
            user_id = randint(0, 50) 
            body = comments_dict["body"]
            created_at = comments_dict["created_utc"]
        
        answer = Answer(answer_id=answer_id,
                    question_id=question_id,
                    user_id=user_id,
                    body=body,
                    created_at=created_at)

        db.session.add(answer)

    db.session.commit()     


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_questions()
    load_answers()
    set_val_user_id()











