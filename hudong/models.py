from enum import unique
from libs.orm import db

class Hudong(db.Model):
    __tablename__ = 'hudong'

    id = db.Column(db.Integer, primary_key=True)
    aname = db.Column(db.String(20))
    eid = db.Column(db.Integer)
    cont = db.Column(db.Text)
    hid = db.Column(db.Integer)
    hname = db.Column(db.String(20))