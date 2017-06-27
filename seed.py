"""Utility file to seed convo database from data in Data/"""

import datetime
from sqlalchemy import func

from model import User, Question, Answer, connect_to_db, db
from server import app
