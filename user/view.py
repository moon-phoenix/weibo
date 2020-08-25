from flask import request, Blueprint
from werkzeug.utils import redirect
from flask import render_template
from flask import session


from libs.orm import db
from user.models import USER

user_bp=Blueprint('user',__name__,url_prefix='/user')
user_bp.template_folder='./templates'

@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user=USER(username=name,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/user/login')
    else:
        return render_template('register.html')

@user_bp.route('/login',methods=('POST','GET'))
def post_website():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user=USER.query.filiter_by(username=username).one()
        except Exception:
            db.session.rollback()
            return '用户昵称不存在'
        if password and user.password == password:
            session['uid']=user.id
            session['username']=user.username
            return render_template('info.html',user=user)
        else:
            return '密码错误'
    else:
        return render_template('login.html')