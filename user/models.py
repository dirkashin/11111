from libs.orm import db

class User(db.Model):
    __table__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(128),nullable=False)
    gender = db.Column(db.Enum('male','female','unknow'),defult='unknow')
    birthday = db.Column(db.Date,default='2000-01-01')
    city = db.Column(db.String(10),default='中国')
    bio = db.Column(db.Text,default='')
    created = db.Column(db.DateTime,nullable=False)    # 用户注册时间