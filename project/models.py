# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
class PhaseDots(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.Integer)
    peak = db.Column(db.Integer)
class WaveForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)