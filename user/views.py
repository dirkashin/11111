from flask import Blueprint

from user.models import User

user_bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user',
    template_folder='./templates'
)

# 注册 register
@user_bp.route('/register')
def register():
    pass
# 登录 login
@user_bp.route('/login')
def login():
    pass
# 退出 logout
@user_bp.route('/logout')
def logout():
    pass
# info
@user_bp.route('/info')
def info():
    pass


