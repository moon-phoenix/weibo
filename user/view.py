import datetime
from sqlalchemy.exc import IntegrityError
from flask import request, Blueprint
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import redirect
from flask import render_template
from flask import session

from libs.orm import db
from user.models import USER
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import save_avatar
from libs.utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user',template_folder = './templates')


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password1 = request.form.get('password1', '').strip()
        password2 = request.form.get('password2', '').strip()
        gender = request.form.get('gender', '').strip()
        birthday = request.form.get('birthday', '').strip()
        city = request.form.get('city', '').strip()
        bio = request.form.get('bio', '').strip()
        now = datetime.datetime.now()

        if not password1 or password1 != password2:
            return render_template('register.html', err='密码不符合要求')

        user = USER(username=username, password=make_password(password1), gender=gender, birthday=birthday, city=city,
                    bio=bio, created=now)

        avatar_file = request.files.get('avatar')
        if avatar_file:
            user.avatar = save_avatar(avatar_file)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', err='昵称被占用')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        try:
            user = USER.query.filter_by(username=username).one()
        except NoResultFound:
            return render_template('login.html', err='用户昵称不存在')
        if check_password(password,user.password):
            session['uid'] = user.id
            session['username'] = user.username
            return redirect('/user/info')
        else:
            return render_template('login.html',err='密码错误')
    else:
        return render_template('login.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_bp.route('/info')
@login_required
def info():
    uid = session['uid']
    user = USER.query.get(uid)
    return render_template('info.html', user=user)
