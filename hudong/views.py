from flask import Blueprint

from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import abort


from libs.orm import db
from hudong.models import Hudong
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import save_avatar
from libs.utils import login_required



from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

hudong_bp = Blueprint(
    'hudong',
    __name__,
    url_prefix='/hudong',
    template_folder='./templates'
)


@hudong_bp.route('/pinglun',methods=('POST','GET'))
def pinglun():
    nickname = session['nickname']

    if request.method == 'POST':
        eid = request.form.get('eid')
        e = Essay.query.filter_by(id=eid).one()
        pl = request.form.get('pl')
        aname = session['nickname']

        # hid 是回复其他评论时,其他评论的id.评论微博时,为0
        hd = Hudong(eid=eid,aname=aname,cont=pl,hid=0,hname=e.nickname)

        db.session.add(hd)
        db.session.commit()
        return redirect('/weibo/xianshi')
    else:
        eid = request.args.get('eid')
        return render_template('pinglun.html',nickname=nickname,eid=eid)

@hudong_bp.route('/huifu',methods=('POST','GET'))
def huifu():
    if request.method == 'POST':
        hf_cont = request.form.get('huifu')
        hf_name = session['nickname']
        bh_id = request.form.get('e_id')
        p_id = request.form.get('p_id')
        p = Hudong.query.filter_by(id=p_id).one() 

        hudong = Hudong(aname=hf_name,eid=bh_id,cont=hf_cont,hid=p_id,hname=p.aname)

        db.session.add(hudong)
        db.session.commit()
        return redirect('/weibo/xianshi')
    else:
        hid = request.args.get('h_id')
        e = Hudong.query.filter_by(id=hid).one()
        nickname = session['nickname']
        return render_template('huifu.html',nickname=nickname,pl_name=e.aname,pl_cont=e.cont,e_id=e.eid,p_id=hid)