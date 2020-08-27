from enum import unique
from libs.orm import db


class Essay(db.Model):
    __tablename__ = 'essay'

    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(20))
    cont = db.Column(db.Text)
    created = db.Column(db.DateTime,nullable=False)
    updated = db.Column(db.DateTime,nullable=False)
