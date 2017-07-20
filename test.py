from unittest import TestCase
from model import connect_to_db, db, User, Answer, Question
from server import app
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn('<h1><center>Learn, Share, Connect</center></h1>',
                         result.data)


class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        #Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/',
                            data={'email': 'cat@gmail.com', 'password': 'abc'},
                            follow_redirects=True
                            )
            self.assertEqual(session['user_id'], 1)
            self.assertIn("You are logged in", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '42'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('Logged Out.', result.data)


# class FlaskTestsDatabase(TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         db.session.close()
#         db.drop_all()

#     def test_questions_page(self):
#         """Test questions page."""

#         result = self.client.post("/questions")
#         self.assertIn("Is recycling pointless?", result.data)

#     def test_question_details(self):
#         """Test question info page."""

#         result = self.client.post("/questions/q1")
#         self.assertIn("Should we save the planet?", result.data)

#     def test_answer(self):
#         """Test answer on specific question page."""

#         result = self.client.post("/questions/q2",
#                                   data={"user_id": 2})
#         self.assertIn("No, I disagree.", result.data)


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Answer.query.delete()
    Question.query.delete()

    # Add sample users, answers and questions
    cat = User(user_name="Cat", email="cat@gmail.com", password="abc")
    dog = User(user_name="Dog", email="dog@gmail.com", password="abc")
    horse = User(user_name="Horse", email="horse@gmail.com", password="abc")

    answer_1 = Answer(question_id="q1", user_id=1, body="Yes, I agree.")
    answer_2 = Answer(question_id="q2", user_id=2, body="No, I disagree.")
    answer_3 = Answer(question_id="q3", user_id=3, body="Hrm, I'm indifferent.")

    question_1 = Question(question_id="q1", title="Should we save the planet?", description=" ", user_id=3)
    question_2 = Question(question_id="q2", title="Is recycling pointless?", description=" ", user_id=3)
    question_3 = Question(question_id="q3", title="Mustard or Ketchup?", description=" ", user_id=1)

    db.session.add_all([cat, dog, horse, answer_1, answer_2, answer_3, question_1, question_2, question_3])
    db.session.commit()

def connect_to_db(app, db_uri="postgresql:///testdb"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    import unittest

    unittest.main()
