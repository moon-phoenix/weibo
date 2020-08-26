from flask import request, Blueprint
from werkzeug.utils import redirect
from flask import render_template
from flask import session


from libs.orm import db
from website.models import WEB

website_bp=Blueprint('website',__name__,url_prefix='/website')
website_bp.template_folder='./templates'

@website_bp.route('/release',methods=('POST','GET'))
def release():
    if request.method == 'POST':
        title = request.form.get('title')
        word = request.form.get('word')
        user=WEB(username='username',title=title,word=word)

        db.session.add(user)
        db.session.commit()
        return redirect('/website/weibo')
    else:
        return render_template('release.html')

@website_bp.route('/weibo')
def weibo():
    web=WEB.query.filter_by(username='username').all()
    return render_template('weibo.html',web=web)

@website_bp.route('/del',methods=('POST','GET'))
def delect():
    id = request.form.get('id')
    web=WEB.query.filter_by(id=id).one()
    db.session.delete(web)
    db.session.commit()
    return redirect('/website/weibo')

@website_bp.route('/modify',methods=('POST','GET'))
def modify():
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')
        word = request.form.get('word')
        web = WEB.query.filter_by(id=id).one()
        web.title=title
        web.word=word
        db.session.commit()
        return redirect('/website/weibo')
    else:
        return render_template('modify.html')
