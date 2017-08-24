from unittest import TestCase
from model import connect_to_db, db, User, Answer, Question
from server import app
from flask import session


class FlaskTestsBasic(TestCase):
    """Tests all routes render, except login/logout."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect only to the demo db
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as user:
            with user.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_index(self):
        """Test root page."""
        # import pdb
        # pdb.set_trace()

        result = self.client.get("/")
        self.assertIn('<h1><center>Learn, Share, Connect</center></h1>',
                         result.data)

        print "DONE WITH INDEX CHECK"

    def test_register_page(self):
        """Test register route rendering."""

        result = self.client.get('/register')
        self.assertIn('<h1>Register</h1>', result.data)

        print "DONE WITH REGISTER CHECK"

    def test_questions_page(self):
        """Test questions route rendering."""
        # import pdb
        # pdb.set_trace()

        result = self.client.get('/questions')
        self.assertIn('<h2>Submit A Question</h2>', result.data)

        print "DONE WITH QUESTIONS PAGE CHECK"


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
            result = c.post('/login',
                            data={'email': 'cat@gmail.com', 'password': 'abc'},
                            follow_redirects=True
                            )
            self.assertEqual(session['user_id'], 1)
            self.assertIn("You are logged in", result.data)

        print "DONE WITH LOGIN CHECK"

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '42'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('Logged Out.', result.data)

        print "DONE WITH LOGOUT CHECK"

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

    db.session.add_all([cat, dog, horse])
    db.session.commit()

    question_1 = Question(question_id="q1", title="Should we save the planet?", description=" ", user_id=3)
    question_2 = Question(question_id="q2", title="Is recycling pointless?", description=" ", user_id=3)
    question_3 = Question(question_id="q3", title="Mustard or Ketchup?", description=" ", user_id=1)

    db.session.add_all([question_1, question_2, question_3])
    db.session.commit()

    answer_1 = Answer(question_id="q1", user_id=1, body="Yes, I agree.")
    answer_2 = Answer(question_id="q2", user_id=2, body="No, I disagree.")
    answer_3 = Answer(question_id="q3", user_id=3, body="Hrm, I'm indifferent.")

    db.session.add_all([answer_1, answer_2, answer_3])
    db.session.commit()

def connect_to_db(app, db_uri="postgresql:///testdb"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    import unittest
    unittest.main()
