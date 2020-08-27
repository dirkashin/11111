from flask import Blueprint


from flask import render_template
from flask import request
from flask import session
from flask import redirect

from libs.orm import db
from user.models import User
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import save_avatar
from libs.utils import login_required



from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import datetime

user_bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user',
    template_folder='./templates'
)

@user_bp.route('/')
def home():
    return render_template('home.html')

# 注册 register
@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        birthday = request.form.get('birthday')

        user = User(nickname=nickname, password=make_password(password), birthday=birthday)

       

        try:
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            return redirect('/user/')
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', err='您的昵称已被占用')
    else:
        return render_template('register.html')



# 登录 login
@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        # 获取用户
        try:
            user = User.query.filter_by(nickname=nickname).one()
        except NoResultFound:
            return render_template('login.html', err='该用户不存在')

        # 检查密码
        if check_password(password, user.password):
            # 在 Session 中记录用户的登录状态
            session['uid'] = user.id
            session['nickname'] = user.nickname
            return redirect('/user/info')
        else:
            return render_template('login.html', err='密码错误')
    else:
        return render_template('login.html')

# 退出 logout
@user_bp.route('/logout')
def logout():
     session.clear()
     return redirect('/user/')


# info
@user_bp.route('/info')
def info():
    '''查看用户信息'''
    uid = session['uid']
    user = User.query.get(uid)
    return render_template('info.html',user=user)

