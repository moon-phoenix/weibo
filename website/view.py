from flask import request, Blueprint
from werkzeug.utils import redirect
from flask import render_template
from flask import session


from libs.orm import db
from website.models import WEB

website_bp=Blueprint('website',__name__,url_prefix='/website')
website_bp.template_folder='./templates'

@website_bp.route('/homepage',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user=WEB(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/user/login')
    else:
        return render_template('register.html')

@website_bp.route('/login',methods=('POST','GET'))
def post_website():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user=WEB.query.filiter_by(username=username).one()
        except Exception:
            db.session.rollback()
            return '用户昵称不存在'
        if password and user.password == password:
            session['uid']=user.id
            session['username']=user.username
            return redirect('/website')
        else:
            return '密码错误'
    else:
        return render_template('login.html')