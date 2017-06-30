"""Models and database functions for Mimi's Convo Project."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """User of Convo website."""

    __tablename__="users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User Info: user_id=%s user_name=%s email=%s>" % (self.user_id, 
                                                    self.user_name, self.email)            


class Answer(db.Model):
    """Answer submitted by a user."""

    __tablename__ = "answers"

    answer_id = db.Column(db.String(10), autoincrement=True, primary_key=True)
    question_id = db.Column(db.String(10), db.ForeignKey('questions.question_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    body = db.Column(db.Text())
    created_at = db.Column(db.DateTime)
    edited_at = db.Column(db.DateTime)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("answers", order_by=answer_id))

    # Define relationship to question
    question = db.relationship("Question", backref=db.backref("answers"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Answer Info: answer_id=%s question_id=%s user_id=%s body=%s created_at=%s edited_at=%s>" % (self.answer_id,
                                                    self.question_id, self.user_id, self.body[:20], self.created_at, self.edited_at)


class Question(db.Model):
    """Question submitted by a user."""

    __tablename__ = "questions"

    question_id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.Text())
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("questions", order_by=question_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Question Info: question_id=%s title=%s description=%s user_id=%s created_at=%s>" % (self.question_id,
                                                            self.title, self.description[:20], self.user_id, self.created_at)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///convo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
