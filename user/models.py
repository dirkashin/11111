from enum import unique
from libs.orm import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(128),nullable=False)
    birthday = db.Column(db.Date,default='2000-01-01')