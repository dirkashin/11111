from flask import Blueprint

from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import abort


from libs.orm import db
from weibo.models import Essay
from hudong.models import Hudong
from hudong.models import Thumb
from user.models import Follow
from user.models import User
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import save_avatar
from libs.utils import login_required



from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import datetime
from math import ceil

weibo_bp = Blueprint(
    'weibo',
    __name__,
    url_prefix='/weibo',
    template_folder='./templates'
)

@weibo_bp.route('/xianshi',methods=('POST','GET'))
def show():
    nickname = session['nickname']

    # try:
        # 控制翻页
    page = int(request.args.get('page',1))
    per_page = 3
    offset = per_page * (page - 1)

    l = Essay.query.order_by(Essay.updated.desc()).limit(per_page).offset(offset)
    
    h = Hudong.query.all()

    z = Thumb.query.filter_by(uid=session['uid'])
    # 求最大页数
    max_page = ceil(Essay.query.count() / per_page)

    # 内容下方,以当前页为中心,显示前后各三个页面的索引
    if page <= 3:
        start, end = 1, 7
    elif page > (max_page - 3):
        start, end = max_page - 6, max_page
    else:
        start, end = (page - 3), (page + 3)
    pages = range(start, end + 1)

    dz_wid = []
    for dz in z:
        dz_wid.append(dz.wid)

    return render_template('xianshi.html',nickname=nickname,l=l,pages=pages,page=page,h=h,z=dz_wid)
    # except:
    #     return render_template('xianshi.html',nickname=nickname)
        


@weibo_bp.route('/zeng',methods=('POST','GET'))
def zeng():
    if request.method == 'POST':
        cont = request.form.get('bo')
        nickname = session['nickname']
        now = datetime.datetime.now()


        essay = Essay(nickname=nickname,cont=cont,created=now,updated=now)

        db.session.add(essay)
        db.session.commit()
        return redirect('/weibo/xianshi')

    else:
        return render_template('zeng.html')

@weibo_bp.route('/gai',methods=('POST','GET'))
def gai():
    nickname = session['nickname']
    try:
        id = int(request.args.get('id'))
        s = Essay.query.get(id)
        return render_template('xiugai.html',cont=s.cont,id=id)
    except:
        l = Essay.query.filter_by(nickname=nickname).all()
        return render_template('gai.html',nickname=nickname,l=l)


@weibo_bp.route('/xiugai',methods=('POST','GET'))
def xiugai():
    id = int(request.form.get('id'))
    cont = request.form.get('newcont')
    now = datetime.datetime.now()


    Essay.query.filter_by(id=id).update({'cont':cont,'updated':now})
    
    db.session.commit()

    return redirect('/weibo/xianshi')



@weibo_bp.route('/shan',methods=('POST','GET'))
def shan():
    nickname = session['nickname']
    try:
        id = int(request.args.get('id'))
        s = Essay.query.get(id)
        db.session.delete(s)
        db.session.commit()
        return redirect('/weibo/xianshi')
    except:
        l = Essay.query.filter_by(nickname=nickname).all()
        return render_template('shan.html',nickname=nickname,l=l)



@weibo_bp.route('/guanzhu_xianshi')
def guanzhu_xianshi():
    nickname = session['nickname']

    # 找出登录用户的关注
    uid = session['uid']
        # 找出关注的人的id
    follow = Follow.query.filter_by(uid=uid).values('fid')    
    l_list = [f for (f,) in follow]
        # 对应出关注的人的名字
    un = User.query.filter(User.id.in_(l_list)).values('nickname')
    un_list = [n for (n,) in un]
        # 根据名字，查出微博实例的basequery类数据
    l = Essay.query.filter(Essay.nickname.in_(un_list))
    
    h = Hudong.query.all()

    z = Thumb.query.filter_by(uid=uid)
    
    dz_wid = []
    for dz in z:
        dz_wid.append(dz.wid)

    return render_template('guanzhu_xianshi.html',nickname=nickname,l=l,h=h,z=dz_wid)
    
@weibo_bp.route('/fans_list')
def fans_list():
    nickname = session['nickname']

    # 找出登录用户的粉丝
    uid = session['uid']
        # 找出粉丝的id
    fans = Follow.query.filter_by(fid=uid).values('uid')    
    fans_id_list = [f for (f,) in fans]
        # 对应出fans实例
    fans = User.query.filter(User.id.in_(fans_id_list))

    return render_template('fans_list.html',nickname=nickname,l=fans)
