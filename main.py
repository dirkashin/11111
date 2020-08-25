#!/usr/bin/env python

from flask import Flask
from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from libs.orm import db
from user.views import user_bp


# 初始化 app
app = Flask(__name__)
app.secret_key = r'laskjdfoipaysdfibaslkdjfhap9sdfy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tmz:19970224Tmz@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# 初始化 manager
manager = Manager(app)

# 初始化 db 和 迁移工具
db.init_app(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# 注册蓝图
app.register_blueprint(user_bp)

@app.route('/')
def hello():
    return 'hello'


if __name__ == "__main__":
    manager.run()